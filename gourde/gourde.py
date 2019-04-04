"""Microframework for Flask."""

import argparse
import flask
import logging
import os
import sys

import pkg_resources

from prometheus_flask_exporter import PrometheusMetrics
from werkzeug.contrib.fixers import ProxyFix

try:
    from raven.contrib.flask import Sentry
except ImportError:
    Sentry = None


class Error(Exception):

    """All local errors."""
    pass


class Gourde(object):

    """Wrapper around Flask."""

    LOG_FORMAT = (
        "[%(asctime)s] %(levelname)s %(module)s "
        "[%(filename)s:%(funcName)s:%(lineno)d] (%(thread)d): %(message)s"
    )

    def __init__(self, app_or_name, registry=None):
        """Build a new Gourde.

        Args:
            Either a flask.Flask or the name of the calling module.
        """
        if isinstance(app_or_name, flask.Flask):
            self.app = app_or_name
        else:
            # Convenience constructor.
            self.app = flask.Flask(app_or_name)
            # Most small applications will work behind a reverse proxy and will
            # need this. If you don't want it, create the app yourself.
            self.app.wsgi_app = ProxyFix(self.app.wsgi_app)

        # The blueprints with our views.
        self.blueprint = flask.Blueprint(
            "gourde", __name__, template_folder="templates"
        )

        self.host = "0.0.0.0"
        self.port = 8080
        self.debug = False
        self.log_level = None
        self.twisted = False
        self.gunicorn = False
        self.threads = None
        self.metrics = None
        self.is_setup = False

        self.setup_blueprint()
        self.setup_prometheus(registry)
        self.setup_sentry(sentry_dsn=None)

    def setup_blueprint(self):
        """Initialize the blueprint."""

        # Register endpoints.
        self.blueprint.add_url_rule("/", "status", self.status)
        self.blueprint.add_url_rule("/healthy", "health", self.healthy)
        self.blueprint.add_url_rule("/ready", "ready", self.ready)
        self.blueprint.add_url_rule("/threads", "threads", self.threads_bt)

    def _add_routes(self):
        """Add some nice default routes."""
        if self.app.has_static_folder:
            self.add_url_rule("/favicon.ico", "favicon", self.favicon)
        self.add_url_rule("/", "__default_redirect_to_status", self.redirect_to_status)

    def setup(self, args=None):
        if self.is_setup:
            return

        # Args.
        if args is None:
            parser = self.get_argparser()
            args = parser.parse_args()
        self.host = args.host
        self.port = args.port
        self.debug = args.debug
        self.log_level = args.log_level
        self.twisted = args.twisted
        self.gunicorn = args.gunicorn
        self.threads = args.threads
        if not args.disable_embedded_logging:
            self.setup_logging(self.log_level)

        # Flask things
        self._add_routes()
        self.app.register_blueprint(self.blueprint, url_prefix="/-")

        def _context():
            return {"gourde": self}

        # Add 'gourde' to the context.
        self.app.context_processor(_context)

        self.is_setup = True

    @staticmethod
    def get_argparser(parser=None):
        """Customize a parser to get the correct options."""
        parser = parser or argparse.ArgumentParser()
        parser.add_argument("--host", default="0.0.0.0", help="Host listen address")
        parser.add_argument("--port", "-p", default=9050, help="Listen port", type=int)
        parser.add_argument(
            "--debug",
            "-d",
            default=False,
            action="store_true",
            help="Enable debug mode",
        )
        parser.add_argument(
            "--log-level",
            "-l",
            default="INFO",
            help="Log Level, empty string to disable.",
        )
        parser.add_argument(
            "--twisted",
            default=False,
            action="store_true",
            help="Use twisted to server requests.",
        )
        parser.add_argument(
            "--gunicorn",
            default=False,
            action="store_true",
            help="Use gunicorn to server requests.",
        )
        parser.add_argument(
            "--threads", default=None, help="Number of threads to use.", type=int
        )
        parser.add_argument("--disable-embedded-logging",
                            default=False,
                            action="store_true",
                            help="Disable embedded logging configuration")
        return parser

    def setup_logging(self, log_level):
        """Setup logging."""
        if not log_level:
            return

        # Remove existing logger.
        self.app.config["LOGGER_HANDLER_POLICY"] = "never"
        self.app.logger.propagate = True

        handler = logging.StreamHandler()
        handler.setFormatter(logging.Formatter(self.LOG_FORMAT))
        self.app.logger.addHandler(handler)
        self.app.logger.setLevel(logging.getLevelName(log_level))
        self.app.logger.info("Logging initialized.")

    def setup_prometheus(self, registry=None):
        """Setup Prometheus."""
        kwargs = {}
        if registry:
            kwargs["registry"] = registry
        self.metrics = PrometheusMetrics(self.app, **kwargs)
        try:
            version = pkg_resources.require(self.app.name)[0].version
        except pkg_resources.DistributionNotFound:
            version = "unknown"
        self.metrics.info(
            "app_info", "Application info", version=version, appname=self.app.name
        )
        self.app.logger.info("Prometheus is enabled.")

    def setup_sentry(self, sentry_dsn):
        sentry_dsn = sentry_dsn or os.getenv("SENTRY_DSN", None)
        if not Sentry or not sentry_dsn:
            return

        sentry = Sentry(dsn=sentry_dsn)
        sentry.init_app(self.app)
        self.app.logger.info("Sentry is enabled.")

    def add_url_rule(self, route, endpoint, handler):
        """Add a new url route.

        Args:
            See flask.Flask.add_url_route().
        """
        self.app.add_url_rule(route, endpoint, handler)

    @property
    def name(self):
        """Return the name of the current application."""
        return self.app.import_name

    def redirect_to_status(self):
        """Redirect to the gourde index."""
        return flask.redirect(flask.url_for("gourde.status"))

    def status(self):
        return flask.render_template("gourde/status.html")

    def is_healthy(self):
        return True

    def healthy(self):
        """Return 200 is healthy, else 500.

        Override is_healthy() to change the health check.
        """
        try:
            if self.is_healthy():
                return "OK", 200

            else:
                return "FAIL", 500

        except Exception as e:
            self.app.logger.exception(e)
            return str(e), 500

    def is_ready(self):
        return True

    def ready(self):
        """Return 200 is ready, else 500.

        Override is_ready() to change the readiness check.
        """
        try:
            if self.is_ready():
                return "OK", 200

            else:
                return "FAIL", 500

        except Exception as e:
            self.app.logger.exception()
            return str(e), 500

    def threads_bt(self):
        """Display thread backtraces."""
        import threading
        import traceback

        threads = {}
        for thread in threading.enumerate():
            frames = sys._current_frames().get(thread.ident)
            if frames:
                stack = traceback.format_stack(frames)
            else:
                stack = []
            threads[thread] = "".join(stack)
        return flask.render_template("gourde/threads.html", threads=threads)

    def favicon(self):
        return flask.send_from_directory(
            self.app.static_folder, "favicon.ico", mimetype="image/vnd.microsoft.icon"
        )

    def run(self, **options):
        """Run the application."""
        if not self.is_setup:
            self.setup()

        if self.twisted:
            self.run_with_twisted(**options)
        elif self.gunicorn:
            self.run_with_gunicorn(**options)
        else:
            self.run_with_werkzeug(**options)

    def run_with_werkzeug(self, **options):
        """Run with werkzeug simple wsgi container."""
        threaded = self.threads is not None and (self.threads > 0)
        self.app.run(
            host=self.host,
            port=self.port,
            debug=self.debug,
            threaded=threaded,
            **options
        )

    def run_with_twisted(self, **options):
        """Run with twisted."""
        from twisted.internet import reactor
        from twisted.python import log
        import flask_twisted

        twisted = flask_twisted.Twisted(self.app)
        if self.threads:
            reactor.suggestThreadPoolSize(self.threads)
        if self.log_level:
            log.startLogging(sys.stderr)
        twisted.run(host=self.host, port=self.port, debug=self.debug, **options)

    def run_with_gunicorn(self, **options):
        """Run with gunicorn."""
        import gunicorn.app.base
        from gunicorn.six import iteritems
        import multiprocessing

        class GourdeApplication(gunicorn.app.base.BaseApplication):

            def __init__(self, app, options=None):
                self.options = options or {}
                self.application = app
                super(GourdeApplication, self).__init__()

            def load_config(self):
                config = dict([(key, value) for key, value in iteritems(self.options)
                               if key in self.cfg.settings and value is not None])
                for key, value in iteritems(config):
                    self.cfg.set(key.lower(), value)

            def load(self):
                return self.application

        options = {
            'bind': '%s:%s' % (self.host, self.port),
            'workers': self.threads or ((multiprocessing.cpu_count() * 2) + 1),
            'debug': self.debug,
            **options,
        }
        GourdeApplication(self.app, options).run()

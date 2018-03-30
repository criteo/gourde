"""Gourde unit tests."""
import unittest
import flask
import prometheus_client
import gourde


class GourdeTest(unittest.TestCase):

    def setUp(self):
        # Make sure we don't use sys.argv
        parser = gourde.Gourde.get_argparser()
        self.args = parser.parse_args([])

        # Don't use a shared registry.
        self.registry = prometheus_client.CollectorRegistry(auto_describe=True)

    def test_basic(self):
        """Create a gourde from a name."""
        g = gourde.Gourde(__name__, registry=self.registry)
        g.setup(self.args)
        self.assertIsNotNone(g)
        self.assertTrue(g.is_healthy())
        self.assertTrue(g.is_ready())
        self.assertIsNotNone(g.metrics)

    def test_flask(self):
        """Create a gourde with a flask."""
        app = flask.Flask(__name__)
        g = gourde.Gourde(app, registry=self.registry)
        g.setup(self.args)
        self.assertIsNotNone(g)

    # TODO:
    # - Test default handlers.


if __name__ == '__main__':
    unittest.main()

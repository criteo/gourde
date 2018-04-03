#!/usr/bin/env python
"""Gourde example."""

import flask
import argparse
from gourde import Gourde


class Error(Exception):

    """All local errors."""
    pass


# This could be as simple as :
# gourde = Gourde(app)
# app = gourde.app

# More complicated example:

# Initialize flask by ourselves.
app = flask.Flask(__name__)


# This needs to go first to have priority over
# the default routes.
@app.route('/example')
def index():
    return 'Example'


# Setup our wrapper.
gourde = Gourde(app)


def main():
    # Setup a custom parser.
    parser = argparse.ArgumentParser(description='Example')
    parser = Gourde.get_argparser(parser)
    args = parser.parse_args()

    # Setup gourde with the args.
    gourde.setup(args)

    def _is_healthy():
        """Custom "health" check."""
        import random
        if random.random() > 0.5:
            raise Error()
        return True

    # Register a custom health check.
    gourde.is_healthy = _is_healthy

    # Start the application.
    gourde.run()


if __name__ == "__main__":
    main()

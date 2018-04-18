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

gourde = Gourde(__name__)
app = gourde.app


# Override the default index
@app.route('/')
def index():
    return flask.render_template('index.html')


# Add a new page.
@app.route('/example')
def example():
    return flask.render_template('example.html')


# Create a custom health check callbback.
def is_healthy():
    """Custom "health" check."""
    import random
    if random.random() > 0.5:
        raise Error()
    return True


def main():
    # Setup a custom parser.
    parser = argparse.ArgumentParser(description='Example')
    parser = Gourde.get_argparser(parser)
    args = parser.parse_args()

    # Setup gourde with the args.
    gourde.setup(args)

    # Register a custom health check.
    gourde.is_healthy = is_healthy

    # Start the application.
    gourde.run()


if __name__ == "__main__":
    main()

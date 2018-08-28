# gourde

[![Build Status](https://travis-ci.org/criteo/gourde.svg?branch=master)](https://travis-ci.org/criteo/gourde)
[![Coverage Status](https://coveralls.io/repos/github/criteo/gourde/badge.svg)](https://coveralls.io/github/criteo/gourde?branch=master)
[![PyPI version](https://badge.fury.io/py/gourde.svg)](https://badge.fury.io/py/gourde)
[![Supported Python versions](https://img.shields.io/pypi/pyversions/gourde.svg)](https://pypi.python.org/pypi/gourde/)

Flask(-Twisted) microframework for microservices with Prometheus and Sentry support.

The goal is to remove most of the boilerplate necessary to start a simple HTTP application.
This provides:
* Sane arguments (--host, --port, --debug, --log-level)
* Twisted support to have a production ready uwsgi container (`gourde.twisted`, `--twisted`)
* Prometheus support with default metrics (`gourde.metrics`: See [prometheus_flask_exporter](https://github.com/rycus86/prometheus_flask_exporter))
* Optional sentry support if the `SENTRY_DSN` env var is set.
* If you have a 'static' directory in your module, just put a favicon.ico inside!

## Quick-start
```python
from gourde import Gourde

gourde = Gourde(__name__)
app = gourde.app  # This is a flask.Flask() app.

@app.route('/example')
def index():
    return 'Example'

def main():
    gourde.run()

if __name__ == '__main__':
    main()
```

Want to know more? Look at [example/app.py](example/app.py), you can run it with `gourde-example`.

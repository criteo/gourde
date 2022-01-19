# gourde

[![Build Status](https://travis-ci.org/criteo/gourde.svg?branch=master)](https://travis-ci.org/criteo/gourde)
[![Coverage Status](https://coveralls.io/repos/github/criteo/gourde/badge.svg)](https://coveralls.io/github/criteo/gourde?branch=master)
[![PyPI version](https://badge.fury.io/py/gourde.svg)](https://badge.fury.io/py/gourde)
[![Supported Python versions](https://img.shields.io/pypi/pyversions/gourde.svg)](https://pypi.python.org/pypi/gourde/)
[![FOSSA Status](https://app.fossa.com/api/projects/git%2Bgithub.com%2Fcriteo%2Fgourde.svg?type=shield)](https://app.fossa.com/projects/git%2Bgithub.com%2Fcriteo%2Fgourde?ref=badge_shield)

Flask(-Twisted/Gunicorn) microframework for microservices with Prometheus and Sentry support.

The goal is to remove most of the boilerplate necessary to start a simple HTTP application.
This provides:

* Sane arguments (`--host`, `--port`, `--debug`, `--log-level`)
* Support to have a production ready uwsgi container (`--twisted` or `--gunicorn`)
* Prometheus support with default metrics (`gourde.metrics`: See [prometheus_flask_exporter](https://github.com/rycus86/prometheus_flask_exporter))
* Optional sentry support if the `SENTRY_DSN` env var is set.
* If you have a 'static' directory in your module, just put a favicon.ico inside!

## Installation

```bash
pip install gourde

# To use a production ready wsgi server install one of the following extra requirements
pip install gourde[twisted]
pip install gourde[gunicorn]
```

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


## License
[![FOSSA Status](https://app.fossa.com/api/projects/git%2Bgithub.com%2Fcriteo%2Fgourde.svg?type=large)](https://app.fossa.com/projects/git%2Bgithub.com%2Fcriteo%2Fgourde?ref=badge_large)
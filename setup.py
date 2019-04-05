#!/usr/bin/env python
import os
import setuptools

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))


def _read_reqs(relpath):
    fullpath = os.path.join(os.path.dirname(__file__), relpath)
    with open(fullpath) as f:
        return [s.strip() for s in f.readlines()
                if (s.strip() and not s.startswith("#"))]


_REQUIREMENTS_TXT = _read_reqs("requirements.txt")
_TESTS_REQUIREMENTS_TXT = _read_reqs("tests-requirements.txt")
_DEPENDENCY_LINKS = [l for l in _REQUIREMENTS_TXT if "://" in l]
_INSTALL_REQUIRES = [l for l in _REQUIREMENTS_TXT if "://" not in l]
_TEST_REQUIRE = [l for l in _TESTS_REQUIREMENTS_TXT if "://" not in l]

readme_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'README.md')
try:
    from m2r import parse_from_file

    readme = parse_from_file(readme_file)
except ImportError:
    # m2r may not be installed in user environment
    with open(readme_file, encoding='utf-8') as f:
        readme = f.read()


setuptools.setup(
    name='gourde',
    version='0.3.0',
    include_package_data=True,
    install_requires=_INSTALL_REQUIRES,
    extras_require={
        'twisted': ['flask-twisted', 'twisted'],
        'gunicorn': ['gunicorn'],
    },
    dependency_links=_DEPENDENCY_LINKS,
    tests_require=_TEST_REQUIRE,
    entry_points={
        'console_scripts': [
            'gourde-example = example.app:main',
        ],
    },
    packages=setuptools.find_packages(),

    # metadata for upload to PyPI
    author="Corentin Chary",
    long_description=readme,
    author_email="c.chary@criteo.com",
    description="Flask(-Twisted) microframework for microservices with Prometheus and Sentry support.",
    license="Apache 2",
    keywords="flask twisted gunicorn microframework microservice prometheus sentry",
    url="https://github.com/criteo/gourde/",
    project_urls={
        "Source Code": "https://github.com/criteo/gourde/",
    },
    classifiers=[
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],
    # This makes sure the templates are easy to import.
    zip_safe=False,
)

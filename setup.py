#! /usr/bin/env python

import os
import sys

from setuptools import setup
from setuptools.command.test import test as TestCommand

import py3s3


with open(os.path.join(os.path.dirname(__file__), "README.rst")) as file:
    README = file.read()


class Tox(TestCommand):

    """Command to make python setup.py test run."""

    def finalize_options(self):
        super().finalize_options()
        self.test_args = []
        self.test_suite = True

    def run_tests(self):
        # Do this import here because tests_require isn't processed
        # early enough to do a module-level import.
        from tox._cmdline import main
        sys.exit(main(self.test_args))


CLASSIFIERS = [
    "Development Status :: 3 - Alpha",
    "Environment :: Web Environment",
    "Intended Audience :: Developers",
    "License :: OSI Approved :: BSD License",
    "Natural Language :: English",
    "Programming Language :: Python",
    "Programming Language :: Python :: 3",
    "Programming Language :: Python :: 3.3",
    "Programming Language :: Python :: 3.4",
    "Programming Language :: Python :: 3 :: Only",
    "Topic :: Internet",
    "Topic :: Internet :: WWW/HTTP",
    "Topic :: Utilities",
]


setup(name='py3s3',
      version=py3s3.__version__,
      author=py3s3.__author__,
      author_email=py3s3.__email__,
      maintainer=py3s3.__author__,
      maintainer_email=py3s3.__email__,
      url='http://github.com/logston/py3s3',
      description='A bare bones package for uploading to and downloading '
                  'from AWS S3 from within Python 3.3+',
      long_description=README,
      license='BSD',
      classifiers=CLASSIFIERS,
      packages=['py3s3'],
      tests_require=['tox'],
      cmdclass={'test': Tox})

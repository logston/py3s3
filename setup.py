#! /usr/bin/env python

import os

from distutils.core import setup

import py3s3


with open(os.path.join(os.path.dirname(__file__), "README.rst")) as file:
    README = file.read()

# TODO choose correct classifiers

CLASSIFIERS = [
    "Development Status :: 0 - Production/Stable",
    "Environment :: Web Environment",
    "Intended Audience :: Developers",
    "License :: OSI Approved :: BSD License",
    "Programming Language :: Python",
    "Programming Language :: Python :: 3",
    "Programming Language :: Python :: 3.3",
    "Topic :: Software Development :: Libraries :: Python Modules",
    "Topic :: System :: Networking",
]

setup(name='py3s3',
      version=py3s3.__version__,
      description='A bare bones package for uploading to and downloading '
                  'from AWS S3 from within Python 3.',
      long_description=README,
      url='http://github.com/logston/py3s3',
      author=py3s3.__author__,
      author_email=py3s3.__email__,
      license='BSD',
      classifiers=CLASSIFIERS,
      packages=['py3s3']
)

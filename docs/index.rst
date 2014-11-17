.. py3s3 documentation master file, created by
   sphinx-quickstart on Tue Jan 28 21:27:11 2014.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

py3s3 | AWS S3 & Python 3.3+ 
============================

A bare bones package for uploading to and downloading from AWS S3 from within 
Python 3.3+

.. toctree::
   :maxdepth: 2


Installation
------------

To install the latest stable version of py3s3::

    $ pip install py3s3

To install the latest development version::

    $ git clone git@github.com:logston/py3s3.git
    $ cd py3s3
    $ python setup.py install


Usage
-----

::

    >>> file_name = '/testdir/test.txt'
    >>> file = S3ContentFile("My file's content", file_name, mimetype='')
    >>> storage = S3Storage('file/name/prefix', 'my_bucket', AWS_ACCESS_KEY, AWS_SECRET_KEY)
    >>> storage._save(file_name, file)
    >>>
    >>> new_file = storage._open(file_name)
    >>> print(new_file.content)
    My file's content


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

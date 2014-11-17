.. image:: https://travis-ci.org/logston/py3s3.png?branch=master
    :target: https://travis-ci.org/logston/py3s3

 
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


Testing
=======

Before you can run the test suite, you will need to set the following
environment variables::

    export AWS_S3_BUCKET='<bucket name>'
    export AWS_S3_ACCESS_KEY='<access key>'
    export AWS_S3_SECRET_KEY='<secret key>'

Once the environment variables have been set, the test suite can be run with::

    python setup.py test

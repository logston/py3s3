"""
    A custom Storage interface for storing files to S3.
"""
from contextlib import closing
from datetime import datetime
import hashlib
import hmac
from http.client import HTTPConnection
import urllib.parse
from wsgiref.handlers import format_date_time

from django.core.files.storage import Storage

from .config import BUCKET
from .config import AWS_ACCESS_KEY
from .config import AWS_SECRET_KEY
from .config import ENCODING
from .files import S3ContentFile
from .utils import b64_string

NETLOC = '%s.s3.amazonaws.com' % BUCKET


class S3IOError(IOError):
    pass


class S3FileDoesNotExistError(S3IOError):
    def __init__(self, name=None, msg=None):
        total_msg = 'File does not exist: {}'.format(name)
        if msg:
            total_msg += ' {}'.format(msg)
        super().__init__(total_msg)


class S3Storage(Storage):
    """
    A custom storage implimentation for use with py3s3.

    An instance of this class can be used to move a py3s3 file
    up to or down from AWS.
    """
    def __init__(self, name_prefix='', bucket=BUCKET,
                 access_key=AWS_ACCESS_KEY, secret_key=AWS_SECRET_KEY):
        self.name_prefix = name_prefix
        self.bucket = bucket
        self.access_key = access_key
        self.secret_key = secret_key

    @staticmethod
    def request_timestamp(timestamp=None):
        if timestamp is None:
            timestamp = datetime.now().timestamp()
        return format_date_time(timestamp)

    @staticmethod
    def datetime_from_aws_timestamp(timestamp):
        """
        Return datetime from parsed AWS header timestamp string.
        AWS Format:  Wed, 28 Oct 2009 22:32:00 GMT
        """
        fmt = '%a, %d %b %Y %X %Z'
        return datetime.strptime(timestamp, fmt)

    def _prepend_name_prefix(self, name):
        """Return file name (ie. path) with the prefix directory prepended"""
        if not self.name_prefix:
            return name
        base = self.name_prefix
        if base[0] != '/':
            base = '/' + base
        if name[0] != '/':
            name = '/' + name
        return base + name

    def request_signature(self, stringtosign):
        """
        Construct a signature by making an RFC2104 HMAC-SHA1
        of the following and converting it to Base64 UTF-8 encoded string.
        """
        digest = hmac.new(
            self.secret_key.encode(ENCODING),
            stringtosign.encode(ENCODING),
            hashlib.sha1
        ).digest()
        return b64_string(digest)

    def _put_file(self, file_object):
        """Send PUT request to S3 with file_object contents"""
        timestamp = self.request_timestamp()

        mimetype = file_object.mimetype if file_object.mimetype else ''
        stringtosign = '\n'.join([
            'PUT',
            file_object.md5hash(),
            mimetype,
            timestamp,
            'x-amz-acl:public-read',
            '/' + self.bucket + file_object.name
        ])
        signature = self.request_signature(stringtosign)

        headers = dict()
        headers['Date'] = timestamp
        headers['Authorization'] = ''.join(['AWS' + ' ',
                                            self.access_key,
                                            ':',
                                            signature])
        headers['Content-Length'] = file_object.size
        headers['Content-MD5'] = file_object.md5hash()
        if mimetype:
            headers['Content-Type'] = file_object.mimetype
        headers['x-amz-acl'] = 'public-read'

        with closing(HTTPConnection(NETLOC)) as conn:
            conn.request('PUT',
                         file_object.name,
                         file_object.read(),
                         headers=headers)
            response = conn.getresponse()

        if response.status not in (200,):
            raise IOError('py3s3 PUT error. Response status: %s' %
                          response.status)

    def _save(self, name, file_object):
        prefixed_name = self._prepend_name_prefix(name)
        file_object.name = prefixed_name
        self._put_file(file_object)
        return name

    def _get_file(self, name):
        """
        Return a signature for use in GET requests
        """
        timestamp = self.request_timestamp()
        stringtosign = '\n'.join([
            'GET',
            '',
            '',
            timestamp,
            '/' + self.bucket + name
        ])
        signature = self.request_signature(stringtosign)
        headers = dict()
        headers['Date'] = timestamp
        if self.access_key and self.secret_key:
            headers['Authorization'] = ''.join(['AWS' + ' ',
                                                self.access_key,
                                                ':',
                                                signature])
        file = S3ContentFile('')
        with closing(HTTPConnection(NETLOC)) as conn:
            conn.request('GET',
                         name,
                         headers=headers)
            response = conn.getresponse()
            if not response.status in (200,):
                if response.length is None:
                    # length == None seems to be returned from GET requests
                    # to non-existing files
                    raise S3FileDoesNotExistError(name)
                # catch all other cases
                raise S3IOError('py3s3 GET error. Response status: %s' %
                                response.status)

            file = S3ContentFile(response.read())
        return file

    def _open(self, name, mode='rb'):
        prefixed_name = self._prepend_name_prefix(name)
        file = self._get_file(prefixed_name)
        file.name = name
        return file

    def delete(self, name):
        prefixed_name = self._prepend_name_prefix(name)
        timestamp = self.request_timestamp()
        stringtosign = '\n'.join([
            'DELETE',
            '',
            '',
            timestamp,
            '/' + self.bucket + prefixed_name
        ])
        signature = self.request_signature(stringtosign)
        headers = dict()
        headers['Date'] = timestamp
        if self.access_key and self.secret_key:
            headers['Authorization'] = ''.join(['AWS' + ' ',
                                                self.access_key,
                                                ':',
                                                signature])
        with closing(HTTPConnection(NETLOC)) as conn:
            conn.request('DELETE',
                         prefixed_name,
                         headers=headers)
            response = conn.getresponse()
            if not response.status in (204,):
                raise S3IOError('py3s3 DELETE error. Response status: %s' %
                                response.status)

    def exists(self, name):
        with closing(HTTPConnection(NETLOC)) as conn:
            conn.request('HEAD', self.url(name))
            response = conn.getresponse()
            return response.status in (200,)

    def listdir(self, path):
        raise NotImplementedError()

    def size(self, name):
        with closing(HTTPConnection(NETLOC)) as conn:
            conn.request('GET', self.url(name))
            return conn.getresponse().length

    def url(self, name):
        """Return URL of resource"""
        scheme = 'http'
        netloc = NETLOC
        path = self._prepend_name_prefix(name)
        query = ''
        fragment = ''
        url_tuple = (scheme, netloc, path, query, fragment)
        return urllib.parse.urlunsplit(url_tuple)

    def modified_time(self, name):
        with closing(HTTPConnection(NETLOC)) as conn:
            conn.request('HEAD', self.url(name))
            dt_header = conn.getresponse().getheader('Last-Modified', None)
        if dt_header is None:
            raise S3IOError('No modified time available for file: %s' %
                            name)
        return self.datetime_from_aws_timestamp(dt_header)

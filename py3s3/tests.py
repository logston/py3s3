import datetime
import os
import time
import unittest

from .storage import S3ContentFile
from .storage import S3IOError
from .storage import S3Storage


BUCKET = os.getenv('AWS_S3_BUCKET', None)
AWS_ACCESS_KEY = os.getenv('AWS_ACCESS_KEY', None)
AWS_SECRET_KEY = os.getenv('AWS_SECRET_KEY', None)


class Py3s3S3StorageTestCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.datetime = datetime.datetime.now()
        cls.modify_time_dt = None

    def setUp(self):
        self.test_content = ''.join([
            'This test content file was uploaded at about ',
            str(self.datetime)
        ])
        self.test_file_name = '/test.txt'
        self.file = S3ContentFile(self.test_content, self.test_file_name)
        self.storage = S3Storage('', BUCKET, AWS_ACCESS_KEY, AWS_SECRET_KEY)

    def test__000_PUT_saves_test_file_to_s3(self):
        name = self.storage._save(self.test_file_name, self.file)
        self.assertEqual(name, self.test_file_name)
        self.__class__.modify_time_dt = datetime.datetime.utcnow()

    def test__001_HEAD_returns_test_file_existance(self):
        self.assertTrue(self.storage.exists(self.test_file_name))

    def test__002_HEAD_returns_correct_file_size(self):
        size = self.storage.size(self.test_file_name)
        self.assertEqual(size, self.file.size)

    def test__003_HEAD_returns_correct_modified_time(self):
        time_ = self.storage.modified_time(self.test_file_name)
        self.assertAlmostEqual(
            time_, self.__class__.modify_time_dt,
            delta=datetime.timedelta(seconds=2)
        )

    def test__004_GET_pulls_test_file_down(self):
        file = self.storage._open(self.test_file_name)
        self.assertEqual(self.file.content, file.content)

    def test__005_DELETE_deletes_test_file_from_s3(self):
        self.storage.delete(self.test_file_name)
        self.assertFalse(self.storage.exists(self.test_file_name))
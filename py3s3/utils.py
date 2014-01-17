from base64 import b64encode
import os

# get keys, bucket name, and encoding from env
ENCODING = os.getenv('AWS_S3_OBJECT_ENCODING', 'utf-8')


def b64_string(bytestring):
    """
    Return an base64 encoded byte string as an ENCODING decoded string
    """
    return b64encode(bytestring).decode(ENCODING)

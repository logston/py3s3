from base64 import b64encode
import os

# get keys, bucket name, and encoding from env
ENCODING = 'utf-8'


def b64_string(bytestring):
    """
    Return an base64 encoded byte string as an ENCODING decoded string
    """
    return b64encode(bytestring).decode(ENCODING)


media_types = {
    "bmp": "image/bmp",
    "css": "text/css",
    "gif": "image/gif",
    "html": "text/html",
    "jpeg": "image/jpeg",
    "jpg": "image/jpeg",
    "mp3": "audio/mpeg",
    "pdf": "application/pdf",
    "png": "image/png",
    "rtf": "text/rtf",
    "txt": "text/plain",
    "tiff": "image/tiff",
    "zip": "application/zip"
}

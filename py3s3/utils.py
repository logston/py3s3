from base64 import b64encode

from .config import ENCODING


def b64_string(bytestring):
    """
    Return an base64 encoded byte string as an ENCODING decoded string
    """
    return b64encode(bytestring).decode(ENCODING)

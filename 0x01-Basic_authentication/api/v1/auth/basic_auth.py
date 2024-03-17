#!/usr/bin/env python3
"""Basic Authentication
"""
import base64
from api.v1.auth.auth import Auth


class BasicAuth(Auth):
    """Basic Authentication
    """
    def extract_base64_authorization_header(self,
                                            authorization_header: str) -> str:
        """Return Base64 part of the Authorization header for a Basic Auth
        """
        if authorization_header is None:
            return None
        if type(authorization_header) is not str:
            return None
        if authorization_header.split(' ')[0] != 'Basic':
            return None
        return authorization_header.split(' ')[1]

    def decode_base64_authorization_header(self,
            base64_authorization_header: str) -> str:   # noqa: E502, E128
        """Return the decoded value of a Base64 string
        """
        if base64_authorization_header is None:
            return None
        if type(base64_authorization_header) is not str:
            return None
        try:
            decoded_bytes = base64.b64decode(base64_authorization_header)
            decoded_string = decoded_bytes.decode('utf-8')
            return decoded_string
        except (base64.binascii.Error, UnicodeDecodeError):
            return None

    def extract_user_credentials(self,
            decoded_base_64_authorization_header) -> (str, str):    # noqa: E502, E128
        """Return user email and password from Base64 decoded value
        """
        if decoded_base_64_authorization_header is None:
            return (None, None)
        if type(decoded_base_64_authorization_header) is not str:
            return (None, None)
        if ':' not in decoded_base_64_authorization_header:
            return (None, None)
        return tuple(decoded_base_64_authorization_header.split(':')[:2])

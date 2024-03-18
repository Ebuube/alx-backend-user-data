#!/usr/bin/env python3
"""Basic Authentication
"""
import base64
from api.v1.auth.auth import Auth
from models.user import User
from typing import TypeVar


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
        return tuple(decoded_base_64_authorization_header.split(':', maxsplit=1)[:2])   # noqa: E502, E128

    def user_object_from_credentials(self,
            user_email: str, user_pwd: str) -> TypeVar('Uesr'):  # noqa: E502, E128
        """Return a user instance based on credentials
        """
        if user_email is None or type(user_email) is not str:
            return None
        if user_pwd is None or type(user_pwd) is not str:
            return None
        User.load_from_file()
        user = User.search(attributes={'email': user_email})
        if not user:
            return None
        user = user[0]
        if not user.is_valid_password(pwd=user_pwd):
            return None
        return user

    def current_user(self, request=None) -> TypeVar('User'):
        """Retrieve the User instance for a request
        """
        header = self.authorization_header(request)
        if header is None:
            return None
        base64_auth_header = self.extract_base64_authorization_header(header)
        if base64_auth_header is None:
            return
        decoded_base64_auth_header = \
                self.decode_base64_authorization_header(base64_auth_header)     # noqa: E502, E128
        if decoded_base64_auth_header is None:
            return None
        user_email, user_pwd = \
                self.extract_user_credentials(decoded_base64_auth_header)   # noqa: E502, E128
        return self.user_object_from_credentials(user_email, user_pwd)

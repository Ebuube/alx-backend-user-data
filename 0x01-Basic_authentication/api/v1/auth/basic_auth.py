#!/usr/bin/env python3
"""Basic Authentication
"""
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

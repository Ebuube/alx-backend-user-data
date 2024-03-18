#!/usr/bin/env python3
"""Handle authentication
"""
import os
from flask import request
from typing import List, TypeVar


class Auth:
    """Authentication class
    """
    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """Demand authentication
        """
        if path is None:
            return True
        if excluded_paths is None or len(excluded_paths) == 0:
            return True
        if type(path) is str and path[-1] != '/':
            path = path + '/'
        for excluded in excluded_paths:
            if excluded[-1] == '*':
                if path.startswith(excluded[:-1]):
                    return False
            elif path == excluded:
                return False
        return True

    def authorization_header(self, request=None) -> str:
        """Handler for authorization header
        """
        if request is None:
            return None
        if 'Authorization' not in request.headers:
            return None
        return request.headers['Authorization']

    def current_user(self, request=None) -> TypeVar('User'):
        """Check the current user
        """
        return None

    def session_cookie(self, request=None):
        """Return the value of the session_id from the cookie
        """
        if request is None:
            return None
        return request.cookies.get(os.getenv('SESSION_NAME'))

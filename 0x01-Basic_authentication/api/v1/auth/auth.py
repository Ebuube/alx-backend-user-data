#!/usr/bin/env python3
"""Handle authentication
"""
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
        if path not in excluded_paths:
            return True
        for excluded in excluded_paths:
            if excluded[-1] == '*':
                if path.startswith(excluded[0:-1]):
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

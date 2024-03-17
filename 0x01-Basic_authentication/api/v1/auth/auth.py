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
        if path[-1] != '/':
            path = path + '/'
        if exluded_paths is None or len(excluded_paths) == 0:
            return True
        if path not in excluded_paths:
            return True
        return False

    def authorization_header(self, request=None) -> str:
        """Handler for authorization header
        """
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """Check the current user
        """
        return None

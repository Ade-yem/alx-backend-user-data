#!/usr/bin/env python3
"""manage the API authentication"""

from flask import request
from typing import List, TypeVar


class Auth:
    """manage the API authentication"""

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """returns False - path and excluded_paths"""
        if path is not None and path[-1] != '/':
            path += '/'
        for excluded in excluded_paths:
            if excluded.endswith('*'):
                if path.startswith(excluded[:-1]):
                    return False
        if excluded_paths is None or path not in excluded_paths\
                or path is None or excluded_paths == []:
            return True
        return False

    def authorization_header(self, request=None) -> str:
        """returns None - request"""
        if request is None or request.headers.get('Authorization') is None:
            return None
        return request.headers.get('Authorization')

    def current_user(self, request=None) -> TypeVar('User'):
        """returns None - request"""
        return None

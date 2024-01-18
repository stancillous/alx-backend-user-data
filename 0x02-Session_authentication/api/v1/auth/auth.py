#!/usr/bin/env python3
"""
class to manage our API authentication
Is the template for all
authentication system that will be implemented"""
from flask import request
from typing import List, TypeVar


class Auth:
    """class to manage authentication"""
    def __init__(self):
        """constructor"""

    def require_auth(self, path: str,
                     excluded_paths: List[str]) -> bool:
        """require auth method"""
        if path is not None and path[-1] != "/":
            path += "/"

        if excluded_paths is None or len(excluded_paths) == 0:
            return True
        if (path not in excluded_paths or path is None):
            return True
        return False

    def authorization_header(self, request=None) -> str:
        """auth header method
        @request: Flask request object"""

        if request is None or "Authorization" not in request.headers:
            return None
        return request.headers.get("Authorization")

    def current_user(self, request=None) -> TypeVar('User'):
        """current user method
        @request: Flask request object
        """
        return None

    def session_cookie(self, request=None):
        """return cookie value of a request"""
        if not request:
            return None
        cookie_value = request.cookies.get("_my_session_id")
        return cookie_value

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
        return False
    
    def authorization_header(self, request=None) -> str:
        """auth header method
        @request: Flask request object"""
        return None
    
    def current_user(self, request=None) -> TypeVar('User'):
        """current user method
        @request: Flask request object
        """
        return None

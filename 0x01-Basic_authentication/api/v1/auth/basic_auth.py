#!/usr/bin/env python3
"""
BasicAuth class
"""
import base64
from api.v1.auth.auth import Auth


class BasicAuth(Auth):
    """BasicAuth class"""
    def __init__(self):
        """constructor"""
        pass

    def extract_base64_authorization_header(self,
                                            authorization_header: str) -> str:
        """returns the base64 part of the auth header"""
        if ((authorization_header is None) or
                (type(authorization_header) != str) or
                not authorization_header.startswith("Basic ")):
            return None
        return authorization_header[6:]

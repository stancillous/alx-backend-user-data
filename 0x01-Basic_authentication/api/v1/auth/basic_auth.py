#!/usr/bin/env python3
"""
BasicAuth class
"""
import base64
# from api.v1.auth.auth import Auth


class BasicAuth():
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

    def decode_base64_authorization_header(self,
                                           base64_authorization_header: str
                                           ) -> str:
        """decodes base64 auth header"""
        if ((base64_authorization_header is None) or
                (type(base64_authorization_header) != str)):
            return None
        try:
            decoded_bytes = base64.b64decode(base64_authorization_header)
            decoded_str = decoded_bytes.decode()
            return decoded_str
        except Exception:
            return None

#!/usr/bin/env python3
"""
BasicAuth class
"""
import base64
from api.v1.auth.auth import Auth
from typing import TypeVar
from models.user import User


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

    def extract_user_credentials(self,
                                 decoded_base64_authorization_header: str
                                 ) -> (str, str):
        """method to extract user creds"""
        if ((decoded_base64_authorization_header is None)
                or (type(decoded_base64_authorization_header) != str)
                or (":" not in decoded_base64_authorization_header)):
            return (None, None)
        user, name = decoded_base64_authorization_header.split(":")
        return (user, name)

    def user_object_from_credentials(self,
                                     user_email: str,
                                     user_pwd: str) -> TypeVar('User'):
        """returns User instance based on their email and password"""
        if user_email is None or type(user_email) != str:
            return None
        if user_pwd is None or type(user_pwd) != str:
            return None

        try:
            all_users = User.search({"email": user_email})
            if all_users == [] or not all_users:
                return None
            for user in all_users:
                if user.is_valid_password(user_pwd):
                    return user
            return None
        except Exception:
            return None

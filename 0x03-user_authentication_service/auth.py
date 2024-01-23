#!/usr/bin/env python3
"""module to handle all auth"""
import bcrypt
from db import DB
import uuid
from typing import TypeVar
from sqlalchemy.exc import NoResultFound


def _hash_password(password: str) -> bytes:
    """hash a passed in password"""
    password_bytes = password.encode()
    return bcrypt.hashpw(password_bytes, bcrypt.gensalt())


def _generate_uuid() -> str:
    """generate a uuid"""
    return str(uuid.uuid4)


class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        self._db = DB()

    def register_user(self, email: str, password: str) -> TypeVar('User'):
        """register a user"""
        try:
            self._db.find_user_by(email=email)
        except NoResultFound:
            hashed_pwd = _hash_password(password)
            return self._db.add_user(email, hashed_pwd)
        else:
            raise ValueError(f"User {email} already exists")

    def valid_login(self, email: str, password: str) -> bool:
        """check user credentials when logging in"""
        try:
            user = self._db.find_user_by(email=email)
            return bcrypt.checkpw(password.encode(),
                                  user.hashed_password.encode())
        except Exception:
            return False

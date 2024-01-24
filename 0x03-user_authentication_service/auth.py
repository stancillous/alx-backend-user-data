#!/usr/bin/env python3
"""module to handle all auth"""
import bcrypt
from db import DB
from db import User
import uuid
from typing import TypeVar, Union
from sqlalchemy.orm.exc import NoResultFound


def _hash_password(password: str) -> bytes:
    """generate a hash of the input password using bcrypt"""
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(password.encode('utf-8'), salt)


def _generate_uuid() -> str:
    """generate a uuid"""
    return str(uuid.uuid4())


class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        """constructor method"""
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

    def create_session(self, email: str) -> str:
        """return session ID as a string"""
        try:
            user = self._db.find_user_by(email=email)
            user.session_id = _generate_uuid()
            self._db._session.commit()
            return user.session_id
        except Exception:
            return None


    def get_user_from_session_id(self, session_id: str) -> Union[User, None]:
        """get user based on passed in session id"""
        if session_id:
            try:
                user = self._db.find_user_by(session_id=session_id)
                return user
            except Exception:
                return None
        return None

    def destroy_session(self, user_id: int) -> None:
        """destroy user session if exists"""
        try:
            user = self._db.find_user_by(id=user_id)
            self._db.update_user(user.id, session_id=None)
            return None
        except Exception:
            return None

    def get_reset_password_token(self, email: str) -> str:
        """method to allow user to get a reset pwd token"""
        try:
            user = self._db.find_user_by(email=email)
            token = _generate_uuid()
            self._db.update_user(user.id, reset_token=token)

        except Exception:
            ValueError

    def update_password(self, reset_token: str, password: str) -> None:
        """use reset token to find the user, and update their
        password with this new one"""
        try:
            user = self._db.find_user_by(reset_token=reset_token)
            hashed_password = _hash_password(password)
            self._db.update_user(user.id, reset_token=None, password=str(hashed_password))
        except Exception:
            raise ValueError

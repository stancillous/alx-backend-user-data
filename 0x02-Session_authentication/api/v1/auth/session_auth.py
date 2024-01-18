#!/usr/bin/env python3
"""
SessionAuth class
"""
from typing import TypeVar
from api.v1.auth.auth import Auth
import uuid
from models.user import User


class SessionAuth(Auth):
    """SessionAuth class"""
    user_id_by_session_id = {}

    def __init__(self):
        """constructor"""
        pass

    def create_session(self, user_id: str = None) -> str:
        """creates session id for a user_id"""
        if not user_id or not isinstance(user_id, str):
            return None
        session_id = str(uuid.uuid4())
        self.user_id_by_session_id[session_id] = user_id
        return session_id

    def user_id_for_session_id(self,
                               session_id: str = None) -> str:
        """return a USER id based on session id"""
        if not session_id or not isinstance(session_id, str):
            return None
        return self.user_id_by_session_id.get(session_id)

    def current_user(self, request=None) -> TypeVar('User'):
        """return User instance based on cookie value"""
        cookie_value = self.session_cookie(request)
        user_id = self.user_id_by_session_id.get(cookie_value)
        user_instance = User.get(user_id)
        return user_instance
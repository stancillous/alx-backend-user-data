#!/usr/bin/env python3
"""class SessionExpAuth that will add an 
expiration date to the session id"""
from api.v1.auth.session_auth import SessionAuth
import os
from datetime import datetime, timedelta


class SessionExpAuth(SessionAuth):
    """class to add an exp date to session id"""
    def __init__(self):
        """constructor method"""
        try:
            session_duration = int(os.getenv("SESSION_DURATION"))
        except Exception:
            session_duration = 0

    def create_session(self, user_id=None):
        """overloads our parent class"""
        try:
            session_id = super().create_session(user_id)
        except Exception:
            session_id = None
        session_dictionary = {
            "user_id": user_id,
            "created_at": datetime.now()
        }
        self.user_id_by_session_id[session_id] 
        return session_id

    def user_id_for_session_id(self, session_id=None):
        """overloads the method in the parent class"""
        if session_id is None or self.user_id_by_session_id.get(session_id) is None:
            return None
        user_id = super().user_id_for_session_id(session_id)
        if self.session_duration <= 0:
            print("\n\n\t\tuser id ", self.user_id_by_session_id.get(session_id))
            return self.user_id_by_session_id.get(session_id)
        if self.user_id_by_session_id.get("created_at") is None:
            return None
        
        created_at = self.user_id_by_session_id.get("created_at")
        time_period = created_at + timedelta(seconds=self.session_duration)

        if time_period < datetime.now():
            print("\n\npassed")
            return None
        return user_id
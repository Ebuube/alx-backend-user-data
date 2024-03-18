#!/usr/bin/env python3
"""Persisted Authentication
"""
from api.v1.auth.session_exp_auth import SessionExpAuth
from models.user_session import UserSession


class SessionDBAuth(SessionExpAuth):
    """Persisted Authentication class
    """
    def create_session(self, user_id=None):
        """Create and persist a User session
        """
        session_id = super().create_session(user_id)
        user_session = UserSession(user_id=user_id, session_id=session_id)
        user_session.save()
        return session_id

    def user_id_for_session_id(self, session_id=None):
        """Get the user_id using a session
        """
        matches = UserSession.search(attributes={'session_id': session_id})
        if not matches or len(matches) == 0:
            return None
        user_session = matches[0]

        # Check if session has expired by adding the 'created_at' attribute
        # to UserSession instance
        return user_session.user_id

    def destroy_session(self, request=None):
        """Destroy a User Session
        """
        if request is None:
            return False
        session_id = self.session_cookie(request)
        if not session_id:
            return False
        # Find User session
        matches = UserSession.search(attributes={'session_id': session_id})
        if not matches or len(matches) == 0:
            return False
        user_session = matches[0]
        # Destroying session
        user_session.remove()
        return True

#!/usr/bin/env python3
"""Make expiring sessions
"""
import os
from api.v1.auth.session_auth import SessionAuth
from datetime import datetime, timedelta


class SessionExpAuth(SessionAuth):
    """Session with expiry date
    """
    def __init__(self):
        """Set instance attributes
        """
        try:
            duration = os.getenv('SESSION_DURATION')
            if duration is None or len(duration) == 0:
                raise ValueError('Session Duration is not set')

            self.session_duration = int(duration)
        except (TypeError, ValueError, KeyError):
            self.session_duration = 0

    def create_session(self, user_id=None):
        """Create an expiring session
        Parameters:
            - user_id : str
        """
        session_id = super().create_session(user_id)
        if not session_id:
            return None
        session_dictionary = {}
        self.user_id_by_session_id[session_id] = session_dictionary
        session_dictionary['user_id'] = user_id
        session_dictionary['created_at'] = datetime.now()
        return session_id

    def user_id_for_session_id(self, session_id=None):
        """Get the ID of a USER on this SESSION
        """
        if session_id is None:
            return None
        if session_id not in self.user_id_by_session_id:
            return None
        session_dictionary = self.user_id_by_session_id.get(session_id)
        if self.session_duration <= 0:
            return session_dictionary.get('user_id')
        if 'created_at' not in session_dictionary:
            return None
        # Check if session is expired
        max_datetime = session_dictionary.get('created_at') + \
                timedelta(seconds=self.session_duration)    # noqa: E502, E128
        if max_datetime < datetime.now():
            return None
        return session_dictionary['user_id']

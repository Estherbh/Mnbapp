import streamlit as st
import secrets
import re
from datetime import datetime, timedelta

class SecurityManager:
    @staticmethod
    def generate_csrf_token():
        if 'csrf_token' not in st.session_state:
            st.session_state.csrf_token = secrets.token_hex(32)
        return st.session_state.csrf_token

    @staticmethod
    def verify_csrf_token(token):
        if 'csrf_token' not in st.session_state:
            return False
        return secrets.compare_digest(token, st.session_state.csrf_token)

    @staticmethod
    def sanitize_input(input_str):
        """Basic sanitization to prevent XSS/Injection."""
        if not isinstance(input_str, str):
            return input_str
        # Remove potentially dangerous characters/tags
        return re.sub(r'[<>&\'"]', '', input_str)

    @staticmethod
    def check_session_timeout(timeout_minutes=30):
        if 'last_activity' not in st.session_state:
            st.session_state.last_activity = datetime.now()
            return True
        
        elapsed = datetime.now() - st.session_state.last_activity
        if elapsed > timedelta(minutes=timeout_minutes):
            st.session_state.authenticated = False
            st.session_state.user = None
            st.warning("Session expirée. Veuillez vous reconnecter.")
            return False
            
        st.session_state.last_activity = datetime.now()
        return True

    @staticmethod
    def log_security_event(event_type, details):
        # In production, log to a secure file or monitoring system
        timestamp = datetime.now().isoformat()
        # print(f"[SECURITY][{timestamp}] {event_type}: {details}") # Uncomment for server logs

import streamlit as st
import json
import bcrypt
import os
from datetime import datetime, timedelta
import re
import time

USERS_FILE = "users.json"
MAX_LOGIN_ATTEMPTS = 5
LOCKOUT_TIME_MINUTES = 15

class SecureAuthManager:
    def __init__(self):
        self.users = self.load_users()
        if 'login_attempts' not in st.session_state:
            st.session_state.login_attempts = 0
        if 'last_failed_login' not in st.session_state:
            st.session_state.last_failed_login = None

    def load_users(self):
        if not os.path.exists(USERS_FILE):
            return {}
        try:
            with open(USERS_FILE, 'r') as f:
                data = json.load(f)
                return {u['email']: u for u in data.get('users', [])}
        except Exception as e:
            st.error(f"Erreur chargement utilisateurs: {e}")
            return {}

    def save_users(self):
        try:
            data = {"users": list(self.users.values())}
            with open(USERS_FILE, 'w') as f:
                json.dump(data, f, indent=2)
            return True
        except Exception as e:
            st.error(f"Erreur sauvegarde utilisateurs: {e}")
            return False

    def verify_password(self, plain_password, hashed_password):
        return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password.encode('utf-8'))

    def hash_password(self, password):
        return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

    def validate_password_strength(self, password):
        if len(password) < 8:
            return False, "Le mot de passe doit contenir au moins 8 caractères."
        if not re.search(r"[A-Z]", password):
            return False, "Le mot de passe doit contenir au moins une majuscule."
        if not re.search(r"[0-9]", password):
            return False, "Le mot de passe doit contenir au moins un chiffre."
        if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
            return False, "Le mot de passe doit contenir au moins un caractère spécial."
        return True, ""

    def check_login(self, email, password):
        # Rate limiting check - DISABLED FOR DEBUGGING
        # if st.session_state.login_attempts >= MAX_LOGIN_ATTEMPTS:
        #     if st.session_state.last_failed_login:
        #         elapsed = datetime.now() - st.session_state.last_failed_login
        #         if elapsed < timedelta(minutes=LOCKOUT_TIME_MINUTES):
        #             remaining = LOCKOUT_TIME_MINUTES - int(elapsed.total_seconds() / 60)
        #             st.error(f"Trop de tentatives échouées. Réessayez dans {remaining} minutes.")
        #             return False
        #         else:
        #             # Reset after lockout period
        #             st.session_state.login_attempts = 0
        #             st.session_state.last_failed_login = None

        user = self.users.get(email)
        
        if user and self.verify_password(password, user['password_hash']):
            st.session_state.login_attempts = 0
            st.session_state.last_failed_login = None
            st.session_state.authenticated = True
            st.session_state.user = user
            st.session_state.email = email
            return True

        st.session_state.login_attempts += 1
        st.session_state.last_failed_login = datetime.now()
        st.error(f"Email ou mot de passe incorrect. Tentatives restantes: {MAX_LOGIN_ATTEMPTS - st.session_state.login_attempts}")
        return False

    def change_password(self, email, old_password, new_password):
        user = self.users.get(email)
        if not user:
            return False, "Utilisateur non trouvé."
            
        if not self.verify_password(old_password, user['password_hash']):
            return False, "Ancien mot de passe incorrect."
            
        is_valid, msg = self.validate_password_strength(new_password)
        if not is_valid:
            return False, msg
            
        user['password_hash'] = self.hash_password(new_password)
        user['must_change_password'] = False
        self.users[email] = user
        if self.save_users():
            return True, "Mot de passe modifié avec succès."
        else:
            return False, "Erreur lors de la sauvegarde."

    def login_form(self):
        # Center the logo with smaller size
        col_logo1, col_logo2, col_logo3 = st.columns([1,2,1])
        with col_logo2:
            try:
                st.image("VNP LOGO FRENCH.jpg", width=200)
            except:
                pass
        
        st.markdown(f"""
            <div style='text-align: center; padding: 30px;'>
                <h1 style='color:#00A87D'>Relations Extérieures / PNVi</h1>
            </div>
        """, unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns([1,2,1])
        with col2:
            with st.form("login_form"):
                email = st.text_input("Email Professionnel")
                password = st.text_input("Mot de passe", type="password")
                submit = st.form_submit_button("Connexion Sécurisée")
                
                if submit:
                    if self.check_login(email.strip(), password.strip()):
                        st.rerun()

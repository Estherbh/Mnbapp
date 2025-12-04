import os
import json
import pickle
import io
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload, MediaFileUpload
import streamlit as st
from datetime import datetime

SCOPES = ['https://www.googleapis.com/auth/drive']
CLIENT_SECRET_FILE = 'client_secret.json'
TOKEN_FILE = 'token.pickle'
CONFIG_FILE = 'config.json'

class DriveManager:
    def __init__(self):
        self.creds = None
        self.service = None
        self.config = self.load_config()
        self.authenticate(allow_browser=False)

    def load_config(self):
        if os.path.exists(CONFIG_FILE):
            with open(CONFIG_FILE, 'r') as f:
                return json.load(f)
        return {}

    def save_config(self):
        with open(CONFIG_FILE, 'w') as f:
            json.dump(self.config, f, indent=2)

    def authenticate(self, allow_browser=True):
        """Authenticates the user with Google Drive API."""
        try:
            if os.path.exists(TOKEN_FILE):
                with open(TOKEN_FILE, 'rb') as token:
                    self.creds = pickle.load(token)
            
            if not self.creds or not self.creds.valid:
                if self.creds and self.creds.expired and self.creds.refresh_token:
                    try:
                        self.creds.refresh(Request())
                    except Exception:
                        self.creds = None
                
                if not self.creds and allow_browser:
                    if os.path.exists(CLIENT_SECRET_FILE):
                        flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRET_FILE, SCOPES)
                        ports = [8502, 8503, 8504, 8505, 9000, 9001]
                        for port in ports:
                            try:
                                self.creds = flow.run_local_server(
                                    port=port,
                                    success_message="Authentification réussie ! Fermez cet onglet."
                                )
                                with open(TOKEN_FILE, 'wb') as token:
                                    pickle.dump(self.creds, token)
                                break
                            except OSError:
                                continue

            if self.creds:
                self.service = build('drive', 'v3', credentials=self.creds)
        except Exception as e:
            if allow_browser:
                st.error(f"Erreur Drive: {e}")

    def list_folders(self):
        """Lists folders in the root directory."""
        if not self.service: return []
        try:
            results = self.service.files().list(
                q="mimeType='application/vnd.google-apps.folder' and trashed=false",
                pageSize=50, fields="nextPageToken, files(id, name)").execute()
            return results.get('files', [])
        except Exception as e:
            st.error(f"Erreur listing dossiers: {e}")
            return []

    def set_data_folder(self, folder_id):
        """Sets the folder ID to sync data from."""
        self.config['drive_folder_id'] = folder_id
        self.save_config()

    def sync_data(self):
        """Downloads configured files from the selected Drive folder."""
        if not self.service:
            return False, "Non authentifié."
        
        folder_id = self.config.get('drive_folder_id')
        if not folder_id:
            return False, "Aucun dossier configuré."

        expected_files = [
            "COLLECTE DES DONNÉES TERRAIN_RELATIONS EXTERIEURES (2).xlsx",
            "Revue de la presse2.xlsx"
        ]
        synced_count = 0
        
        try:
            query = f"'{folder_id}' in parents and trashed=false"
            results = self.service.files().list(q=query, fields="files(id, name)").execute()
            drive_files = {f['name']: f['id'] for f in results.get('files', [])}
            
            for target_filename in expected_files:
                if target_filename in drive_files:
                    file_id = drive_files[target_filename]
                    request = self.service.files().get_media(fileId=file_id)
                    fh = io.FileIO(target_filename, 'wb')
                    downloader = MediaIoBaseDownload(fh, request)
                    done = False
                    while done is False:
                        status, done = downloader.next_chunk()
                    fh.close()
                    synced_count += 1
            
            self.config['last_sync'] = datetime.now().isoformat()
            self.save_config()
            return True, f"Synchronisation réussie ({synced_count} fichiers)."
            
        except Exception as e:
            return False, f"Erreur: {e}"

    def upload_file(self, file_path, folder_id=None):
        """Uploads a file to Google Drive."""
        if not self.service:
            return False, "Non authentifié."
        
        try:
            file_metadata = {'name': os.path.basename(file_path)}
            if folder_id:
                file_metadata['parents'] = [folder_id]
            
            media = MediaFileUpload(file_path, resumable=True)
            
            file = self.service.files().create(body=file_metadata, media_body=media, fields='id').execute()
            return True, f"Fichier uploadé avec succès (ID: {file.get('id')})"
        except Exception as e:
            return False, f"Erreur d'upload: {e}"

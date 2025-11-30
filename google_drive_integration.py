import streamlit as st
import os
import json
import pickle
import io
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload
from datetime import datetime

SCOPES = ['https://www.googleapis.com/auth/drive.readonly']
CLIENT_SECRET_FILE = 'client_secret.json'
TOKEN_FILE = 'token.pickle'
CONFIG_FILE = 'config.json'

def render_drive_sidebar():
    """Render Google Drive integration in the sidebar"""
    st.markdown("---")
    st.subheader("🔗 Google Drive")

    # Initialize session state
    if 'drive_authenticated' not in st.session_state:
        st.session_state.drive_authenticated = False
    if 'drive_service' not in st.session_state:
        st.session_state.drive_service = None
    if 'drive_config' not in st.session_state:
        st.session_state.drive_config = load_config()

    # Authentication section
    if not st.session_state.drive_authenticated:
        st.info("🔐 Connectez-vous à Google Drive pour synchroniser les données.")

        if st.button("🔑 Authentifier Google Drive", use_container_width=True):
            try:
                creds = authenticate_drive()
                if creds:
                    st.session_state.drive_service = build('drive', 'v3', credentials=creds)
                    st.session_state.drive_authenticated = True
                    st.success("✅ Connecté à Google Drive!")
                    st.rerun()
            except Exception as e:
                st.error(f"❌ Erreur d'authentification: {str(e)}")
                if "WinError 10048" in str(e):
                    st.warning("💡 Le port 8502 est déjà utilisé. Essayez de fermer d'autres applications ou redémarrez l'application.")
    else:
        st.success("✅ Connecté à Google Drive")

        # Folder selection
        folders = list_drive_folders()
        if folders:
            folder_options = ["-- Sélectionner un dossier --"] + [name for name, _ in folders]
            selected_folder = st.selectbox(
                "📁 Dossier de données",
                options=folder_options,
                key='drive_folder_select'
            )

            if selected_folder != "-- Sélectionner un dossier --":
                folder_id = next((fid for name, fid in folders if name == selected_folder), None)
                if folder_id:
                    st.session_state.drive_config['drive_folder_id'] = folder_id
                    save_config(st.session_state.drive_config)

                    # List files in folder
                    files = list_drive_files(folder_id)
                    if files:
                        st.subheader("📄 Fichiers disponibles")
                        for file_name, file_id, mime_type in files:
                            col1, col2 = st.columns([3, 1])
                            with col1:
                                st.write(f"📄 {file_name}")
                            with col2:
                                if st.button(f"📥 Télécharger", key=f"download_{file_id}"):
                                    download_drive_file(file_id, file_name)
                                    st.success(f"✅ {file_name} téléchargé!")

        # Sync button
        if st.button("🔄 Synchroniser les données", use_container_width=True):
            success, message = sync_drive_data()
            if success:
                st.success(message)
                st.rerun()
            else:
                st.error(message)

        # Disconnect
        if st.button("🔌 Déconnecter", use_container_width=True):
            st.session_state.drive_authenticated = False
            st.session_state.drive_service = None
            st.rerun()

def load_config():
    """Load configuration from file"""
    if os.path.exists(CONFIG_FILE):
        try:
            with open(CONFIG_FILE, 'r') as f:
                return json.load(f)
        except:
            pass
    return {}

def save_config(config):
    """Save configuration to file"""
    try:
        with open(CONFIG_FILE, 'w') as f:
            json.dump(config, f, indent=2)
    except Exception as e:
        st.error(f"Erreur sauvegarde config: {e}")

def authenticate_drive():
    """Authenticate with Google Drive API"""
    creds = None

    # Load existing token
    if os.path.exists(TOKEN_FILE):
        try:
            with open(TOKEN_FILE, 'rb') as token:
                creds = pickle.load(token)
        except:
            creds = None

    # Refresh or re-authenticate if needed
    if creds and creds.expired and creds.refresh_token:
        try:
            creds.refresh(Request())
        except:
            creds = None

    if not creds:
        if os.path.exists(CLIENT_SECRET_FILE):
            try:
                flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRET_FILE, SCOPES)
                # Try different ports to avoid conflicts
                ports_to_try = [8505, 8506, 8507, 8508, 8509, 8510, 9000, 9001, 9002, 9003, 9004, 9005, 8502, 8503, 8504, 8080, 8081]
                creds = None

                for port in ports_to_try:
                    try:
                        creds = flow.run_local_server(
                            port=port,
                            success_message="Authentification réussie ! Vous pouvez fermer cet onglet.",
                            open_browser=True
                        )
                        break
                    except Exception as e:
                        if "WinError 10048" in str(e) or "Address already in use" in str(e):
                            continue  # Try next port
                        else:
                            raise e

                if creds:
                    # Save token
                    with open(TOKEN_FILE, 'wb') as token:
                        pickle.dump(creds, token)

            except Exception as e:
                raise Exception(f"Erreur d'authentification Drive: {e}")

    return creds

def list_drive_folders():
    """List folders in Google Drive"""
    if not st.session_state.drive_service:
        return []

    try:
        results = st.session_state.drive_service.files().list(
            q="mimeType='application/vnd.google-apps.folder' and trashed=false",
            pageSize=50, fields="nextPageToken, files(id, name)").execute()
        return [(f['name'], f['id']) for f in results.get('files', [])]
    except Exception as e:
        st.error(f"Erreur listing dossiers: {e}")
        return []

def list_drive_files(folder_id):
    """List files in a specific folder"""
    if not st.session_state.drive_service:
        return []

    try:
        query = f"'{folder_id}' in parents and trashed=false"
        results = st.session_state.drive_service.files().list(
            q=query, fields="files(id, name, mimeType)").execute()
        return [(f['name'], f['id'], f.get('mimeType', '')) for f in results.get('files', [])]
    except Exception as e:
        st.error(f"Erreur listing fichiers: {e}")
        return []

def download_drive_file(file_id, file_name):
    """Download a file from Google Drive"""
    if not st.session_state.drive_service:
        return

    try:
        request = st.session_state.drive_service.files().get_media(fileId=file_id)
        fh = io.FileIO(file_name, 'wb')
        downloader = MediaIoBaseDownload(fh, request)
        done = False
        while done is False:
            status, done = downloader.next_chunk()
        fh.close()
    except Exception as e:
        st.error(f"Erreur téléchargement: {e}")

def sync_drive_data():
    """Sync data files from configured Drive folder"""
    if not st.session_state.drive_service:
        return False, "Non authentifié."

    folder_id = st.session_state.drive_config.get('drive_folder_id')
    if not folder_id:
        return False, "Aucun dossier configuré."

    try:
        # Expected files to sync
        expected_files = [
            "COLLECTE DES DONNÉES TERRAIN_RELATIONS EXTERIEURES (2).xlsx",
            "Revue de la presse2.xlsx"
        ]

        # List files in folder
        query = f"'{folder_id}' in parents and trashed=false"
        results = st.session_state.drive_service.files().list(
            q=query, fields="files(id, name)").execute()
        drive_files = {f['name']: f['id'] for f in results.get('files', [])}

        synced_count = 0
        for file_name in expected_files:
            if file_name in drive_files:
                download_drive_file(drive_files[file_name], file_name)
                synced_count += 1

        # Update last sync time
        st.session_state.drive_config['last_sync'] = datetime.now().isoformat()
        save_config(st.session_state.drive_config)

        return True, f"Synchronisation réussie ({synced_count} fichiers)."

    except Exception as e:
        return False, f"Erreur de synchronisation: {e}"

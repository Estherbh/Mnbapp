import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import time
from typing import List, Dict, Optional, Tuple
import re
from collections import Counter
import io
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# --- CONFIGURATION & THEME ---
# Virunga Color Palette
COLORS = {
    "ORANGE": "#EF7D00",
    "FOREST_GREEN": "#00A87D",
    "LIME_GREEN": "#DCDF00",
    "LAKE_BLUE": "#007D7D",
    "DARK_HEADER": "#2C3E50",
    "LIGHT_BG": "#F8F9FA",
    "WHITE": "#FFFFFF",
    "DANGER": "#DC3545",
    "SUCCESS": "#28A745",
    "GRAY": "#6c757d"
}

# Page Configuration
st.set_page_config(
    page_title="Virunga Intelligent Dashboard",
    page_icon="VNP LOGO FRENCH.jpg",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for Premium Look
st.markdown(f"""
    <style>
    /* Main Background */
    .stApp {{
        background-color: {COLORS['LIGHT_BG']};
    }}
    
    /* Headers */
    h1, h2, h3 {{
        color: {COLORS['DARK_HEADER']};
        font-family: 'Helvetica Neue', sans-serif;
        font-weight: 700;
    }}
    
    /* Custom Cards */
    .metric-card {{
        background-color: white;
        padding: 20px;
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        text-align: center;
        border-top: 5px solid {COLORS['FOREST_GREEN']};
        margin-bottom: 20px;
    }}
    
    .metric-value {{
        font-size: 28px;
        font-weight: bold;
        color: {COLORS['ORANGE']};
    }}
    
    .metric-label {{
        font-size: 14px;
        color: #666;
        text-transform: uppercase;
        letter-spacing: 1px;
    }}
    
    /* Sidebar */
    section[data-testid="stSidebar"] {{
        background-color: {COLORS['DARK_HEADER']};
    }}
    
    /* Buttons */
    .stButton>button {{
        background-color: {COLORS['ORANGE']};
        color: white;
        border-radius: 5px;
        border: none;
        padding: 10px 20px;
        font-weight: bold;
        transition: all 0.3s ease;
        width: 100%;
    }}
    .stButton>button:hover {{
        background-color: {COLORS['FOREST_GREEN']};
        box-shadow: 0 5px 15px rgba(0,0,0,0.2);
    }}
    </style>
""", unsafe_allow_html=True)

# --- DATA LOADER ---
# --- DATA LOADER OPTIMIZED ---
@st.cache_data(ttl=3600)
def load_data_optimized():
    """
    Loads data efficiently with caching and optimized Excel reading.
    """
    # File Paths
    FILE_ACTIVITIES = "COLLECTE DES DONNÉES TERRAIN_RELATIONS EXTERIEURES (2).xlsx"
    FILE_PRESS = "Revue de la presse.xlsx"
    
    df_activities = pd.DataFrame()
    df_visits = pd.DataFrame()
    df_press = pd.DataFrame()
    
    with st.spinner("⚡ Chargement des données en cours..."):
        # Load Activities
        try:
            # Optimize: Read only necessary columns if possible, but for now we read all and process
            df_activities = pd.read_excel(FILE_ACTIVITIES, sheet_name='Donnees_Activites')
            
            # Flexible column mapping using keyword search
            actual_cols = df_activities.columns.tolist()
            column_mapping_act = {}
            
            # Find columns by keywords
            for col in actual_cols:
                col_lower = col.lower()
                if 'date' in col_lower and 'activit' in col_lower:
                    column_mapping_act[col] = "Date_Activite"
                elif 'nom' in col_lower and 'activit' in col_lower:
                    column_mapping_act[col] = "Nom"
                elif col == 'Organisateur':
                    column_mapping_act[col] = "Organisateur"
                elif 'type' in col_lower and 'activit' in col_lower:
                    column_mapping_act[col] = "Type"
                elif 'secteur' in col_lower:
                    column_mapping_act[col] = "Secteur"
                elif 'ciser' in col_lower and 'lieu' in col_lower:
                    column_mapping_act[col] = "Lieu_Precis"
                elif 'hommes' in col_lower:
                    column_mapping_act[col] = "Hommes"
                elif 'femmes' in col_lower:
                    column_mapping_act[col] = "Femmes"
                elif 'enfants' in col_lower:
                    column_mapping_act[col] = "Enfants"
            
            df_activities.rename(columns=column_mapping_act, inplace=True)
            df_activities.columns = df_activities.columns.str.strip()
            
            # Use Date_Activite for temporal analysis
            if 'Date_Activite' in df_activities.columns:
                df_activities['Date_Activite'] = pd.to_datetime(df_activities['Date_Activite'], errors='coerce')
                df_activities['Mois'] = df_activities['Date_Activite'].dt.strftime('%Y-%m')
                
            # Pre-calculate totals
            cols_num = ['Hommes', 'Femmes', 'Enfants']
            for col in cols_num:
                if col in df_activities.columns:
                    df_activities[col] = pd.to_numeric(df_activities[col], errors='coerce').fillna(0).astype(int)
            
            if all(c in df_activities.columns for c in cols_num):
                df_activities['Total_Participants'] = df_activities[cols_num].sum(axis=1)

            # Load Visits
            try:
                df_visits = pd.read_excel(FILE_ACTIVITIES, sheet_name='Visitestage')
                
                # Use first column (Timestamp) as Date
                if len(df_visits.columns) > 0:
                    df_visits.rename(columns={df_visits.columns[0]: 'Date'}, inplace=True)
                
                # Map other columns by keywords
                for col in df_visits.columns:
                    col_lower = str(col).lower()
                    if 'nombre' in col_lower and 'visiteur' in col_lower:
                        df_visits.rename(columns={col: 'Nombre'}, inplace=True)
                    elif 'objet' in col_lower:
                        df_visits.rename(columns={col: 'Objet'}, inplace=True)
                    elif 'organisation' in col_lower or 'institution' in col_lower:
                        df_visits.rename(columns={col: 'Organisation'}, inplace=True)
                
                df_visits.columns = df_visits.columns.str.strip()
                
                if 'Date' in df_visits.columns:
                    df_visits['Date'] = pd.to_datetime(df_visits['Date'], errors='coerce')
                    df_visits['Mois'] = df_visits['Date'].dt.strftime('%Y-%m')
                if 'Nombre' in df_visits.columns:
                    df_visits['Nombre'] = pd.to_numeric(df_visits['Nombre'], errors='coerce').fillna(0).astype(int)
            except Exception as e:
                st.warning(f"Note: Feuille 'Visitestage' non trouvee ({e})")

        except Exception as e:
            st.error(f"Erreur chargement Activités: {e}")
            df_activities = pd.DataFrame(columns=["Date_Activite", "Organisateur", "Secteur", "Lieu_Precis", "Type", "Hommes", "Femmes", "Enfants", "Total_Participants"])

        # Load Press Review
        try:
            df_press = pd.read_excel(FILE_PRESS)
            
            # Map columns by keywords
            for col in df_press.columns:
                col_lower = str(col).lower()
                if 'date' in col_lower or 'dtae' in col_lower:
                    df_press.rename(columns={col: 'Date'}, inplace=True)
                elif 'media' in col_lower or 'source' in col_lower:
                    df_press.rename(columns={col: 'Media'}, inplace=True)
                elif 'titre' in col_lower or 'title' in col_lower:
                    df_press.rename(columns={col: 'Titre'}, inplace=True)
                elif 'ton' in col_lower or 'sentiment' in col_lower:
                    df_press.rename(columns={col: 'Ton'}, inplace=True)
                elif 'thematique' in col_lower or 'theme' in col_lower:
                    df_press.rename(columns={col: 'Thematique'}, inplace=True)
                elif 'zone' in col_lower and 'concern' in col_lower:
                    df_press.rename(columns={col: 'Zone_Concernee'}, inplace=True)
            
            df_press.columns = df_press.columns.str.strip()
            
            # Extract zone from 'Zone_Concernee' (text before ':')
            if 'Zone_Concernee' in df_press.columns:
                df_press['Zone'] = df_press['Zone_Concernee'].astype(str).apply(
                    lambda x: x.split(':')[0].strip() if ':' in x else x
                )
            
            if 'Date' in df_press.columns:
                df_press['Date'] = pd.to_datetime(df_press['Date'], errors='coerce')
                df_press['Mois'] = df_press['Date'].dt.strftime('%Y-%m')
            
            # Clean NaN values to prevent JSON errors
            df_press = df_press.fillna('')
                
        except Exception as e:
            st.error(f"Erreur chargement Presse: {e}")
            df_press = pd.DataFrame(columns=["Date", "Media", "Titre", "Ton", "Thematique", "Zone"])

    return df_activities, df_visits, df_press

# --- AUTHENTICATION MANAGER ---
class AuthManager:
    def __init__(self):
        # In production, use a database or secure secrets manager
        self.users = {
            "bbwende@virunga.org": {"role": "owner", "name": "Bienvenu Bwende"},
            "admin@virunga.org": {"role": "admin", "name": "Admin System"},
            "guest@virunga.org": {"role": "viewer", "name": "Invité"}
        }

    def check_password(self):
        """Simple password check for demo purposes."""
        if "authenticated" not in st.session_state:
            st.session_state.authenticated = False

        if not st.session_state.authenticated:
            st.markdown(f"""
                <div style='text-align: center; padding: 50px;'>
                    <h1 style='color:{COLORS['FOREST_GREEN']}'>Virunga Intelligence</h1>
                    <p>Système de Monitoring Avancé</p>
                </div>
            """, unsafe_allow_html=True)
            
            col1, col2, col3 = st.columns([1,2,1])
            with col2:
                email = st.text_input("Email Professionnel", key="login_email")
                password = st.text_input("Mot de passe", type="password", key="login_password")
                if st.button("Connexion Sécurisée"):
                    email_clean = email.strip()
                    password_clean = password.strip()
                    # st.write(f"Debug: '{email_clean}' / '{password_clean}'") # Uncomment for debug
                    if email_clean in self.users and password_clean == "virunga2025":
                        st.session_state.authenticated = True
                        st.session_state.user = self.users[email_clean]
                        st.session_state.email = email_clean
                        st.rerun()
                    else:
                        st.error(f"Accès refusé. Vérifiez vos identifiants. (Tentative: {email_clean})")
            return False
        return True

# --- INTELLIGENCE ENGINE (ML & ANALYTICS) ---
class VirungaIntelligence:
    def __init__(self):
        pass

    def analyze_sentiment(self, text: str) -> Tuple[str, float]:
        """
        Analyzes sentiment of text.
        In production, connect to OpenAI API here.
        """
        # Mock logic based on keywords for demo
        positive_words = ['succès', 'réussite', 'bon', 'paix', 'développement', 'naissance', 'espoir']
        negative_words = ['guerre', 'conflit', 'menace', 'décès', 'attaque', 'inquiet']
        
        text_lower = str(text).lower()
        score = 0
        for word in positive_words:
            if word in text_lower: score += 1
        for word in negative_words:
            if word in text_lower: score -= 1
            
        if score > 0: return "Positif", 0.8 + (score * 0.05)
        if score < 0: return "Négatif", 0.2 + (score * 0.05)
        return "Neutre", 0.5

    def generate_kpis(self, df: pd.DataFrame, form_type: str) -> Dict:
        """Generates KPIs dynamically based on form type."""
        kpis = {}
        if form_type == "activities":
            kpis['total_activities'] = len(df)
            kpis['total_participants'] = df['Hommes'].sum() + df['Femmes'].sum() + df['Enfants'].sum()
            kpis['avg_participants'] = int(kpis['total_participants'] / len(df)) if len(df) > 0 else 0
            kpis['top_sector'] = df['Secteur'].mode()[0] if not df.empty else "N/A"
        elif form_type == "visitors":
            kpis['total_visitors'] = df['Nombre'].sum()
            kpis['top_site'] = df['Site'].mode()[0] if not df.empty else "N/A"
        return kpis

    @st.cache_data
    def cluster_activities(_self, df: pd.DataFrame):
        """
        Uses Machine Learning (K-Means) to group activities.
        Cached for performance.
        """
        from sklearn.cluster import KMeans
        from sklearn.preprocessing import StandardScaler
        from sklearn.metrics import silhouette_score
        
        if len(df) < 5: return df, 0.0
        
        # Prepare features
        if 'Total_Participants' not in df.columns:
             df['Total_Participants'] = df['Hommes'] + df['Femmes'] + df['Enfants']
             
        features = df[['Total_Participants']].fillna(0)
        
        scaler = StandardScaler()
        scaled_features = scaler.fit_transform(features)
        
        kmeans = KMeans(n_clusters=3, random_state=42)
        df['Cluster'] = kmeans.fit_predict(scaled_features)
        
        # Calculate Silhouette Score
        score = silhouette_score(scaled_features, df['Cluster'])
        
        # Map clusters
        centroids = kmeans.cluster_centers_
        sorted_idx = np.argsort(centroids.flatten())
        cluster_map = {sorted_idx[0]: 'Standard', sorted_idx[1]: 'Impact Moyen', sorted_idx[2]: 'Impact Majeur'}
        df['Impact_Label'] = df['Cluster'].map(cluster_map)
        
        return df, score

# --- UI COMPONENTS ---
def render_sidebar():
    with st.sidebar:
        # Use local logo if available
        try:
            st.image("VNP LOGO FRENCH.jpg", width=150)
        except:
            st.image("https://virunga.org/wp-content/themes/virunga/assets/images/logo.svg", width=150)
            
        st.markdown("---")
        if st.session_state.get('authenticated', False):
            st.write(f"User: **{st.session_state.user['name']}**")
            st.write(f"Role: {st.session_state.user['role'].upper()}")
        st.markdown("---")
        
        page = st.radio("Navigation", [
            "Vue d'ensemble",
            "Activités Terrain",
            "Visites & Stages",
            "Revue de Presse",
            "Administration"
        ])
        
        st.markdown("---")
        if st.button("Déconnexion"):
            st.session_state.authenticated = False
            st.rerun()
            
        return page

def render_kpi_row(kpis: Dict):
    """Renders a row of KPI cards."""
    cols = st.columns(len(kpis))
    for i, (label, value) in enumerate(kpis.items()):
        with cols[i]:
            st.markdown(f"""
                <div class="metric-card">
                    <div class="metric-label">{label}</div>
                    <div class="metric-value">{value}</div>
                </div>
            """, unsafe_allow_html=True)

def render_compact_type_chart(df):
    """Renders a compact horizontal bar chart for Activity Types."""
    if 'Type' not in df.columns: return None
    
    type_counts = df['Type'].value_counts().head(5)
    
    fig = go.Figure(data=[
        go.Bar(
            x=type_counts.values,
            y=type_counts.index,
            orientation='h',
            marker=dict(color=type_counts.values, colorscale='Viridis', showscale=False),
            text=type_counts.values,
            textposition='auto',
        )
    ])
    
    fig.update_layout(
        height=300,
        margin=dict(l=0, r=0, t=30, b=0),
        xaxis_title="Nombre",
        yaxis=dict(categoryorder='total ascending'),
        plot_bgcolor='rgba(0,0,0,0)'
    )
    return fig

def render_demographic_donut(df):
    """Renders a readable donut chart for demographics."""
    if not all(col in df.columns for col in ['Hommes', 'Femmes', 'Enfants']): return None
    
    values = [df['Hommes'].sum(), df['Femmes'].sum(), df['Enfants'].sum()]
    labels = ['Hommes', 'Femmes', 'Enfants']
    
    fig = go.Figure(data=[go.Pie(
        labels=labels,
        values=values,
        hole=0.6,
        marker_colors=[COLORS['LAKE_BLUE'], COLORS['ORANGE'], COLORS['LIME_GREEN']],
        textinfo='label+percent+value',
        textfont_size=12
    )])
    
    fig.update_layout(
        height=350,
        margin=dict(l=20, r=20, t=20, b=20),
        showlegend=True,
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
    )
    return fig

def convert_df_to_excel(df):
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        df.to_excel(writer, index=False, sheet_name='Donnees')
    processed_data = output.getvalue()
    return processed_data

def send_email_notification(subject, body, to_email):
    """
    Mock function to send email.
    In production, use smtplib with Gmail or SendGrid API.
    """
    with st.spinner(f"Envoi du mail à {to_email}..."):
        time.sleep(1) # Simulate network delay
    st.toast(f"Email envoyé avec succès à {to_email}!", icon="E")

# --- MAIN APP LOGIC ---
def main():
    auth = AuthManager()
    if not auth.check_password():
        return

    page = render_sidebar()
    
    # Load Data
    # Load Data Optimized
    df_activities, df_visits, df_press = load_data_optimized()
    intelligence = VirungaIntelligence()

    if page == "Vue d'ensemble":
        st.title("Tableau de Bord Exécutif")
        st.markdown("Bienvenue sur le système de monitoring centralisé du Parc National des Virunga.")
        
        # Global Stats
        total_acts = len(df_activities)
        total_visits = df_visits['Nombre'].sum() if not df_visits.empty and 'Nombre' in df_visits.columns else 0
        total_press = len(df_press)
        
        # Calculate Sentiment Score safely
        if not df_press.empty and 'Ton' in df_press.columns:
            positive_count = df_press[df_press['Ton'].str.contains('Positif', case=False, na=False)].shape[0]
            sentiment_score = int((positive_count / total_press) * 100) if total_press > 0 else 0
        else:
            sentiment_score = 0
        
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.markdown(f'<div class="metric-card"><div class="metric-value">{total_acts}</div><div class="metric-label">Activités Terrain</div></div>', unsafe_allow_html=True)
        with col2:
            st.markdown(f'<div class="metric-card"><div class="metric-value">{total_visits}</div><div class="metric-label">Visiteurs/Stagiaires</div></div>', unsafe_allow_html=True)
        with col3:
            st.markdown(f'<div class="metric-card"><div class="metric-value">{total_press}</div><div class="metric-label">Articles Presse</div></div>', unsafe_allow_html=True)
        with col4:
            st.markdown(f'<div class="metric-card"><div class="metric-value">{sentiment_score}%</div><div class="metric-label">Score Perception</div></div>', unsafe_allow_html=True)

        # Recent Activity Chart
        if not df_activities.empty and 'Date' in df_activities.columns:
            st.subheader("Tendance des Activités")
            daily_counts = df_activities.groupby('Date').size().reset_index(name='Nombre')
            fig_trend = px.line(daily_counts, x='Date', y='Nombre', title="Évolution des Activités", color_discrete_sequence=[COLORS['ORANGE']])
            st.plotly_chart(fig_trend, use_container_width=True)

    elif page == "Activités Terrain":
        st.title("Analyse des Activités Terrain")
        
        # --- FILTERS ---
        with st.expander("Filtres Avancés", expanded=True):
            col1, col2, col3, col4 = st.columns(4)
            
            # Filter by Month
            months = sorted(df_activities['Mois'].dropna().unique()) if 'Mois' in df_activities.columns else []
            selected_month = col1.multiselect("Mois", months)
            
            # Filter by Organizer
            organizers = sorted(df_activities['Organisateur'].dropna().unique()) if 'Organisateur' in df_activities.columns else []
            selected_organizer = col2.multiselect("Organisateur", organizers)
            
            # Filter by Sector
            sectors = sorted(df_activities['Secteur'].dropna().unique()) if 'Secteur' in df_activities.columns else []
            selected_sector = col3.multiselect("Secteur", sectors)
            
            # Filter by Type
            types = sorted(df_activities['Type'].dropna().unique()) if 'Type' in df_activities.columns else []
            selected_type = col4.multiselect("Type d'Activité", types)

        # Apply Filters
        filtered_df = df_activities.copy()
        if selected_month: filtered_df = filtered_df[filtered_df['Mois'].isin(selected_month)]
        if selected_organizer: filtered_df = filtered_df[filtered_df['Organisateur'].isin(selected_organizer)]
        if selected_sector: filtered_df = filtered_df[filtered_df['Secteur'].isin(selected_sector)]
        if selected_type: filtered_df = filtered_df[filtered_df['Type'].isin(selected_type)]
        
        # --- KPIS ---
        st.markdown("### Indicateurs Clés")
        kpis = {
            "Total Activités": len(filtered_df),
            "Participants (Est.)": int(filtered_df['Hommes'].sum() + filtered_df['Femmes'].sum()) if 'Hommes' in filtered_df.columns else 0,
            "Lieux Couverts": filtered_df['Lieu'].nunique() if 'Lieu' in filtered_df.columns else 0
        }
        render_kpi_row(kpis)
        
        # --- CHARTS ---
        st.markdown("### Visualisation Avancée")
        
        # Row 1: Demographics and Zones
        c1, c2 = st.columns(2)
        
        with c1:
            st.subheader("Démographie")
            fig_demo = render_demographic_donut(filtered_df)
            if fig_demo:
                st.plotly_chart(fig_demo, use_container_width=True)
            else:
                st.warning("Données démographiques manquantes.")
                
        with c2:
            st.subheader("Zones Couvertes")
            if 'Secteur' in filtered_df.columns and not filtered_df['Secteur'].isna().all():
                sector_counts = filtered_df['Secteur'].value_counts().reset_index()
                sector_counts.columns = ['Secteur', 'Nombre']
                fig_sect = px.bar(sector_counts, x='Secteur', y='Nombre', color='Secteur', 
                                color_discrete_sequence=px.colors.qualitative.Prism)
                fig_sect.update_layout(height=350, margin=dict(l=0, r=0, t=20, b=0), showlegend=False)
                st.plotly_chart(fig_sect, use_container_width=True)
            else:
                st.info("Aucune donnée de secteur disponible.")

        # Row 2: Organizers and Types
        c3, c4 = st.columns(2)
        with c3:
            st.subheader("Top Organisateurs")
            if 'Organisateur' in filtered_df.columns and not filtered_df['Organisateur'].isna().all():
                top_orgs = filtered_df['Organisateur'].value_counts().head(10).reset_index()
                top_orgs.columns = ['Organisateur', 'Nombre']
                fig_org = px.bar(top_orgs, x='Nombre', y='Organisateur', orientation='h', color_discrete_sequence=[COLORS['FOREST_GREEN']])
                fig_org.update_layout(height=300, yaxis={'categoryorder':'total ascending'}, margin=dict(l=0, r=0, t=20, b=0))
                st.plotly_chart(fig_org, use_container_width=True)
            else:
                st.info("Aucune donnée d'organisateur disponible.")
        
        with c4:
             st.subheader("Types d'Activité")
             fig_type = render_compact_type_chart(filtered_df)
             if fig_type:
                st.plotly_chart(fig_type, use_container_width=True)
             else:
                st.info("Aucune donnée de type disponible.")

        # Row 3: Temporal Evolution
        st.subheader("Evolution Temporelle")
        if 'Date_Activite' in filtered_df.columns and not filtered_df['Date_Activite'].isna().all():
            monthly_counts = filtered_df.groupby(filtered_df['Date_Activite'].dt.to_period('M')).size().reset_index(name='Nombre')
            monthly_counts['Date_Activite'] = monthly_counts['Date_Activite'].dt.to_timestamp()
            fig_temp = px.line(monthly_counts, x='Date_Activite', y='Nombre', markers=True,
                             title="Nombre d'activites par mois (base sur Date de l'activite)",
                             color_discrete_sequence=[COLORS['ORANGE']])
            fig_temp.update_layout(height=300, margin=dict(l=0, r=0, t=40, b=0))
            st.plotly_chart(fig_temp, use_container_width=True)
        else:
            st.info("Aucune donnee temporelle disponible.")
        
        # Row 4: Zone Details (Secteur + Lieu Precis)
        st.subheader("Details des Zones")
        c5, c6 = st.columns(2)
        with c5:
            st.subheader("Par Secteur")
            if 'Secteur' in filtered_df.columns and not filtered_df['Secteur'].isna().all():
                sector_detail = filtered_df['Secteur'].value_counts().reset_index()
                sector_detail.columns = ['Secteur', 'Nombre']
                fig_sect_detail = px.pie(sector_detail, values='Nombre', names='Secteur',
                                        color_discrete_sequence=px.colors.qualitative.Set3)
                fig_sect_detail.update_layout(height=300, margin=dict(l=0, r=0, t=20, b=0))
                st.plotly_chart(fig_sect_detail, use_container_width=True)
        
        with c6:
            st.subheader("Lieux Precis (Top 10)")
            if 'Lieu_Precis' in filtered_df.columns and not filtered_df['Lieu_Precis'].isna().all():
                lieu_counts = filtered_df['Lieu_Precis'].value_counts().head(10).reset_index()
                lieu_counts.columns = ['Lieu', 'Nombre']
                fig_lieu = px.bar(lieu_counts, x='Nombre', y='Lieu', orientation='h',
                                color_discrete_sequence=[COLORS['FOREST_GREEN']])
                fig_lieu.update_layout(height=300, yaxis={'categoryorder':'total ascending'}, margin=dict(l=0, r=0, t=20, b=0))
                st.plotly_chart(fig_lieu, use_container_width=True)

        # --- CLUSTERING & PERFORMANCE ---
        st.markdown("### Classification Automatique des Activites")
        if len(filtered_df) > 5:
            df_clustered, score = intelligence.cluster_activities(filtered_df.copy())
            
            # Simplified UX for Clustering
            col_exp1, col_exp2, col_exp3 = st.columns(3)
            
            std_count = len(df_clustered[df_clustered['Impact_Label'] == 'Standard'])
            med_count = len(df_clustered[df_clustered['Impact_Label'] == 'Impact Moyen'])
            maj_count = len(df_clustered[df_clustered['Impact_Label'] == 'Impact Majeur'])
            
            with col_exp1:
                st.metric("Standard", std_count, help="Activites regulieres, petit comite.")
            with col_exp2:
                st.metric("Impact Moyen", med_count, help="Activites importantes, participation moyenne.")
            with col_exp3:
                st.metric("Impact Majeur", maj_count, help="Grands evenements, forte mobilisation.")

            # Simple bar chart instead of scatter
            impact_summary = df_clustered['Impact_Label'].value_counts().reset_index()
            impact_summary.columns = ['Categorie', 'Nombre']
            
            fig_impact = px.bar(
                impact_summary,
                x='Categorie',
                y='Nombre',
                color='Categorie',
                title="Repartition des Activites par Impact",
                color_discrete_map={
                    'Standard': '#95a5a6',
                    'Impact Moyen': COLORS['LAKE_BLUE'],
                    'Impact Majeur': COLORS['ORANGE']
                },
                text='Nombre'
            )
            fig_impact.update_layout(
                height=350,
                showlegend=False,
                xaxis_title="Categorie d'Impact",
                yaxis_title="Nombre d'Activites"
            )
            fig_impact.update_traces(textposition='outside')
            st.plotly_chart(fig_impact, use_container_width=True)
            
            # Optional: Show technical score only in expander
            with st.expander("Voir details techniques (Score IA)"):
                st.metric("Score de Silhouette", f"{score:.2f}")
                st.caption("Un score > 0.5 indique une excellente separation des groupes.")
        else:
            st.info("Pas assez de donnees pour l'analyse IA (min 5 activites).")

        # --- DATA & EXPORT ---
        st.subheader("Données Détaillées")
        st.dataframe(filtered_df, use_container_width=True)
        
        col_dl, col_drive = st.columns(2)
        with col_dl:
            excel_data = convert_df_to_excel(filtered_df)
            st.download_button(
                label="Télécharger Excel",
                data=excel_data,
                file_name='activites_virunga.xlsx',
                mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
            )
        with col_drive:
            if st.button("Sauvegarder sur Drive"):
                # Mock Drive Save
                time.sleep(1)
                st.success("Rapport sauvegardé dans 'Virunga/Rapports' sur Google Drive!")

    elif page == "Visites & Stages":
        st.title("Suivi des Visites et Stages")
        
        # Filters
        with st.expander("Filtres Visites", expanded=True):
            c1, c2, c3 = st.columns(3)
            months_v = sorted(df_visits['Mois'].dropna().unique()) if 'Mois' in df_visits.columns else []
            sel_month_v = c1.multiselect("Mois", months_v)
            
            orgs_v = sorted(df_visits['Organisation'].dropna().unique()) if 'Organisation' in df_visits.columns else []
            sel_org_v = c2.multiselect("Organisation", orgs_v)
            
            # Filter by Objet (Visite/Stage)
            objets_v = sorted(df_visits['Objet'].dropna().unique()) if 'Objet' in df_visits.columns else []
            sel_objet_v = c3.multiselect("Type (Visite/Stage)", objets_v)
            
        # Apply Filters
        filtered_visits = df_visits.copy()
            fig_temp_press = px.line(monthly_press, x='Date', y='Nombre', markers=True,
                                   title="Articles par mois",
                                   color_discrete_sequence=[COLORS['ORANGE']])
            fig_temp_press.update_layout(height=300, margin=dict(l=0, r=0, t=40, b=0))
            st.plotly_chart(fig_temp_press, use_container_width=True)
            
            # Evolution by Tone
            if 'Ton' in filtered_press.columns and not filtered_press['Ton'].isna().all():
                monthly_ton = filtered_press.groupby([filtered_press['Date'].dt.to_period('M'), 'Ton']).size().reset_index(name='Nombre')
                monthly_ton['Date'] = monthly_ton['Date'].dt.to_timestamp()
                fig_ton_temp = px.line(monthly_ton, x='Date', y='Nombre', color='Ton', markers=True,
                                      title="Evolution du Ton Mediatique",
                                      color_discrete_map={'Positif': COLORS['SUCCESS'], 'Negatif': COLORS['DANGER'], 'Neutre': COLORS['GRAY']})
                fig_ton_temp.update_layout(height=300, margin=dict(l=0, r=0, t=40, b=0))
                st.plotly_chart(fig_ton_temp, use_container_width=True)

        # --- ARTICLES LIST & EXPORT ---
        st.subheader("Derniers Articles")
        st.dataframe(filtered_press, use_container_width=True)
        
        excel_press = convert_df_to_excel(filtered_press)
        st.download_button(
            label="Télécharger Excel",
            data=excel_press,
            file_name='revue_presse_virunga.xlsx',
            mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
        )

    elif page == "Administration":
        st.title("Administration")
        st.info("Module de gestion des utilisateurs et des paramètres système.")

if __name__ == "__main__":
    main()

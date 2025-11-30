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
from auth_manager import SecureAuthManager
from drive_manager import DriveManager
from security import SecurityManager
from data_manager import load_data_core

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
    
    /* Mobile Optimization */
    @media (max-width: 768px) {{
        .metric-card {{
            margin-bottom: 10px;
            padding: 10px;
        }}
        .metric-value {{
            font-size: 20px;
        }}
        .metric-label {{
            font-size: 12px;
        }}
        h1 {{
            font-size: 24px !important;
        }}
        h2 {{
            font-size: 20px !important;
        }}
        h3 {{
            font-size: 18px !important;
        }}
    }}
    </style>
""", unsafe_allow_html=True)

# --- DATA LOADER ---
# --- DATA LOADER OPTIMIZED ---
@st.cache_data(ttl=14400) # Increased to 4 hours
def load_data_optimized():
    """
    Loads data efficiently with caching using the core data manager.
    """
    with st.spinner("⚡ Chargement des données en cours..."):
        return load_data_core()

# --- AUTHENTICATION MANAGER ---
# Replaced by auth_manager.py


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
            "Profil",
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
        margin=dict(l=10, r=10, t=30, b=10),
        xaxis_title="Nombre",
        yaxis=dict(categoryorder='total ascending'),
        plot_bgcolor='white',
        paper_bgcolor='white',
        font=dict(color='black')
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
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        plot_bgcolor='white',
        paper_bgcolor='white',
        font=dict(color='black')
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
    # Security Checks
    if not SecurityManager.check_session_timeout():
        st.rerun()
        
    auth = SecureAuthManager()
    
    if "authenticated" not in st.session_state:
        st.session_state.authenticated = False

    if not st.session_state.authenticated:
        auth.login_form()
        return

    page = render_sidebar()
    
    # Load Data
    # Automatic Sync Check
    drive_mgr = DriveManager()
    if drive_mgr.config.get('drive_folder_id'):
        last_sync = drive_mgr.config.get('last_sync')
        if not last_sync or (datetime.now() - datetime.fromisoformat(last_sync)) > timedelta(minutes=60):
            with st.spinner("Synchronisation automatique avec Google Drive..."):
                drive_mgr.sync_data()

    # Load Data Optimized
    df_activities, df_visits, df_press = load_data_optimized()
    intelligence = VirungaIntelligence()

    if page == "Vue d'ensemble":
        st.title("Tableau de Bord Exécutif")
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

        st.markdown("""
        <div style='text-align: center; font-size: 1.3em; margin-top: 20px; padding: 20px; background-color: white; border-radius: 10px; border-left: 5px solid #00A87D; box-shadow: 0 4px 6px rgba(0,0,0,0.1);'>
            Au Parc National des Virunga, nous accordons une importance particulière aux relations avec les communautés riveraines et l’ensemble de nos parties prenantes.<br>
            En parcourant cette interface, vous le découvrirez très rapidement.<br><br>
            <strong>C’est parti ! 😊</strong>
        </div>
        """, unsafe_allow_html=True)

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
        total_act = len(filtered_df)
        total_part = int(filtered_df['Hommes'].sum() + filtered_df['Femmes'].sum()) if 'Hommes' in filtered_df.columns else 0
        
        # Count unique locations (sectors + precise locations)
        unique_sectors = filtered_df['Secteur'].nunique() if 'Secteur' in filtered_df.columns else 0
        unique_lieux = filtered_df['Lieu_Precis'].nunique() if 'Lieu_Precis' in filtered_df.columns else 0
        lieux_couverts = max(unique_sectors, unique_lieux)
        
        kpis = {
            "Total Activites": total_act,
            "Participants (Est.)": total_part,
            "Lieux Couverts": lieux_couverts
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
                fig_sect.update_layout(
                    height=350, 
                    margin=dict(l=10, r=10, t=20, b=10), 
                    showlegend=False,
                    plot_bgcolor='white',
                    paper_bgcolor='white',
                    font=dict(color='black')
                )
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
                fig_org.update_layout(
                    height=300, 
                    yaxis={'categoryorder':'total ascending'}, 
                    margin=dict(l=10, r=10, t=20, b=10),
                    plot_bgcolor='white',
                    paper_bgcolor='white',
                    font=dict(color='black')
                )
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
            fig_temp.update_layout(
                height=300, 
                margin=dict(l=10, r=10, t=40, b=10),
                plot_bgcolor='white',
                paper_bgcolor='white',
                font=dict(color='black')
            )
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
                fig_sect_detail.update_layout(
                    height=300, 
                    margin=dict(l=10, r=10, t=20, b=10),
                    plot_bgcolor='white',
                    paper_bgcolor='white',
                    font=dict(color='black')
                )
                st.plotly_chart(fig_sect_detail, use_container_width=True)
        
        with c6:
            st.subheader("Lieux Precis (Top 10)")
            if 'Lieu_Precis' in filtered_df.columns and not filtered_df['Lieu_Precis'].isna().all():
                lieu_counts = filtered_df['Lieu_Precis'].value_counts().head(10).reset_index()
                lieu_counts.columns = ['Lieu', 'Nombre']
                fig_lieu = px.bar(lieu_counts, x='Nombre', y='Lieu', orientation='h',
                                color_discrete_sequence=[COLORS['FOREST_GREEN']])
                fig_lieu.update_layout(
                    height=300, 
                    yaxis={'categoryorder':'total ascending'}, 
                    margin=dict(l=10, r=10, t=20, b=10),
                    plot_bgcolor='white',
                    paper_bgcolor='white',
                    font=dict(color='black')
                )
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
                yaxis_title="Nombre d'Activites",
                plot_bgcolor='white',
                paper_bgcolor='white',
                font=dict(color='black'),
                margin=dict(l=10, r=10, t=30, b=10)
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
        if sel_month_v: filtered_visits = filtered_visits[filtered_visits['Mois'].isin(sel_month_v)]
        if sel_org_v: filtered_visits = filtered_visits[filtered_visits['Organisation'].isin(sel_org_v)]
        if sel_objet_v: filtered_visits = filtered_visits[filtered_visits['Objet'].isin(sel_objet_v)]
        
        # KPIs
        total_v = filtered_visits['Nombre'].sum() if 'Nombre' in filtered_visits.columns else 0
        unique_orgs = filtered_visits['Organisation'].nunique() if 'Organisation' in filtered_visits.columns else 0
        
        kpis_v = {"Total Visiteurs": total_v, "Organisations": unique_orgs}
        render_kpi_row(kpis_v)
        
        # Charts Row 1
        c1, c2 = st.columns(2)
        with c1:
            st.subheader("Top Organisations")
            if 'Organisation' in filtered_visits.columns and not filtered_visits['Organisation'].isna().all():
                top_orgs_v = filtered_visits.groupby('Organisation')['Nombre'].sum().reset_index().sort_values('Nombre', ascending=False).head(10)
                fig_v = px.bar(top_orgs_v, x='Nombre', y='Organisation', orientation='h', color_discrete_sequence=[COLORS['LAKE_BLUE']])
                fig_v.update_layout(
                    height=300, 
                    yaxis={'categoryorder':'total ascending'}, 
                    margin=dict(l=10, r=10, t=20, b=10),
                    plot_bgcolor='white',
                    paper_bgcolor='white',
                    font=dict(color='black')
                )
                st.plotly_chart(fig_v, use_container_width=True)
        
        with c2:
            st.subheader("Répartition Visite/Stage")
            if 'Objet' in filtered_visits.columns and not filtered_visits['Objet'].isna().all():
                objet_counts = filtered_visits.groupby('Objet')['Nombre'].sum().reset_index()
                fig_objet = px.pie(objet_counts, values='Nombre', names='Objet', hole=0.4,
                                  color_discrete_sequence=[COLORS['ORANGE'], COLORS['FOREST_GREEN']])
                fig_objet.update_layout(
                    height=300, 
                    margin=dict(l=10, r=10, t=20, b=10),
                    plot_bgcolor='white',
                    paper_bgcolor='white',
                    font=dict(color='black')
                )
                st.plotly_chart(fig_objet, use_container_width=True)
        
        # Temporal Evolution
        st.subheader("Evolution Temporelle")
        if 'Date' in filtered_visits.columns and not filtered_visits['Date'].isna().all():
            # Overall evolution
            monthly_v = filtered_visits.groupby(filtered_visits['Date'].dt.to_period('M'))['Nombre'].sum().reset_index()
            monthly_v['Date'] = monthly_v['Date'].dt.to_timestamp()
            fig_dv = px.line(monthly_v, x='Date', y='Nombre', markers=True,
                           title="Total Visiteurs par mois",
                           color_discrete_sequence=[COLORS['ORANGE']])
            fig_dv.update_layout(
                height=300, 
                margin=dict(l=10, r=10, t=40, b=10),
                plot_bgcolor='white',
                paper_bgcolor='white',
                font=dict(color='black')
            )
            st.plotly_chart(fig_dv, use_container_width=True)
            
            # Evolution by Objet (Visite vs Stage)
            if 'Objet' in filtered_visits.columns:
                monthly_objet = filtered_visits.groupby([filtered_visits['Date'].dt.to_period('M'), 'Objet'])['Nombre'].sum().reset_index()
                monthly_objet['Date'] = monthly_objet['Date'].dt.to_timestamp()
                fig_objet_temp = px.line(monthly_objet, x='Date', y='Nombre', color='Objet', markers=True,
                                        title="Evolution par Type (Visite vs Stage)",
                                        color_discrete_map={'Visite': COLORS['LAKE_BLUE'], 'Stage': COLORS['FOREST_GREEN']})
                fig_objet_temp.update_layout(
                    height=300, 
                    margin=dict(l=10, r=10, t=40, b=10),
                    plot_bgcolor='white',
                    paper_bgcolor='white',
                    font=dict(color='black')
                )
                st.plotly_chart(fig_objet_temp, use_container_width=True)
        
        # Data
        st.subheader("Données Détaillées")
        st.dataframe(filtered_visits, use_container_width=True)
        
        excel_visits = convert_df_to_excel(filtered_visits)
        st.download_button(
            label="Télécharger Excel",
            data=excel_visits,
            file_name='visites_stages_virunga.xlsx',
            mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
        )

    elif page == "Revue de Presse":
        st.title("Intelligence Media")
        
        # Filters
        with st.expander("Filtres Presse", expanded=True):
            c1, c2, c3, c4 = st.columns(4)
            
            tones = sorted(df_press['Ton'].dropna().unique()) if 'Ton' in df_press.columns else []
            sel_tone = c1.multiselect("Ton", tones)
            
            medias = sorted(df_press['Media'].dropna().unique()) if 'Media' in df_press.columns else []
            sel_media = c2.multiselect("Media", medias)
            
            months_p = sorted(df_press['Mois'].dropna().unique()) if 'Mois' in df_press.columns else []
            sel_month_p = c3.multiselect("Mois", months_p)
            
            zones_p = sorted(df_press['Zone'].dropna().unique()) if 'Zone' in df_press.columns else []
            sel_zone_p = c4.multiselect("Zone Concernée", zones_p)
        
        # Apply Filters
        filtered_press = df_press.copy()
        if sel_tone: filtered_press = filtered_press[filtered_press['Ton'].isin(sel_tone)]
        if sel_media: filtered_press = filtered_press[filtered_press['Media'].isin(sel_media)]
        if sel_month_p: filtered_press = filtered_press[filtered_press['Mois'].isin(sel_month_p)]
        if sel_zone_p: filtered_press = filtered_press[filtered_press['Zone'].isin(sel_zone_p)]
        
        # KPIs
        st.markdown("### Indicateurs Clés")
        total_articles = len(filtered_press)
        total_medias = filtered_press['Media'].nunique() if 'Media' in filtered_press.columns else 0
        
        pos_count = filtered_press[filtered_press['Ton'].str.contains('Positif', case=False, na=False)].shape[0] if 'Ton' in filtered_press.columns else 0
        neg_count = filtered_press[filtered_press['Ton'].str.contains('Negatif', case=False, na=False)].shape[0] if 'Ton' in filtered_press.columns else 0
        
        pos_pct = int((pos_count / total_articles) * 100) if total_articles > 0 else 0
        neg_pct = int((neg_count / total_articles) * 100) if total_articles > 0 else 0
        
        kpis_p = {
            "Total Articles": total_articles,
            "Medias Actifs": total_medias,
            "Taux Positif": f"{pos_pct}% ({pos_count})",
            "Taux Negatif": f"{neg_pct}% ({neg_count})"
        }
        render_kpi_row(kpis_p)

        # Charts
        st.markdown("### Analyse Détaillée")
        
        # Row 1: Media and Tone
        c1, c2 = st.columns(2)
        with c1:
            if 'Media' in filtered_press.columns and not filtered_press['Media'].isna().all():
                st.subheader("Articles par Media")
                media_counts = filtered_press['Media'].value_counts().head(10).reset_index()
                media_counts.columns = ['Media', 'Nombre']
                fig_media = px.bar(media_counts, x='Nombre', y='Media', orientation='h', color_discrete_sequence=[COLORS['LAKE_BLUE']])
                fig_media.update_layout(
                    height=300, 
                    yaxis={'categoryorder':'total ascending'}, 
                    margin=dict(l=10, r=10, t=20, b=10),
                    plot_bgcolor='white',
                    paper_bgcolor='white',
                    font=dict(color='black')
                )
                st.plotly_chart(fig_media, use_container_width=True)
                
        with c2:
            if 'Ton' in filtered_press.columns and not filtered_press['Ton'].isna().all():
                st.subheader("Répartition par Ton")
                ton_counts = filtered_press['Ton'].value_counts().reset_index()
                ton_counts.columns = ['Ton', 'Nombre']
                fig_ton = px.pie(ton_counts, values='Nombre', names='Ton', hole=0.4,
                               color_discrete_map={'Positif': COLORS['SUCCESS'], 'Negatif': COLORS['DANGER'], 'Neutre': COLORS['GRAY']})
                fig_ton.update_layout(
                    height=300, 
                    margin=dict(l=10, r=10, t=20, b=10),
                    plot_bgcolor='white',
                    paper_bgcolor='white',
                    font=dict(color='black')
                )
                st.plotly_chart(fig_ton, use_container_width=True)

        # Row 2: Zone and Theme
        c3, c4 = st.columns(2)
        with c3:
            if 'Zone' in filtered_press.columns and not filtered_press['Zone'].isna().all():
                st.subheader("Zones Concernées")
                zone_counts = filtered_press['Zone'].value_counts().reset_index()
                zone_counts.columns = ['Zone', 'Nombre']
                fig_zone = px.pie(zone_counts, values='Nombre', names='Zone', hole=0.4, color_discrete_sequence=px.colors.sequential.Plasma)
                fig_zone.update_layout(
                    height=300, 
                    margin=dict(l=10, r=10, t=20, b=10),
                    plot_bgcolor='white',
                    paper_bgcolor='white',
                    font=dict(color='black')
                )
                st.plotly_chart(fig_zone, use_container_width=True)
        
        with c4:
            if 'Thematique' in filtered_press.columns and not filtered_press['Thematique'].isna().all():
                st.subheader("Thématiques Traitées")
                them_counts = filtered_press['Thematique'].value_counts().head(10).reset_index()
                them_counts.columns = ['Thematique', 'Nombre']
                fig_them = px.bar(them_counts, x='Thematique', y='Nombre', color='Thematique', color_discrete_sequence=px.colors.qualitative.Pastel)
                fig_them.update_layout(
                    height=300, 
                    margin=dict(l=10, r=10, t=20, b=10), 
                    showlegend=False,
                    plot_bgcolor='white',
                    paper_bgcolor='white',
                    font=dict(color='black')
                )
                st.plotly_chart(fig_them, use_container_width=True)
        
        # Row 3: Ton per Media
        if 'Ton' in filtered_press.columns and 'Media' in filtered_press.columns:
            st.subheader("Ton par Media")
            ton_media = filtered_press.groupby(['Media', 'Ton']).size().reset_index(name='Nombre')
            # Limit to top 10 media
            top_media = filtered_press['Media'].value_counts().head(10).index
            ton_media = ton_media[ton_media['Media'].isin(top_media)]
            fig_ton_media = px.bar(ton_media, x='Nombre', y='Media', color='Ton', orientation='h',
                                 color_discrete_map={'Positif': COLORS['SUCCESS'], 'Negatif': COLORS['DANGER'], 'Neutre': COLORS['GRAY']})
            fig_ton_media.update_layout(
                height=300, 
                margin=dict(l=10, r=10, t=20, b=10),
                plot_bgcolor='white',
                paper_bgcolor='white',
                font=dict(color='black')
            )
            st.plotly_chart(fig_ton_media, use_container_width=True)
        
        # Temporal Evolution
        st.subheader("Evolution Temporelle")
        if 'Date' in filtered_press.columns and not filtered_press['Date'].isna().all():
            # Overall articles evolution
            monthly_press = filtered_press.groupby(filtered_press['Date'].dt.to_period('M')).size().reset_index(name='Nombre')
            monthly_press['Date'] = monthly_press['Date'].dt.to_timestamp()
            fig_temp_press = px.line(monthly_press, x='Date', y='Nombre', markers=True,
                                   title="Articles par mois",
                                   color_discrete_sequence=[COLORS['ORANGE']])
            fig_temp_press.update_layout(
                height=300, 
                margin=dict(l=10, r=10, t=40, b=10),
                plot_bgcolor='white',
                paper_bgcolor='white',
                font=dict(color='black')
            )
            st.plotly_chart(fig_temp_press, use_container_width=True)
            
            # Evolution by Tone
            if 'Ton' in filtered_press.columns and not filtered_press['Ton'].isna().all():
                monthly_ton = filtered_press.groupby([filtered_press['Date'].dt.to_period('M'), 'Ton']).size().reset_index(name='Nombre')
                monthly_ton['Date'] = monthly_ton['Date'].dt.to_timestamp()
                fig_ton_temp = px.line(monthly_ton, x='Date', y='Nombre', color='Ton', markers=True,
                                      title="Evolution du Ton Mediatique",
                                      color_discrete_map={'Positif': COLORS['SUCCESS'], 'Negatif': COLORS['DANGER'], 'Neutre': COLORS['GRAY']})
                fig_ton_temp.update_layout(
                    height=300, 
                    margin=dict(l=10, r=10, t=40, b=10),
                    plot_bgcolor='white',
                    paper_bgcolor='white',
                    font=dict(color='black')
                )
                st.plotly_chart(fig_ton_temp, use_container_width=True)

        # Data
        st.subheader("Derniers Articles")
        st.dataframe(filtered_press, use_container_width=True)
        
        excel_press = convert_df_to_excel(filtered_press)
        st.download_button(
            label="Télécharger Excel",
            data=excel_press,
            file_name='revue_presse_virunga.xlsx',
            mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
        )

    elif page == "Profil":
        st.title("Mon Profil")
        
        col1, col2 = st.columns([1, 2])
        
        with col1:
            st.markdown("### Informations")
            st.write(f"**Nom:** {st.session_state.user['name']}")
            st.write(f"**Email:** {st.session_state.email}")
            st.write(f"**Rôle:** {st.session_state.user['role'].upper()}")
            
        with col2:
            st.markdown("### Sécurité")
            with st.form("change_password_form"):
                st.subheader("Changer le mot de passe")
                current_pwd = st.text_input("Mot de passe actuel", type="password")
                new_pwd = st.text_input("Nouveau mot de passe", type="password", help="Min 8 caractères, majuscule, chiffre, spécial")
                confirm_pwd = st.text_input("Confirmer le nouveau mot de passe", type="password")
                
                if st.form_submit_button("Mettre à jour"):
                    if new_pwd != confirm_pwd:
                        st.error("Les nouveaux mots de passe ne correspondent pas.")
                    else:
                        success, msg = auth.change_password(st.session_state.email, current_pwd, new_pwd)
                        if success:
                            st.success(msg)
                        else:
                            st.error(msg)

    elif page == "Administration":
        st.title("Administration")
        
        # Check if user has admin rights
        if st.session_state.user['role'] not in ['owner', 'admin']:
            st.error("Accès refusé. Vous devez être administrateur pour accéder à cette page.")
            return
        
        st.markdown("### Gestion des Utilisateurs")
        
        # Initialize session state for users if not exists
        if 'all_users' not in st.session_state:
            st.session_state.all_users = {
                "bbwende@virunga.org": {"role": "owner", "name": "Bienvenu Bwende"},
                "admin@virunga.org": {"role": "admin", "name": "Admin System"},
                "guest@virunga.org": {"role": "viewer", "name": "Invité"}
            }
        
        # Display current users
        st.subheader("Utilisateurs Actuels")
        users_data = []
        for email, info in st.session_state.all_users.items():
            users_data.append({
                "Email": email,
                "Nom": info['name'],
                "Role": info['role']
            })
        
        df_users = pd.DataFrame(users_data)
        st.dataframe(df_users, use_container_width=True)
        
        # Add new user section
        st.markdown("---")
        st.subheader("Ajouter un Nouvel Utilisateur")
        
        col1, col2, col3 = st.columns(3)
        with col1:
            new_email = st.text_input("Email", key="new_user_email")
        with col2:
            new_name = st.text_input("Nom Complet", key="new_user_name")
        with col3:
            new_role = st.selectbox("Rôle", ["viewer", "admin", "owner"], key="new_user_role")
        
        if st.button("Ajouter Utilisateur"):
            if new_email and new_name:
                if new_email in st.session_state.all_users:
                    st.error("Cet email existe déjà!")
                else:
                    st.session_state.all_users[new_email] = {
                        "role": new_role,
                        "name": new_name
                    }
                    st.success(f"Utilisateur {new_name} ajouté avec succès!")
                    st.rerun()
            else:
                st.warning("Veuillez remplir tous les champs.")
        
        # Modify/Delete user section
        st.markdown("---")
        st.subheader("Modifier ou Supprimer un Utilisateur")
        
        selected_email = st.selectbox("Selectionner un utilisateur", list(st.session_state.all_users.keys()))
        
        if selected_email:
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("**Modifier le Rôle**")
                current_role = st.session_state.all_users[selected_email]['role']
                new_role_mod = st.selectbox("Nouveau Rôle", ["viewer", "admin", "owner"], 
                                           index=["viewer", "admin", "owner"].index(current_role),
                                           key="modify_role")
                
                if st.button("Mettre à Jour le Rôle"):
                    st.session_state.all_users[selected_email]['role'] = new_role_mod
                    st.success(f"Rôle mis à jour pour {selected_email}")
                    st.rerun()
            
            with col2:
                st.markdown("**Supprimer l'Utilisateur**")
                st.warning(f"Supprimer: {selected_email}")
                
                if st.button("Confirmer la Suppression", type="primary"):
                    if selected_email == st.session_state.email:
                        st.error("Vous ne pouvez pas supprimer votre propre compte!")
                    else:
                        del st.session_state.all_users[selected_email]
                        st.success(f"Utilisateur {selected_email} supprimé")
                        st.rerun()
        
        # Role descriptions
        st.markdown("---")
        st.subheader("Description des Rôles")
        
        roles_info = {
            "Owner": "Accès complet - Peut tout faire y compris gérer les administrateurs",
            "Admin": "Peut gérer les utilisateurs et accéder à toutes les données",
            "Viewer": "Peut uniquement consulter les données, pas de modification"
        }
        
        for role, description in roles_info.items():
            st.markdown(f"**{role}**: {description}")
        
        # Export users list
        st.markdown("---")
        if st.button("Exporter la Liste des Utilisateurs"):
            excel_users = convert_df_to_excel(df_users)
            st.download_button(
                label="Télécharger Excel",
                data=excel_users,
                file_name='utilisateurs_virunga.xlsx',
                mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
        )

        st.markdown("---")
        st.subheader("Configuration Google Drive")
        
        if st.session_state.user['role'] == 'owner':
            drive_mgr = DriveManager()
            col_d1, col_d2 = st.columns(2)
            
            with col_d1:
                st.write("Statut: " + ("✅ Connecté" if drive_mgr.creds else "❌ Non connecté"))
                if st.button("Connecter Google Drive"):
                    drive_mgr.authenticate()
                    st.rerun()
                
                if drive_mgr.creds:
                    folders = drive_mgr.list_folders()
                    folder_options = {f['name']: f['id'] for f in folders}
                    
                    current_folder_id = drive_mgr.config.get('drive_folder_id')
                    current_index = 0
                    if current_folder_id:
                        for name, fid in folder_options.items():
                            if fid == current_folder_id:
                                current_index = list(folder_options.keys()).index(name)
                                break
                    
                    selected_folder_name = st.selectbox(
                        "Sélectionner le dossier de données", 
                        list(folder_options.keys()),
                        index=current_index if folder_options else 0
                    )
                    
                    if st.button("Sauvegarder Configuration"):
                        if selected_folder_name:
                            drive_mgr.set_data_folder(folder_options[selected_folder_name])
                            st.success(f"Dossier '{selected_folder_name}' configuré!")
            
            with col_d2:
                st.write(f"Dernière synchro: {drive_mgr.config.get('last_sync', 'Jamais')}")
                if st.button("Synchroniser Maintenant"):
                    with st.spinner("Téléchargement des fichiers..."):
                        success, msg = drive_mgr.sync_data()
                        if success:
                            st.success(msg)
                            time.sleep(1)
                            st.rerun()
                        else:
                            st.error(msg)
        else:
            st.info("La configuration Google Drive est réservée au propriétaire.")

if __name__ == "__main__":
    main()

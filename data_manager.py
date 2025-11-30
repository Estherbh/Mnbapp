import pandas as pd
import streamlit as st

# File Paths
FILE_ACTIVITIES = "COLLECTE DES DONNÉES TERRAIN_RELATIONS EXTERIEURES (2).xlsx"
FILE_PRESS = "Revue de la presse2.xlsx"

def load_data_core():
    """
    Core data loading logic, decoupled from Streamlit caching for API usage.
    Returns tuple of (df_activities, df_visits, df_press)
    """
    df_activities = pd.DataFrame()
    df_visits = pd.DataFrame()
    df_press = pd.DataFrame()
    
    # Load Activities
    try:
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

    except Exception as e:
        print(f"Erreur chargement Activités: {e}")
        df_activities = pd.DataFrame(columns=["Date_Activite", "Organisateur", "Secteur", "Lieu_Precis", "Type", "Hommes", "Femmes", "Enfants", "Total_Participants"])

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
        print(f"Note: Feuille 'Visitestage' non trouvee ({e})")

    # Load Press Review
    try:
        df_press = pd.read_excel(FILE_PRESS)
        
        # Map columns by keywords
        for col in df_press.columns:
            col_lower = str(col).lower()
            if 'date' in col_lower or 'dtae' in col_lower:
                df_press.rename(columns={col: 'Date'}, inplace=True)
            elif 'media' in col_lower or 'source' in col_lower or 'média' in col_lower:
                df_press.rename(columns={col: 'Media'}, inplace=True)
            elif 'titre' in col_lower or 'title' in col_lower or 'sujet' in col_lower:
                df_press.rename(columns={col: 'Titre'}, inplace=True)
            elif 'ton' in col_lower or 'sentiment' in col_lower:
                df_press.rename(columns={col: 'Ton'}, inplace=True)
            elif 'thematique' in col_lower or 'theme' in col_lower or 'thématique' in col_lower:
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
        print(f"Erreur chargement Presse: {e}")
        df_press = pd.DataFrame(columns=["Date", "Media", "Titre", "Ton", "Thematique", "Zone"])

    return df_activities, df_visits, df_press

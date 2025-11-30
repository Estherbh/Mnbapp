# Documentation API - Virunga Dashboard

## Vue d'ensemble

Le **Virunga Dashboard** est une application web de monitoring et d'analyse des données pour le Parc National des Virunga. L'application est construite avec Streamlit et offre des fonctionnalités d'analyse avancée, de visualisation de données et de gestion sécurisée des utilisateurs.

## Architecture de l'Application

### Structure des Fichiers

```
developpement/
├── virunga_app.py              # Application principale Streamlit
├── auth_manager.py             # Gestion de l'authentification
├── security.py                 # Gestionnaire de sécurité
├── drive_manager.py            # Intégration Google Drive
├── google_drive_integration.py # Module Google Drive
├── users.json                  # Base de données utilisateurs
├── config.json                 # Configuration Google Drive
├── requirements.txt            # Dépendances Python
├── Dockerfile                  # Configuration Docker
├── app.yaml                    # Configuration Google Cloud
└── run_app.bat                 # Script de lancement Windows
```

### Modules Principaux

#### 1. **virunga_app.py** - Application Principale
- **Responsabilité** : Point d'entrée de l'application, gestion des pages et visualisations
- **Classes** :
  - `VirungaIntelligence` : Moteur d'analyse ML et génération de KPIs
- **Fonctions principales** :
  - `load_data_optimized()` : Chargement optimisé des données Excel
  - `render_sidebar()` : Navigation latérale
  - `render_kpi_row()` : Affichage des indicateurs clés
  - `main()` : Logique principale de l'application

#### 2. **auth_manager.py** - Authentification
- **Responsabilité** : Gestion sécurisée de l'authentification et des mots de passe
- **Classe** : `SecureAuthManager`
- **Méthodes** :
  - `load_users()` : Charge les utilisateurs depuis users.json
  - `save_users()` : Sauvegarde les utilisateurs
  - `verify_password()` : Vérifie un mot de passe avec bcrypt
  - `hash_password()` : Hash un mot de passe avec bcrypt
  - `validate_password_strength()` : Valide la force d'un mot de passe
  - `check_login()` : Vérifie les identifiants de connexion
  - `change_password()` : Change le mot de passe d'un utilisateur
  - `login_form()` : Affiche le formulaire de connexion

#### 3. **security.py** - Sécurité
- **Responsabilité** : Gestion de la sécurité des sessions
- **Classe** : `SecurityManager`
- **Méthodes** :
  - `check_session_timeout()` : Vérifie le timeout de session

#### 4. **drive_manager.py** - Google Drive
- **Responsabilité** : Synchronisation avec Google Drive
- **Classe** : `DriveManager`
- **Méthodes** :
  - `sync_data()` : Synchronise les données avec Google Drive

## Pages de l'Application

### 1. **Page de Connexion**
- **Route** : `/` (non authentifié)
- **Titre** : "Relations Extérieures / PNVi"
- **Fonctionnalités** :
  - Authentification par email/mot de passe
  - Limitation des tentatives de connexion (5 max)
  - Verrouillage temporaire après échecs (15 minutes)

### 2. **Vue d'ensemble**
- **Route** : Navigation → "Vue d'ensemble"
- **Fonctionnalités** :
  - KPIs globaux (Activités, Visiteurs, Articles, Score Perception)
  - Message de bienvenue
  - Tendance des activités

### 3. **Activités Terrain**
- **Route** : Navigation → "Activités Terrain"
- **Fonctionnalités** :
  - Filtres avancés (Mois, Organisateur, Secteur, Type)
  - Indicateurs clés
  - Visualisations démographiques
  - Classification automatique par IA (K-Means clustering)
  - Export Excel et sauvegarde Google Drive

### 4. **Visites & Stages**
- **Route** : Navigation → "Visites & Stages"
- **Fonctionnalités** :
  - Filtres (Mois, Organisation, Type)
  - Top organisations
  - Répartition Visite/Stage
  - Évolution temporelle
  - Export Excel

### 5. **Revue de Presse**
- **Route** : Navigation → "Revue de Presse"
- **Fonctionnalités** :
  - Filtres (Ton, Media, Mois, Zone)
  - Analyse de sentiment
  - Répartition par média et thématique
  - Évolution du ton médiatique
  - Export Excel

### 6. **Profil**
- **Route** : Navigation → "Profil"
- **Fonctionnalités** :
  - Affichage des informations utilisateur
  - Changement de mot de passe sécurisé
  - Validation de la force du mot de passe

### 7. **Administration**
- **Route** : Navigation → "Administration"
- **Accès** : Réservé aux rôles `owner` et `admin`
- **Fonctionnalités** :
  - Gestion des utilisateurs
  - Configuration système

## Authentification et Sécurité

### Système d'Authentification

L'application utilise un système d'authentification basé sur :
- **Fichier** : `users.json`
- **Hashing** : bcrypt pour les mots de passe
- **Session** : Streamlit session_state

### Structure users.json

```json
{
  "users": [
    {
      "email": "user@virunga.org",
      "password_hash": "$2b$12$...",
      "name": "Nom Utilisateur",
      "role": "viewer",
      "must_change_password": false
    }
  ]
}
```

### Rôles Utilisateurs

- **owner** : Accès complet, administration
- **admin** : Accès complet, administration
- **editor** : Lecture et modification des données
- **viewer** : Lecture seule

### Politique de Mot de Passe

Un mot de passe valide doit contenir :
- ✅ Au moins 8 caractères
- ✅ Au moins une majuscule
- ✅ Au moins un chiffre
- ✅ Au moins un caractère spécial (!@#$%^&*(),.?":{}|<>)

### Sécurité des Sessions

- **Timeout** : 30 minutes d'inactivité
- **Tentatives de connexion** : Maximum 5 tentatives
- **Verrouillage** : 15 minutes après 5 échecs

## Sources de Données

### Fichiers Excel

1. **COLLECTE DES DONNÉES TERRAIN_RELATIONS EXTERIEURES (2).xlsx**
   - Feuille `Donnees_Activites` : Activités terrain
   - Feuille `Visitestage` : Visites et stages

2. **Revue de la presse2.xlsx**
   - Données de presse et médias

### Colonnes Importantes

#### Activités Terrain
- `Date_Activite` : Date de l'activité
- `Nom` : Nom de l'activité
- `Organisateur` : Organisation responsable
- `Type` : Type d'activité
- `Secteur` : Zone géographique
- `Lieu_Precis` : Localisation précise
- `Hommes`, `Femmes`, `Enfants` : Démographie

#### Visites & Stages
- `Date` : Date de la visite/stage
- `Nombre` : Nombre de visiteurs
- `Objet` : Type (Visite/Stage)
- `Organisation` : Organisation visitante

#### Revue de Presse
- `Date` : Date de publication
- `Media` : Source média
- `Titre` : Titre de l'article
- `Ton` : Sentiment (Positif/Négatif/Neutre)
- `Thematique` : Thème de l'article
- `Zone_Concernee` : Zone géographique

## Déploiement

### Prérequis

- Python 3.8+
- Environnement virtuel (conda ou venv)
- Fichiers de données Excel
- Logo : `VNP LOGO FRENCH.jpg`

### Installation Locale

#### Windows

1. **Cloner le projet**
   ```bash
   cd "C:\TECH\ML virunga tracker\developpement"
   ```

2. **Créer l'environnement virtuel**
   ```bash
   python -m venv .venv
   .venv\Scripts\activate
   ```

3. **Installer les dépendances**
   ```bash
   pip install -r requirements.txt
   ```

4. **Lancer l'application**
   ```bash
   streamlit run virunga_app.py
   ```
   
   Ou utiliser le script :
   ```bash
   run_app.bat
   ```

5. **Accéder à l'application**
   - URL locale : `http://localhost:8501`

#### Linux/Mac

```bash
cd /path/to/developpement
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
streamlit run virunga_app.py
```

### Déploiement sur Google Cloud Platform (GCP)

#### Configuration

1. **Installer Google Cloud SDK**
   ```bash
   gcloud init
   ```

2. **Configurer le projet**
   ```bash
   gcloud config set project YOUR_PROJECT_ID
   ```

3. **Déployer l'application**
   ```bash
   gcloud app deploy app.yaml
   ```

#### Fichier app.yaml

```yaml
runtime: python39
entrypoint: streamlit run virunga_app.py --server.port=$PORT --server.address=0.0.0.0

instance_class: F2

automatic_scaling:
  max_instances: 3
  min_instances: 1
```

### Déploiement avec Docker

#### Construire l'image

```bash
docker build -t virunga-dashboard .
```

#### Lancer le conteneur

```bash
docker run -p 8501:8501 virunga-dashboard
```

#### Dockerfile

```dockerfile
FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

EXPOSE 8501

CMD ["streamlit", "run", "virunga_app.py", "--server.port=8501", "--server.address=0.0.0.0"]
```

### Déploiement sur Heroku

1. **Créer l'application**
   ```bash
   heroku create virunga-dashboard
   ```

2. **Ajouter les fichiers nécessaires**
   - `Procfile` :
     ```
     web: sh setup.sh && streamlit run virunga_app.py
     ```
   
   - `setup.sh` :
     ```bash
     mkdir -p ~/.streamlit/
     echo "\
     [server]\n\
     headless = true\n\
     port = $PORT\n\
     enableCORS = false\n\
     \n\
     " > ~/.streamlit/config.toml
     ```

3. **Déployer**
   ```bash
   git push heroku main
   ```

### Déploiement sur Streamlit Cloud

1. **Créer un compte** sur [streamlit.io/cloud](https://streamlit.io/cloud)

2. **Connecter le repository GitHub**

3. **Configurer le déploiement**
   - Main file path : `virunga_app.py`
   - Python version : 3.9

4. **Ajouter les secrets** (Settings → Secrets)
   ```toml
   # Si nécessaire pour Google Drive
   [google]
   credentials = "..."
   ```

## Variables d'Environnement

### Optionnelles

- `STREAMLIT_SERVER_PORT` : Port du serveur (défaut : 8501)
- `STREAMLIT_SERVER_ADDRESS` : Adresse du serveur (défaut : localhost)
- `GOOGLE_APPLICATION_CREDENTIALS` : Chemin vers les credentials Google Drive

## API Endpoints (Streamlit)

Streamlit ne fournit pas d'API REST traditionnelle, mais l'application expose les fonctionnalités suivantes :

### Authentification
- **Méthode** : `SecureAuthManager.check_login(email, password)`
- **Retour** : `bool` - True si authentifié

### Chargement de Données
- **Méthode** : `load_data_optimized()`
- **Retour** : `Tuple[DataFrame, DataFrame, DataFrame]` - (activités, visites, presse)
- **Cache** : 4 heures (TTL)

### Analyse IA
- **Méthode** : `VirungaIntelligence.cluster_activities(df)`
- **Retour** : `Tuple[DataFrame, float]` - (données clustérisées, score silhouette)

### Changement de Mot de Passe
- **Méthode** : `SecureAuthManager.change_password(email, old_pwd, new_pwd)`
- **Retour** : `Tuple[bool, str]` - (succès, message)

## Maintenance et Monitoring

### Logs

Les logs Streamlit sont disponibles dans :
- **Local** : Terminal de lancement
- **GCP** : Google Cloud Logging
- **Heroku** : `heroku logs --tail`

### Mise à Jour des Données

Les fichiers Excel doivent être mis à jour manuellement ou via Google Drive :
1. Remplacer les fichiers Excel dans le répertoire
2. L'application rechargera automatiquement les données (cache : 4h)

### Backup

Recommandations :
- Sauvegarder `users.json` régulièrement
- Sauvegarder les fichiers Excel
- Utiliser Google Drive pour la synchronisation automatique

## Support et Contact

Pour toute question ou problème :
- **Email** : bbwende@virunga.org
- **Documentation** : Ce fichier
- **Code source** : `C:\TECH\ML virunga tracker\developpement`

## Changelog

### Version Actuelle
- ✅ Titre de connexion : "Relations Extérieures / PNVi"
- ✅ Changement de mot de passe dans la page "Profil"
- ✅ Authentification sécurisée avec bcrypt
- ✅ Analyse IA avec K-Means clustering
- ✅ Export Excel et Google Drive
- ✅ Visualisations interactives avec Plotly
- ✅ Gestion des rôles utilisateurs
- ✅ Timeout de session (30 min)

# Virunga Dashboard - Relations Extérieures / PNVi

Application de monitoring et d'analyse pour le Parc National des Virunga, intégrant l'analyse de données terrain, le suivi des visiteurs et l'intelligence média.

## 🌟 Fonctionnalités

### Tableau de Bord
- **Vue d'ensemble** : KPIs globaux et tendances
- **Activités Terrain** : Analyse des activités avec clustering IA (K-Means)
- **Visites & Stages** : Suivi des visiteurs et stagiaires
- **Revue de Presse** : Analyse de sentiment et monitoring médiatique

### Sécurité & Authentification
- ✅ Authentification sécurisée avec bcrypt
- ✅ Gestion des rôles (owner, admin, editor, viewer)
- ✅ Changement de mot de passe dans la page "Profil"
- ✅ Validation de la force des mots de passe
- ✅ Timeout de session (30 minutes)
- ✅ Protection contre les attaques par force brute

### Intégration Google Drive (Optionnelle)
- Synchronisation automatique des fichiers Excel
- Configuration via interface utilisateur
- Voir [DEPLOYMENT.md](DEPLOYMENT.md) pour la configuration

## 🚀 Installation Locale

### Prérequis
- Python 3.8+
- Fichiers de données Excel

### Windows

```bash
# Cloner le repository
git clone https://github.com/Estherbh/Mnbapp.git
cd Mnbapp

# Créer l'environnement virtuel
python -m venv .venv
.venv\Scripts\activate

# Installer les dépendances
pip install -r requirements.txt

# Lancer l'application
streamlit run virunga_app.py
```

Ou utiliser le script :
```bash
run_app.bat
```

### Linux/Mac

```bash
git clone https://github.com/Estherbh/Mnbapp.git
cd Mnbapp
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
streamlit run virunga_app.py
```

## 📝 Configuration Initiale

### 1. Créer le fichier users.json

```json
{
  "users": [
    {
      "email": "votre.email@virunga.org",
      "password_hash": "$2b$12$...",
      "name": "Votre Nom",
      "role": "owner",
      "must_change_password": false
    }
  ]
}
```

Pour générer un hash de mot de passe :
```bash
python generate_hash.py
```

### 2. Ajouter les fichiers de données

Placez ces fichiers dans le répertoire principal :
- `COLLECTE DES DONNÉES TERRAIN_RELATIONS EXTERIEURES (2).xlsx`
- `Revue de la presse2.xlsx`
- `VNP LOGO FRENCH.jpg`

## 🌐 Déploiement

Voir [API_DOCUMENTATION.md](API_DOCUMENTATION.md) pour les instructions détaillées de déploiement sur :
- Streamlit Cloud (recommandé)
- Google Cloud Platform
- Heroku
- Docker

### Déploiement Rapide sur Streamlit Cloud

1. Pusher le code sur GitHub
2. Connecter le repository sur [streamlit.io/cloud](https://streamlit.io/cloud)
3. Configurer :
   - Main file : `virunga_app.py`
   - Python version : 3.9
4. Ajouter les fichiers de données et `users.json` manuellement

## 📚 Documentation

- [API_DOCUMENTATION.md](API_DOCUMENTATION.md) - Documentation complète de l'API
- [DEPLOYMENT.md](DEPLOYMENT.md) - Guide de déploiement et configuration Google Drive
- [SECURITY.md](SECURITY.md) - Politique de sécurité

## 🔐 Sécurité

- Les mots de passe sont hashés avec bcrypt
- Les fichiers sensibles (`users.json`, `client_secret.json`) sont exclus du Git
- Timeout de session automatique
- Validation stricte des mots de passe

## 📊 Technologies

- **Frontend** : Streamlit
- **Visualisation** : Plotly
- **ML** : scikit-learn (K-Means clustering)
- **Authentification** : bcrypt
- **Data** : pandas, openpyxl
- **Cloud** : Google Drive API (optionnel)

## 👥 Rôles Utilisateurs

- **owner** : Accès complet + administration
- **admin** : Accès complet + administration
- **editor** : Lecture et modification
- **viewer** : Lecture seule

## 🆘 Support

Pour toute question ou problème :
- Email : bbwende@virunga.org
- Documentation : Voir les fichiers .md dans le repository

## 📄 Licence

Propriété du Parc National des Virunga

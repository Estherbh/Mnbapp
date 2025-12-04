# 🚀 Déploiement Rapide - 5 Minutes

## Prérequis
- Compte Google Cloud
- Fichiers de données Excel

---

## 🎯 Étapes Rapides

### 1. Créer le Projet GCP
```
console.cloud.google.com → Nouveau Projet → "virunga-dashboard"
```

### 2. Ouvrir Cloud Shell
```
Cliquez sur l'icône >_ en haut à droite
```

### 3. Uploader le Code
```bash
git clone https://github.com/Estherbh/Mnbapp.git
cd Mnbapp
```

### 4. Créer users.json
```bash
nano users.json
```

Collez :
```json
{
  "users": [
    {
      "email": "votre.email@virunga.org",
      "password_hash": "$2b$12$HASH_ICI",
      "name": "Votre Nom",
      "role": "owner",
      "must_change_password": false
    }
  ]
}
```

Générer le hash :
```bash
python3 generate_hash.py
```

### 5. Uploader les Fichiers Excel
```
Cloud Shell → Menu ⋮ → Upload → Sélectionner les fichiers
```

### 6. Vérifier
```bash
python3 check_deployment.py
```

### 7. Déployer
```bash
gcloud app deploy
```

### 8. Accéder
```bash
gcloud app browse
```

---

## ✅ C'est Tout !

**URL de votre app** : `https://virunga-dashboard.ew.r.appspot.com`

**Guide complet** : Voir `GUIDE_DEPLOIEMENT_GCP.md`

**Support** : bbwende@virunga.org

# 🚀 Guide de Déploiement GCP - Virunga Dashboard

## ✅ Prérequis
- Compte Google Cloud (gratuit pour commencer)
- Fichiers de données Excel
- Fichier `users.json` avec vos utilisateurs

---

## 📋 ÉTAPE 1 : Préparer Google Cloud

### 1.1 Créer un Projet
1. Allez sur [console.cloud.google.com](https://console.cloud.google.com/)
2. Cliquez sur **"Sélectionner un projet"** → **"Nouveau projet"**
3. Nom : `virunga-dashboard`
4. Cliquez sur **"Créer"**

### 1.2 Activer la Facturation
1. Menu ☰ → **Facturation**
2. Associez une carte bancaire (300$ de crédit gratuit pour 90 jours)
3. **Note** : L'app coûtera ~5-15$/mois après les crédits gratuits

### 1.3 Activer App Engine
1. Menu ☰ → **App Engine**
2. Cliquez sur **"Créer une application"**
3. Région : **europe-west1** (Belgique)
4. Cliquez sur **"Suivant"**

---

## 💻 ÉTAPE 2 : Ouvrir Cloud Shell

1. En haut à droite, cliquez sur l'icône **Cloud Shell** `>_`
2. Un terminal s'ouvre en bas de l'écran
3. Attendez qu'il soit prêt (vous verrez votre nom d'utilisateur)

---

## 📦 ÉTAPE 3 : Uploader Votre Code

### Option A : Depuis GitHub (Recommandé)

```bash
# Cloner votre repository
git clone https://github.com/Estherbh/Mnbapp.git
cd Mnbapp

# Vérifier que vous êtes sur la bonne branche
git branch
```

### Option B : Upload Direct

1. Dans Cloud Shell, cliquez sur **⋮** (trois points) → **Upload**
2. Uploadez tout le dossier `developpement` en ZIP
3. Décompressez :
```bash
unzip developpement.zip
cd developpement
```

---

## 🔐 ÉTAPE 4 : Ajouter les Fichiers Sensibles

### 4.1 Créer users.json

```bash
nano users.json
```

Collez ce contenu (modifiez avec vos infos) :

```json
{
  "users": [
    {
      "email": "bbwende@virunga.org",
      "password_hash": "$2b$12$VOTRE_HASH_ICI",
      "name": "Bienvenu Bwende",
      "role": "owner",
      "must_change_password": false
    }
  ]
}
```

**Pour générer le hash du mot de passe :**
```bash
python3 generate_hash.py
```

Sauvegardez : `Ctrl+O` → `Entrée` → `Ctrl+X`

### 4.2 Uploader les Fichiers Excel

**Méthode 1 : Via l'interface Cloud Shell**
1. Cliquez sur **⋮** → **Upload**
2. Sélectionnez :
   - `COLLECTE DES DONNÉES TERRAIN_RELATIONS EXTERIEURES (2).xlsx`
   - `Revue de la presse2.xlsx`
   - `VNP LOGO FRENCH.jpg`

**Méthode 2 : Via Google Cloud Storage (si fichiers trop gros)**
```bash
# Créer un bucket temporaire
gsutil mb gs://virunga-temp-upload

# Uploader depuis votre PC vers le bucket (depuis votre terminal local)
gsutil cp "COLLECTE DES DONNÉES TERRAIN_RELATIONS EXTERIEURES (2).xlsx" gs://virunga-temp-upload/

# Dans Cloud Shell, télécharger du bucket
gsutil cp gs://virunga-temp-upload/*.xlsx .
gsutil cp gs://virunga-temp-upload/*.jpg .
```

### 4.3 Vérifier les Fichiers

```bash
ls -lh
```

Vous devez voir :
- ✅ virunga_app.py
- ✅ requirements.txt
- ✅ app.yaml
- ✅ users.json
- ✅ Les fichiers Excel
- ✅ VNP LOGO FRENCH.jpg

---

## 🚀 ÉTAPE 5 : Déployer !

### 5.1 Configurer le Projet

```bash
# Définir le projet actif
gcloud config set project virunga-dashboard

# Vérifier
gcloud config list
```

### 5.2 Lancer le Déploiement

```bash
gcloud app deploy
```

**Réponses aux questions :**
- `Do you want to continue (Y/n)?` → Tapez `Y`
- Attendez 5-10 minutes...

### 5.3 Activer les APIs (si demandé)

Si vous voyez des erreurs "API not enabled", exécutez :

```bash
gcloud services enable appengine.googleapis.com
gcloud services enable cloudbuild.googleapis.com
```

Puis relancez :
```bash
gcloud app deploy
```

---

## 🎉 ÉTAPE 6 : Accéder à Votre Application

### 6.1 Obtenir l'URL

```bash
gcloud app browse
```

Ou manuellement : `https://virunga-dashboard.ew.r.appspot.com`

### 6.2 Tester la Connexion

1. Ouvrez l'URL dans votre navigateur
2. Connectez-vous avec vos identifiants
3. ✅ **Succès !**

---

## 🔧 Commandes Utiles

### Voir les Logs en Temps Réel
```bash
gcloud app logs tail -s default
```

### Mettre à Jour l'Application
```bash
# Après avoir modifié le code
gcloud app deploy
```

### Voir les Versions Déployées
```bash
gcloud app versions list
```

### Supprimer une Ancienne Version
```bash
gcloud app versions delete VERSION_ID
```

### Arrêter l'Application (économiser)
```bash
# Mettre min_instances à 0 dans app.yaml, puis
gcloud app deploy
```

---

## 💰 Gestion des Coûts

### Coûts Estimés
- **Gratuit** : 300$ de crédit pendant 90 jours
- **Après** : ~5-15$/mois selon l'utilisation
- **Instance F2** : ~0.10$/heure quand active

### Optimiser les Coûts
1. Dans `app.yaml`, gardez `min_instances: 0`
2. L'app s'arrête automatiquement si pas d'utilisation
3. Surveillez : Menu ☰ → **Facturation** → **Rapports**

### Alertes Budget
```bash
# Créer une alerte à 10$
gcloud billing budgets create \
  --billing-account=VOTRE_BILLING_ACCOUNT_ID \
  --display-name="Virunga Budget" \
  --budget-amount=10USD
```

---

## 🔒 Sécurité Post-Déploiement

### 1. Configurer HTTPS (Automatique)
GCP active HTTPS automatiquement ✅

### 2. Restreindre l'Accès par IP (Optionnel)

Créez `dispatch.yaml` :
```yaml
dispatch:
  - url: "*/.*"
    service: default
```

### 3. Configurer un Domaine Personnalisé

```bash
# Ajouter votre domaine
gcloud app domain-mappings create dashboard.virunga.org
```

Puis ajoutez les enregistrements DNS fournis.

---

## 🐛 Dépannage

### Erreur : "API not enabled"
```bash
gcloud services enable appengine.googleapis.com
gcloud services enable cloudbuild.googleapis.com
```

### Erreur : "Insufficient permissions"
Vérifiez que vous êtes propriétaire du projet :
```bash
gcloud projects get-iam-policy virunga-dashboard
```

### Erreur : "Module not found"
Vérifiez `requirements.txt` :
```bash
cat requirements.txt
```

### L'App ne Démarre Pas
Consultez les logs :
```bash
gcloud app logs tail -s default
```

### Erreur de Mémoire
Augmentez `instance_class` dans `app.yaml` :
```yaml
instance_class: F4  # Au lieu de F2
```

---

## 📊 Monitoring

### Voir les Métriques
1. Menu ☰ → **App Engine** → **Dashboard**
2. Vous verrez :
   - Requêtes/seconde
   - Latence
   - Erreurs
   - Coûts

### Configurer des Alertes
1. Menu ☰ → **Monitoring** → **Alerting**
2. Créez des alertes pour :
   - Erreurs > 5%
   - Latence > 2s
   - Coûts > 10$

---

## 🔄 Mise à Jour de l'Application

### Workflow Complet

```bash
# 1. Modifier le code localement
# 2. Tester localement
streamlit run virunga_app.py

# 3. Commiter sur GitHub
git add .
git commit -m "Mise à jour fonctionnalité X"
git push

# 4. Dans Cloud Shell
cd Mnbapp
git pull

# 5. Redéployer
gcloud app deploy

# 6. Vérifier
gcloud app browse
```

---

## 📞 Support

### Problèmes Techniques
- Email : bbwende@virunga.org
- Documentation GCP : [cloud.google.com/appengine/docs](https://cloud.google.com/appengine/docs)

### Ressources Utiles
- [Streamlit sur GCP](https://docs.streamlit.io/knowledge-base/tutorials/deploy/gcp)
- [App Engine Pricing](https://cloud.google.com/appengine/pricing)
- [GCP Free Tier](https://cloud.google.com/free)

---

## ✅ Checklist Finale

Avant de déployer, vérifiez :

- [ ] Projet GCP créé
- [ ] Facturation activée
- [ ] App Engine initialisé
- [ ] Code uploadé dans Cloud Shell
- [ ] `users.json` créé avec hash valide
- [ ] Fichiers Excel uploadés
- [ ] Logo uploadé
- [ ] `requirements.txt` complet
- [ ] `app.yaml` configuré
- [ ] `.streamlit/config.toml` présent
- [ ] Commande `gcloud app deploy` exécutée
- [ ] URL testée et fonctionnelle

---

## 🎯 Prochaines Étapes

1. ✅ Déployer l'application
2. 🔐 Configurer les utilisateurs
3. 📊 Uploader les données
4. 🌐 Partager l'URL avec l'équipe
5. 📈 Monitorer l'utilisation
6. 💾 Configurer les backups automatiques

---

**Félicitations ! Votre dashboard Virunga est maintenant en ligne ! 🎉**

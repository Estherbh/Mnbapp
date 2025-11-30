# Guide de Déploiement - Virunga Dashboard

## Configuration Google Drive (Optionnelle)

Pour activer l'intégration Google Drive :

1. **Créer un projet Google Cloud** :
   - Aller sur https://console.cloud.google.com
   - Créer un nouveau projet
   - Activer l'API Google Drive

2. **Créer les credentials OAuth 2.0** :
   - Dans "APIs & Services" → "Credentials"
   - Créer "OAuth 2.0 Client ID"
   - Type : "Desktop app"
   - Télécharger le fichier JSON

3. **Configurer l'application** :
   - Renommer le fichier téléchargé en `client_secret.json`
   - Placer dans le répertoire de l'application
   - Au premier lancement, suivre le processus d'authentification

4. **Utilisation** :
   - Dans la sidebar, cliquer sur "Authentifier Google Drive"
   - Sélectionner le dossier contenant vos fichiers Excel
   - Utiliser "Synchroniser les données" pour mettre à jour

## Notes Importantes

- Le fichier `client_secret.json` est sensible et ne doit PAS être commité sur GitHub
- Le fichier `users.json` contient les mots de passe hashés et ne doit PAS être commité
- Créez vos propres fichiers de configuration après le déploiement

## Fichiers à Créer Manuellement

Après le déploiement, créez ces fichiers :

### users.json
```json
{
  "users": [
    {
      "email": "votre.email@virunga.org",
      "password_hash": "hash_bcrypt_ici",
      "name": "Votre Nom",
      "role": "owner",
      "must_change_password": false
    }
  ]
}
```

Pour générer un hash de mot de passe, utilisez `generate_hash.py`.

### config.json (si Google Drive activé)
```json
{
  "drive_folder_id": "",
  "last_sync": ""
}
```

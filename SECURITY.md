# Politique de Sécurité

## Gestion des Utilisateurs

- **Mots de passe**: Tous les mots de passe sont hashés avec bcrypt avant d'être stockés.
- **Complexité**: Les mots de passe doivent contenir au moins 8 caractères, une majuscule, un chiffre et un caractère spécial.
- **Sessions**: Les sessions expirent automatiquement après 30 minutes d'inactivité.
- **Tentatives de connexion**: Le compte est temporairement bloqué après 5 tentatives échouées.

## Protection des Données

- **Google Drive**: L'accès aux données se fait via OAuth2 en lecture seule.
- **Stockage Local**: Les fichiers Excel sont stockés localement sur le serveur pour des performances optimales.
- **Secrets**: Les clés API et secrets doivent être configurés via des variables d'environnement en production.

## Bonnes Pratiques pour le Déploiement

1.  Ne jamais commiter `users.json` ou `token.pickle` dans le dépôt Git.
2.  Utiliser HTTPS en production.
3.  Changer la `SECRET_KEY` dans le fichier `.env` ou les variables d'environnement.
4.  Mettre à jour régulièrement les dépendances (`pip install -U -r requirements.txt`).

## Signalement de Vulnérabilités

Si vous découvrez une faille de sécurité, veuillez contacter immédiatement l'équipe technique à `security@virunga.org`.

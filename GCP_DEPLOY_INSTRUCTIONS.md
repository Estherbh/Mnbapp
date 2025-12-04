# Guide de Déploiement sur Google Cloud Platform (GCP)

Comme le SDK `gcloud` n'est pas installé sur votre machine, la méthode la plus simple et la plus rapide est d'utiliser **Cloud Shell** (le terminal en ligne de Google).

## Étape 1 : Préparer le Projet Google Cloud

1.  Allez sur la [Console Google Cloud](https://console.cloud.google.com/).
2.  Connectez-vous avec votre compte Google.
3.  En haut à gauche, cliquez sur la liste des projets et faites **"Nouveau Projet"**.
4.  Nommez-le (ex: `virunga-dashboard`) et créez-le.
5.  Une fois créé, sélectionnez ce projet.

## Étape 2 : Ouvrir Cloud Shell

1.  En haut à droite de la console, cliquez sur l'icône **Cloud Shell** (un carré avec `>_`).
2.  Un terminal va s'ouvrir en bas de votre écran.

## Étape 3 : Récupérer votre Code

Dans le terminal Cloud Shell, tapez ces commandes :

```bash
# 1. Cloner votre repository GitHub
git clone https://github.com/Estherbh/Mnbapp.git

# 2. Entrer dans le dossier
cd Mnbapp

# 3. S'assurer d'être sur la branche principale
git checkout main
```

## Étape 4 : Ajouter les Fichiers Manquants

Comme nous avons sécurisé le projet, certains fichiers ne sont pas sur GitHub. Vous devez les créer dans Cloud Shell.

### A. Créer users.json

Tapez cette commande pour ouvrir l'éditeur nano :
```bash
nano users.json
```

Collez ceci (modifiez avec vos infos) :
```json
{
  "users": [
    {
      "email": "bbwende@virunga.org",
      "password_hash": "$2b$12$...", 
      "name": "Admin",
      "role": "owner",
      "must_change_password": false
    }
  ]
}
```
*(Pour sauvegarder : Ctrl+O, Entrée, puis Ctrl+X)*

### B. Uploader les fichiers Excel

1.  Dans Cloud Shell, cliquez sur les **trois points** (menu) au-dessus du terminal.
2.  Choisissez **"Upload"** (Téléverser).
3.  Sélectionnez vos fichiers sur votre ordinateur :
    *   `COLLECTE DES DONNÉES TERRAIN_RELATIONS EXTERIEURES (2).xlsx`
    *   `Revue de la presse2.xlsx`
    *   `VNP LOGO FRENCH.jpg`

*(Si les fichiers sont uploadés à la racine, déplacez-les dans le dossier Mnbapp avec `mv ../NomFichier.xlsx .`)*

## Étape 5 : Déployer !

Lancez simplement cette commande :

```bash
gcloud app deploy
```

1.  Il vous demandera de choisir une région (choisissez `europe-west1` pour la Belgique/Europe).
2.  Confirmez avec `Y`.
3.  Attendez quelques minutes...

🎉 **Succès !** Google vous donnera une URL (ex: `https://virunga-dashboard.ew.r.appspot.com`). C'est l'adresse de votre application en ligne !

---

## Besoin d'aide ?

Si vous avez une erreur "API not enabled", Cloud Shell vous proposera de l'activer. Dites simplement "Oui" (Y).

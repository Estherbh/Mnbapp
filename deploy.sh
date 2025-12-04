#!/bin/bash

# Script de déploiement automatisé pour Virunga Dashboard sur GCP
# Usage: bash deploy.sh

set -e  # Arrêter en cas d'erreur

echo "=========================================="
echo "🚀 DÉPLOIEMENT VIRUNGA DASHBOARD"
echo "=========================================="
echo ""

# Couleurs
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Fonction pour afficher les messages
log_info() {
    echo -e "${GREEN}✓${NC} $1"
}

log_error() {
    echo -e "${RED}✗${NC} $1"
}

log_warning() {
    echo -e "${YELLOW}⚠${NC} $1"
}

# 1. Vérifier que nous sommes dans le bon répertoire
if [ ! -f "virunga_app.py" ]; then
    log_error "Fichier virunga_app.py non trouvé. Êtes-vous dans le bon répertoire ?"
    exit 1
fi
log_info "Répertoire correct"

# 2. Vérifier les fichiers requis
echo ""
echo "📋 Vérification des fichiers..."

required_files=(
    "virunga_app.py"
    "requirements.txt"
    "app.yaml"
    "users.json"
    "COLLECTE DES DONNÉES TERRAIN_RELATIONS EXTERIEURES (2).xlsx"
    "Revue de la presse2.xlsx"
    "VNP LOGO FRENCH.jpg"
)

missing_files=()
for file in "${required_files[@]}"; do
    if [ -f "$file" ]; then
        log_info "$file"
    else
        log_error "$file MANQUANT"
        missing_files+=("$file")
    fi
done

if [ ${#missing_files[@]} -ne 0 ]; then
    echo ""
    log_error "Fichiers manquants détectés. Veuillez les ajouter avant de continuer."
    exit 1
fi

# 3. Vérifier la configuration GCP
echo ""
echo "🔧 Vérification de la configuration GCP..."

PROJECT_ID=$(gcloud config get-value project 2>/dev/null)
if [ -z "$PROJECT_ID" ]; then
    log_error "Aucun projet GCP configuré"
    echo ""
    echo "Configurez votre projet avec :"
    echo "  gcloud config set project VOTRE_PROJECT_ID"
    exit 1
fi
log_info "Projet GCP: $PROJECT_ID"

# 4. Vérifier que App Engine est initialisé
echo ""
echo "🌐 Vérification App Engine..."

if ! gcloud app describe &>/dev/null; then
    log_warning "App Engine n'est pas initialisé"
    echo ""
    read -p "Voulez-vous initialiser App Engine maintenant ? (y/n) " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        echo "Sélectionnez une région (recommandé: europe-west1)"
        gcloud app create
    else
        log_error "App Engine doit être initialisé pour continuer"
        exit 1
    fi
fi
log_info "App Engine initialisé"

# 5. Activer les APIs nécessaires
echo ""
echo "🔌 Activation des APIs..."

apis=(
    "appengine.googleapis.com"
    "cloudbuild.googleapis.com"
)

for api in "${apis[@]}"; do
    if gcloud services list --enabled --filter="name:$api" --format="value(name)" | grep -q "$api"; then
        log_info "$api déjà activée"
    else
        log_warning "Activation de $api..."
        gcloud services enable "$api"
        log_info "$api activée"
    fi
done

# 6. Exécuter le script de vérification Python
echo ""
echo "🔍 Vérification finale..."

if [ -f "check_deployment.py" ]; then
    python3 check_deployment.py
    if [ $? -ne 0 ]; then
        log_error "La vérification a échoué"
        exit 1
    fi
else
    log_warning "Script check_deployment.py non trouvé, vérification ignorée"
fi

# 7. Demander confirmation
echo ""
echo "=========================================="
echo "📦 PRÊT POUR LE DÉPLOIEMENT"
echo "=========================================="
echo ""
echo "Projet: $PROJECT_ID"
echo "Région: $(gcloud app describe --format='value(locationId)' 2>/dev/null || echo 'Non définie')"
echo ""
read -p "Voulez-vous continuer avec le déploiement ? (y/n) " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    log_warning "Déploiement annulé"
    exit 0
fi

# 8. Déployer
echo ""
echo "🚀 Déploiement en cours..."
echo ""

gcloud app deploy --quiet

if [ $? -eq 0 ]; then
    echo ""
    echo "=========================================="
    echo "✅ DÉPLOIEMENT RÉUSSI !"
    echo "=========================================="
    echo ""
    
    # Obtenir l'URL
    APP_URL=$(gcloud app browse --no-launch-browser 2>&1 | grep -o 'https://[^ ]*' || echo "")
    
    if [ -n "$APP_URL" ]; then
        echo "🌐 URL de l'application:"
        echo "   $APP_URL"
    else
        echo "🌐 Pour obtenir l'URL:"
        echo "   gcloud app browse"
    fi
    
    echo ""
    echo "📊 Pour voir les logs:"
    echo "   gcloud app logs tail -s default"
    echo ""
    echo "📈 Pour voir le dashboard:"
    echo "   https://console.cloud.google.com/appengine?project=$PROJECT_ID"
    echo ""
    echo "=========================================="
else
    echo ""
    log_error "Le déploiement a échoué"
    echo ""
    echo "Pour voir les logs d'erreur:"
    echo "  gcloud app logs tail -s default"
    exit 1
fi

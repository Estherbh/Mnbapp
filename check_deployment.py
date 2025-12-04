#!/usr/bin/env python3
"""
Script de vérification pré-déploiement pour Virunga Dashboard
Vérifie que tous les fichiers nécessaires sont présents
"""

import os
import sys
import json

# Couleurs pour le terminal
GREEN = '\033[92m'
RED = '\033[91m'
YELLOW = '\033[93m'
RESET = '\033[0m'

def check_file(filename, required=True):
    """Verifie si un fichier existe"""
    exists = os.path.exists(filename)
    status = f"{GREEN}[OK]{RESET}" if exists else f"{RED}[X]{RESET}"
    req_text = "(REQUIS)" if required else "(optionnel)"
    print(f"{status} {filename} {req_text}")
    return exists if required else True

def check_json_valid(filename):
    """Verifie si un fichier JSON est valide"""
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            json.load(f)
        print(f"  {GREEN}-> JSON valide{RESET}")
        return True
    except Exception as e:
        print(f"  {RED}-> Erreur JSON: {e}{RESET}")
        return False

def main():
    print("\n" + "="*60)
    print("VERIFICATION PRE-DEPLOIEMENT - VIRUNGA DASHBOARD")
    print("="*60 + "\n")
    
    all_ok = True
    
    # Fichiers Python requis
    print("[*] Fichiers Python:")
    all_ok &= check_file("virunga_app.py")
    all_ok &= check_file("auth_manager.py")
    all_ok &= check_file("data_manager.py")
    all_ok &= check_file("drive_manager.py")
    all_ok &= check_file("security.py")
    print()
    
    # Fichiers de configuration
    print("[*] Fichiers de Configuration:")
    all_ok &= check_file("requirements.txt")
    all_ok &= check_file("app.yaml")
    all_ok &= check_file(".streamlit/config.toml")
    all_ok &= check_file(".gcloudignore")
    print()
    
    # Fichiers sensibles
    print("[*] Fichiers Sensibles:")
    users_exists = check_file("users.json")
    all_ok &= users_exists
    if users_exists:
        all_ok &= check_json_valid("users.json")
    
    check_file("client_secret.json", required=False)
    print()
    
    # Fichiers de donnees
    print("[*] Fichiers de Donnees:")
    all_ok &= check_file("COLLECTE DES DONNÉES TERRAIN_RELATIONS EXTERIEURES (2).xlsx")
    all_ok &= check_file("Revue de la presse2.xlsx")
    all_ok &= check_file("VNP LOGO FRENCH.jpg")
    print()
    
    # Verifications supplementaires
    print("[*] Verifications Supplementaires:")
    
    # Vérifier requirements.txt
    if os.path.exists("requirements.txt"):
        with open("requirements.txt", 'r') as f:
            content = f.read()
            required_packages = ['streamlit', 'pandas', 'bcrypt', 'plotly', 'scikit-learn']
            missing = [pkg for pkg in required_packages if pkg not in content]
            if missing:
                print(f"{RED}[X]{RESET} Packages manquants dans requirements.txt: {', '.join(missing)}")
                all_ok = False
            else:
                print(f"{GREEN}[OK]{RESET} Tous les packages requis sont presents")
    
    # Vérifier app.yaml
    if os.path.exists("app.yaml"):
        with open("app.yaml", 'r') as f:
            content = f.read()
            if 'runtime: python' in content and 'entrypoint:' in content:
                print(f"{GREEN}[OK]{RESET} app.yaml correctement configure")
            else:
                print(f"{RED}[X]{RESET} app.yaml mal configure")
                all_ok = False
    
    print()
    print("="*60)
    
    if all_ok:
        print(f"{GREEN}[OK] TOUT EST PRET POUR LE DEPLOIEMENT !{RESET}")
        print("\nCommande a executer :")
        print(f"{YELLOW}gcloud app deploy{RESET}")
    else:
        print(f"{RED}[ERREUR] CERTAINS FICHIERS SONT MANQUANTS{RESET}")
        print("\nConsultez le guide : GUIDE_DEPLOIEMENT_GCP.md")
        sys.exit(1)
    
    print("="*60 + "\n")

if __name__ == "__main__":
    main()

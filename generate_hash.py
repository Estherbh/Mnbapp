#!/usr/bin/env python3
"""Générateur de hash de mot de passe pour Virunga Dashboard"""

import bcrypt
import getpass
import sys

def generate_hash(password):
    """Génère un hash bcrypt pour un mot de passe"""
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed.decode('utf-8')

def validate_password(password):
    """Valide la force du mot de passe"""
    if len(password) < 8:
        return False, "Le mot de passe doit contenir au moins 8 caractères"
    if not any(c.isupper() for c in password):
        return False, "Le mot de passe doit contenir au moins une majuscule"
    if not any(c.isdigit() for c in password):
        return False, "Le mot de passe doit contenir au moins un chiffre"
    if not any(c in "!@#$%^&*(),.?\":{}|<>" for c in password):
        return False, "Le mot de passe doit contenir au moins un caractère spécial"
    return True, "OK"

def main():
    print("\n" + "="*60)
    print("🔐 GÉNÉRATEUR DE HASH - VIRUNGA DASHBOARD")
    print("="*60 + "\n")
    
    print("Exigences du mot de passe :")
    print("  • Minimum 8 caractères")
    print("  • Au moins 1 majuscule")
    print("  • Au moins 1 chiffre")
    print("  • Au moins 1 caractère spécial (!@#$%^&*...)")
    print()
    
    # Demander le mot de passe
    password = getpass.getpass("Entrez le mot de passe : ")
    password_confirm = getpass.getpass("Confirmez le mot de passe : ")
    
    # Vérifier que les mots de passe correspondent
    if password != password_confirm:
        print("\n❌ Les mots de passe ne correspondent pas !")
        sys.exit(1)
    
    # Valider la force du mot de passe
    is_valid, message = validate_password(password)
    if not is_valid:
        print(f"\n❌ {message}")
        sys.exit(1)
    
    # Générer le hash
    print("\n⏳ Génération du hash...")
    password_hash = generate_hash(password)
    
    print("\n" + "="*60)
    print("✅ HASH GÉNÉRÉ AVEC SUCCÈS")
    print("="*60)
    print(f"\n{password_hash}\n")
    print("Copiez ce hash dans votre fichier users.json")
    print("="*60 + "\n")

if __name__ == "__main__":
    main()

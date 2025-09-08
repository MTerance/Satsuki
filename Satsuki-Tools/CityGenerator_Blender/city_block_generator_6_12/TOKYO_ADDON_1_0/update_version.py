#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
SCRIPT DE MISE À JOUR AUTOMATIQUE DE VERSION
Tokyo City Generator - Système de versioning

Usage: python update_version.py [nouveau_numero]
Example: python update_version.py 1.0.9
"""

import re
import sys
import os

def update_version_in_file(file_path, old_version, new_version):
    """Met à jour la version dans le fichier __init__.py"""
    
    if not os.path.exists(file_path):
        print(f"❌ Fichier non trouvé: {file_path}")
        return False
    
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Patterns à remplacer
    patterns = [
        # bl_info version tuple
        (rf'"version": \({old_version.replace(".", ", ")}\)',
         f'"version": ({new_version.replace(".", ", ")})'),
        
        # bl_info name
        (rf'"name": "Tokyo City Generator {old_version}"',
         f'"name": "Tokyo City Generator {new_version}"'),
        
        # bl_label
        (rf'bl_label = "Tokyo City Generator {old_version}"',
         f'bl_label = "Tokyo City Generator {new_version}"'),
        
        # Logs registered
        (rf'Tokyo City Generator {old_version} registered!',
         f'Tokyo City Generator {new_version} registered!'),
        
        # Logs unregistered
        (rf'Tokyo City Generator {old_version} unregistered!',
         f'Tokyo City Generator {new_version} unregistered!')
    ]
    
    updated_content = content
    changes_made = 0
    
    for pattern, replacement in patterns:
        new_content = re.sub(pattern, replacement, updated_content)
        if new_content != updated_content:
            changes_made += 1
            updated_content = new_content
    
    if changes_made > 0:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(updated_content)
        print(f"✅ {changes_made} éléments mis à jour dans {file_path}")
        return True
    else:
        print(f"⚠️  Aucune modification nécessaire dans {file_path}")
        return False

def main():
    if len(sys.argv) != 2:
        print("❌ Usage: python update_version.py [nouveau_numero]")
        print("📋 Exemple: python update_version.py 1.0.9")
        sys.exit(1)
    
    new_version = sys.argv[1]
    
    # Valider le format de version
    if not re.match(r'^\d+\.\d+\.\d+$', new_version):
        print("❌ Format de version invalide. Utilisez X.Y.Z (ex: 1.0.9)")
        sys.exit(1)
    
    init_file = "__init__.py"
    
    if not os.path.exists(init_file):
        print(f"❌ Fichier {init_file} non trouvé dans le répertoire courant")
        sys.exit(1)
    
    # Détecter la version actuelle
    with open(init_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    version_match = re.search(r'"version": \((\d+), (\d+), (\d+)\)', content)
    if not version_match:
        print("❌ Impossible de détecter la version actuelle")
        sys.exit(1)
    
    current_version = f"{version_match.group(1)}.{version_match.group(2)}.{version_match.group(3)}"
    
    print(f"🔄 Mise à jour de version:")
    print(f"   📈 {current_version} → {new_version}")
    
    # Confirmer
    response = input(f"✅ Confirmer la mise à jour ? (y/N): ")
    if response.lower() != 'y':
        print("❌ Annulé")
        sys.exit(0)
    
    # Mettre à jour
    if update_version_in_file(init_file, current_version, new_version):
        print(f"🎉 Version mise à jour avec succès!")
        print(f"🚀 Vous pouvez maintenant exécuter: python DEPLOY_TOKYO_1_0.py")
    else:
        print("❌ Échec de la mise à jour")
        sys.exit(1)

if __name__ == "__main__":
    main()

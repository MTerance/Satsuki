#!/usr/bin/env python3
"""
Script de déploiement automatique pour l'addon City Block Generator
Copie automatiquement les fichiers Python vers le répertoire des addons de Blender
"""

import os
import shutil
import sys
from pathlib import Path

# Configuration des chemins
SOURCE_DIR = r"C:\Users\sshom\source\repos\Satsuki\Satsuki-Tools\CityGenerator_Blender\city_block_generator"
TARGET_DIR = r"C:\Users\sshom\AppData\Roaming\Blender Foundation\Blender\4.5\scripts\addons\city_block_generator"

# Fichiers Python à copier
PYTHON_FILES = [
    "__init__.py",
    "generator.py", 
    "operators.py",
    "ui.py",
    "reload_addon.py"
]

def ensure_target_directory():
    """Crée le répertoire de destination s'il n'existe pas"""
    try:
        Path(TARGET_DIR).mkdir(parents=True, exist_ok=True)
        print(f"✅ Répertoire de destination vérifié: {TARGET_DIR}")
        return True
    except Exception as e:
        print(f"❌ Erreur création répertoire de destination: {e}")
        return False

def copy_python_files():
    """Copie tous les fichiers Python vers le répertoire addon de Blender"""
    copied_files = 0
    failed_files = 0
    
    print("📂 Copie des fichiers Python...")
    
    for filename in PYTHON_FILES:
        source_path = os.path.join(SOURCE_DIR, filename)
        target_path = os.path.join(TARGET_DIR, filename)
        
        try:
            if os.path.exists(source_path):
                # Copier le fichier
                shutil.copy2(source_path, target_path)
                
                # Vérifier que la copie a réussi
                if os.path.exists(target_path):
                    source_size = os.path.getsize(source_path)
                    target_size = os.path.getsize(target_path)
                    
                    if source_size == target_size:
                        print(f"✅ {filename} copié ({source_size} bytes)")
                        copied_files += 1
                    else:
                        print(f"⚠️ {filename} copié mais tailles différentes (source: {source_size}, cible: {target_size})")
                        failed_files += 1
                else:
                    print(f"❌ {filename} : échec de la copie")
                    failed_files += 1
            else:
                print(f"⚠️ {filename} : fichier source introuvable")
                failed_files += 1
                
        except Exception as e:
            print(f"❌ Erreur lors de la copie de {filename}: {e}")
            failed_files += 1
    
    return copied_files, failed_files

def backup_existing_addon():
    """Crée une sauvegarde de l'addon existant s'il existe"""
    if os.path.exists(TARGET_DIR):
        backup_dir = f"{TARGET_DIR}_backup_{int(time.time())}"
        try:
            shutil.copytree(TARGET_DIR, backup_dir)
            print(f"💾 Sauvegarde créée: {backup_dir}")
            return True
        except Exception as e:
            print(f"⚠️ Impossible de créer la sauvegarde: {e}")
            return False
    return True

def verify_installation():
    """Vérifie que tous les fichiers ont été correctement installés"""
    print("\n🔍 Vérification de l'installation...")
    
    all_good = True
    for filename in PYTHON_FILES:
        target_path = os.path.join(TARGET_DIR, filename)
        if os.path.exists(target_path):
            print(f"✅ {filename} présent")
        else:
            print(f"❌ {filename} manquant")
            all_good = False
    
    return all_good

def main():
    """Fonction principale de déploiement"""
    print("🚀 === DÉPLOIEMENT ADDON CITY BLOCK GENERATOR ===")
    print(f"📁 Source: {SOURCE_DIR}")
    print(f"📁 Destination: {TARGET_DIR}")
    print()
    
    # Vérifier que le répertoire source existe
    if not os.path.exists(SOURCE_DIR):
        print(f"❌ ERREUR: Répertoire source introuvable: {SOURCE_DIR}")
        return False
    
    # Créer le répertoire de destination
    if not ensure_target_directory():
        return False
    
    # Copier les fichiers
    copied, failed = copy_python_files()
    
    # Vérifier l'installation
    success = verify_installation()
    
    # Résumé
    print(f"\n📊 === RÉSUMÉ DU DÉPLOIEMENT ===")
    print(f"✅ Fichiers copiés avec succès: {copied}")
    print(f"❌ Fichiers en échec: {failed}")
    print(f"🎯 Installation {'réussie' if success else 'échouée'}")
    
    if success:
        print("\n🎉 DÉPLOIEMENT TERMINÉ AVEC SUCCÈS!")
        print("💡 Vous pouvez maintenant:")
        print("   1. Ouvrir Blender")
        print("   2. Aller dans Edit > Preferences > Add-ons")
        print("   3. Rechercher 'City Block Generator'")
        print("   4. Activer l'addon")
        print("   5. Utiliser les boutons de rechargement pour les mises à jour")
        
        return True
    else:
        print("\n💥 DÉPLOIEMENT ÉCHOUÉ!")
        print("🔧 Vérifiez les permissions et les chemins")
        return False

if __name__ == "__main__":
    import time
    success = main()
    
    input("\nAppuyez sur Entrée pour fermer...")
    sys.exit(0 if success else 1)

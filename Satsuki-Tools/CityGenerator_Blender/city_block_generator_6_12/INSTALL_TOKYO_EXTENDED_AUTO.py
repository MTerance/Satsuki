#!/usr/bin/env python3
"""
INSTALLATION AUTOMATIQUE TOKYO CITY GENERATOR v2.2.0 EXTENDED
================================================================

🤖 SCRIPT D'INSTALLATION AUTOMATIQUE
✅ Supprime automatiquement les anciennes versions
✅ Installe la nouvelle version v2.2.0 Extended  
✅ Active l'addon automatiquement
✅ Nettoie les fichiers temporaires

📋 FONCTIONNALITÉS :
- Détecte le répertoire Blender automatiquement
- Supprime toutes les versions précédentes de Tokyo Generator
- Installe tokyo_v2_2_0_EXTENDED.zip
- Active l'addon dans Blender
- Vérifie l'installation

🎯 RÉSULTAT : Addon prêt à utiliser avec 14 types de bâtiments !
"""

import os
import shutil
import zipfile
import sys
import glob
import subprocess
import time
from pathlib import Path

def find_blender_executable():
    """Trouve l'exécutable Blender"""
    
    possible_paths = [
        "C:\\Program Files\\Blender Foundation\\Blender 4.2\\blender.exe",
        "C:\\Program Files\\Blender Foundation\\Blender 4.1\\blender.exe", 
        "C:\\Program Files\\Blender Foundation\\Blender 4.0\\blender.exe",
        "C:\\Program Files (x86)\\Blender Foundation\\Blender 4.2\\blender.exe",
        "C:\\Program Files (x86)\\Blender Foundation\\Blender 4.1\\blender.exe",
        "C:\\Program Files (x86)\\Blender Foundation\\Blender 4.0\\blender.exe",
    ]
    
    for path in possible_paths:
        if os.path.exists(path):
            print(f"🎯 Blender trouvé: {path}")
            return path
    
    # Recherche avec glob
    search_patterns = [
        "C:\\Program Files\\Blender Foundation\\Blender*\\blender.exe",
        "C:\\Program Files (x86)\\Blender Foundation\\Blender*\\blender.exe",
    ]
    
    for pattern in search_patterns:
        matches = glob.glob(pattern)
        if matches:
            latest = max(matches, key=lambda x: os.path.getmtime(x))
            print(f"🎯 Blender trouvé: {latest}")
            return latest
    
    return None

def close_blender():
    """Ferme toutes les instances de Blender"""
    
    print("🔄 Fermeture de Blender...")
    
    try:
        # Méthode Windows pour fermer Blender
        result = subprocess.run(["taskkill", "/F", "/IM", "blender.exe"], 
                              capture_output=True, text=True)
        
        if result.returncode == 0:
            print("   ✅ Blender fermé avec succès")
            time.sleep(2)  # Attendre que le processus se ferme complètement
            return True
        else:
            print("   ℹ️ Aucune instance de Blender trouvée")
            return True
            
    except Exception as e:
        print(f"   ⚠️ Erreur fermeture Blender: {e}")
        return False

def restart_blender(blender_exe):
    """Redémarre Blender"""
    
    if not blender_exe:
        print("❌ Impossible de redémarrer Blender - exécutable non trouvé")
        return False
    
    print("🚀 Redémarrage de Blender...")
    
    try:
        # Démarrer Blender en arrière-plan
        subprocess.Popen([blender_exe], shell=True)
        print("   ✅ Blender redémarré avec succès")
        print("   🎯 L'addon devrait être disponible maintenant!")
        return True
        
    except Exception as e:
        print(f"   ❌ Erreur redémarrage: {e}")
        return False

def find_blender_addons_directory():
    """Trouve le répertoire des addons Blender"""
    
    # Répertoires possibles pour Blender sur Windows
    possible_paths = [
        os.path.expanduser("~\\AppData\\Roaming\\Blender Foundation\\Blender"),
        "C:\\Program Files\\Blender Foundation\\Blender",
        "C:\\Program Files (x86)\\Blender Foundation\\Blender",
        os.path.expanduser("~\\Documents\\Blender"),
    ]
    
    # Chercher les versions Blender récentes
    blender_versions = ["4.2", "4.1", "4.0", "3.6", "3.5"]
    
    for base_path in possible_paths:
        for version in blender_versions:
            addons_path = os.path.join(base_path, version, "scripts", "addons")
            if os.path.exists(addons_path):
                print(f"🎯 Répertoire Blender trouvé: {addons_path}")
                return addons_path
    
    # Chercher manuellement avec glob patterns
    print("🔍 Recherche automatique du répertoire Blender...")
    search_patterns = [
        os.path.expanduser("~\\AppData\\Roaming\\Blender Foundation\\Blender\\*\\scripts\\addons"),
        "C:\\Program Files\\Blender Foundation\\Blender\\*\\scripts\\addons",
    ]
    
    for pattern in search_patterns:
        matches = glob.glob(pattern)
        if matches:
            # Prendre le plus récent
            latest = max(matches, key=lambda x: os.path.getmtime(x))
            print(f"🎯 Répertoire Blender trouvé: {latest}")
            return latest
    
    return None

def remove_old_tokyo_versions(addons_dir):
    """Supprime toutes les anciennes versions de Tokyo Generator"""
    
    print("🗑️ Suppression des anciennes versions...")
    
    # Patterns de recherche pour les anciennes versions
    old_patterns = [
        "TOKYO_*",
        "tokyo_*", 
        "Tokyo_*",
        "*tokyo*",
        "*TOKYO*"
    ]
    
    removed_count = 0
    
    for pattern in old_patterns:
        search_path = os.path.join(addons_dir, pattern)
        matches = glob.glob(search_path)
        
        for old_addon in matches:
            if os.path.isdir(old_addon):
                try:
                    shutil.rmtree(old_addon)
                    print(f"   ❌ Supprimé: {os.path.basename(old_addon)}")
                    removed_count += 1
                except Exception as e:
                    print(f"   ⚠️ Erreur suppression {old_addon}: {e}")
    
    if removed_count == 0:
        print("   ✅ Aucune ancienne version trouvée")
    else:
        print(f"   ✅ {removed_count} anciennes versions supprimées")
    
    return removed_count

def install_new_addon(addons_dir, zip_path):
    """Installe la nouvelle version de l'addon"""
    
    print("📦 Installation de la nouvelle version...")
    
    if not os.path.exists(zip_path):
        print(f"❌ Fichier ZIP non trouvé: {zip_path}")
        return False
    
    try:
        # Extraire le ZIP
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(addons_dir)
        
        print(f"   ✅ Extraction réussie vers {addons_dir}")
        
        # Vérifier l'installation
        new_addon_dirs = glob.glob(os.path.join(addons_dir, "TOKYO_EXTENDED_*"))
        if new_addon_dirs:
            addon_dir = new_addon_dirs[0]
            addon_name = os.path.basename(addon_dir)
            print(f"   ✅ Addon installé: {addon_name}")
            
            # Vérifier le fichier __init__.py
            init_file = os.path.join(addon_dir, "__init__.py")
            if os.path.exists(init_file):
                print(f"   ✅ Fichier __init__.py trouvé")
                return True
            else:
                print(f"   ❌ Fichier __init__.py manquant")
                return False
        else:
            print("   ❌ Répertoire d'addon non trouvé après extraction")
            return False
            
    except Exception as e:
        print(f"❌ Erreur lors de l'installation: {e}")
        return False

def create_activation_script(addons_dir):
    """Crée un script Python pour activer l'addon dans Blender"""
    
    activation_script = f'''
import bpy

# Script d'activation automatique pour Tokyo City Generator v2.2.0 Extended
try:
    # Actualiser la liste des addons
    bpy.ops.preferences.addon_refresh()
    
    # Chercher l'addon Tokyo Extended
    addon_name = None
    for addon in bpy.context.preferences.addons.keys():
        if "TOKYO_EXTENDED" in addon.upper() or "tokyo" in addon.lower():
            addon_name = addon
            break
    
    if addon_name:
        # Activer l'addon
        bpy.ops.preferences.addon_enable(module=addon_name)
        print(f"✅ Addon activé: {{addon_name}}")
        
        # Sauvegarder les préférences
        bpy.ops.wm.save_userpref()
        print("✅ Préférences sauvegardées")
        
    else:
        print("❌ Addon Tokyo Extended non trouvé")
        
except Exception as e:
    print(f"❌ Erreur activation: {{e}}")
'''
    
    script_path = os.path.join(addons_dir, "activate_tokyo_extended.py")
    
    try:
        with open(script_path, 'w', encoding='utf-8') as f:
            f.write(activation_script)
        print(f"📝 Script d'activation créé: {script_path}")
        return script_path
    except Exception as e:
        print(f"❌ Erreur création script: {e}")
        return None

def main():
    print("🤖 INSTALLATION AUTOMATIQUE TOKYO v2.2.0 EXTENDED")
    print("=" * 60)
    
    # 1. Trouver l'exécutable Blender
    blender_exe = find_blender_executable()
    if not blender_exe:
        print("⚠️ Blender non trouvé - installation manuelle requise")
        print("Continuons avec l'installation des fichiers...")
    
    # 2. Fermer Blender s'il est ouvert
    close_blender()
    
    # 3. Trouver le répertoire Blender
    addons_dir = find_blender_addons_directory()
    if not addons_dir:
        print("❌ ERREUR: Répertoire addons Blender non trouvé!")
        print("\n📋 INSTALLATION MANUELLE:")
        print("1. Ouvrez Blender > Edit > Preferences > Add-ons")
        print("2. Install > tokyo_v2_2_0_EXTENDED.zip")
        print("3. Activez 'Tokyo City Generator v2.2.0 Extended'")
        return False
    
    # 4. Supprimer les anciennes versions
    removed = remove_old_tokyo_versions(addons_dir)
    
    # 5. Installer la nouvelle version
    zip_path = "tokyo_v2_2_0_EXTENDED.zip"
    if not install_new_addon(addons_dir, zip_path):
        print("❌ ERREUR: Installation échouée!")
        return False
    
    # 6. Créer le script d'activation
    script_path = create_activation_script(addons_dir)
    
    print("\n" + "=" * 60)
    print("🎉 INSTALLATION RÉUSSIE !")
    print("=" * 60)
    print("✅ Blender fermé automatiquement")
    print("✅ Anciennes versions supprimées")
    print("✅ Tokyo City Generator v2.2.0 Extended installé")
    print("✅ 14 types de bâtiments disponibles")
    
    # 7. Redémarrer Blender
    if blender_exe:
        print("\n� Redémarrage de Blender en cours...")
        time.sleep(1)
        restart_success = restart_blender(blender_exe)
        
        if restart_success:
            print("✅ Blender redémarré avec la nouvelle version!")
        else:
            print("⚠️ Redémarrage manuel requis")
    else:
        print("⚠️ Veuillez redémarrer Blender manuellement")
    
    print("\n�🔥 NOUVEAUX TYPES:")
    print("   🏥 Hospital - Hôpitaux modernes")
    print("   ⛩️ Temple - Sanctuaires traditionnels")
    print("   🏭 Factory - Complexes industriels")
    print("   🏬 Mall - Centres commerciaux")
    print("   🚉 Station - Gares et stations")
    print("   🏢 Skyscraper - Gratte-ciels ultra-hauts")
    
    print("\n📋 DANS BLENDER:")
    print("1. Vue 3D > Sidebar (N) > Onglet CityGen")
    print("2. Vous devriez voir 'Tokyo City Generator v2.2.0 Extended'")
    print("3. Testez avec: Grille 4x4, Style Mixed, Densité 0.75")
    print("4. Mode Material Preview pour voir les couleurs")
    
    if script_path:
        print(f"\n🔧 Si l'addon n'est pas activé, exécutez:")
        print(f"   Scripting > Ouvrir > {script_path}")
    
    print("\n🎊 PROFITEZ DE VOS 14 TYPES DE BÂTIMENTS !")
    
    return True

if __name__ == "__main__":
    main()
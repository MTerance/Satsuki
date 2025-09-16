#!/usr/bin/env python3
"""
NETTOYAGE COMPLET ET RÉINSTALLATION TOKYO v2.2.0
=================================================

🧹 NETTOYAGE FORCÉ DE TOUTES LES VERSIONS TOKYO
🔧 INSTALLATION PROPRE DE LA v2.2.0 EXTENDED
🔄 REDÉMARRAGE AUTOMATIQUE DE BLENDER

Ce script fait un nettoyage radical pour éliminer toute trace des anciennes versions.
"""

import os
import shutil
import zipfile
import sys
import glob
import subprocess
import time
from pathlib import Path

def force_close_blender():
    """Force la fermeture complète de Blender"""
    
    print("🔄 Fermeture forcée de Blender...")
    
    try:
        # Méthode 1: Fermeture douce
        subprocess.run(["taskkill", "/IM", "blender.exe"], capture_output=True)
        time.sleep(2)
        
        # Méthode 2: Fermeture forcée
        subprocess.run(["taskkill", "/F", "/IM", "blender.exe"], capture_output=True)
        time.sleep(3)
        
        print("   ✅ Blender complètement fermé")
        return True
        
    except Exception as e:
        print(f"   ⚠️ Erreur fermeture: {e}")
        return False

def find_all_blender_directories():
    """Trouve TOUS les répertoires Blender possibles"""
    
    base_paths = [
        os.path.expanduser("~\\AppData\\Roaming\\Blender Foundation\\Blender"),
        os.path.expanduser("~\\AppData\\Local\\Blender Foundation\\Blender"),
        "C:\\Program Files\\Blender Foundation\\Blender",
        "C:\\Program Files (x86)\\Blender Foundation\\Blender",
    ]
    
    all_addon_dirs = []
    
    for base_path in base_paths:
        if os.path.exists(base_path):
            # Chercher toutes les versions
            for version_dir in os.listdir(base_path):
                version_path = os.path.join(base_path, version_dir)
                addons_path = os.path.join(version_path, "scripts", "addons")
                if os.path.exists(addons_path):
                    all_addon_dirs.append(addons_path)
                    print(f"📁 Répertoire trouvé: {addons_path}")
    
    return all_addon_dirs

def nuclear_cleanup_tokyo(addon_dirs):
    """Suppression nucléaire de toutes les versions Tokyo"""
    
    print("💥 NETTOYAGE NUCLÉAIRE DE TOUTES LES VERSIONS TOKYO")
    print("-" * 50)
    
    total_removed = 0
    
    # Patterns de recherche très larges
    patterns = [
        "*tokyo*", "*TOKYO*", "*Tokyo*",
        "*EXTENDED*", "*extended*",
        "*city*", "*CITY*", "*City*",
        "TOKYO_*", "tokyo_*",
    ]
    
    for addon_dir in addon_dirs:
        print(f"🔍 Nettoyage de: {addon_dir}")
        
        for pattern in patterns:
            search_path = os.path.join(addon_dir, pattern)
            matches = glob.glob(search_path)
            
            for match in matches:
                if os.path.isdir(match):
                    try:
                        # Forcer les permissions avant suppression
                        os.system(f'attrib -R "{match}\\*.*" /S')
                        shutil.rmtree(match, ignore_errors=True)
                        print(f"   ❌ SUPPRIMÉ: {os.path.basename(match)}")
                        total_removed += 1
                    except Exception as e:
                        print(f"   ⚠️ Erreur suppression {match}: {e}")
                        # Tentative avec rmdir /S
                        try:
                            os.system(f'rmdir /S /Q "{match}"')
                            print(f"   ❌ FORCÉ: {os.path.basename(match)}")
                            total_removed += 1
                        except:
                            pass
    
    print(f"✅ NETTOYAGE TERMINÉ: {total_removed} éléments supprimés")
    return total_removed

def install_fresh_addon(primary_addon_dir):
    """Installation propre de la nouvelle version"""
    
    print("📦 INSTALLATION PROPRE v2.2.0...")
    
    zip_path = "tokyo_v2_2_0_EXTENDED.zip"
    if not os.path.exists(zip_path):
        print(f"❌ ZIP non trouvé: {zip_path}")
        return False
    
    try:
        # Extraction
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(primary_addon_dir)
        
        # Vérifier
        new_dirs = glob.glob(os.path.join(primary_addon_dir, "TOKYO_EXTENDED_*"))
        if new_dirs:
            addon_dir = new_dirs[0]
            init_file = os.path.join(addon_dir, "__init__.py")
            
            if os.path.exists(init_file):
                # Vérifier le contenu du __init__.py
                with open(init_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                    if "v2.2.0" in content and "Extended" in content:
                        print("   ✅ v2.2.0 Extended installée correctement")
                        return True
                    else:
                        print("   ❌ Mauvaise version dans __init__.py")
                        return False
            else:
                print("   ❌ __init__.py manquant")
                return False
        else:
            print("   ❌ Répertoire addon non trouvé")
            return False
            
    except Exception as e:
        print(f"❌ Erreur installation: {e}")
        return False

def create_activation_script(addon_dir):
    """Crée un script d'activation spécifique"""
    
    script_content = '''
import bpy

def activate_tokyo_extended():
    """Active spécifiquement Tokyo Extended v2.2.0"""
    
    try:
        # Actualiser
        bpy.ops.preferences.addon_refresh()
        
        # Chercher l'addon spécifique
        addon_module = "TOKYO_EXTENDED_V2_2_0"
        
        # Désactiver d'abord toutes les versions Tokyo
        for addon_name in list(bpy.context.preferences.addons.keys()):
            if any(keyword in addon_name.upper() for keyword in ["TOKYO", "CITY"]):
                try:
                    bpy.ops.preferences.addon_disable(module=addon_name)
                    print(f"Désactivé: {addon_name}")
                except:
                    pass
        
        # Activer la nouvelle version
        try:
            bpy.ops.preferences.addon_enable(module=addon_module)
            print(f"✅ ACTIVÉ: {addon_module}")
            
            # Sauvegarder
            bpy.ops.wm.save_userpref()
            print("✅ Préférences sauvegardées")
            
            return True
            
        except Exception as e:
            print(f"❌ Erreur activation: {e}")
            return False
            
    except Exception as e:
        print(f"❌ Erreur générale: {e}")
        return False

# Exécuter l'activation
if __name__ == "__main__":
    activate_tokyo_extended()
'''
    
    script_path = os.path.join(addon_dir, "FORCE_ACTIVATE_TOKYO_V2_2_0.py")
    
    try:
        with open(script_path, 'w', encoding='utf-8') as f:
            f.write(script_content)
        print(f"📝 Script d'activation créé: {script_path}")
        return script_path
    except Exception as e:
        print(f"❌ Erreur script: {e}")
        return None

def main():
    print("💥 NETTOYAGE COMPLET TOKYO + RÉINSTALLATION v2.2.0")
    print("=" * 60)
    
    # 1. Fermer Blender
    force_close_blender()
    
    # 2. Trouver tous les répertoires
    addon_dirs = find_all_blender_directories()
    if not addon_dirs:
        print("❌ Aucun répertoire Blender trouvé!")
        return False
    
    # 3. Nettoyage nucléaire
    nuclear_cleanup_tokyo(addon_dirs)
    
    # 4. Installation propre
    primary_dir = addon_dirs[0]  # Utiliser le premier trouvé
    if not install_fresh_addon(primary_dir):
        print("❌ Installation échouée!")
        return False
    
    # 5. Script d'activation
    script_path = create_activation_script(primary_dir)
    
    # 6. Redémarrer Blender
    blender_exe = find_blender_executable()
    if blender_exe:
        print("\n🚀 Redémarrage de Blender...")
        subprocess.Popen([blender_exe])
        time.sleep(3)
        print("✅ Blender redémarré")
    
    print("\n" + "=" * 60)
    print("🎉 NETTOYAGE + INSTALLATION TERMINÉS !")
    print("=" * 60)
    print("✅ Toutes les anciennes versions supprimées")
    print("✅ Tokyo City Generator v2.2.0 Extended installé")
    print("✅ Blender redémarré")
    
    print("\n📋 DANS BLENDER:")
    print("1. Allez dans Edit > Preferences > Add-ons")
    print("2. Cherchez 'Tokyo City Generator v2.2.0 Extended'")
    print("3. ACTIVEZ l'addon (cochez la case)")
    print("4. Vue 3D > Sidebar (N) > CityGen")
    
    if script_path:
        print(f"\n🔧 Si problème, exécutez dans Scripting:")
        print(f"   {script_path}")
    
    print("\n🏗️ NOUVEAUX BÂTIMENTS v2.2.0:")
    print("   🏥 Hospital 🏭 Factory 🏬 Mall")
    print("   ⛩️ Temple 🚉 Station 🏢 Skyscraper")
    
    return True

def find_blender_executable():
    """Trouve Blender"""
    patterns = [
        "C:\\Program Files\\Blender Foundation\\Blender*\\blender.exe",
        "C:\\Program Files (x86)\\Blender Foundation\\Blender*\\blender.exe",
    ]
    
    for pattern in patterns:
        matches = glob.glob(pattern)
        if matches:
            return max(matches, key=os.path.getmtime)
    return None

if __name__ == "__main__":
    main()
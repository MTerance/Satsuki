"""
DÉPLOIEMENT ADDON CLEAN V6.14.0
Déploie l'addon nettoyé et optimisé
"""

import shutil
import os

def deployer_addon_clean():
    """Déploie l'addon nettoyé v6.14.0"""
    
    print("🚀 === DÉPLOIEMENT ADDON CLEAN V6.14.0 === 🚀")
    
    source_path = "../1_ADDON_CLEAN"
    addon_path = r"C:\Users\sshom\Documents\assets\Tools\city_block_generator_6_14_clean"
    
    # Vérifier que l'addon nettoyé existe
    required_files = ["__init__.py", "generator.py", "operators.py", "ui.py"]
    
    print("📋 Vérification addon nettoyé...")
    for file in required_files:
        file_path = os.path.join(source_path, file)
        if os.path.exists(file_path):
            size = os.path.getsize(file_path)
            print(f"   ✅ {file}: {size:,} bytes")
        else:
            print(f"   ❌ {file}: MANQUANT!")
            return False
    
    # Supprimer l'ancien addon s'il existe
    if os.path.exists(addon_path):
        print("🗑️ Suppression ancien addon...")
        shutil.rmtree(addon_path, ignore_errors=True)
    
    # Créer le dossier parent
    os.makedirs(os.path.dirname(addon_path), exist_ok=True)
    
    # Copier l'addon nettoyé
    print("📋 Copie addon nettoyé...")
    shutil.copytree(source_path, addon_path)
    
    # Vérification finale
    print("🔍 Vérification finale...")
    total_size = 0
    for file in required_files:
        file_path = os.path.join(addon_path, file)
        if os.path.exists(file_path):
            size = os.path.getsize(file_path)
            total_size += size
            print(f"   ✅ {file}: {size:,} bytes")
        else:
            print(f"   ❌ {file}: ÉCHEC COPIE!")
            return False
    
    print(f"📊 Taille totale addon: {total_size:,} bytes")
    
    print("🎯 === DÉPLOIEMENT RÉUSSI === 🎯")
    print(f"📁 Addon installé: {addon_path}")
    print(f"📊 Version: 6.14.0 CLEAN")
    print(f"🧹 Code mort supprimé, optimisé")
    print(f"🌊 Courbes Blender natives conservées")
    print("")
    print("🔄 === INSTRUCTIONS BLENDER ===")
    print("1. 🔄 REDÉMARRER Blender")
    print("2. 🔧 Edit > Preferences > Add-ons")
    print("3. 🗑️ SUPPRIMER l'ancien addon")
    print("4. ➕ Install > Sélectionner:")
    print(f"   📁 {addon_path}")
    print("5. ✅ ACTIVER City Block Generator v6.14.0")
    
    return True

if __name__ == "__main__":
    success = deployer_addon_clean()
    if success:
        print("🔥✅ DÉPLOIEMENT CLEAN RÉUSSI !")
    else:
        print("❌ DÉPLOIEMENT CLEAN ÉCHOUÉ !")

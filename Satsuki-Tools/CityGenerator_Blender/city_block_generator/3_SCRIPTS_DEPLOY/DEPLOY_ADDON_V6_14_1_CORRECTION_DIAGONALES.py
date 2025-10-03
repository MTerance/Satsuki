"""
DÉPLOIEMENT ADDON V6.14.1 - CORRECTION DIAGONALES
Déploie l'addon avec la correction des marques diagonales
"""

import shutil
import os
import sys
from datetime import datetime

def deployer_addon_v6_14_1():
    """Déploie l'addon v6.14.1 avec correction diagonales"""
    
    print("🚀 === DÉPLOIEMENT ADDON V6.14.1 - CORRECTION DIAGONALES === 🚀")
    print(f"📅 Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("")
    
    # Chemins
    source_path = os.path.abspath("../1_ADDON_CLEAN")
    target_path = r"C:\Users\sshom\Documents\assets\Tools\city_block_generator_6_14_1"
    blender_path = r"C:\Users\sshom\AppData\Roaming\Blender Foundation\Blender\4.5\scripts\addons\city_block_generator_6_14_1"
    
    # Fichiers requis
    required_files = ["__init__.py", "generator.py", "operators.py", "ui.py"]
    
    print("🔍 === VÉRIFICATION SOURCE === 🔍")
    print(f"📁 Source: {source_path}")
    
    total_source_size = 0
    for file in required_files:
        file_path = os.path.join(source_path, file)
        if os.path.exists(file_path):
            size = os.path.getsize(file_path)
            total_source_size += size
            print(f"   ✅ {file}: {size:,} bytes")
        else:
            print(f"   ❌ {file}: MANQUANT!")
            return False
    
    print(f"📊 Taille totale source: {total_source_size:,} bytes")
    
    # Vérifier version dans __init__.py
    init_path = os.path.join(source_path, "__init__.py")
    with open(init_path, 'r', encoding='utf-8') as f:
        content = f.read()
        if '"version": (6, 14, 1)' in content:
            print("   ✅ Version 6.14.1 confirmée")
        else:
            print("   ⚠️ Version non confirmée - vérifiez __init__.py")
    
    # Vérifier correction diagonales dans generator.py
    gen_path = os.path.join(source_path, "generator.py")
    with open(gen_path, 'r', encoding='utf-8') as f:
        content = f.read()
        if 'if False:  # curve_intensity > 0.7' in content:
            print("   ✅ Correction diagonales confirmée")
        else:
            print("   ⚠️ Correction diagonales NON TROUVÉE!")
            return False
    
    print("")
    print("🎯 === DÉPLOIEMENT DOUBLE === 🎯")
    
    # === DÉPLOIEMENT 1: Dossier assets ===
    print("📁 1. Déploiement vers assets...")
    if os.path.exists(target_path):
        print("🗑️ Suppression ancien addon assets...")
        shutil.rmtree(target_path, ignore_errors=True)
    
    os.makedirs(os.path.dirname(target_path), exist_ok=True)
    shutil.copytree(source_path, target_path)
    print(f"   ✅ Copié vers: {target_path}")
    
    # === DÉPLOIEMENT 2: Blender addons ===
    print("📁 2. Déploiement vers Blender...")
    if os.path.exists(blender_path):
        print("🗑️ Suppression ancien addon Blender...")
        shutil.rmtree(blender_path, ignore_errors=True)
    
    os.makedirs(os.path.dirname(blender_path), exist_ok=True)
    shutil.copytree(source_path, blender_path)
    print(f"   ✅ Copié vers: {blender_path}")
    
    print("")
    print("🔍 === VÉRIFICATION FINALE === 🔍")
    
    # Vérifier assets
    print("📁 Vérification assets...")
    for file in required_files:
        file_path = os.path.join(target_path, file)
        if os.path.exists(file_path):
            size = os.path.getsize(file_path)
            print(f"   ✅ {file}: {size:,} bytes")
        else:
            print(f"   ❌ {file}: ÉCHEC!")
            return False
    
    # Vérifier Blender
    print("📁 Vérification Blender...")
    for file in required_files:
        file_path = os.path.join(blender_path, file)
        if os.path.exists(file_path):
            size = os.path.getsize(file_path)
            print(f"   ✅ {file}: {size:,} bytes")
        else:
            print(f"   ❌ {file}: ÉCHEC!")
            return False
    
    print("")
    print("🎉 === DÉPLOIEMENT RÉUSSI === 🎉")
    print("📊 Statistiques:")
    print(f"   📦 Version: 6.14.1")
    print(f"   🔧 Correction: Marques diagonales éliminées") 
    print(f"   📁 Assets: {target_path}")
    print(f"   📁 Blender: {blender_path}")
    print(f"   📊 Taille: {total_source_size:,} bytes")
    print("")
    print("🔄 === INSTRUCTIONS BLENDER === 🔄")
    print("OPTION A - Auto (addon déjà installé):")
    print("   1. 🔄 REDÉMARRER Blender")
    print("   2. 🎯 L'addon v6.14.1 est déjà installé!")
    print("   3. ✅ Vérifier version dans le panneau CityGen")
    print("")
    print("OPTION B - Manuel (nouveau déploiement):")
    print("   1. 🔄 REDÉMARRER Blender")
    print("   2. 🔧 Edit > Preferences > Add-ons")
    print("   3. 🗑️ SUPPRIMER ancien addon si présent")
    print("   4. ➕ Install > Sélectionner dossier:")
    print(f"      📁 {blender_path}")
    print("   5. ✅ ACTIVER City Block Generator")
    print("")
    print("🧪 === TEST RECOMMANDÉ === 🧪")
    print("   📊 Grille: 3x3")
    print("   🌊 Curve Intensity: 0.5")
    print("   🎯 Mode: Organique")
    print("   ✅ Attendu: Courbes SANS marques diagonales")
    
    return True

def main():
    """Fonction principale"""
    try:
        success = deployer_addon_v6_14_1()
        
        if success:
            print("")
            print("🔥✅ DÉPLOIEMENT V6.14.1 RÉUSSI !")
            print("🎯 Correction diagonales appliquée")
            print("🌊 Prêt pour test courbes organiques")
        else:
            print("")
            print("❌ DÉPLOIEMENT V6.14.1 ÉCHOUÉ !")
            
        input("\nAppuyez sur Entrée pour fermer...")
        return success
        
    except Exception as e:
        print(f"💥 ERREUR CRITIQUE: {e}")
        import traceback
        print(f"Traceback: {traceback.format_exc()}")
        input("\nAppuyez sur Entrée pour fermer...")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)

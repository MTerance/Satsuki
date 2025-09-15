#!/usr/bin/env python3
"""
TOKYO CITY GENERATOR V2.1.8 - STABLE
Correction finale de l'erreur Transmission qui empêchait la génération
"""

import os
import shutil
import zipfile

def create_tokyo_v2_1_8():
    """Créer Tokyo v2.1.8 STABLE - sans erreurs"""
    
    print("=" * 60)
    print("🔧 TOKYO V2.1.8 - VERSION STABLE")
    print("Correction erreur Transmission + matériaux simplifiés")
    print("=" * 60)
    
    # Chemins
    source_file = r"TOKYO_SIMPLE_V2_1\__init__.py"
    blendfiles_dir = r"C:\Users\sshom\OneDrive\Documents\Assets\BlendFiles"
    
    # Package
    addon_name = "tokyo_city_generator"
    package_name = f"{addon_name}_v2_1_8_STABLE"
    
    # Structure temporaire
    temp_dir = f"temp_{addon_name}_v2_1_8"
    addon_folder = os.path.join(temp_dir, addon_name)
    
    if os.path.exists(temp_dir):
        shutil.rmtree(temp_dir)
    
    os.makedirs(addon_folder, exist_ok=True)
    
    print(f"📁 Structure: {addon_name}/")
    
    # Copier __init__.py
    if os.path.exists(source_file):
        dest_init = os.path.join(addon_folder, "__init__.py")
        shutil.copy2(source_file, dest_init)
        print(f"  ✅ {addon_name}/__init__.py")
    else:
        print(f"  ❌ ERREUR: {source_file} introuvable!")
        return None
    
    # Archive ZIP
    zip_path = os.path.join(blendfiles_dir, f"{package_name}.zip")
    
    print(f"📦 Création: {package_name}.zip")
    
    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(temp_dir):
            for file in files:
                file_path = os.path.join(root, file)
                arc_name = os.path.relpath(file_path, temp_dir)
                zipf.write(file_path, arc_name)
                print(f"  📄 {arc_name}")
    
    # Nettoyer
    shutil.rmtree(temp_dir)
    
    print("\\n" + "=" * 60)
    print("✅ TOKYO V2.1.8 STABLE CRÉÉ!")
    print("=" * 60)
    print(f"📦 {zip_path}")
    
    print("\\n🔧 CORRECTIONS CRITIQUES V2.1.8:")
    print("  🚨 ERREUR TRANSMISSION supprimée (causait plantage)")
    print("  🚨 MATÉRIAUX SIMPLIFIÉS (compatibilité 100% Blender 4.0+)")
    print("  ✅ 8 types de bâtiments avec couleurs distinctes")
    print("  ✅ Densité optimisée (2-10 bâtiments par bloc)")
    print("  ✅ Positionnement corrigé (proche des trottoirs)")
    
    print("\\n🎯 MAINTENANT ÇA DOIT MARCHER:")
    print("1. Installer tokyo_city_generator_v2_1_8_STABLE.zip")
    print("2. Générer ville - AUCUNE ERREUR dans console")
    print("3. Voir BEAUCOUP plus de bâtiments variés")
    print("4. Couleurs différentes par type de bâtiment")
    
    return zip_path

if __name__ == "__main__":
    try:
        result = create_tokyo_v2_1_8()
        if result:
            print(f"\\n🎉 VERSION STABLE: {result}")
        else:
            print("\\n❌ ÉCHEC")
    except Exception as e:
        print(f"\\n💥 ERREUR: {e}")
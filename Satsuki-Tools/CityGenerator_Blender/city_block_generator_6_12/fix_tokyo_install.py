#!/usr/bin/env python3
"""
CORRECTION INSTALLATION TOKYO CITY GENERATOR V2.1.6
Structure ZIP compatible Blender
"""

import os
import shutil
import zipfile
from datetime import datetime

def create_tokyo_v2_1_6_fixed():
    """Créer le package Tokyo v2.1.6 avec la bonne structure pour Blender"""
    
    print("=" * 60)
    print("CORRECTION INSTALLATION TOKYO V2.1.6")
    print("Structure ZIP compatible Blender")
    print("=" * 60)
    
    # Définir les chemins
    source_dir = "TOKYO_SIMPLE_V2_1"
    assets_dir = r"c:\Users\sshom\Documents\assets\Tools"
    blendfiles_dir = r"C:\Users\sshom\OneDrive\Documents\Assets\BlendFiles"
    package_name = "tokyo_city_generator_v2_1_6"
    
    # Créer le dossier temporaire avec la bonne structure
    temp_dir = os.path.join(assets_dir, "temp_tokyo")
    addon_dir = os.path.join(temp_dir, package_name)
    
    if os.path.exists(temp_dir):
        shutil.rmtree(temp_dir)
    
    os.makedirs(addon_dir, exist_ok=True)
    
    # Copier les fichiers dans le dossier addon
    files_to_copy = ["__init__.py"]
    
    print("📋 Création de la structure compatible Blender:")
    for file in files_to_copy:
        source_path = os.path.join(source_dir, file)
        dest_path = os.path.join(addon_dir, file)
        
        if os.path.exists(source_path):
            shutil.copy2(source_path, dest_path)
            print(f"  ✅ {package_name}/{file}")
        else:
            print(f"  ❌ MANQUANT: {file}")
    
    # Créer le README dans le dossier addon
    readme_content = """# Tokyo City Generator v2.1.6

## Installation
1. Télécharger tokyo_city_generator_v2_1_6.zip
2. Blender > Edit > Preferences > Add-ons
3. Install from File > Sélectionner le ZIP
4. Activer "Tokyo City Generator"
5. Panneau dans 3D Viewport > Sidebar (N) > CityGen

## Corrections v2.1.6
- Trottoirs aux intersections
- Bâtiments près des trottoirs
- 8 types de bâtiments variés
"""
    
    readme_path = os.path.join(addon_dir, "README.md")
    with open(readme_path, 'w', encoding='utf-8') as f:
        f.write(readme_content)
    print(f"  ✅ {package_name}/README.md")
    
    # Créer l'archive ZIP avec la bonne structure
    zip_path_tools = os.path.join(assets_dir, f"{package_name}.zip")
    zip_path_blendfiles = os.path.join(blendfiles_dir, f"{package_name}.zip")
    
    print(f"📦 Création de l'archive compatible Blender...")
    
    with zipfile.ZipFile(zip_path_tools, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(addon_dir):
            for file in files:
                file_path = os.path.join(root, file)
                # Structure: tokyo_city_generator_v2_1_6/__init__.py
                arc_name = os.path.relpath(file_path, temp_dir)
                zipf.write(file_path, arc_name)
                print(f"  📄 Ajouté: {arc_name}")
    
    # Copier vers BlendFiles
    shutil.copy2(zip_path_tools, zip_path_blendfiles)
    
    # Nettoyer le dossier temporaire
    shutil.rmtree(temp_dir)
    
    print("\n" + "=" * 60)
    print("✅ TOKYO V2.1.6 STRUCTURE CORRIGÉE!")
    print("=" * 60)
    print(f"📦 Archive Tools: {zip_path_tools}")
    print(f"📦 Archive BlendFiles: {zip_path_blendfiles}")
    print(f"📁 Structure: {package_name}/__init__.py")
    print(f"📁 Structure: {package_name}/README.md")
    print("\n🔧 INSTALLATION DANS BLENDER:")
    print("1. Edit > Preferences > Add-ons")
    print("2. Install from File > tokyo_city_generator_v2_1_6.zip")
    print("3. Rechercher 'Tokyo City Generator'")
    print("4. Activer l'addon ✅")
    print("5. Panneau CityGen dans sidebar (N)")
    
    return zip_path_blendfiles

if __name__ == "__main__":
    try:
        package_path = create_tokyo_v2_1_6_fixed()
        print(f"\n🎉 Package installable créé: {package_path}")
    except Exception as e:
        print(f"\n❌ ERREUR: {e}")
        input("Appuyez sur Entrée pour continuer...")
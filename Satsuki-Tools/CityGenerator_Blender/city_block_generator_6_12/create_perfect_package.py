#!/usr/bin/env python3
"""
CRÉATION PACKAGE BLENDER PARFAIT - TOKYO V2.1.6
Structure garantie compatible avec Blender
"""

import os
import shutil
import zipfile
from datetime import datetime

def create_perfect_blender_package():
    """Créer un package 100% compatible avec l'installation Blender"""
    
    print("=" * 60)
    print("CRÉATION PACKAGE BLENDER PARFAIT")
    print("Tokyo City Generator v2.1.6")
    print("=" * 60)
    
    # Chemins
    source_file = r"TOKYO_SIMPLE_V2_1\__init__.py"
    blendfiles_dir = r"C:\Users\sshom\OneDrive\Documents\Assets\BlendFiles"
    
    # Nom du package et structure
    addon_name = "tokyo_city_generator"
    package_name = f"{addon_name}_v2_1_6_INSTALL"
    
    # Créer dossier temporaire avec structure Blender
    temp_dir = f"temp_{addon_name}"
    addon_folder = os.path.join(temp_dir, addon_name)
    
    if os.path.exists(temp_dir):
        shutil.rmtree(temp_dir)
    
    os.makedirs(addon_folder, exist_ok=True)
    
    print(f"📁 Structure créée: {addon_folder}/")
    
    # Copier __init__.py
    if os.path.exists(source_file):
        dest_init = os.path.join(addon_folder, "__init__.py")
        shutil.copy2(source_file, dest_init)
        print(f"  ✅ {addon_name}/__init__.py")
        
        # Lire et afficher le bl_info pour vérification
        with open(dest_init, 'r', encoding='utf-8') as f:
            content = f.read()
            if 'bl_info' in content:
                lines = content.split('\\n')
                for i, line in enumerate(lines[:15]):
                    if 'bl_info' in line or (i > 0 and '}' not in lines[i-1] and i < 10):
                        print(f"    {line}")
    else:
        print(f"  ❌ ERREUR: {source_file} introuvable!")
        return None
    
    # Créer un __init__.py minimal si besoin (Blender best practice)
    init_comment = '''"""
Tokyo City Generator v2.1.6
Générateur de ville japonaise avec 8 types de bâtiments
Trottoirs fixes et espacement optimisé
"""

'''
    
    with open(dest_init, 'r', encoding='utf-8') as f:
        original_content = f.read()
    
    if not original_content.startswith('"""'):
        with open(dest_init, 'w', encoding='utf-8') as f:
            f.write(init_comment + original_content)
        print(f"  ✅ Documentation ajoutée")
    
    # Créer l'archive ZIP avec compression optimale
    zip_path = os.path.join(blendfiles_dir, f"{package_name}.zip")
    
    print(f"📦 Création archive: {package_name}.zip")
    
    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED, compresslevel=6) as zipf:
        for root, dirs, files in os.walk(temp_dir):
            for file in files:
                file_path = os.path.join(root, file)
                # Structure dans le ZIP: tokyo_city_generator/__init__.py
                arc_name = os.path.relpath(file_path, temp_dir)
                zipf.write(file_path, arc_name)
                print(f"  📄 Compressé: {arc_name}")
    
    # Vérifier le contenu du ZIP
    print(f"\\n🔍 VÉRIFICATION DU ZIP:")
    with zipfile.ZipFile(zip_path, 'r') as zipf:
        for info in zipf.filelist:
            print(f"  📋 {info.filename} ({info.file_size} bytes)")
    
    # Nettoyer
    shutil.rmtree(temp_dir)
    
    print("\\n" + "=" * 60)
    print("✅ PACKAGE PARFAIT CRÉÉ!")
    print("=" * 60)
    print(f"📦 Fichier: {zip_path}")
    print(f"📁 Structure: {addon_name}/__init__.py")
    print(f"💾 Prêt pour Blender!")
    
    print("\\n🎯 INSTALLATION:")
    print("1. Blender > Edit > Preferences > Add-ons")
    print("2. Install from File...")
    print(f"3. Sélectionner: {package_name}.zip")
    print("4. Rechercher 'Tokyo City Generator'")
    print("5. Activer avec la checkbox ✅")
    print("6. Aller dans 3D Viewport > Sidebar (N) > CityGen")
    
    return zip_path

if __name__ == "__main__":
    try:
        result = create_perfect_blender_package()
        if result:
            print(f"\\n🎉 SUCCÈS: {result}")
        else:
            print("\\n❌ ÉCHEC de création du package")
    except Exception as e:
        print(f"\\n💥 ERREUR: {e}")
        import traceback
        traceback.print_exc()
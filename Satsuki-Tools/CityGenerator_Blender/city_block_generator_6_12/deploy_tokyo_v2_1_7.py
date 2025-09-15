#!/usr/bin/env python3
"""
TOKYO CITY GENERATOR V2.1.7 - CORRECTIONS MAJEURES
Répare: génération bâtiments, positionnement, variété types
"""

import os
import shutil
import zipfile

def create_tokyo_v2_1_7():
    """Créer Tokyo v2.1.7 avec corrections majeures"""
    
    print("=" * 60)
    print("🚨 TOKYO V2.1.7 - CORRECTIONS MAJEURES")
    print("Réparation génération et positionnement")
    print("=" * 60)
    
    # Chemins
    source_file = r"TOKYO_SIMPLE_V2_1\__init__.py"
    blendfiles_dir = r"C:\Users\sshom\OneDrive\Documents\Assets\BlendFiles"
    
    # Package
    addon_name = "tokyo_city_generator"
    package_name = f"{addon_name}_v2_1_7_FIXED"
    
    # Structure temporaire
    temp_dir = f"temp_{addon_name}_v2_1_7"
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
    print("✅ TOKYO V2.1.7 CRÉÉ!")
    print("=" * 60)
    print(f"📦 {zip_path}")
    
    print("\\n🔧 CORRECTIONS V2.1.7:")
    print("  ✅ Calcul correct largeurs routes (main 6.0, secondary 3.2)")
    print("  ✅ Espace bâtiments recalculé précisément") 
    print("  ✅ Densité augmentée (0.8 par défaut)")
    print("  ✅ Plus de bâtiments par bloc (2-10 au lieu de 1-6)")
    print("  ✅ Debug ajouté pour diagnostics")
    print("  ✅ Conditions d'espace réduites (1m au lieu de 3m)")
    
    print("\\n🎯 TESTE MAINTENANT:")
    print("1. Installer tokyo_city_generator_v2_1_7_FIXED.zip")
    print("2. Générer ville 5x5 avec density 0.8")
    print("3. Vérifier bâtiments nombreux et variés")
    print("4. Regarder console Blender pour debug")
    
    return zip_path

if __name__ == "__main__":
    try:
        result = create_tokyo_v2_1_7()
        if result:
            print(f"\\n🎉 PRÊT: {result}")
        else:
            print("\\n❌ ÉCHEC")
    except Exception as e:
        print(f"\\n💥 ERREUR: {e}")
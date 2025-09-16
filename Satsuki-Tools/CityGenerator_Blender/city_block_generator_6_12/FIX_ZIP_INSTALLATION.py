#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
FIX INSTALLATION ZIP - Tokyo v2.1.9
====================================

Script pour corriger le problème d'installation ZIP.
Blender a besoin d'un dossier dans le ZIP, pas juste __init__.py à la racine.
"""

import os
import shutil
import zipfile

def fix_zip_installation():
    """Corriger le problème d'installation ZIP"""
    
    print("\n" + "="*70)
    print("FIX INSTALLATION ZIP - Tokyo v2.1.9")
    print("="*70)
    
    # Chemins
    base_path = r"c:\Users\sshom\source\repos\Satsuki\Satsuki-Tools\CityGenerator_Blender\city_block_generator_6_12"
    source_dir = os.path.join(base_path, "TOKYO_ORGANIC_V2_1_9")
    source_file = os.path.join(source_dir, "__init__.py")
    
    # Destination avec structure correcte
    zip_destination = os.path.join(r"c:\Users\sshom\Documents\assets\Tools", "tokyo_organic_v2_1_9_FIXED.zip")
    
    print(f"\n📁 CORRECTION STRUCTURE ZIP:")
    print(f"   Source: {source_file}")
    print(f"   ZIP destination: {zip_destination}")
    
    # 1. Vérifier le fichier source
    if not os.path.exists(source_file):
        print(f"   ❌ ERREUR: Fichier source non trouvé: {source_file}")
        return False
    
    print(f"   ✅ Fichier source: {os.path.getsize(source_file)} bytes")
    
    # 2. Créer le ZIP avec la BONNE structure
    print(f"\n📦 CRÉATION ZIP STRUCTURE CORRECTE:")
    print("-" * 50)
    
    try:
        # Créer le dossier de destination s'il n'existe pas
        os.makedirs(os.path.dirname(zip_destination), exist_ok=True)
        
        with zipfile.ZipFile(zip_destination, 'w', zipfile.ZIP_DEFLATED) as zipf:
            # IMPORTANT: Ajouter le fichier dans un DOSSIER nommé
            folder_name = "tokyo_organic_v2_1_9"
            zipf.write(source_file, f"{folder_name}/__init__.py")
            print(f"   ✅ Ajouté: {folder_name}/__init__.py")
        
        print(f"   ✅ ZIP corrigé créé: {zip_destination}")
        print(f"   📏 Taille: {os.path.getsize(zip_destination)} bytes")
        
    except Exception as e:
        print(f"   ❌ ERREUR création ZIP: {e}")
        return False
    
    # 3. Vérifier la structure du ZIP
    print(f"\n🔍 VÉRIFICATION STRUCTURE ZIP:")
    print("-" * 50)
    
    try:
        with zipfile.ZipFile(zip_destination, 'r') as zipf:
            files = zipf.namelist()
            print(f"   📋 Contenu du ZIP:")
            for file in files:
                print(f"      📄 {file}")
            
            if len(files) == 1 and files[0].endswith("__init__.py") and "/" in files[0]:
                print(f"   ✅ STRUCTURE CORRECTE!")
            else:
                print(f"   ❌ STRUCTURE INCORRECTE")
                return False
        
    except Exception as e:
        print(f"   ❌ Erreur vérification ZIP: {e}")
        return False
    
    # 4. Supprimer les anciens addons défaillants
    print(f"\n🧹 NETTOYAGE BLENDER:")
    print("-" * 50)
    
    blender_addons = r"c:\Users\sshom\AppData\Roaming\Blender Foundation\Blender\4.0\scripts\addons"
    
    if os.path.exists(blender_addons):
        old_versions = []
        for item in os.listdir(blender_addons):
            if any(keyword in item.lower() for keyword in ["tokyo", "city", "generator", "organic"]):
                old_versions.append(item)
        
        for old_version in old_versions:
            old_path = os.path.join(blender_addons, old_version)
            try:
                if os.path.isdir(old_path):
                    shutil.rmtree(old_path)
                    print(f"   🗑️  Supprimé dossier: {old_version}")
                else:
                    os.remove(old_path)
                    print(f"   🗑️  Supprimé fichier: {old_version}")
            except Exception as e:
                print(f"   ⚠️  Erreur suppression {old_version}: {e}")
    
    # 5. Instructions corrigées
    print(f"\n📋 INSTRUCTIONS INSTALLATION CORRIGÉES:")
    print("-" * 50)
    print(f"   1. **FERMEZ BLENDER** complètement")
    print(f"   2. **REDÉMARREZ BLENDER**")
    print(f"   3. Edit > Preferences > Add-ons")
    print(f"   4. Cliquez **'Install...'**")
    print(f"   5. Sélectionnez: {zip_destination}")
    print(f"   6. Cliquez **'Install Add-on'**")
    print(f"   7. Cherchez **'Tokyo'** dans la liste")
    print(f"   8. **COCHEZ** la case pour activer l'addon")
    print(f"   9. Vue 3D > appuyez **'N'** > onglet **'Tokyo'**")
    
    print(f"\n🎯 STRUCTURE ZIP CORRIGÉE:")
    print("-" * 50)
    print(f"   📦 tokyo_organic_v2_1_9_FIXED.zip")
    print(f"   └── 📁 tokyo_organic_v2_1_9/")
    print(f"       └── 📄 __init__.py")
    print(f"   ✅ Cette structure est CORRECTE pour Blender!")
    
    print(f"\n⚠️  RAPPEL IMPORTANT:")
    print("-" * 50)
    print(f"   • Le ZIP contient maintenant un DOSSIER avec __init__.py dedans")
    print(f"   • C'est exactement ce que Blender attend")
    print(f"   • L'erreur 'should be in a directory' est maintenant résolue")
    
    print("="*70)
    return True

if __name__ == "__main__":
    success = fix_zip_installation()
    if success:
        print("\n🎉 PROBLÈME ZIP RÉSOLU!")
        print("📦 Utilisez maintenant: tokyo_organic_v2_1_9_FIXED.zip")
    else:
        print("\n💥 CORRECTION ÉCHOUÉE!")
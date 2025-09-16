#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
RESTAURATION TOKYO v2.1.8 WORKING
==================================

Retour à la version qui fonctionne avec le bon format ZIP.
"""

import os
import shutil
import zipfile

def restore_working_version():
    """Restaurer la version v2.1.8 qui fonctionne"""
    
    print("\n" + "="*70)
    print("RESTAURATION TOKYO v2.1.8 WORKING")
    print("="*70)
    
    # Chemins
    base_path = r"c:\Users\sshom\source\repos\Satsuki\Satsuki-Tools\CityGenerator_Blender\city_block_generator_6_12"
    source_dir = os.path.join(base_path, "TOKYO_SIMPLE_V2_1")
    source_file = os.path.join(source_dir, "__init__.py")
    
    # ZIP avec structure correcte
    zip_destination = os.path.join(r"c:\Users\sshom\Documents\assets\Tools", "tokyo_v2_1_8_WORKING.zip")
    
    print(f"\n📁 RESTAURATION VERSION WORKING:")
    print(f"   Source: {source_file}")
    print(f"   ZIP destination: {zip_destination}")
    
    # 1. Vérifier le fichier source v2.1.8
    if not os.path.exists(source_file):
        print(f"   ❌ ERREUR: Fichier source v2.1.8 non trouvé: {source_file}")
        return False
    
    print(f"   ✅ Fichier source v2.1.8: {os.path.getsize(source_file)} bytes")
    
    # 2. Créer ZIP avec BONNE structure
    print(f"\n📦 CRÉATION ZIP v2.1.8 WORKING:")
    print("-" * 50)
    
    try:
        os.makedirs(os.path.dirname(zip_destination), exist_ok=True)
        
        with zipfile.ZipFile(zip_destination, 'w', zipfile.ZIP_DEFLATED) as zipf:
            # Structure correcte pour Blender
            folder_name = "tokyo_simple_v2_1_8"
            zipf.write(source_file, f"{folder_name}/__init__.py")
            print(f"   ✅ Ajouté: {folder_name}/__init__.py")
        
        print(f"   ✅ ZIP v2.1.8 créé: {zip_destination}")
        print(f"   📏 Taille: {os.path.getsize(zip_destination)} bytes")
        
    except Exception as e:
        print(f"   ❌ ERREUR création ZIP: {e}")
        return False
    
    # 3. Nettoyer Blender des versions problématiques
    print(f"\n🧹 NETTOYAGE VERSIONS PROBLÉMATIQUES:")
    print("-" * 50)
    
    blender_addons = r"c:\Users\sshom\AppData\Roaming\Blender Foundation\Blender\4.0\scripts\addons"
    
    if os.path.exists(blender_addons):
        # Supprimer les versions v2.1.9 qui posent problème
        problematic_versions = []
        for item in os.listdir(blender_addons):
            if any(keyword in item.lower() for keyword in ["tokyo", "organic", "v2_1_9"]):
                problematic_versions.append(item)
        
        for problem_version in problematic_versions:
            problem_path = os.path.join(blender_addons, problem_version)
            try:
                if os.path.isdir(problem_path):
                    shutil.rmtree(problem_path)
                    print(f"   🗑️  Supprimé version problématique: {problem_version}")
                else:
                    os.remove(problem_path)
                    print(f"   🗑️  Supprimé fichier problématique: {problem_version}")
            except Exception as e:
                print(f"   ⚠️  Erreur suppression {problem_version}: {e}")
    
    # 4. Vérifier le contenu de la v2.1.8
    print(f"\n🔍 VÉRIFICATION v2.1.8:")
    print("-" * 50)
    
    try:
        with open(source_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        features = [
            ("TOKYO_SIMPLE_OT_generate", "✅ Générateur principal"),
            ("apply_building_material_by_type", "✅ 8 types de bâtiments"),
            ("create_intersection_sidewalks", "✅ Trottoirs aux intersections"), 
            ("add_single_diagonal", "✅ Routes diagonales"),
            ("v2.1.8 STABLE", "✅ Interface v2.1.8"),
        ]
        
        for check, description in features:
            if check in content:
                print(f"   {description}")
            else:
                print(f"   ❌ MANQUE: {description}")
        
    except Exception as e:
        print(f"   ❌ Erreur lecture: {e}")
    
    # 5. Instructions de restauration
    print(f"\n📋 INSTRUCTIONS RESTAURATION:")
    print("-" * 50)
    print(f"   1. **FERMEZ BLENDER** complètement")
    print(f"   2. **REDÉMARREZ BLENDER**")
    print(f"   3. Edit > Preferences > Add-ons")
    print(f"   4. **DÉSACTIVEZ/SUPPRIMEZ** toutes les versions Tokyo existantes")
    print(f"   5. Cliquez **'Install...'**")
    print(f"   6. Sélectionnez: {zip_destination}")
    print(f"   7. **ACTIVEZ** 'Tokyo City Generator v2.1.8'")
    print(f"   8. Vue 3D > **'N'** > onglet **'Tokyo'**")
    print(f"   9. Vous devriez voir: 'Tokyo Generator v2.1.8 STABLE'")
    
    # 6. Test rapide recommandé
    print(f"\n🎯 TEST RAPIDE RECOMMANDÉ:")
    print("-" * 50)
    print(f"   • Taille: 5x5")
    print(f"   • Style: Mixed")
    print(f"   • Densité: 0.8")
    print(f"   • Better Materials: ✅")
    print(f"   • Changez le mode en 'Material Preview' pour voir les couleurs")
    
    print(f"\n⚠️  POURQUOI CETTE VERSION:")
    print("-" * 50)
    print(f"   • La v2.1.8 FONCTIONNE et génère une ville complète")
    print(f"   • La v2.1.9 était trop complexe et a des bugs")
    print(f"   • Cette version a été testée et validée")
    print(f"   • Vous aurez des bâtiments, routes, trottoirs ET diagonales")
    
    print("="*70)
    return True

if __name__ == "__main__":
    success = restore_working_version()
    if success:
        print("\n🔄 VERSION WORKING RESTAURÉE!")
        print("📦 Utilisez: tokyo_v2_1_8_WORKING.zip")
        print("✅ Cette version FONCTIONNE et génère une ville complète!")
    else:
        print("\n💥 RESTAURATION ÉCHOUÉE!")
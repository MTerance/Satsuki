#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
REDÉPLOIEMENT TOKYO v2.1.8 CORRECTED
====================================

Script pour redéployer la v2.1.8 avec l'interface corrigée.
"""

import os
import shutil
import zipfile

def redeploy_tokyo_v2_1_8_corrected():
    """Redéployer la v2.1.8 avec interface corrigée"""
    
    print("\n" + "="*70)
    print("REDÉPLOIEMENT TOKYO v2.1.8 INTERFACE CORRIGÉE")
    print("="*70)
    
    # Chemins
    base_path = r"c:\Users\sshom\source\repos\Satsuki\Satsuki-Tools\CityGenerator_Blender\city_block_generator_6_12"
    source_dir = os.path.join(base_path, "TOKYO_SIMPLE_V2_1")
    source_file = os.path.join(source_dir, "__init__.py")
    
    # Destinations
    blender_addons = r"c:\Users\sshom\AppData\Roaming\Blender Foundation\Blender\4.0\scripts\addons"
    zip_destination = os.path.join(r"c:\Users\sshom\Documents\assets\Tools", "tokyo_v2_1_8_corrected.zip")
    
    print(f"\n📁 CHEMINS:")
    print(f"   Source: {source_file}")
    print(f"   Blender addons: {blender_addons}")
    print(f"   ZIP destination: {zip_destination}")
    
    # 1. Vérifier que le fichier source existe
    if not os.path.exists(source_file):
        print(f"   ❌ ERREUR: Fichier source non trouvé: {source_file}")
        return False
    
    print(f"   ✅ Fichier source: {os.path.getsize(source_file)} bytes")
    
    # 2. Supprimer les anciennes versions dans Blender
    print(f"\n🧹 NETTOYAGE ANCIENNES VERSIONS:")
    print("-" * 40)
    
    if os.path.exists(blender_addons):
        # Supprimer toutes les versions Tokyo existantes
        old_versions = []
        for item in os.listdir(blender_addons):
            if any(keyword in item.lower() for keyword in ["tokyo", "city", "generator"]):
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
    
    # 3. Créer le nouveau package ZIP
    print(f"\n📦 CRÉATION PACKAGE ZIP:")
    print("-" * 40)
    
    try:
        # Créer le dossier de destination s'il n'existe pas
        os.makedirs(os.path.dirname(zip_destination), exist_ok=True)
        
        with zipfile.ZipFile(zip_destination, 'w', zipfile.ZIP_DEFLATED) as zipf:
            # Ajouter le fichier __init__.py à la racine du ZIP
            zipf.write(source_file, "__init__.py")
            print(f"   ✅ Ajouté: __init__.py")
        
        print(f"   ✅ Package ZIP créé: {zip_destination}")
        print(f"   📏 Taille: {os.path.getsize(zip_destination)} bytes")
        
    except Exception as e:
        print(f"   ❌ ERREUR création ZIP: {e}")
        return False
    
    # 4. Installation directe dans Blender
    print(f"\n⚙️ INSTALLATION DIRECTE:")
    print("-" * 40)
    
    if os.path.exists(blender_addons):
        addon_dest = os.path.join(blender_addons, "tokyo_simple_v2_1_8")
        
        try:
            # Créer le dossier addon
            os.makedirs(addon_dest, exist_ok=True)
            
            # Copier __init__.py
            shutil.copy2(source_file, addon_dest)
            
            print(f"   ✅ Addon installé dans: {addon_dest}")
            
        except Exception as e:
            print(f"   ❌ ERREUR installation directe: {e}")
    
    # 5. Vérification du contenu
    print(f"\n🔍 VÉRIFICATION CONTENU:")
    print("-" * 40)
    
    try:
        with open(source_file, 'r', encoding='utf-8') as f:
            content = f.read()
            
        # Vérifier que les corrections sont présentes
        if "v2.1.8 STABLE" in content:
            print("   ✅ Interface corrigée: v2.1.8 STABLE")
        else:
            print("   ⚠️  Interface non corrigée")
            
        if "apply_building_material_by_type" in content:
            print("   ✅ Système 8 types de bâtiments: présent")
        else:
            print("   ❌ Système 8 types manquant")
            
        if "create_intersection_sidewalks" in content:
            print("   ✅ Trottoirs aux intersections: présent")
        else:
            print("   ❌ Trottoirs aux intersections manquant")
            
    except Exception as e:
        print(f"   ❌ Erreur vérification: {e}")
    
    # 6. Instructions
    print(f"\n📋 INSTRUCTIONS:")
    print("-" * 40)
    print(f"   1. **REDÉMARREZ BLENDER** complètement")
    print(f"   2. Edit > Preferences > Add-ons")
    print(f"   3. Désactivez/supprimez l'ancien 'Tokyo Generator v2.1.4 FIXED'")
    print(f"   4. Installez le nouveau ZIP: {zip_destination}")
    print(f"   5. Activez 'Tokyo City Generator v2.1.8'")
    print(f"   6. Dans la vue 3D: sidebar (N) > onglet 'Tokyo'")
    print(f"   7. Vous devriez voir: '🏙️ Tokyo Generator v2.1.8 STABLE'")
    
    print(f"\n✨ FONCTIONNALITÉS v2.1.8:")
    print("-" * 40)
    print(f"   🏢 8 types de bâtiments colorés")
    print(f"   🚶 Trottoirs aux intersections")
    print(f"   🎨 Matériaux compatibles Blender 4.0+")
    print(f"   ↗️ Routes diagonales (grilles 6x6+)")
    print(f"   🔧 Interface simplifiée et stable")
    
    print("="*70)
    return True

if __name__ == "__main__":
    success = redeploy_tokyo_v2_1_8_corrected()
    if success:
        print("\n🎉 REDÉPLOIEMENT RÉUSSI!")
        print("N'oubliez pas de REDÉMARRER BLENDER !")
    else:
        print("\n💥 REDÉPLOIEMENT ÉCHOUÉ!")
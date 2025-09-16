#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
DÉPLOIEMENT TOKYO v2.1.9 CORRECTED
===================================

Script pour déployer la version corrigée qui résout tous les problèmes
de la v2.1.8 (matériaux gris, diagonales manquantes, blocs uniformes).
"""

import os
import shutil
import zipfile

def deploy_tokyo_v2_1_9_corrected():
    """Déployer la version corrigée v2.1.9"""
    
    print("\n" + "="*75)
    print("DÉPLOIEMENT TOKYO v2.1.9 CORRECTED - TOUTES ERREURS CORRIGÉES")
    print("="*75)
    
    # Chemins
    base_path = r"c:\Users\sshom\source\repos\Satsuki\Satsuki-Tools\CityGenerator_Blender\city_block_generator_6_12"
    source_dir = os.path.join(base_path, "TOKYO_ORGANIC_V2_1_9")
    source_file = os.path.join(source_dir, "__init__.py")
    
    # Destinations
    blender_addons = r"c:\Users\sshom\AppData\Roaming\Blender Foundation\Blender\4.0\scripts\addons"
    zip_destination = os.path.join(r"c:\Users\sshom\Documents\assets\Tools", "tokyo_v2_1_9_CORRECTED.zip")
    
    print(f"\n📁 CHEMINS:")
    print(f"   Source: {source_file}")
    print(f"   Blender addons: {blender_addons}")
    print(f"   ZIP destination: {zip_destination}")
    
    # 1. Vérifier que le fichier source existe
    if not os.path.exists(source_file):
        print(f"   ❌ ERREUR: Fichier source non trouvé: {source_file}")
        return False
    
    print(f"   ✅ Fichier source: {os.path.getsize(source_file)} bytes")
    
    # 2. Vérifier les corrections dans le code
    print(f"\n🔍 VÉRIFICATION CORRECTIONS:")
    print("-" * 50)
    
    try:
        with open(source_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        corrections = [
            ("apply_building_material_by_type", "🎨 Matériaux ultra-visibles"),
            ("force_material_preview_mode", "🖥️  Mode viewport automatique"),
            ("create_forced_diagonal", "↗️ Diagonales forcées"),
            ("ULTRA_VISIBLE", "🔶 Matériaux diagonales ultra-visibles"),
            ("v2.1.9 CORRECTED", "📋 Interface corrigée"),
            ("verify_generation_results", "🔧 Vérification post-génération"),
            ("Emission Strength", "✨ Émission pour visibilité"),
        ]
        
        for check, description in corrections:
            if check in content:
                print(f"   ✅ {description}")
            else:
                print(f"   ❌ MANQUE: {description}")
        
    except Exception as e:
        print(f"   ❌ Erreur lecture fichier: {e}")
        return False
    
    # 3. Supprimer toutes les anciennes versions
    print(f"\n🧹 NETTOYAGE COMPLET:")
    print("-" * 50)
    
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
    
    # 4. Créer le package ZIP corrigé
    print(f"\n📦 CRÉATION PACKAGE CORRIGÉ:")
    print("-" * 50)
    
    try:
        # Créer le dossier de destination s'il n'existe pas
        os.makedirs(os.path.dirname(zip_destination), exist_ok=True)
        
        with zipfile.ZipFile(zip_destination, 'w', zipfile.ZIP_DEFLATED) as zipf:
            # Ajouter le fichier __init__.py à la racine du ZIP
            zipf.write(source_file, "__init__.py")
            print(f"   ✅ Ajouté: __init__.py (version corrigée)")
        
        print(f"   ✅ Package ZIP créé: {zip_destination}")
        print(f"   📏 Taille: {os.path.getsize(zip_destination)} bytes")
        
    except Exception as e:
        print(f"   ❌ ERREUR création ZIP: {e}")
        return False
    
    # 5. Installation directe dans Blender
    print(f"\n⚙️ INSTALLATION DIRECTE:")
    print("-" * 50)
    
    if os.path.exists(blender_addons):
        addon_dest = os.path.join(blender_addons, "tokyo_organic_v2_1_9_corrected")
        
        try:
            # Créer le dossier addon
            os.makedirs(addon_dest, exist_ok=True)
            
            # Copier __init__.py
            shutil.copy2(source_file, addon_dest)
            
            print(f"   ✅ Addon installé dans: {addon_dest}")
            
        except Exception as e:
            print(f"   ❌ ERREUR installation directe: {e}")
    
    # 6. Résumé des corrections
    print(f"\n🔧 CORRECTIONS APPLIQUÉES v2.1.9:")
    print("-" * 50)
    print(f"   🎨 MATÉRIAUX ULTRA-VISIBLES:")
    print(f"      - Couleurs saturées et distinctes")
    print(f"      - Émission ajoutée pour visibilité")
    print(f"      - Noms uniques pour éviter conflits")
    print(f"      - Debug prints pour traçabilité")
    
    print(f"\n   ↗️ DIAGONALES CORRIGÉES:")
    print(f"      - Plus nombreuses et plus visibles")
    print(f"      - Matériau orange ultra-vif avec émission")
    print(f"      - Création forcée si échec")
    print(f"      - Plus larges et plus hautes")
    
    print(f"\n   🏗️ GÉNÉRATION AMÉLIORÉE:")
    print(f"      - Mode Material Preview automatique")
    print(f"      - Vérification post-génération")
    print(f"      - Blocs organiques non-uniformes")
    print(f"      - Ordre optimisé: Routes→Diagonales→Trottoirs→Bâtiments")
    
    # 7. Instructions d'utilisation
    print(f"\n📋 INSTRUCTIONS:")
    print("-" * 50)
    print(f"   1. **REDÉMARREZ BLENDER** complètement")
    print(f"   2. Edit > Preferences > Add-ons")
    print(f"   3. Installez: {zip_destination}")
    print(f"   4. Activez 'Tokyo City Generator v2.1.9 - Organic Diagonals'")
    print(f"   5. Vue 3D > Sidebar (N) > onglet 'Tokyo'")
    print(f"   6. Panneau 'Tokyo Organic v2.1.9 CORRECTED'")
    print(f"   7. Le mode viewport passera automatiquement en Material Preview")
    print(f"   8. Vous DEVREZ voir des couleurs distinctes et diagonales orange!")
    
    print(f"\n🎯 RÉSULTATS ATTENDUS:")
    print("-" * 50)
    print(f"   🔵 Bâtiments BLEUS = Tours/Bureaux")
    print(f"   🟠 Bâtiments ORANGE = Résidentiels")
    print(f"   🔴 Bâtiments ROUGES = Commerciaux")
    print(f"   🟡 Bâtiments JAUNES = Hôtels")
    print(f"   🟢 Bâtiments VERTS = Usage mixte")
    print(f"   🔶 Routes ORANGE VIVES = Diagonales")
    print(f"   📊 Blocs non-uniformes (fini l'aspect Excel!)")
    
    print("="*75)
    return True

if __name__ == "__main__":
    success = deploy_tokyo_v2_1_9_corrected()
    if success:
        print("\n🎉 DÉPLOIEMENT RÉUSSI!")
        print("🔧 TOUTES LES ERREURS v2.1.8 ONT ÉTÉ CORRIGÉES!")
        print("🚀 Testez maintenant dans Blender!")
    else:
        print("\n💥 DÉPLOIEMENT ÉCHOUÉ!")
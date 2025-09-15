#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
DÉPLOIEMENT TOKYO ORGANIC v2.1.9
=================================

Script pour déployer et installer la nouvelle version organique
avec routes diagonales courtes et blocs non uniformes.
"""

import os
import shutil
import zipfile
import sys

def deploy_tokyo_organic_v2_1_9():
    """Déployer Tokyo Organic v2.1.9"""
    
    print("\n" + "="*70)
    print("DÉPLOIEMENT TOKYO ORGANIC v2.1.9")
    print("="*70)
    
    # Chemins
    base_path = r"c:\Users\sshom\source\repos\Satsuki\Satsuki-Tools\CityGenerator_Blender\city_block_generator_6_12"
    source_dir = os.path.join(base_path, "TOKYO_ORGANIC_V2_1_9")
    
    # Destinations
    blender_addons = r"c:\Users\sshom\AppData\Roaming\Blender Foundation\Blender\4.0\scripts\addons"
    zip_destination = os.path.join(r"c:\Users\sshom\Documents\assets\Tools", "tokyo_organic_v2_1_9.zip")
    
    print(f"\n📁 CHEMINS:")
    print(f"   Source: {source_dir}")
    print(f"   Blender addons: {blender_addons}")
    print(f"   ZIP destination: {zip_destination}")
    
    # 1. Vérifier la source
    print(f"\n🔍 VÉRIFICATION SOURCE:")
    print("-" * 40)
    
    if not os.path.exists(source_dir):
        print(f"   ❌ ERREUR: Dossier source non trouvé: {source_dir}")
        return False
    
    init_file = os.path.join(source_dir, "__init__.py")
    if not os.path.exists(init_file):
        print(f"   ❌ ERREUR: __init__.py manquant dans {source_dir}")
        return False
    
    print(f"   ✅ Dossier source: OK")
    print(f"   ✅ __init__.py: {os.path.getsize(init_file)} bytes")
    
    # 2. Créer dossier de destination s'il n'existe pas
    print(f"\n📂 PRÉPARATION DESTINATIONS:")
    print("-" * 40)
    
    os.makedirs(os.path.dirname(zip_destination), exist_ok=True)
    print(f"   ✅ Dossier ZIP destination créé")
    
    if os.path.exists(blender_addons):
        print(f"   ✅ Dossier Blender addons trouvé")
    else:
        print(f"   ⚠️  Dossier Blender addons non trouvé: {blender_addons}")
        print(f"      L'installation directe ne sera pas possible")
    
    # 3. Supprimer les anciennes versions dans Blender
    print(f"\n🧹 NETTOYAGE ANCIENNES VERSIONS:")
    print("-" * 40)
    
    if os.path.exists(blender_addons):
        old_versions = []
        for item in os.listdir(blender_addons):
            if "tokyo" in item.lower() or "TOKYO" in item:
                old_versions.append(item)
        
        for old_version in old_versions:
            old_path = os.path.join(blender_addons, old_version)
            try:
                if os.path.isdir(old_path):
                    shutil.rmtree(old_path)
                    print(f"   🗑️  Supprimé: {old_version}")
                else:
                    os.remove(old_path)
                    print(f"   🗑️  Supprimé: {old_version}")
            except Exception as e:
                print(f"   ⚠️  Erreur suppression {old_version}: {e}")
    
    # 4. Créer le package ZIP
    print(f"\n📦 CRÉATION PACKAGE ZIP:")
    print("-" * 40)
    
    try:
        with zipfile.ZipFile(zip_destination, 'w', zipfile.ZIP_DEFLATED) as zipf:
            # Ajouter le fichier __init__.py à la racine du ZIP
            zipf.write(init_file, "__init__.py")
            print(f"   ✅ Ajouté: __init__.py")
        
        print(f"   ✅ Package ZIP créé: {zip_destination}")
        print(f"   📏 Taille: {os.path.getsize(zip_destination)} bytes")
        
    except Exception as e:
        print(f"   ❌ ERREUR création ZIP: {e}")
        return False
    
    # 5. Installation directe dans Blender (si possible)
    print(f"\n⚙️ INSTALLATION DIRECTE:")
    print("-" * 40)
    
    if os.path.exists(blender_addons):
        addon_dest = os.path.join(blender_addons, "tokyo_organic_v2_1_9")
        
        try:
            # Créer le dossier addon
            os.makedirs(addon_dest, exist_ok=True)
            
            # Copier __init__.py
            shutil.copy2(init_file, addon_dest)
            
            print(f"   ✅ Addon installé dans: {addon_dest}")
            
        except Exception as e:
            print(f"   ❌ ERREUR installation directe: {e}")
    
    # 6. Vérification finale
    print(f"\n✅ VÉRIFICATION FINALE:")
    print("-" * 40)
    
    if os.path.exists(zip_destination):
        print(f"   ✅ Package ZIP: {zip_destination}")
    else:
        print(f"   ❌ Package ZIP non créé")
        return False
    
    if os.path.exists(blender_addons):
        addon_final = os.path.join(blender_addons, "tokyo_organic_v2_1_9")
        if os.path.exists(addon_final):
            print(f"   ✅ Installation directe: {addon_final}")
        else:
            print(f"   ❌ Installation directe échouée")
    
    # 7. Instructions
    print(f"\n📋 INSTRUCTIONS D'UTILISATION:")
    print("-" * 40)
    print(f"   1. MÉTHODE AUTOMATIQUE (si disponible):")
    print(f"      - Redémarrez Blender")
    print(f"      - Allez dans Edit > Preferences > Add-ons")
    print(f"      - Cherchez 'Tokyo Organic' et activez-le")
    
    print(f"\n   2. MÉTHODE MANUELLE (installation ZIP):")
    print(f"      - Dans Blender: Edit > Preferences > Add-ons")
    print(f"      - Cliquez 'Install...'")
    print(f"      - Sélectionnez: {zip_destination}")
    print(f"      - Activez 'Tokyo City Generator v2.1.9 - Organic Diagonals'")
    
    print(f"\n   3. UTILISATION:")
    print(f"      - Dans la vue 3D, appuyez 'N' pour ouvrir la sidebar")
    print(f"      - Onglet 'Tokyo'")
    print(f"      - Panneau 'Tokyo Organic City v2.1.9'")
    print(f"      - Réglez les paramètres et cliquez 'Générer Ville Organique'")
    
    print(f"\n🌟 NOUVEAUTÉS v2.1.9:")
    print("-" * 40)
    print(f"   ✨ Routes diagonales COURTES entre intersections")
    print(f"   ✨ Blocs NON UNIFORMES (fini le style Excel!)")
    print(f"   ✨ Trottoirs adaptatifs aux diagonales")
    print(f"   ✨ 8 types de bâtiments colorés distinctifs")
    print(f"   ✨ Génération organique optimisée")
    print(f"   ✨ Ordre: Routes → Diagonales → Trottoirs → Bâtiments")
    
    print("="*70)
    return True

if __name__ == "__main__":
    success = deploy_tokyo_organic_v2_1_9()
    if success:
        print("\n🎉 DÉPLOIEMENT RÉUSSI!")
    else:
        print("\n💥 DÉPLOIEMENT ÉCHOUÉ!")
        sys.exit(1)
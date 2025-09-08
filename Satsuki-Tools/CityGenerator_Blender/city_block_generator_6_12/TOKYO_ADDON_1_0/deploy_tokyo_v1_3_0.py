# TOKYO ADDON DEPLOY v1.3.0 - FINAL DEPLOYMENT
# Script de déploiement final pour l'addon avec système de textures avancé

import os
import shutil
import zipfile
from datetime import datetime

def deploy_tokyo_addon_v1_3_0():
    """Déploie l'addon Tokyo v1.3.0 avec système de textures complet"""
    
    # Chemins de déploiement
    addon_source = r"c:\Users\sshom\source\repos\Satsuki\Satsuki-Tools\CityGenerator_Blender\city_block_generator_6_12\TOKYO_ADDON_1_0"
    addon_target = r"c:\Users\sshom\Documents\assets\Tools\tokyo_city_generator_1_3_0"
    blender_addons = r"C:\Users\sshom\AppData\Roaming\Blender Foundation\Blender\4.0\scripts\addons\tokyo_city_generator"
    
    print("🚀 DÉPLOIEMENT TOKYO CITY GENERATOR v1.3.0")
    print("🎨 AVEC SYSTÈME DE TEXTURES INTELLIGENT")
    print("=" * 60)
    
    # Étape 1: Nettoyer et créer le dossier de destination
    if os.path.exists(addon_target):
        print(f"🗑️ Suppression ancienne version: {addon_target}")
        shutil.rmtree(addon_target)
    
    os.makedirs(addon_target, exist_ok=True)
    print(f"📁 Dossier cible créé: {addon_target}")
    
    # Étape 2: Copier tous les fichiers essentiels
    essential_files = [
        "__init__.py",                    # Addon principal v1.3.0
        "texture_system.py",              # Système de textures intelligent
        "setup_textures.py",              # Configuration automatique
        "test_texture_system.py",         # Tests complets
        "create_demo_textures.py",        # Générateur de démo
        "deploy_texture_system.py",       # Script de déploiement
        "TEXTURE_SYSTEM_GUIDE.md",       # Guide complet
        "TOKYO_TEXTURE_SYSTEM_FINAL.md", # Récapitulatif final
        "README.md",                      # Documentation de base
        "URBAN_REVOLUTION.md"             # Documentation système urbain
    ]
    
    print("\n📋 Copie des fichiers du système:")
    copied_files = 0
    for file in essential_files:
        source_file = os.path.join(addon_source, file)
        target_file = os.path.join(addon_target, file)
        
        if os.path.exists(source_file):
            shutil.copy2(source_file, target_file)
            file_size = os.path.getsize(source_file)
            print(f"  ✅ {file} ({file_size:,} bytes)")
            copied_files += 1
        else:
            print(f"  ⚠️ {file} non trouvé")
    
    print(f"\n📊 {copied_files}/{len(essential_files)} fichiers copiés")
    
    # Étape 3: Créer le fichier de version
    version_file = os.path.join(addon_target, "VERSION.txt")
    with open(version_file, 'w', encoding='utf-8') as f:
        f.write("Tokyo City Generator v1.3.0\n")
        f.write("=================================\n\n")
        f.write(f"Date de build: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}\n")
        f.write("Nouvelles fonctionnalités v1.3.0:\n")
        f.write("• Système de textures intelligent\n")
        f.write("• Sélection automatique selon dimensions\n")
        f.write("• 20 catégories de textures spécialisées\n")
        f.write("• Mapping adaptatif par type de bâtiment\n")
        f.write("• Interface mise à jour avec contrôles\n")
        f.write("• Documentation complète incluse\n")
        f.write("• Scripts de test et démo intégrés\n\n")
        f.write("Compatibilité: Blender 4.0+\n")
        f.write("Auteur: Tokyo Urban Designer\n")
    
    print("✅ Fichier de version créé")
    
    # Étape 4: Créer l'archive ZIP de distribution
    timestamp = datetime.now().strftime('%Y%m%d_%H%M')
    zip_name = f"tokyo_city_generator_v1_3_0_texture_system_{timestamp}.zip"
    zip_path = os.path.join(os.path.dirname(addon_target), zip_name)
    
    print(f"\n📦 Création de l'archive: {zip_name}")
    total_size = 0
    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED, compresslevel=6) as zipf:
        for root, dirs, files in os.walk(addon_target):
            for file in files:
                file_path = os.path.join(root, file)
                archive_name = os.path.relpath(file_path, addon_target)
                zipf.write(file_path, archive_name)
                
                file_size = os.path.getsize(file_path)
                total_size += file_size
                print(f"  📄 {archive_name} ({file_size:,} bytes)")
    
    zip_size = os.path.getsize(zip_path)
    compression_ratio = (1 - zip_size / total_size) * 100 if total_size > 0 else 0
    print(f"\n📊 Archive créée: {zip_size:,} bytes (compression: {compression_ratio:.1f}%)")
    
    # Étape 5: Installation directe dans Blender
    print(f"\n🔧 Installation dans Blender:")
    
    if os.path.exists(os.path.dirname(blender_addons)):
        if os.path.exists(blender_addons):
            shutil.rmtree(blender_addons)
            print("  🗑️ Ancienne version supprimée de Blender")
        
        shutil.copytree(addon_target, blender_addons)
        print(f"  ✅ Addon installé: {blender_addons}")
        
        # Vérifier l'installation
        init_file = os.path.join(blender_addons, "__init__.py")
        if os.path.exists(init_file):
            print("  ✅ Fichier principal vérifié")
        else:
            print("  ❌ Erreur: fichier principal manquant")
    else:
        print(f"  ⚠️ Dossier Blender non trouvé: {os.path.dirname(blender_addons)}")
        print("  📝 Installation manuelle requise")
    
    # Étape 6: Créer le guide d'installation rapide
    quick_install = os.path.join(addon_target, "INSTALLATION_RAPIDE.md")
    with open(quick_install, 'w', encoding='utf-8') as f:
        f.write("# 🚀 TOKYO CITY GENERATOR v1.3.0 - INSTALLATION RAPIDE\n\n")
        f.write("## ✨ NOUVEAU: SYSTÈME DE TEXTURES INTELLIGENT!\n\n")
        f.write("### 🎯 Installation en 3 étapes:\n\n")
        f.write("#### 1. 📦 Installer l'addon\n")
        f.write("- Ouvrir Blender\n")
        f.write("- Edit > Preferences > Add-ons\n")
        f.write("- Install > Sélectionner `__init__.py`\n")
        f.write("- Activer 'Tokyo City Generator 1.3.0'\n\n")
        f.write("#### 2. 🗂️ Configurer les textures (optionnel)\n")
        f.write("- Dans Blender Text Editor:\n")
        f.write("  ```python\n")
        f.write("  exec(open('setup_textures.py').read())\n")
        f.write("  ```\n")
        f.write("- Ajouter vos textures dans:\n")
        f.write("  `C:/Users/sshom/Documents/Assets/Textures/Tokyo_Buildings/`\n\n")
        f.write("#### 3. 🏙️ Générer votre ville\n")
        f.write("- Onglet 'Tokyo' (sidebar N)\n")
        f.write("- Cocher 'Advanced Textures'\n")
        f.write("- Cliquer 'Generate Tokyo District'\n")
        f.write("- Admirer les textures automatiques!\n\n")
        f.write("### 🎨 Nouveautés v1.3.0:\n")
        f.write("- ✅ **Textures intelligentes** selon hauteur/largeur\n")
        f.write("- ✅ **5 catégories automatiques** (gratte-ciels, commercial, etc.)\n")
        f.write("- ✅ **20 dossiers spécialisés** pour vos textures\n")
        f.write("- ✅ **Mapping adaptatif** par type de bâtiment\n")
        f.write("- ✅ **Fallback sécurisé** sans erreurs\n\n")
        f.write("📚 Voir `TEXTURE_SYSTEM_GUIDE.md` pour plus de détails!\n")
    
    print("✅ Guide d'installation rapide créé")
    
    # Étape 7: Créer le changelog
    changelog = os.path.join(addon_target, "CHANGELOG.md")
    with open(changelog, 'w', encoding='utf-8') as f:
        f.write("# 📝 TOKYO CITY GENERATOR - CHANGELOG\n\n")
        f.write("## 🎨 Version 1.3.0 (7 septembre 2025)\n")
        f.write("### 🆕 NOUVEAU: Système de textures intelligent\n")
        f.write("- ✅ Sélection automatique selon hauteur/largeur des bâtiments\n")
        f.write("- ✅ 5 catégories intelligentes: gratte-ciels, commercial, midrise, résidentiel, lowrise\n")
        f.write("- ✅ 20 dossiers spécialisés pour organisation des textures\n")
        f.write("- ✅ Mapping adaptatif par type (étirement vertical pour gratte-ciels, etc.)\n")
        f.write("- ✅ Support formats: .jpg, .png, .exr, .hdr, .tiff, .bmp\n")
        f.write("- ✅ Interface mise à jour avec option 'Advanced Textures'\n")
        f.write("- ✅ Fallback sécurisé vers matériaux procéduraux\n")
        f.write("- ✅ Scripts de test et démo inclus\n")
        f.write("- ✅ Documentation complète avec guides détaillés\n\n")
        f.write("## 🏗️ Version 1.0.8 (précédente)\n")
        f.write("- ✅ Système urbain révolutionnaire (blocs-trottoirs + circulation)\n")
        f.write("- ✅ 5 types de rues intelligentes\n")
        f.write("- ✅ 3 zones distinctes (business, commercial, résidentiel)\n")
        f.write("- ✅ Variation organique des rues\n")
        f.write("- ✅ Contrôle de densité\n")
        f.write("- ✅ Matériaux de base différenciés\n")
    
    print("✅ Changelog créé")
    
    # Étape 8: Rapport final
    print("\n" + "=" * 60)
    print("🎉 DÉPLOIEMENT TOKYO v1.3.0 TERMINÉ!")
    print("=" * 60)
    
    print(f"📁 Dossier source: {addon_source}")
    print(f"📁 Dossier cible: {addon_target}")
    print(f"📦 Archive ZIP: {zip_path}")
    print(f"🔧 Blender: {'✅ Installé' if os.path.exists(blender_addons) else '⚠️ Manuel'}")
    
    print(f"\n📊 Statistiques:")
    print(f"  📄 Fichiers copiés: {copied_files}")
    print(f"  💾 Taille totale: {total_size:,} bytes")
    print(f"  🗜️ Taille ZIP: {zip_size:,} bytes")
    print(f"  📈 Compression: {compression_ratio:.1f}%")
    
    print(f"\n🎯 NOUVEAUTÉS v1.3.0:")
    print("  🎨 Système de textures intelligent")
    print("  📐 Sélection selon dimensions")
    print("  🗂️ 20 catégories spécialisées")
    print("  🎛️ Interface mise à jour")
    print("  📚 Documentation complète")
    print("  🧪 Scripts de test inclus")
    
    print(f"\n🚀 L'addon est prêt à être utilisé!")
    print("📝 Voir 'INSTALLATION_RAPIDE.md' pour commencer")
    
    return {
        'target_dir': addon_target,
        'zip_file': zip_path,
        'blender_installed': os.path.exists(blender_addons),
        'files_copied': copied_files,
        'total_size': total_size,
        'zip_size': zip_size
    }

if __name__ == "__main__":
    try:
        result = deploy_tokyo_addon_v1_3_0()
        print(f"\n✨ SUCCÈS! Addon Tokyo v1.3.0 déployé avec système de textures")
        print(f"📍 Emplacement: {result['target_dir']}")
        print(f"📦 Archive: {result['zip_file']}")
        
        if result['blender_installed']:
            print("🎮 Redémarrez Blender pour utiliser la nouvelle version!")
        else:
            print("📝 Installation manuelle requise dans Blender")
            
    except Exception as e:
        print(f"❌ Erreur lors du déploiement: {e}")
        import traceback
        traceback.print_exc()

# TOKYO ADDON DEPLOY AVEC SYSTÈME TEXTURES v1.2.0
# Script de déploiement pour l'addon avec le nouveau système de textures

import os
import shutil
import zipfile
from datetime import datetime

def deploy_tokyo_addon_with_textures():
    """Déploie l'addon Tokyo avec le système de textures"""
    
    # Chemins
    addon_source = r"c:\Users\sshom\source\repos\Satsuki\Satsuki-Tools\CityGenerator_Blender\city_block_generator_6_12\TOKYO_ADDON_1_0"
    addon_target = r"c:\Users\sshom\Documents\assets\Tools\tokyo_city_generator_1_2_0"
    blender_addons = r"C:\Users\sshom\AppData\Roaming\Blender Foundation\Blender\4.0\scripts\addons\tokyo_city_generator"
    
    print("🚀 DÉPLOIEMENT TOKYO ADDON v1.2.0 AVEC SYSTÈME TEXTURES")
    print("=" * 60)
    
    # Étape 1: Créer le dossier de destination
    if os.path.exists(addon_target):
        print(f"🗑️ Suppression ancien dossier: {addon_target}")
        shutil.rmtree(addon_target)
    
    os.makedirs(addon_target, exist_ok=True)
    print(f"📁 Dossier de destination créé: {addon_target}")
    
    # Étape 2: Copier les fichiers essentiels
    essential_files = [
        "__init__.py",           # Addon principal avec textures
        "texture_system.py",     # Système de textures
        "setup_textures.py",     # Script de setup
        "test_texture_system.py", # Script de test
        "create_demo_textures.py", # Créateur de textures démo
        "TEXTURE_SYSTEM_GUIDE.md", # Guide complet
        "README.md",            # Documentation existante
        "URBAN_REVOLUTION.md"   # Documentation existante
    ]
    
    print("\n📋 Copie des fichiers essentiels:")
    for file in essential_files:
        source_file = os.path.join(addon_source, file)
        target_file = os.path.join(addon_target, file)
        
        if os.path.exists(source_file):
            shutil.copy2(source_file, target_file)
            print(f"  ✅ {file}")
        else:
            print(f"  ⚠️ {file} non trouvé")
    
    # Étape 3: Mettre à jour le bl_info avec version textures
    init_file = os.path.join(addon_target, "__init__.py")
    if os.path.exists(init_file):
        with open(init_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Mettre à jour la version
        content = content.replace(
            '"name": "Tokyo City Generator 1.0.8"',
            '"name": "Tokyo City Generator 1.2.0 TEXTURE SYSTEM"'
        )
        content = content.replace(
            '"version": (1, 0, 8)',
            '"version": (1, 2, 0)'
        )
        content = content.replace(
            '"description": "Generate realistic Tokyo-style districts with clean geometry and proper proportions"',
            '"description": "Generate realistic Tokyo-style districts with INTELLIGENT TEXTURE SYSTEM based on building dimensions"'
        )
        
        with open(init_file, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print("  ✅ Version mise à jour dans __init__.py")
    
    # Étape 4: Créer un ZIP pour distribution
    zip_name = f"tokyo_city_generator_1_2_0_texture_system_{datetime.now().strftime('%Y%m%d')}.zip"
    zip_path = os.path.join(os.path.dirname(addon_target), zip_name)
    
    print(f"\n📦 Création du ZIP: {zip_name}")
    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(addon_target):
            for file in files:
                file_path = os.path.join(root, file)
                archive_name = os.path.relpath(file_path, addon_target)
                zipf.write(file_path, archive_name)
                print(f"  📄 {archive_name}")
    
    # Étape 5: Copier vers Blender si demandé
    if os.path.exists(os.path.dirname(blender_addons)):
        print(f"\n🔄 Installation directe dans Blender:")
        print(f"   Source: {addon_target}")
        print(f"   Cible: {blender_addons}")
        
        if os.path.exists(blender_addons):
            shutil.rmtree(blender_addons)
            print("  🗑️ Ancien addon supprimé")
        
        shutil.copytree(addon_target, blender_addons)
        print("  ✅ Addon installé dans Blender")
    else:
        print(f"\n⚠️ Dossier Blender non trouvé: {blender_addons}")
    
    # Étape 6: Créer le guide d'installation
    install_guide = os.path.join(addon_target, "INSTALLATION_TEXTURE_SYSTEM.md")
    with open(install_guide, 'w', encoding='utf-8') as f:
        f.write("# 🎨 TOKYO CITY GENERATOR v1.2.0 - INSTALLATION\n\n")
        f.write("## 🚀 NOUVEAU SYSTÈME DE TEXTURES INTELLIGENT!\n\n")
        f.write("### 📦 Installation:\n")
        f.write("1. **Fermez Blender** complètement\n")
        f.write("2. **Extraire** ce dossier vers un lieu sûr\n")
        f.write("3. **Installer** l'addon dans Blender:\n")
        f.write("   - Edit > Preferences > Add-ons\n")
        f.write("   - Install > Sélectionner `__init__.py`\n")
        f.write("   - Activer 'Tokyo City Generator 1.2.0'\n\n")
        f.write("### 🎨 Configuration des textures:\n")
        f.write("1. **Exécuter** dans Blender Text Editor:\n")
        f.write("   ```python\n")
        f.write("   exec(open('setup_textures.py').read())\n")
        f.write("   ```\n")
        f.write("2. **Ajouter vos textures** dans:\n")
        f.write("   `C:/Users/sshom/Documents/Assets/Textures/Tokyo_Buildings/`\n")
        f.write("3. **Activer 'Advanced Textures'** dans l'addon\n\n")
        f.write("### 🧪 Test:\n")
        f.write("1. Onglet 'Tokyo' (sidebar N)\n")
        f.write("2. Cocher 'Advanced Textures'\n")
        f.write("3. Generate Tokyo District\n")
        f.write("4. Admirer les textures automatiques!\n\n")
        f.write("📚 Voir `TEXTURE_SYSTEM_GUIDE.md` pour plus de détails.\n")
    
    print(f"  ✅ Guide d'installation créé")
    
    # Résumé final
    print("\n" + "=" * 60)
    print("✅ DÉPLOIEMENT TERMINÉ!")
    print("=" * 60)
    print(f"📁 Dossier: {addon_target}")
    print(f"📦 Archive: {zip_path}")
    print(f"🔧 Blender: {'✅ Installé' if os.path.exists(blender_addons) else '⚠️ Manuel'}")
    print("\n🎯 NOUVEAUTÉS v1.2.0:")
    print("  🎨 Système de textures intelligent")
    print("  📐 Sélection selon hauteur/largeur")
    print("  🗂️ 20 catégories de textures")
    print("  🎛️ Interface mise à jour")
    print("  🧪 Scripts de test inclus")
    print("\n🚀 L'addon est prêt à être utilisé!")
    
    return addon_target, zip_path

if __name__ == "__main__":
    try:
        target, zip_file = deploy_tokyo_addon_with_textures()
        print(f"\n🎉 Succès! Addon déployé avec système de textures")
        print(f"📍 Emplacement: {target}")
        print(f"📦 Archive: {zip_file}")
    except Exception as e:
        print(f"❌ Erreur lors du déploiement: {e}")
        import traceback
        traceback.print_exc()

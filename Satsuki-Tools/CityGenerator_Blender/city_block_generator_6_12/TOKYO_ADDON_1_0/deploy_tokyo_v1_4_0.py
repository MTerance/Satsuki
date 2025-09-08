# DÉPLOIEMENT TOKYO CITY GENERATOR v1.4.0
# Script de déploiement automatique avec version incrémentée

import os
import shutil
import zipfile
import time
from datetime import datetime

def deploy_tokyo_addon_v1_4_0():
    """Déploie Tokyo City Generator v1.4.0 avec interface textures complète"""
    
    print("🚀 DÉPLOIEMENT TOKYO CITY GENERATOR v1.4.0")
    print("=" * 55)
    print("🎯 NOUVELLES FONCTIONNALITÉS v1.4.0:")
    print("   ✅ Interface 'Texture Base Path' visible")
    print("   ✅ Configuration chemin textures dans l'interface")
    print("   ✅ Chemin par défaut configuré automatiquement")
    print("   ✅ Numéro de version corrigé dans l'interface")
    print("=" * 55)
    
    # Chemins
    source_dir = r"c:\Users\sshom\source\repos\Satsuki\Satsuki-Tools\CityGenerator_Blender\city_block_generator_6_12\TOKYO_ADDON_1_0"
    target_base = r"c:\Users\sshom\Documents\assets\Tools"
    target_dir = os.path.join(target_base, "tokyo_city_generator_1_4_0")
    blender_addons = r"C:\Users\sshom\AppData\Roaming\Blender Foundation\Blender\4.0\scripts\addons"
    blender_target = os.path.join(blender_addons, "tokyo_city_generator")
    
    print(f"📁 Source: {source_dir}")
    print(f"🎯 Target: {target_dir}")
    print(f"🔧 Blender: {blender_target}")
    
    # Étape 1: Nettoyer et créer le dossier target
    print(f"\n🧹 1. PRÉPARATION")
    
    if os.path.exists(target_dir):
        print(f"   🗑️ Suppression ancien dossier...")
        shutil.rmtree(target_dir, ignore_errors=True)
        time.sleep(0.5)
    
    os.makedirs(target_dir, exist_ok=True)
    print(f"   ✅ Dossier target créé: {target_dir}")
    
    # Étape 2: Copier les fichiers essentiels
    print(f"\n📦 2. COPIE DES FICHIERS v1.4.0")
    
    essential_files = [
        "__init__.py",           # Fichier principal avec interface v1.4.0
        "texture_system.py",     # Système de textures intelligent
        "setup_textures.py",     # Setup automatique des dossiers
        "README.md",             # Documentation
        "CHANGELOG.md",          # Journal des modifications
        "INSTALLATION_RAPIDE.md"  # Guide d'installation
    ]
    
    files_copied = 0
    total_size = 0
    
    for filename in essential_files:
        source_file = os.path.join(source_dir, filename)
        target_file = os.path.join(target_dir, filename)
        
        if os.path.exists(source_file):
            shutil.copy2(source_file, target_file)
            size = os.path.getsize(target_file)
            total_size += size
            files_copied += 1
            print(f"   ✅ {filename} ({size:,} bytes)")
        else:
            print(f"   ⚠️ {filename} - fichier manquant")
    
    # Étape 3: Créer la documentation v1.4.0
    print(f"\n📋 3. DOCUMENTATION v1.4.0")
    
    # README spécifique v1.4.0
    readme_v1_4_0 = f"""# Tokyo City Generator v1.4.0 TEXTURE SYSTEM

## 🆕 NOUVEAUTÉS v1.4.0 (vs v1.3.0)

### ✅ CORRECTIONS INTERFACE
- **Interface 'Texture Base Path' maintenant VISIBLE**
- **Numéro de version corrigé: 1.4.0** (plus 1.0.8)
- **Configuration chemin textures directement dans Blender**
- **Chemin par défaut automatique**

### 🎯 ACCÈS AU SYSTÈME DE TEXTURES

1. **📐 Vue 3D > Sidebar (N) > Onglet Tokyo**
2. **✅ Cochez "Advanced Textures"**
3. **📁 "Texture Path" apparaît automatiquement**
4. **🎯 Configurez le chemin ou gardez celui par défaut**

### 🎨 UTILISATION

```
┌─────────────────────────────────┐
│ 🗾 Tokyo City Generator 1.4.0   │
├─────────────────────────────────┤
│ District Size:    [3      ]     │
│ Block Density:    [0.8    ]     │
│ Building Variety: [Mixed  ▼]    │
│ Organic Streets:  [0.2    ]     │
│                                 │
│ ✅ Advanced Textures             │ ← SYSTÈME INTELLIGENT
│ 📁 Texture Path: [Browse...]    │ ← MAINTENANT VISIBLE!
│                                 │
│ [🚀 Generate Tokyo District]   │
└─────────────────────────────────┘
```

## 🏗️ INSTALLATION

1. **💾 Téléchargez le zip:** `tokyo_city_generator_1_4_0.zip`
2. **⚙️ Blender > Edit > Preferences > Add-ons**
3. **📦 Install from Disk** → Sélectionnez le zip
4. **✅ Activez "Tokyo City Generator 1.4.0 TEXTURE SYSTEM"**
5. **🎯 Vue 3D > N > Tokyo** → Interface complète disponible!

## 🎨 SYSTÈME INTELLIGENT

Le système analyse automatiquement chaque bâtiment:
- **📏 Hauteur & Largeur** → Catégorie automatique
- **🎲 Sélection aléatoire** → Variété naturelle
- **🎭 Matériau avancé** → Rendu réaliste

### Categories:
- **🏢 Gratte-ciels** (>15 étages) → Verre, métal moderne
- **🏬 Commercial** (8-15 étages) → Bureaux, centres
- **🏘️ Moyenne** (4-8 étages) → Urbain standard
- **🏠 Résidentiel** (2-4 étages) → Chaleureux
- **🏪 Petits** (1-2 étages) → Boutiques locales

## 📁 STRUCTURE TEXTURES

Chemin par défaut: `C:\\Users\\sshom\\Documents\\assets\\Tools\\tokyo_textures`

```
📁 tokyo_textures/
├── 🏢 skyscrapers/    (5 sous-dossiers)
├── 🏬 commercial/     (5 sous-dossiers)
├── 🏘️ midrise/        (5 sous-dossiers)
├── 🏠 residential/    (5 sous-dossiers)
└── 🏪 lowrise/       (5 sous-dossiers)
```

Chaque catégorie: facade/, roof/, details/, materials/, special/

## 🔧 DÉPANNAGE

### Interface "Texture Path" invisible?
- Vérifiez version 1.4.0 dans Add-ons
- Redémarrez Blender complètement
- Cochez d'abord "Advanced Textures"

### Textures non appliquées?
- Vérifiez le chemin configuré
- Ajoutez des images dans les dossiers
- Format supporté: .jpg, .png, .tga, .bmp

## 🎯 VERSION

- **Version:** 1.4.0 TEXTURE SYSTEM
- **Date:** {datetime.now().strftime('%Y-%m-%d')}
- **Blender:** 4.0+
- **Python:** 3.11+

🎉 **v1.4.0 - Interface Texture Path enfin visible!** ✨
"""
    
    readme_path = os.path.join(target_dir, "README_v1_4_0.md")
    with open(readme_path, 'w', encoding='utf-8') as f:
        f.write(readme_v1_4_0)
    
    print(f"   ✅ README v1.4.0 créé")
    
    # Changelog v1.4.0
    changelog_v1_4_0 = f"""# CHANGELOG - Tokyo City Generator

## v1.4.0 - {datetime.now().strftime('%Y-%m-%d')} - INTERFACE TEXTURE PATH FIXÉE

### 🆕 NOUVELLES FONCTIONNALITÉS
- ✅ **Interface "Texture Base Path" maintenant VISIBLE**
- ✅ **Configuration chemin textures dans l'interface Blender**
- ✅ **Chemin par défaut configuré automatiquement**
- ✅ **Fonction create_advanced_building_material() mise à jour**

### 🔧 CORRECTIONS
- ✅ **Numéro de version corrigé: 1.4.0** (plus 1.0.8 dans l'interface)
- ✅ **Propriété tokyo_texture_base_path ajoutée**
- ✅ **Interface dynamique: Texture Path visible quand Advanced Textures activé**
- ✅ **Paramètre texture_base_path passé au système de textures**

### 📋 DÉTAILS TECHNIQUES
- Ajout propriété `bpy.types.Scene.tokyo_texture_base_path`
- Modification `create_advanced_building_material()` pour accepter chemin custom
- Interface conditionnelle: Texture Path apparaît quand Advanced Textures = ON
- Mise à jour bl_label panneau: "Tokyo City Generator 1.4.0"

### 🎯 MIGRATION depuis v1.3.0
- Supprimez v1.3.0 de Blender Add-ons
- Installez v1.4.0
- L'option "Texture Path" apparaîtra automatiquement

---

## v1.3.0 - 2025-09-07 - SYSTÈME DE TEXTURES INTELLIGENT
### 🆕 NOUVELLES FONCTIONNALITÉS
- ✅ Système de textures intelligent basé sur dimensions
- ✅ 5 catégories automatiques de bâtiments
- ✅ 20 dossiers de textures organisés
- ✅ Sélection aléatoire pour variété naturelle
- ✅ Matériaux avancés avec propriétés réalistes

### 🔧 AMÉLIORATIONS
- ✅ Analyse automatique hauteur/largeur
- ✅ Classification intelligente des bâtiments
- ✅ Support textures multiples par catégorie
- ✅ Fallback vers système basique si textures indisponibles

---

## v1.0.8 - Base
### 📋 FONCTIONNALITÉS DE BASE
- ✅ Génération districts Tokyo basique
- ✅ Zones mixtes (business, commercial, résidentiel)
- ✅ Routes organiques
- ✅ Densité et variété configurables
"""
    
    changelog_path = os.path.join(target_dir, "CHANGELOG_v1_4_0.md")
    with open(changelog_path, 'w', encoding='utf-8') as f:
        f.write(changelog_v1_4_0)
    
    print(f"   ✅ CHANGELOG v1.4.0 créé")
    
    # Étape 4: Créer le ZIP de distribution
    print(f"\n📦 4. CRÉATION ZIP DISTRIBUTION")
    
    zip_name = f"tokyo_city_generator_1_4_0.zip"
    zip_path = os.path.join(target_base, zip_name)
    
    if os.path.exists(zip_path):
        os.remove(zip_path)
    
    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(target_dir):
            for file in files:
                file_path = os.path.join(root, file)
                arcname = os.path.relpath(file_path, target_dir)
                zipf.write(file_path, f"tokyo_city_generator/{arcname}")
    
    zip_size = os.path.getsize(zip_path)
    compression_ratio = (1 - zip_size / total_size) * 100 if total_size > 0 else 0
    
    print(f"   ✅ ZIP créé: {zip_path}")
    print(f"   📊 Taille: {zip_size:,} bytes (compression: {compression_ratio:.1f}%)")
    
    # Étape 5: Installation dans Blender
    print(f"\n🔧 5. INSTALLATION BLENDER")
    
    # Supprimer l'ancienne version
    if os.path.exists(blender_target):
        print(f"   🗑️ Suppression ancienne version...")
        shutil.rmtree(blender_target, ignore_errors=True)
        time.sleep(0.5)
    
    # Copier la nouvelle version
    shutil.copytree(target_dir, blender_target)
    print(f"   ✅ Installation: {blender_target}")
    
    # Vérification installation
    init_file = os.path.join(blender_target, "__init__.py")
    if os.path.exists(init_file):
        with open(init_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        if '"version": (1, 4, 0)' in content:
            print(f"   ✅ Version 1.4.0 confirmée")
        
        if "tokyo_texture_base_path" in content:
            print(f"   ✅ Propriété Texture Base Path détectée")
        
        if "Tokyo City Generator 1.4.0" in content:
            print(f"   ✅ Interface 1.4.0 confirmée")
    
    # Étape 6: Résumé final
    print(f"\n✅ DÉPLOIEMENT v1.4.0 TERMINÉ!")
    print("=" * 55)
    print(f"📊 STATISTIQUES:")
    print(f"   📁 Fichiers copiés: {files_copied}")
    print(f"   💾 Taille totale: {total_size:,} bytes")
    print(f"   📦 ZIP: {zip_size:,} bytes")
    print(f"   🗜️ Compression: {compression_ratio:.1f}%")
    
    print(f"\n🎯 NOUVEAUTÉS v1.4.0:")
    print(f"   ✅ Interface 'Texture Base Path' VISIBLE")
    print(f"   ✅ Numéro version corrigé: 1.4.0")
    print(f"   ✅ Configuration chemin textures dans Blender")
    print(f"   ✅ Chemin par défaut automatique")
    
    print(f"\n🚀 INSTRUCTIONS BLENDER:")
    print(f"   1. 🔄 Redémarrez Blender")
    print(f"   2. ⚙️ Edit > Preferences > Add-ons")
    print(f"   3. 🔍 Cherchez 'Tokyo City Generator 1.4.0'")
    print(f"   4. ✅ Activez l'addon")
    print(f"   5. 📐 Vue 3D > N > Tokyo")
    print(f"   6. ✅ Advanced Textures → 'Texture Path' apparaît!")
    
    print(f"\n📁 FICHIERS DISPONIBLES:")
    print(f"   📦 Distribution: {zip_path}")
    print(f"   🔧 Blender: {blender_target}")
    print(f"   📋 Documentation: {target_dir}")
    
    return {
        "success": True,
        "version": "1.4.0",
        "files_copied": files_copied,
        "total_size": total_size,
        "zip_path": zip_path,
        "blender_path": blender_target
    }

if __name__ == "__main__":
    try:
        result = deploy_tokyo_addon_v1_4_0()
        
        if result["success"]:
            print(f"\n🎉 SUCCESS! Tokyo v1.4.0 déployé avec succès!")
            print(f"🎨 L'interface 'Texture Base Path' est maintenant visible!")
        else:
            print(f"\n❌ ÉCHEC du déploiement")
            
    except Exception as e:
        print(f"❌ Erreur critique: {e}")
        import traceback
        traceback.print_exc()

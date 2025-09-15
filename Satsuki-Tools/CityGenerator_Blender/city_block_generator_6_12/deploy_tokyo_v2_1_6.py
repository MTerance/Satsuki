#!/usr/bin/env python3
"""
DÉPLOIEMENT TOKYO CITY GENERATOR V2.1.6
Corrections majeures: trottoirs aux intersections + bâtiments collés aux trottoirs
"""

import os
import shutil
import zipfile
from datetime import datetime

def create_tokyo_v2_1_6_package():
    """Créer le package Tokyo City Generator v2.1.6 avec corrections des trottoirs"""
    
    print("=" * 60)
    print("CRÉATION TOKYO CITY GENERATOR V2.1.6")
    print("CORRECTIONS MAJEURES DES TROTTOIRS")
    print("=" * 60)
    
    # Définir les chemins
    source_dir = "TOKYO_SIMPLE_V2_1"
    assets_dir = r"c:\Users\sshom\Documents\assets\Tools"
    package_name = "tokyo_fixed_sidewalks_v2_1_6"
    
    # Créer le dossier de destination
    dest_dir = os.path.join(assets_dir, package_name)
    
    if os.path.exists(dest_dir):
        print(f"⚠️  Suppression de l'ancien dossier: {dest_dir}")
        shutil.rmtree(dest_dir)
    
    print(f"📁 Création du dossier: {dest_dir}")
    os.makedirs(dest_dir, exist_ok=True)
    
    # Copier les fichiers
    files_to_copy = [
        "__init__.py",
    ]
    
    print("📋 Copie des fichiers:")
    for file in files_to_copy:
        source_path = os.path.join(source_dir, file)
        dest_path = os.path.join(dest_dir, file)
        
        if os.path.exists(source_path):
            shutil.copy2(source_path, dest_path)
            print(f"  ✅ {file}")
        else:
            print(f"  ❌ MANQUANT: {file}")
    
    # Créer le fichier README pour cette version
    readme_content = """# TOKYO CITY GENERATOR V2.1.6 - TROTTOIRS FIXES

## 🔧 CORRECTIONS MAJEURES V2.1.6

### ✅ PROBLÈMES RÉSOLUS
1. **TROTTOIRS AUX INTERSECTIONS** - Plus d'espaces vides aux coins des carrefours
2. **BÂTIMENTS COLLÉS AUX TROTTOIRS** - Suppression des espaces non modélisés
3. **8 TYPES DE BÂTIMENTS** - Variété architecturale maintenue

### 🏗️ NOUVELLES FONCTIONNALITÉS
- **Trottoirs aux coins** - Segments de trottoir automatiques aux intersections
- **Espacement optimal** - Bâtiments à 0.8m des trottoirs (au lieu de 2.5m)
- **Continuité urbaine** - Plus d'espaces vides dans la ville

## 🏢 TYPES DE BÂTIMENTS (V2.1.5+)

### 🏙️ CENTRE VILLE
- **TOWERS** (Tours) - Verre et métal, éclairage moderne
- **OFFICE** (Bureaux) - Verre teinté, fenêtres éclairées

### 🏘️ ZONES MIXTES  
- **HOTEL** (Hôtels) - Matériaux luxueux, éclairage élégant
- **MIXED_USE** (Usage mixte) - Matériaux neutres polyvalents
- **COMMERCIAL** (Commerces) - Couleurs vives, signalétique

### 🏠 PÉRIPHÉRIE
- **RESIDENTIAL** (Résidentiel) - Béton et brique, couleurs chaudes
- **WAREHOUSE** (Entrepôts) - Métallique industriel
- **SCHOOL** (Écoles) - Couleurs institutionnelles

## ⚙️ PARAMÈTRES SIMPLES
1. **Grid Size** (3-15) - Taille de la grille
2. **Building Density** (0.3-0.9) - Densité des bâtiments  
3. **Road Width** (2-8) - Largeur des routes
4. **Max Height** (15-80) - Hauteur maximale

## 🔧 INSTALLATION
1. Ouvrir Blender (4.0+)
2. Edit > Preferences > Add-ons
3. Install from File > tokyo_fixed_sidewalks_v2_1_6.zip
4. Activer "Tokyo City Generator"
5. Panneau dans 3D Viewport > Sidebar (N) > CityGen

## 🎯 AMÉLIORATIONS TECHNIQUES
- **Algorithme de coins** - Génération automatique des trottoirs aux intersections
- **Espacement optimisé** - Réduction de l'espace bâtiment-trottoir de 2.5m à 0.8m
- **Continuité urbaine** - Suppression des espaces vides problématiques
- **Matériaux réalistes** - Système de matériaux par type de bâtiment maintenu

## 📸 AVANT/APRÈS
- **AVANT**: Espaces vides aux carrefours, bâtiments flottants
- **APRÈS**: Trottoirs continus, bâtiments collés aux trottoirs

Version: 2.1.6 | Créé le: {}
Compatible: Blender 4.0+
Corrections: Trottoirs + Espacement bâtiments
""".format(datetime.now().strftime("%d/%m/%Y"))
    
    readme_path = os.path.join(dest_dir, "README.md")
    with open(readme_path, 'w', encoding='utf-8') as f:
        f.write(readme_content)
    print(f"  ✅ README.md créé")
    
    # Créer l'archive ZIP
    zip_path = os.path.join(assets_dir, f"{package_name}.zip")
    print(f"📦 Création de l'archive: {zip_path}")
    
    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(dest_dir):
            for file in files:
                file_path = os.path.join(root, file)
                arc_name = os.path.relpath(file_path, dest_dir)
                zipf.write(file_path, arc_name)
                print(f"  📄 Ajouté: {arc_name}")
    
    print("\n" + "=" * 60)
    print("✅ TOKYO CITY GENERATOR V2.1.6 CRÉÉ AVEC SUCCÈS!")
    print("=" * 60)
    print(f"📍 Dossier: {dest_dir}")
    print(f"📦 Archive: {zip_path}")
    print("\n🔧 CORRECTIONS V2.1.6:")
    print("  ✅ Trottoirs automatiques aux intersections")
    print("  ✅ Bâtiments collés aux trottoirs (0.8m au lieu de 2.5m)")
    print("  ✅ Suppression des espaces vides")
    print("  ✅ Continuité urbaine améliorée")
    print("\n🏗️ FONCTIONNALITÉS MAINTENUES:")
    print("  • 8 types de bâtiments variés")
    print("  • Système de zonage urbain intelligent")
    print("  • Matériaux réalistes par type")
    print("  • Routes et diagonales optimisées")
    print("\n🎯 Prêt pour test dans Blender!")
    
    return zip_path

if __name__ == "__main__":
    try:
        package_path = create_tokyo_v2_1_6_package()
        print(f"\n🎉 Package créé: {package_path}")
    except Exception as e:
        print(f"\n❌ ERREUR: {e}")
        input("Appuyez sur Entrée pour continuer...")
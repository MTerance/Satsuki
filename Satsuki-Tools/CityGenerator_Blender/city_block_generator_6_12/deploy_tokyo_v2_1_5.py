#!/usr/bin/env python3
"""
DÉPLOIEMENT TOKYO CITY GENERATOR V2.1.5
Nouvelle version avec 8 types de bâtiments et matériaux réalistes
"""

import os
import shutil
import zipfile
from datetime import datetime

def create_tokyo_v2_1_5_package():
    """Créer le package Tokyo City Generator v2.1.5 avec types de bâtiments"""
    
    print("=" * 60)
    print("CRÉATION TOKYO CITY GENERATOR V2.1.5")
    print("Nouvelle version avec 8 types de bâtiments")
    print("=" * 60)
    
    # Définir les chemins
    source_dir = "TOKYO_SIMPLE_V2_1"
    assets_dir = r"c:\Users\sshom\Documents\assets\Tools"
    package_name = "tokyo_building_variety_v2_1_5"
    
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
    readme_content = """# TOKYO CITY GENERATOR V2.1.5 - BUILDING VARIETY

## 🏗️ NOUVEAUTÉS V2.1.5
- **8 TYPES DE BÂTIMENTS DIFFÉRENTS** avec matériaux réalistes
- **SYSTÈME DE ZONAGE URBAIN** intelligent
- **MATÉRIAUX SPÉCIALISÉS** par type de bâtiment
- **FORMES VARIÉES** selon l'usage du bâtiment

## 🏢 TYPES DE BÂTIMENTS DISPONIBLES

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

## 🎯 LOGIQUE DE PLACEMENT
- **Centre**: Tours et bureaux (buildings modernes)
- **Intermédiaire**: Hôtels, commerces, usage mixte
- **Périphérie**: Résidentiel, entrepôts, écoles

## 🔧 INSTALLATION
1. Ouvrir Blender (4.0+)
2. Edit > Preferences > Add-ons
3. Install from File > tokyo_building_variety_v2_1_5.zip
4. Activer "Tokyo City Generator"
5. Panneau dans 3D Viewport > Sidebar (N) > CityGen

## 🎨 MATÉRIAUX AUTOMATIQUES
- **Verre** pour bureaux et tours
- **Béton/Brique** pour résidentiel
- **Métal** pour industriel
- **Couleurs vives** pour commercial
- **Éclairage automatique** selon le type

Version: 2.1.5 | Créé le: {}
Compatible: Blender 4.0+
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
    print("✅ TOKYO CITY GENERATOR V2.1.5 CRÉÉ AVEC SUCCÈS!")
    print("=" * 60)
    print(f"📍 Dossier: {dest_dir}")
    print(f"📦 Archive: {zip_path}")
    print("\n🎯 NOUVEAUTÉS V2.1.5:")
    print("  • 8 types de bâtiments avec matériaux réalistes")
    print("  • Système de zonage urbain intelligent")
    print("  • Tours et bureaux au centre-ville")
    print("  • Résidentiel et industriel en périphérie")
    print("  • Matériaux automatiques par type")
    print("  • Éclairage dynamique des fenêtres")
    print("\n🔧 Prêt pour installation dans Blender!")
    
    return zip_path

if __name__ == "__main__":
    try:
        package_path = create_tokyo_v2_1_5_package()
        print(f"\n🎉 Package créé: {package_path}")
    except Exception as e:
        print(f"\n❌ ERREUR: {e}")
        input("Appuyez sur Entrée pour continuer...")
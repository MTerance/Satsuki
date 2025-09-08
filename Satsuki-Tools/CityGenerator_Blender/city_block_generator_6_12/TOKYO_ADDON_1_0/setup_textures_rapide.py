# SETUP RAPIDE - Créer la structure de textures Tokyo v1.3.0

import os
import shutil

def setup_tokyo_textures_quick():
    """Crée rapidement la structure de dossiers pour les textures Tokyo"""
    
    print("🎨 SETUP RAPIDE - SYSTÈME DE TEXTURES TOKYO")
    print("=" * 50)
    
    # Chemin de base pour les textures
    base_path = r"C:\Users\sshom\Documents\assets\Tools\tokyo_textures"
    
    print(f"📁 Création dans: {base_path}")
    
    # Catégories de bâtiments avec descriptions
    categories = {
        "skyscrapers": "Gratte-ciels (>15 étages) - Textures modernes, verre, métal",
        "commercial": "Commercial (8-15 étages) - Bureaux, centres commerciaux",
        "midrise": "Moyenne hauteur (4-8 étages) - Bâtiments urbains standards",
        "residential": "Résidentiel (2-4 étages) - Appartements, maisons",
        "lowrise": "Petits bâtiments (1-2 étages) - Boutiques, locaux"
    }
    
    # Sous-dossiers pour chaque catégorie
    subfolders = {
        "facade": "Textures de façade principale",
        "roof": "Textures de toit et toiture",
        "details": "Détails architecturaux (fenêtres, balcons)",
        "materials": "Matériaux spéciaux (métal, verre, bois)"
    }
    
    # Créer la structure
    total_folders = 0
    
    try:
        # Créer le dossier de base
        os.makedirs(base_path, exist_ok=True)
        print(f"✅ Dossier de base créé: {base_path}")
        
        # Créer README principal
        readme_content = """# TOKYO TEXTURES - Système Intelligent v1.3.0

## 📖 GUIDE D'UTILISATION

Ce dossier contient les textures pour le système intelligent de Tokyo City Generator.

### 🏗️ STRUCTURE:
- Chaque catégorie correspond à un type de bâtiment
- Le système sélectionne automatiquement selon la hauteur
- Plus de textures = plus de variété!

### 🎨 FORMATS SUPPORTÉS:
- .jpg, .png, .tga, .bmp, .tiff
- Résolution recommandée: 1024x1024 ou 2048x2048

### 🚀 UTILISATION:
1. Placez vos textures dans les bons dossiers
2. Dans Blender: Activez "Advanced Textures"
3. Configurez "Texture Base Path" vers ce dossier
4. Générez votre ville!

### 🎯 CATÉGORIES:
"""
        
        # Créer chaque catégorie
        for category, description in categories.items():
            category_path = os.path.join(base_path, category)
            os.makedirs(category_path, exist_ok=True)
            total_folders += 1
            
            print(f"📂 {category}/ - {description}")
            
            readme_content += f"\n#### {category.upper()}/\n{description}\n"
            
            # Créer les sous-dossiers
            for subfolder, sub_description in subfolders.items():
                subfolder_path = os.path.join(category_path, subfolder)
                os.makedirs(subfolder_path, exist_ok=True)
                total_folders += 1
                
                print(f"  📁 {subfolder}/ - {sub_description}")
                
                # Créer un fichier .gitkeep pour conserver la structure
                gitkeep_path = os.path.join(subfolder_path, ".gitkeep")
                with open(gitkeep_path, 'w') as f:
                    f.write(f"# {sub_description}\n# Placez vos textures {subfolder} ici")
        
        readme_content += """
### 📊 INTELLIGENCE DU SYSTÈME:

🏢 **SKYSCRAPERS** (>15 étages)
   → Textures modernes, reflets, verre, acier

🏬 **COMMERCIAL** (8-15 étages)  
   → Bureaux, centres d'affaires, enseignes

🏘️ **MIDRISE** (4-8 étages)
   → Bâtiments urbains classiques, béton

🏠 **RESIDENTIAL** (2-4 étages)
   → Appartements, briques, couleurs chaudes

🏪 **LOWRISE** (1-2 étages)
   → Boutiques, cafés, textures locales

### 🎲 SÉLECTION ALÉATOIRE:
Le système choisit aléatoirement parmi les textures disponibles
pour créer de la variété naturelle dans vos villes!

### 🔄 MISE À JOUR:
Ajoutez simplement de nouvelles textures dans les dossiers.
Le système les détectera automatiquement!
"""
        
        # Sauvegarder le README
        readme_path = os.path.join(base_path, "README.md")
        with open(readme_path, 'w', encoding='utf-8') as f:
            f.write(readme_content)
        
        print(f"\n📋 README créé: {readme_path}")
        
        # Créer des exemples de configuration
        config_content = f"""# CONFIGURATION TOKYO TEXTURES

## 📁 Chemin configuré:
{base_path}

## ⚙️ Dans Blender:
1. Activez l'addon Tokyo City Generator v1.3.0
2. Vue 3D > Sidebar (N) > Onglet Tokyo
3. ✅ Cochez "Advanced Textures"
4. 📁 "Texture Base Path" → {base_path}
5. 🚀 Generate Tokyo City!

## 📊 Structure créée:
- {len(categories)} catégories de bâtiments
- {len(subfolders)} types de textures par catégorie  
- {total_folders} dossiers au total

## 🎨 Prochaines étapes:
1. Ajoutez vos textures dans les dossiers appropriés
2. Testez la génération dans Blender
3. Profitez de la magie du système intelligent! ✨
"""
        
        config_path = os.path.join(base_path, "CONFIGURATION.txt")
        with open(config_path, 'w', encoding='utf-8') as f:
            f.write(config_content)
        
        print(f"⚙️ Configuration sauvée: {config_path}")
        
        print(f"\n✅ SETUP TERMINÉ!")
        print(f"📊 {total_folders} dossiers créés")
        print(f"📁 Chemin: {base_path}")
        print(f"\n🎯 PROCHAINES ÉTAPES:")
        print(f"1. Ajoutez vos textures dans les dossiers")
        print(f"2. Dans Blender: Advanced Textures → ON")
        print(f"3. Texture Base Path → {base_path}")
        print(f"4. Générez votre ville Tokyo! 🏙️")
        
        return base_path
        
    except Exception as e:
        print(f"❌ Erreur lors du setup: {e}")
        return None

def create_sample_textures():
    """Crée des fichiers d'exemple pour tester"""
    print(f"\n🎨 Création de fichiers d'exemple...")
    
    base_path = r"C:\Users\sshom\Documents\assets\Tools\tokyo_textures"
    
    # Créer des fichiers README dans chaque dossier
    categories = ["skyscrapers", "commercial", "midrise", "residential", "lowrise"]
    subfolders = ["facade", "roof", "details", "materials"]
    
    for category in categories:
        for subfolder in subfolders:
            folder_path = os.path.join(base_path, category, subfolder)
            
            example_file = os.path.join(folder_path, "EXEMPLE_TEXTURES.txt")
            
            examples = {
                "facade": [
                    "building_concrete_01.jpg",
                    "glass_facade_modern.png", 
                    "brick_wall_red.jpg",
                    "metal_panels_blue.png"
                ],
                "roof": [
                    "roof_tiles_clay.jpg",
                    "metal_roof_steel.png",
                    "concrete_flat_roof.jpg",
                    "green_roof_garden.png"
                ],
                "details": [
                    "windows_modern.png",
                    "balcony_iron.jpg",
                    "door_entrance.png",
                    "architectural_details.jpg"
                ],
                "materials": [
                    "steel_brushed.jpg",
                    "glass_tinted.png",
                    "wood_panels.jpg",
                    "stone_natural.png"
                ]
            }
            
            content = f"""# EXEMPLES DE TEXTURES - {subfolder.upper()}

## 📋 Types de fichiers recommandés pour {category}/{subfolder}:

"""
            
            for example in examples[subfolder]:
                content += f"- {example}\n"
                
            content += f"""
## 📏 Spécifications:
- Format: .jpg, .png, .tga, .bmp, .tiff
- Résolution: 1024x1024 ou 2048x2048
- Type: {subfolder} pour bâtiments {category}

## 🎯 Usage:
Le système sélectionnera aléatoirement parmi ces textures
pour créer des matériaux réalistes automatiquement!

## 💡 Conseil:
Plus vous ajoutez de textures variées, plus vos villes
seront diverses et intéressantes! 🌆
"""
            
            with open(example_file, 'w', encoding='utf-8') as f:
                f.write(content)
    
    print(f"✅ Fichiers d'exemple créés dans tous les dossiers")

if __name__ == "__main__":
    # Setup principal
    texture_path = setup_tokyo_textures_quick()
    
    if texture_path:
        # Créer les exemples
        create_sample_textures()
        
        print(f"\n🎉 SETUP COMPLET! 🎉")
        print(f"📁 Dossier: {texture_path}")
        print(f"🚀 Prêt pour Tokyo City Generator v1.3.0!")
    else:
        print(f"❌ Échec du setup")

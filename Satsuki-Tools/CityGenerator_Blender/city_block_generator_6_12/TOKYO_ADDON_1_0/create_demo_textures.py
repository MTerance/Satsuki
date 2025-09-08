# TOKYO TEXTURE DEMO CREATOR v1.0
# Crée des textures procédurales de démonstration pour tester le système

import os
from PIL import Image, ImageDraw, ImageFont
import random

def create_demo_textures():
    """Crée des textures de démonstration pour chaque catégorie"""
    
    base_path = "C:/Users/sshom/Documents/Assets/Textures/Tokyo_Buildings/"
    
    # Définitions des catégories et leurs couleurs
    texture_specs = {
        # GRATTE-CIELS - Tons bleus et métalliques
        "skyscrapers": {
            "glass_towers": [(70, 130, 180), (100, 150, 200), (50, 100, 160)],
            "modern_office": [(80, 80, 120), (100, 100, 140), (60, 60, 100)],
            "metallic_facades": [(120, 120, 140), (140, 140, 160), (100, 100, 120)],
            "corporate_buildings": [(90, 110, 130), (110, 130, 150), (70, 90, 110)]
        },
        
        # COMMERCIAL - Couleurs vives et variées
        "commercial": {
            "shopping_centers": [(220, 50, 50), (50, 220, 50), (50, 50, 220), (220, 220, 50)],
            "retail_facades": [(200, 100, 50), (100, 200, 50), (100, 50, 200), (200, 200, 100)],
            "colorful_buildings": [(255, 100, 100), (100, 255, 100), (100, 100, 255), (255, 255, 100)],
            "modern_stores": [(180, 80, 80), (80, 180, 80), (80, 80, 180), (180, 180, 80)]
        },
        
        # MIDRISE - Tons moyens urbains
        "midrise": {
            "apartment_blocks": [(150, 130, 110), (170, 150, 130), (130, 110, 90)],
            "office_buildings": [(120, 120, 120), (140, 140, 140), (100, 100, 100)],
            "mixed_use": [(160, 140, 120), (140, 120, 100), (180, 160, 140)],
            "urban_housing": [(140, 120, 100), (160, 140, 120), (120, 100, 80)]
        },
        
        # RÉSIDENTIEL - Tons chauds et naturels
        "residential": {
            "japanese_houses": [(160, 120, 80), (140, 100, 60), (180, 140, 100)],
            "modern_homes": [(200, 180, 160), (180, 160, 140), (220, 200, 180)],
            "traditional_buildings": [(120, 80, 40), (100, 60, 20), (140, 100, 60)],
            "small_apartments": [(180, 160, 140), (160, 140, 120), (200, 180, 160)]
        },
        
        # LOWRISE - Tons variés de petits commerces
        "lowrise": {
            "small_shops": [(200, 150, 100), (150, 200, 100), (100, 150, 200)],
            "cafes_restaurants": [(180, 140, 100), (140, 180, 100), (100, 140, 180)],
            "services": [(160, 160, 160), (140, 140, 140), (180, 180, 180)],
            "traditional_stores": [(140, 100, 60), (120, 80, 40), (160, 120, 80)]
        }
    }
    
    print("🎨 Création des textures de démonstration...")
    
    # Créer les textures pour chaque catégorie
    for category, subcategories in texture_specs.items():
        print(f"\n📁 Catégorie: {category}")
        
        for subcategory, colors in subcategories.items():
            folder_path = os.path.join(base_path, category, subcategory)
            
            if not os.path.exists(folder_path):
                print(f"⚠️ Dossier non trouvé: {folder_path}")
                continue
            
            # Créer 3 textures variantes pour chaque sous-catégorie
            for i, base_color in enumerate(colors[:3]):
                texture_name = f"{subcategory}_{i+1:02d}.jpg"
                texture_path = os.path.join(folder_path, texture_name)
                
                # Créer la texture procédurale
                texture_img = create_procedural_facade_texture(base_color, subcategory, 512, 512)
                texture_img.save(texture_path, "JPEG", quality=85)
                
                print(f"  ✅ {texture_name}")
    
    print(f"\n🎉 Textures de démonstration créées!")
    print(f"📁 Dossier: {base_path}")
    return True

def create_procedural_facade_texture(base_color, subcategory, width, height):
    """Crée une texture procédurale de façade"""
    
    # Créer l'image de base
    img = Image.new('RGB', (width, height), base_color)
    draw = ImageDraw.Draw(img)
    
    # Ajouter des éléments selon le type
    if "glass" in subcategory or "office" in subcategory or "skyscraper" in subcategory:
        # Façade vitrée - grille de fenêtres
        create_glass_facade_pattern(draw, width, height, base_color)
    
    elif "commercial" in subcategory or "retail" in subcategory or "colorful" in subcategory:
        # Façade commerciale - fenêtres et éléments colorés
        create_commercial_facade_pattern(draw, width, height, base_color)
    
    elif "residential" in subcategory or "house" in subcategory or "apartment" in subcategory:
        # Façade résidentielle - fenêtres domestiques
        create_residential_facade_pattern(draw, width, height, base_color)
    
    elif "traditional" in subcategory:
        # Façade traditionnelle - éléments japonais
        create_traditional_facade_pattern(draw, width, height, base_color)
    
    else:
        # Façade générique
        create_generic_facade_pattern(draw, width, height, base_color)
    
    return img

def create_glass_facade_pattern(draw, width, height, base_color):
    """Crée un motif de façade vitrée"""
    window_width = 40
    window_height = 60
    spacing_x = 50
    spacing_y = 70
    
    # Couleur des fenêtres (plus sombre)
    window_color = tuple(max(0, c - 50) for c in base_color)
    frame_color = tuple(min(255, c + 30) for c in base_color)
    
    for y in range(10, height - window_height, spacing_y):
        for x in range(10, width - window_width, spacing_x):
            # Cadre de fenêtre
            draw.rectangle([x-2, y-2, x+window_width+2, y+window_height+2], fill=frame_color)
            # Fenêtre
            draw.rectangle([x, y, x+window_width, y+window_height], fill=window_color)
            # Reflet (ligne claire)
            draw.line([x+5, y+5, x+window_width-5, y+5], fill=tuple(min(255, c + 80) for c in window_color), width=2)

def create_commercial_facade_pattern(draw, width, height, base_color):
    """Crée un motif de façade commerciale"""
    # Fenêtres de magasin (plus grandes)
    window_width = 80
    window_height = 40
    spacing_y = 60
    
    window_color = tuple(max(0, c - 30) for c in base_color)
    bright_color = tuple(min(255, c + 60) for c in base_color)
    
    for y in range(20, height - window_height, spacing_y):
        for x in range(15, width - window_width, window_width + 20):
            # Grande fenêtre de magasin
            draw.rectangle([x, y, x+window_width, y+window_height], fill=window_color)
            # Élément décoratif coloré
            draw.rectangle([x, y-10, x+window_width, y], fill=bright_color)

def create_residential_facade_pattern(draw, width, height, base_color):
    """Crée un motif de façade résidentielle"""
    window_width = 30
    window_height = 40
    spacing_x = 45
    spacing_y = 55
    
    window_color = tuple(max(0, c - 40) for c in base_color)
    frame_color = tuple(c + random.randint(-20, 20) for c in base_color)
    frame_color = tuple(max(0, min(255, c)) for c in frame_color)
    
    for y in range(15, height - window_height, spacing_y):
        for x in range(20, width - window_width, spacing_x):
            # Fenêtre résidentielle
            draw.rectangle([x-1, y-1, x+window_width+1, y+window_height+1], fill=frame_color)
            draw.rectangle([x, y, x+window_width, y+window_height], fill=window_color)
            # Volet ou détail
            if random.random() > 0.5:
                shutter_color = tuple(max(0, c - 60) for c in base_color)
                draw.rectangle([x-5, y, x, y+window_height], fill=shutter_color)

def create_traditional_facade_pattern(draw, width, height, base_color):
    """Crée un motif de façade traditionnelle japonaise"""
    # Lignes horizontales (style traditionnel)
    line_color = tuple(max(0, c - 60) for c in base_color)
    accent_color = tuple(min(255, c + 40) for c in base_color)
    
    # Lignes horizontales régulières
    for y in range(0, height, 25):
        draw.line([0, y, width, y], fill=line_color, width=3)
    
    # Petites fenêtres traditionnelles
    window_size = 20
    for y in range(30, height - window_size, 50):
        for x in range(30, width - window_size, 60):
            draw.rectangle([x, y, x+window_size, y+window_size], fill=line_color)
            # Détail central
            draw.rectangle([x+5, y+5, x+window_size-5, y+window_size-5], fill=accent_color)

def create_generic_facade_pattern(draw, width, height, base_color):
    """Crée un motif de façade générique"""
    window_width = 35
    window_height = 50
    spacing_x = 50
    spacing_y = 65
    
    window_color = tuple(max(0, c - 35) for c in base_color)
    
    for y in range(20, height - window_height, spacing_y):
        for x in range(25, width - window_width, spacing_x):
            draw.rectangle([x, y, x+window_width, y+window_height], fill=window_color)

if __name__ == "__main__":
    try:
        from PIL import Image, ImageDraw
        create_demo_textures()
        print("\n🎯 Les textures de démonstration sont prêtes!")
        print("🚀 Vous pouvez maintenant tester le système de textures dans Blender")
    except ImportError:
        print("❌ PIL (Pillow) non installé. Installez avec: pip install Pillow")
    except Exception as e:
        print(f"❌ Erreur: {e}")

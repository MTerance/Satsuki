"""
Système de textures unifié v2.0 pour Tokyo City Generator
Amélioration du système multi-étages avec support pour tous les algorithmes
"""

import bpy
import random
import os
from pathlib import Path
from typing import Dict, List, Tuple, Optional

class UnifiedTextureSystem:
    """Système de textures unifié pour tous les algorithmes de génération"""
    
    def __init__(self):
        self.version = "2.0.0"
        self.texture_base_path = self.get_texture_base_path()
        self.texture_categories = self.init_texture_categories()
        self.cache = {}  # Cache des matériaux créés
        
        print(f"🎨 UnifiedTextureSystem v{self.version} initialisé")
        print(f"📁 Base path: {self.texture_base_path}")
    
    def get_texture_base_path(self) -> str:
        """Détermine le chemin de base des textures avec plusieurs fallbacks"""
        possible_paths = [
            "C:/Users/sshom/Documents/assets/Tools/tokyo_textures/",
            "C:/Users/sshom/Documents/Assets/Textures/Tokyo_Buildings/",
            "C:/Users/sshom/OneDrive/Documents/Assets/Textures/Tokyo_Buildings/",
            os.path.join(os.path.dirname(__file__), "textures"),
            "//Tokyo_Textures/Buildings/"
        ]
        
        for path in possible_paths:
            if os.path.exists(path):
                print(f"✅ Chemin textures trouvé: {path}")
                return path
        
        # Aucun chemin trouvé, créer la structure par défaut
        default_path = "C:/Users/sshom/Documents/assets/Tools/tokyo_textures/"
        self.create_texture_structure(default_path)
        return default_path
    
    def init_texture_categories(self) -> Dict:
        """Initialise les catégories de textures étendues pour v2.0"""
        return {
            # GRATTE-CIELS - Bâtiments > 50m
            'skyscraper': {
                'height_range': (50, 200),
                'width_range': (10, 40),
                'texture_folders': [
                    'skyscrapers/glass_towers',
                    'skyscrapers/modern_office',
                    'skyscrapers/metallic_facades',
                    'skyscrapers/corporate_buildings'
                ],
                'material_props': {
                    'metallic': 0.8,
                    'roughness': 0.2,
                    'emission': 0.1  # Lumière des fenêtres
                }
            },
            
            # COMMERCIAL - Centres commerciaux 10-50m, large
            'commercial': {
                'height_range': (10, 50),
                'width_range': (15, 50),
                'texture_folders': [
                    'commercial/shopping_centers',
                    'commercial/retail_facades',
                    'commercial/colorful_buildings',
                    'commercial/modern_stores'
                ],
                'material_props': {
                    'metallic': 0.3,
                    'roughness': 0.6,
                    'saturation': 1.2  # Plus coloré
                }
            },
            
            # IMMEUBLES MOYENS - 20-50m, étroit
            'midrise': {
                'height_range': (20, 50),
                'width_range': (5, 15),
                'texture_folders': [
                    'midrise/apartment_blocks',
                    'midrise/office_buildings',
                    'midrise/mixed_use',
                    'midrise/urban_housing'
                ],
                'material_props': {
                    'metallic': 0.2,
                    'roughness': 0.7,
                }
            },
            
            # RÉSIDENTIEL - Maisons < 20m
            'residential': {
                'height_range': (3, 20),
                'width_range': (5, 15),
                'texture_folders': [
                    'residential/japanese_houses',
                    'residential/modern_homes',
                    'residential/traditional_buildings',
                    'residential/small_apartments'
                ],
                'material_props': {
                    'metallic': 0.1,
                    'roughness': 0.8,
                    'warmth': 1.1  # Tons plus chauds
                }
            },
            
            # PETITS BÂTIMENTS - < 10m
            'lowrise': {
                'height_range': (2, 10),
                'width_range': (3, 12),
                'texture_folders': [
                    'lowrise/small_shops',
                    'lowrise/cafes_restaurants',
                    'lowrise/services',
                    'lowrise/traditional_stores'
                ],
                'material_props': {
                    'metallic': 0.15,
                    'roughness': 0.75,
                    'detail': 1.3  # Plus de détails
                }
            },
            
            # INDUSTRIEL - Nouveau pour v2.0
            'industrial': {
                'height_range': (5, 25),
                'width_range': (15, 60),
                'texture_folders': [
                    'industrial/warehouses',
                    'industrial/factories',
                    'industrial/storage_buildings'
                ],
                'material_props': {
                    'metallic': 0.6,
                    'roughness': 0.9,
                    'weathering': 1.5  # Aspect vieilli
                }
            }
        }
    
    def create_building_material(self, category: str, zone_type: str, height: float, 
                               width: float, algorithm: str = 'tokyo') -> bpy.types.Material:
        """Crée un matériau de bâtiment adapté à la catégorie et à l'algorithme"""
        
        # Clé de cache
        cache_key = f"{category}_{zone_type}_{algorithm}_{int(height)}_{int(width)}"
        if cache_key in self.cache:
            return self.cache[cache_key]
        
        # Nom du matériau
        mat_name = f"Unified_{algorithm.title()}_{category}_{int(height)}m"
        
        try:
            # Essayer de créer avec textures
            material = self.create_textured_material(mat_name, category, height, width, algorithm)
            print(f"🎨 Matériau texturé créé: {mat_name}")
        except Exception as e:
            print(f"⚠️ Erreur texture {mat_name}: {e}")
            # Fallback vers matériau procédural
            material = self.create_procedural_material(mat_name, category, zone_type, height, algorithm)
            print(f"🎨 Matériau procédural créé: {mat_name}")
        
        # Mettre en cache
        self.cache[cache_key] = material
        return material
    
    def create_textured_material(self, name: str, category: str, height: float, 
                               width: float, algorithm: str) -> bpy.types.Material:
        """Crée un matériau avec texture multi-étages"""
        
        # Obtenir les informations de la catégorie
        cat_info = self.texture_categories.get(category, self.texture_categories['residential'])
        
        # Choisir un fichier texture
        texture_file = self.find_texture_file(category)
        if not texture_file:
            raise FileNotFoundError(f"No texture found for category {category}")
        
        # Créer le matériau
        mat = bpy.data.materials.new(name=name)
        mat.use_nodes = True
        nodes = mat.node_tree.nodes
        links = mat.node_tree.links
        
        # Nettoyer les nodes existants
        nodes.clear()
        
        # NODES PRINCIPAUX
        output = nodes.new(type='ShaderNodeOutputMaterial')
        bsdf = nodes.new(type='ShaderNodeBsdfPrincipled')
        
        # TEXTURE IMAGE
        img_texture = nodes.new(type='ShaderNodeTexImage')
        img_texture.image = bpy.data.images.load(texture_file)
        
        # MAPPING UV MULTI-ÉTAGES
        mapping = nodes.new(type='ShaderNodeMapping')
        coord = nodes.new(type='ShaderNodeTexCoord')
        
        # CALCUL DU FACTEUR DE RÉPÉTITION v2.0 AMÉLIORÉ
        floors_per_texture = 4.0
        meters_per_floor = 3.0
        building_floors = height / meters_per_floor
        repetitions_verticales = building_floors / floors_per_texture
        
        # Ajustement selon l'algorithme
        if algorithm == 'organic':
            repetitions_verticales *= random.uniform(0.8, 1.2)  # Variation organique
        elif algorithm == 'grid':
            repetitions_verticales = round(repetitions_verticales)  # Répétitions exactes
        # Tokyo reste naturel
        
        # Répétition horizontale selon la largeur
        repetitions_horizontales = max(1.0, width / 8.0)
        
        # Configuration du mapping
        mapping.inputs['Scale'].default_value = (repetitions_horizontales, repetitions_verticales, 1.0)
        
        # PROPRIÉTÉS MATÉRIAU SELON CATÉGORIE
        mat_props = cat_info['material_props']
        
        bsdf.inputs['Metallic'].default_value = mat_props.get('metallic', 0.2)
        bsdf.inputs['Roughness'].default_value = mat_props.get('roughness', 0.7)
        
        # Émission pour gratte-ciels (fenêtres éclairées)
        if 'emission' in mat_props:
            bsdf.inputs['Emission Strength'].default_value = mat_props['emission']
            # Couleur d'émission chaude
            bsdf.inputs['Emission Color'].default_value = (1.0, 0.9, 0.7, 1.0)
        
        # NODES ADDITIONNELS v2.0
        
        # ColorRamp pour ajuster le contraste selon l'algorithme
        if algorithm in ['organic', 'tokyo']:
            color_ramp = nodes.new(type='ShaderNodeValToRGB')
            color_ramp.color_ramp.elements[0].color = (0.8, 0.8, 0.8, 1.0)
            color_ramp.color_ramp.elements[1].color = (1.2, 1.2, 1.2, 1.0)
            
            # Connexions avec ColorRamp
            links.new(img_texture.outputs['Color'], color_ramp.inputs['Fac'])
            links.new(color_ramp.outputs['Color'], bsdf.inputs['Base Color'])
            
            color_ramp.location = (200, 100)
        else:
            # Connexion directe pour Grid
            links.new(img_texture.outputs['Color'], bsdf.inputs['Base Color'])
        
        # CONNEXIONS PRINCIPALES
        links.new(coord.outputs['UV'], mapping.inputs['Vector'])
        links.new(mapping.outputs['Vector'], img_texture.inputs['Vector'])
        links.new(bsdf.outputs['BSDF'], output.inputs['Surface'])
        
        # POSITIONNEMENT DES NODES
        output.location = (600, 0)
        bsdf.location = (400, 0)
        img_texture.location = (0, 0)
        mapping.location = (-200, 0)
        coord.location = (-400, 0)
        
        print(f"🏗️ Matériau {name}: {repetitions_verticales:.1f}x vertical, {repetitions_horizontales:.1f}x horizontal")
        return mat
    
    def create_procedural_material(self, name: str, category: str, zone_type: str, 
                                 height: float, algorithm: str) -> bpy.types.Material:
        """Crée un matériau procédural amélioré v2.0"""
        
        mat = bpy.data.materials.new(name=name)
        mat.use_nodes = True
        nodes = mat.node_tree.nodes
        links = mat.node_tree.links
        
        nodes.clear()
        
        # Nodes de base
        output = nodes.new(type='ShaderNodeOutputMaterial')
        bsdf = nodes.new(type='ShaderNodeBsdfPrincipled')
        
        # Couleur selon catégorie et algorithme
        base_colors = {
            'skyscraper': (0.6, 0.7, 0.9, 1.0),  # Bleu moderne
            'commercial': (0.8, 0.6, 0.5, 1.0),  # Brun commercial
            'residential': (0.9, 0.8, 0.7, 1.0), # Beige résidentiel
            'midrise': (0.7, 0.7, 0.8, 1.0),     # Gris urbain
            'lowrise': (0.8, 0.7, 0.6, 1.0),     # Brun clair
            'industrial': (0.5, 0.5, 0.6, 1.0)   # Gris industriel
        }
        
        base_color = base_colors.get(category, (0.7, 0.7, 0.7, 1.0))
        
        # Variation selon l'algorithme
        if algorithm == 'organic':
            # Couleurs plus naturelles et variées
            variation = [random.uniform(0.8, 1.2) for _ in range(3)]
            base_color = tuple(min(1.0, base_color[i] * variation[i]) for i in range(3)) + (1.0,)
        elif algorithm == 'grid':
            # Couleurs plus uniformes
            base_color = tuple(base_color[i] * 0.9 for i in range(3)) + (1.0,)
        # Tokyo reste naturel
        
        bsdf.inputs['Base Color'].default_value = base_color
        
        # Propriétés selon catégorie
        cat_info = self.texture_categories.get(category, self.texture_categories['residential'])
        mat_props = cat_info['material_props']
        
        bsdf.inputs['Metallic'].default_value = mat_props.get('metallic', 0.2)
        bsdf.inputs['Roughness'].default_value = mat_props.get('roughness', 0.7)
        
        # Émission pour gratte-ciels
        if category == 'skyscraper':
            bsdf.inputs['Emission Strength'].default_value = 0.05
            bsdf.inputs['Emission Color'].default_value = (1.0, 0.9, 0.7, 1.0)
        
        # Connexions
        links.new(bsdf.outputs['BSDF'], output.inputs['Surface'])
        
        # Positionnement
        output.location = (200, 0)
        bsdf.location = (0, 0)
        
        return mat
    
    def find_texture_file(self, category: str) -> Optional[str]:
        """Trouve un fichier texture pour la catégorie donnée"""
        cat_info = self.texture_categories.get(category)
        if not cat_info:
            return None
        
        # Chercher dans les dossiers de la catégorie
        for folder in cat_info['texture_folders']:
            folder_path = os.path.join(self.texture_base_path, folder)
            if os.path.exists(folder_path):
                # Extensions supportées
                extensions = ['.jpg', '.jpeg', '.png', '.tga', '.exr']
                for file in os.listdir(folder_path):
                    if any(file.lower().endswith(ext) for ext in extensions):
                        return os.path.join(folder_path, file)
        
        return None
    
    def create_texture_structure(self, base_path: str):
        """Crée la structure de dossiers de textures"""
        print(f"🗂️ Création structure textures dans: {base_path}")
        
        # Créer tous les dossiers nécessaires
        all_folders = []
        for category in self.texture_categories.values():
            all_folders.extend(category['texture_folders'])
        
        for folder in all_folders:
            folder_path = os.path.join(base_path, folder)
            os.makedirs(folder_path, exist_ok=True)
            
            # Créer un fichier README dans chaque dossier
            readme_path = os.path.join(folder_path, "README.txt")
            if not os.path.exists(readme_path):
                with open(readme_path, 'w') as f:
                    f.write(f"Texture folder: {folder}\n")
                    f.write("Place your texture files here (4 floors per texture)\n")
                    f.write("Supported formats: JPG, PNG, TGA, EXR\n")
        
        print(f"✅ Structure de textures créée avec {len(all_folders)} dossiers")
    
    def create_road_material(self, road_type: str = 'asphalt', algorithm: str = 'tokyo') -> bpy.types.Material:
        """Crée un matériau de route adapté à l'algorithme"""
        
        cache_key = f"road_{road_type}_{algorithm}"
        if cache_key in self.cache:
            return self.cache[cache_key]
        
        mat_name = f"Unified_Road_{algorithm.title()}_{road_type}"
        mat = bpy.data.materials.new(name=mat_name)
        mat.use_nodes = True
        nodes = mat.node_tree.nodes
        links = mat.node_tree.links
        
        nodes.clear()
        
        output = nodes.new(type='ShaderNodeOutputMaterial')
        bsdf = nodes.new(type='ShaderNodeBsdfPrincipled')
        
        # Couleur selon type et algorithme
        road_colors = {
            'tokyo': (0.2, 0.2, 0.25, 1.0),    # Gris foncé urbain
            'organic': (0.3, 0.25, 0.2, 1.0),  # Brun terre
            'grid': (0.15, 0.15, 0.15, 1.0)    # Noir asphalte
        }
        
        base_color = road_colors.get(algorithm, (0.2, 0.2, 0.2, 1.0))
        bsdf.inputs['Base Color'].default_value = base_color
        bsdf.inputs['Roughness'].default_value = 0.9
        bsdf.inputs['Metallic'].default_value = 0.0
        
        links.new(bsdf.outputs['BSDF'], output.inputs['Surface'])
        
        output.location = (200, 0)
        bsdf.location = (0, 0)
        
        self.cache[cache_key] = mat
        return mat
    
    def get_stats(self) -> Dict:
        """Retourne les statistiques du système de textures"""
        return {
            'version': self.version,
            'base_path': self.texture_base_path,
            'categories': len(self.texture_categories),
            'cached_materials': len(self.cache),
            'path_exists': os.path.exists(self.texture_base_path)
        }

# Instance globale
unified_texture_system = UnifiedTextureSystem()

def register():
    """Enregistrement du système de textures unifié"""
    print("🎨 Système de textures unifié v2.0 enregistré")

def unregister():
    """Désenregistrement du système de textures unifié"""
    print("🔄 Système de textures unifié v2.0 désenregistré")
# TOKYO TEXTURE SYSTEM v1.2.0
# Système de textures automatiques selon hauteur/largeur des bâtiments

import bpy
import bmesh
import random
import os
import mathutils
from pathlib import Path

class TokyoTextureSystem:
    """Système de textures intelligent pour Tokyo City Generator"""
    
    def __init__(self):
        # Configuration des dossiers de textures
        self.texture_base_path = self.get_texture_base_path()
        self.texture_categories = {
            # GRATTE-CIELS (Business) - Hauteur > 50m
            'skyscraper': {
                'height_range': (50, 200),
                'width_range': (10, 40),
                'texture_folders': [
                    'skyscrapers/glass_towers',
                    'skyscrapers/modern_office',
                    'skyscrapers/metallic_facades',
                    'skyscrapers/corporate_buildings'
                ]
            },
            
            # CENTRES COMMERCIAUX (Commercial) - Hauteur 10-50m, Largeur > 15m
            'commercial': {
                'height_range': (10, 50),
                'width_range': (15, 50),
                'texture_folders': [
                    'commercial/shopping_centers',
                    'commercial/retail_facades',
                    'commercial/colorful_buildings',
                    'commercial/modern_stores'
                ]
            },
            
            # IMMEUBLES MOYENS (Mixed) - Hauteur 20-50m, Largeur < 15m
            'midrise': {
                'height_range': (20, 50),
                'width_range': (5, 15),
                'texture_folders': [
                    'midrise/apartment_blocks',
                    'midrise/office_buildings',
                    'midrise/mixed_use',
                    'midrise/urban_housing'
                ]
            },
            
            # MAISONS RÉSIDENTIELLES (Residential) - Hauteur < 20m
            'residential': {
                'height_range': (3, 20),
                'width_range': (5, 15),
                'texture_folders': [
                    'residential/japanese_houses',
                    'residential/modern_homes',
                    'residential/traditional_buildings',
                    'residential/small_apartments'
                ]
            },
            
            # PETITS BÂTIMENTS (Low-rise) - Hauteur < 10m
            'lowrise': {
                'height_range': (2, 10),
                'width_range': (3, 12),
                'texture_folders': [
                    'lowrise/small_shops',
                    'lowrise/cafes_restaurants',
                    'lowrise/services',
                    'lowrise/traditional_stores'
                ]
            }
        }
    
    def get_texture_base_path(self):
        """Détermine le chemin de base des textures"""
        # Essayer plusieurs emplacements possibles
        possible_paths = [
            "C:/Users/sshom/Documents/Assets/Textures/Tokyo_Buildings/",
            "C:/Users/sshom/OneDrive/Documents/Assets/Textures/Tokyo_Buildings/",
            os.path.join(os.path.dirname(__file__), "textures", "buildings"),
            "//Tokyo_Textures/Buildings/"  # Chemin Blender relatif
        ]
        
        for path in possible_paths:
            if os.path.exists(path):
                return path
        
        # Si aucun dossier n'existe, créer la structure de base
        default_path = "C:/Users/sshom/Documents/Assets/Textures/Tokyo_Buildings/"
        self.create_texture_folders(default_path)
        return default_path
    
    def create_texture_folders(self, base_path):
        """Crée la structure de dossiers de textures"""
        print(f"🗂️ Création structure textures dans: {base_path}")
        
        folders_to_create = []
        for category in self.texture_categories.values():
            for folder in category['texture_folders']:
                folders_to_create.append(os.path.join(base_path, folder))
        
        for folder_path in folders_to_create:
            os.makedirs(folder_path, exist_ok=True)
            # Créer un fichier README dans chaque dossier
            readme_path = os.path.join(folder_path, "README.txt")
            if not os.path.exists(readme_path):
                with open(readme_path, 'w') as f:
                    f.write(f"Dossier de textures pour: {os.path.basename(folder_path)}\n")
                    f.write("Formats supportés: .jpg, .png, .exr, .hdr\n")
                    f.write("Taille recommandée: 1024x1024 ou plus\n")
    
    def categorize_building(self, height, width_x, width_y, zone_type):
        """Détermine la catégorie de bâtiment selon ses dimensions"""
        avg_width = (width_x + width_y) / 2
        
        # Logique de catégorisation
        if height > 50:
            return 'skyscraper'
        elif height > 20 and avg_width > 15:
            return 'commercial'
        elif height > 20 and avg_width <= 15:
            return 'midrise'
        elif height > 10:
            return 'residential'
        else:
            return 'lowrise'
    
    def get_random_texture(self, category):
        """Sélectionne une texture aléatoire dans la catégorie"""
        if category not in self.texture_categories:
            print(f"⚠️ Catégorie inconnue: {category}")
            return None
        
        category_info = self.texture_categories[category]
        texture_folders = category_info['texture_folders']
        
        # Choisir un dossier aléatoire
        selected_folder = random.choice(texture_folders)
        folder_path = os.path.join(self.texture_base_path, selected_folder)
        
        if not os.path.exists(folder_path):
            print(f"⚠️ Dossier texture inexistant: {folder_path}")
            return None
        
        # Lister les fichiers image
        image_extensions = {'.jpg', '.jpeg', '.png', '.exr', '.hdr', '.tiff', '.bmp'}
        image_files = []
        
        for file in os.listdir(folder_path):
            if Path(file).suffix.lower() in image_extensions:
                image_files.append(os.path.join(folder_path, file))
        
        if not image_files:
            print(f"⚠️ Aucune texture trouvée dans: {folder_path}")
            return None
        
        # Retourner un fichier aléatoire
        selected_texture = random.choice(image_files)
        print(f"🎨 Texture sélectionnée: {os.path.basename(selected_texture)} pour {category}")
        return selected_texture
    
    def create_advanced_building_material(self, zone_type, height, width_x, width_y, building_name, texture_base_path=None):
        """Crée un matériau avancé avec texture selon les dimensions"""
        
        # Utiliser le chemin fourni ou celui par défaut
        if texture_base_path:
            self.base_path = texture_base_path
        
        # Déterminer la catégorie de bâtiment
        category = self.categorize_building(height, width_x, width_y, zone_type)
        
        # Créer le matériau
        mat_name = f"Tokyo_Advanced_{category}_{building_name}"
        mat = bpy.data.materials.new(name=mat_name)
        mat.use_nodes = True
        
        # Nettoyer les nœuds existants
        mat.node_tree.nodes.clear()
        
        # Essayer de charger une texture
        texture_path = self.get_random_texture(category)
        
        if texture_path and os.path.exists(texture_path):
            # MATÉRIAU AVEC TEXTURE
            material = self.create_textured_material(mat, texture_path, category, zone_type)
        else:
            # MATÉRIAU PROCÉDURAL DE FALLBACK
            material = self.create_procedural_material(mat, category, zone_type, height)
        
        print(f"🏗️ Matériau créé: {mat_name} (catégorie: {category})")
        return material
    
    def create_textured_material(self, mat, texture_path, category, zone_type):
        """Crée un matériau avec texture d'image"""
        nodes = mat.node_tree.nodes
        links = mat.node_tree.links
        
        # Nœuds principaux
        output = nodes.new(type='ShaderNodeOutputMaterial')
        bsdf = nodes.new(type='ShaderNodeBsdfPrincipled')
        
        # Nœud texture d'image
        img_texture = nodes.new(type='ShaderNodeTexImage')
        
        # Charger l'image
        try:
            img = bpy.data.images.load(texture_path)
            img_texture.image = img
        except:
            print(f"❌ Erreur chargement texture: {texture_path}")
            return self.create_procedural_material(mat, category, zone_type, 0)
        
        # Nœud de mapping pour contrôler la taille
        mapping = nodes.new(type='ShaderNodeMapping')
        coord = nodes.new(type='ShaderNodeTexCoord')
        
        # Paramètres selon la catégorie
        if category == 'skyscraper':
            # Gratte-ciels: texture étirée verticalement
            mapping.inputs['Scale'].default_value = (1.0, 0.1, 1.0)  # Étirement vertical
            bsdf.inputs['Metallic'].default_value = 0.8
            bsdf.inputs['Roughness'].default_value = 0.2
        elif category == 'commercial':
            # Commercial: texture normale
            mapping.inputs['Scale'].default_value = (1.0, 1.0, 1.0)
            bsdf.inputs['Metallic'].default_value = 0.3
            bsdf.inputs['Roughness'].default_value = 0.6
        elif category == 'residential':
            # Résidentiel: texture plus petite (détaillée)
            mapping.inputs['Scale'].default_value = (2.0, 2.0, 2.0)
            bsdf.inputs['Metallic'].default_value = 0.1
            bsdf.inputs['Roughness'].default_value = 0.8
        else:
            # Autres: texture standard
            mapping.inputs['Scale'].default_value = (1.5, 1.5, 1.5)
            bsdf.inputs['Metallic'].default_value = 0.2
            bsdf.inputs['Roughness'].default_value = 0.7
        
        # Connexions
        links.new(coord.outputs['UV'], mapping.inputs['Vector'])
        links.new(mapping.outputs['Vector'], img_texture.inputs['Vector'])
        links.new(img_texture.outputs['Color'], bsdf.inputs['Base Color'])
        links.new(bsdf.outputs['BSDF'], output.inputs['Surface'])
        
        # Positionnement des nœuds
        output.location = (400, 0)
        bsdf.location = (200, 0)
        img_texture.location = (0, 0)
        mapping.location = (-200, 0)
        coord.location = (-400, 0)
        
        return mat
    
    def create_procedural_material(self, mat, category, zone_type, height):
        """Crée un matériau procédural de fallback"""
        nodes = mat.node_tree.nodes
        links = mat.node_tree.links
        
        # Nœuds de base
        output = nodes.new(type='ShaderNodeOutputMaterial')
        bsdf = nodes.new(type='ShaderNodeBsdfPrincipled')
        
        # Couleur selon la catégorie
        if category == 'skyscraper':
            color = (0.7, 0.8, 0.9, 1.0)  # Bleu vitré
            metallic = 0.8
            roughness = 0.1
        elif category == 'commercial':
            # Couleurs vives pour commercial
            colors = [
                (0.9, 0.3, 0.3, 1.0),  # Rouge
                (0.3, 0.9, 0.3, 1.0),  # Vert
                (0.3, 0.3, 0.9, 1.0),  # Bleu
                (0.9, 0.7, 0.3, 1.0),  # Orange
            ]
            color = random.choice(colors)
            metallic = 0.3
            roughness = 0.6
        elif category == 'residential':
            color = (0.8, 0.7, 0.6, 1.0)  # Beige
            metallic = 0.1
            roughness = 0.8
        else:
            color = (0.6, 0.6, 0.6, 1.0)  # Gris
            metallic = 0.2
            roughness = 0.7
        
        # Appliquer les paramètres
        bsdf.inputs['Base Color'].default_value = color
        bsdf.inputs['Metallic'].default_value = metallic
        bsdf.inputs['Roughness'].default_value = roughness
        
        # Connexions
        links.new(bsdf.outputs['BSDF'], output.inputs['Surface'])
        
        # Positionnement
        output.location = (200, 0)
        bsdf.location = (0, 0)
        
        print(f"🎨 Matériau procédural créé pour {category}")
        return mat

# Instance globale du système
tokyo_texture_system = TokyoTextureSystem()

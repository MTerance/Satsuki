# TOKYO TEXTURE SYSTEM v1.3.0
# Système de textures automatiques selon hauteur/largeur des bâtiments + ROUTES ET TROTTOIRS

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
    
    def get_category_texture_path(self, category):
        """Retourne le chemin principal des textures pour une catégorie"""
        if category not in self.texture_categories:
            return None
        
        category_info = self.texture_categories[category]
        if category_info['texture_folders']:
            first_folder = category_info['texture_folders'][0]
            return os.path.join(self.texture_base_path, first_folder)
        return None
    
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
        """Crée un matériau avancé avec texture selon les dimensions - SYSTÈME MULTI-ÉTAGES"""
        
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
            # MATÉRIAU AVEC TEXTURE MULTI-ÉTAGES
            print(f"🎨 Création texture multi-étages pour {category} (hauteur: {height:.1f}m)")
            material = self.create_textured_material(mat, texture_path, category, zone_type, height)
        else:
            # MATÉRIAU PROCÉDURAL DE FALLBACK
            print(f"⚠️ Aucune texture trouvée dans: {self.get_category_texture_path(category)}")
            print(f"🎨 Matériau procédural créé pour {category}")
            material = self.create_procedural_material(mat, category, zone_type, height)
        
        print(f"🏗️ Matériau créé: {mat_name} (catégorie: {category})")
        return material
    
    def create_textured_material(self, mat, texture_path, category, zone_type, building_height=None):
        """Crée un matériau avec texture d'image - SYSTÈME MULTI-ÉTAGES"""
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
            print(f"✅ Image chargée: {os.path.basename(texture_path)}")
        except:
            print(f"❌ Erreur chargement texture: {texture_path}")
            return self.create_procedural_material(mat, category, zone_type, 0)
        
        # Nœud de mapping pour contrôler la répétition multi-étages
        mapping = nodes.new(type='ShaderNodeMapping')
        coord = nodes.new(type='ShaderNodeTexCoord')
        
        # CALCUL INTELLIGENT MULTI-ÉTAGES
        # Chaque fichier texture contient 4 étages
        etages_par_texture = 4
        hauteur_etage_standard = 3.0  # 3 mètres par étage
        
        if building_height:
            # Calculer le nombre d'étages réel du bâtiment
            nb_etages_building = max(1, building_height / hauteur_etage_standard)
            
            # Calculer combien de fois répéter la texture verticalement
            repetitions_verticales = nb_etages_building / etages_par_texture
            
            print(f"🏗️ Bâtiment {building_height:.1f}m = {nb_etages_building:.1f} étages")
            print(f"🔄 Répétitions texture: {repetitions_verticales:.2f}")
        else:
            # Valeurs par défaut selon la catégorie
            if category == 'skyscraper':
                repetitions_verticales = 15.0  # ~60 étages
            elif category == 'midrise':
                repetitions_verticales = 3.0   # ~12 étages
            elif category == 'commercial':
                repetitions_verticales = 2.0   # ~8 étages
            else:
                repetitions_verticales = 1.0   # ~4 étages
        
        # Paramètres de mapping optimisés pour les façades
        mapping.inputs['Scale'].default_value = (1.0, repetitions_verticales, 1.0)
        
        # Paramètres matériau selon la catégorie
        if category == 'skyscraper':
            bsdf.inputs['Metallic'].default_value = 0.8
            bsdf.inputs['Roughness'].default_value = 0.2
            print(f"🏢 Matériau gratte-ciel: métallique brillant")
        elif category == 'commercial':
            bsdf.inputs['Metallic'].default_value = 0.3
            bsdf.inputs['Roughness'].default_value = 0.6
            print(f"🏪 Matériau commercial: semi-brillant")
        elif category == 'residential':
            bsdf.inputs['Metallic'].default_value = 0.1
            bsdf.inputs['Roughness'].default_value = 0.8
            print(f"🏠 Matériau résidentiel: mat")
        else:
            bsdf.inputs['Metallic'].default_value = 0.2
            bsdf.inputs['Roughness'].default_value = 0.7
            print(f"🏗️ Matériau standard")
        
        # Connexions du système de nodes
        links.new(coord.outputs['UV'], mapping.inputs['Vector'])
        links.new(mapping.outputs['Vector'], img_texture.inputs['Vector'])
        links.new(img_texture.outputs['Color'], bsdf.inputs['Base Color'])
        links.new(bsdf.outputs['BSDF'], output.inputs['Surface'])
        
        # Positionnement des nœuds pour clarté
        output.location = (400, 0)
        bsdf.location = (200, 0)
        img_texture.location = (0, 0)
        mapping.location = (-200, 0)
        coord.location = (-400, 0)
        
        print(f"🎨 Matériau multi-étages créé avec {repetitions_verticales:.1f}x répétition verticale")
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


class TokyoRoadTextureSystem:
    """Système de textures avancé pour routes et trottoirs Tokyo"""
    
    def __init__(self, base_texture_path):
        self.base_path = base_texture_path
        self.asphalt_texture_path = os.path.join(base_texture_path, "roads", "asphalt_quad.jpg")  # Texture avec 4 zones
        self.normal_map_path = os.path.join(base_texture_path, "roads", "asphalt_normal.jpg")
        self.specular_map_path = os.path.join(base_texture_path, "roads", "asphalt_specular.jpg")
        
        # Configuration des zones de texture (UV mapping)
        self.texture_zones = {
            'road_center': {
                'uv_offset': (0.0, 0.5),     # Haut gauche
                'uv_scale': (0.5, 0.5),     # Taille de zone
                'description': 'Centre route - asphalte uni'
            },
            'road_border': {
                'uv_offset': (0.5, 0.0),     # Bas droite  
                'uv_scale': (0.5, 0.5),     # Ligne blanche parallèle au trottoir
                'description': 'Bords route - ligne blanche'
            },
            'sidewalk_concrete': {
                'uv_offset': (0.5, 0.5),     # Haut droite
                'uv_scale': (0.5, 0.5),     # Texture trottoir 1
                'description': 'Trottoir béton'
            },
            'sidewalk_tiles': {
                'uv_offset': (0.0, 0.0),     # Bas gauche
                'uv_scale': (0.5, 0.5),     # Texture trottoir 2
                'description': 'Trottoir carrelage'
            }
        }
    
    def create_road_material(self, road_type="center", material_name="Tokyo_Road"):
        """Crée un matériau de route avec mapping UV spécifique"""
        
        # Créer le matériau
        mat = bpy.data.materials.new(name=material_name)
        mat.use_nodes = True
        nodes = mat.node_tree.nodes
        links = mat.node_tree.links
        nodes.clear()
        
        # Nœuds principaux
        output = nodes.new(type='ShaderNodeOutputMaterial')
        bsdf = nodes.new(type='ShaderNodeBsdfPrincipled')
        
        # Vérifier si la texture existe
        if not os.path.exists(self.asphalt_texture_path):
            print(f"⚠️ Texture route non trouvée: {self.asphalt_texture_path}")
            return self._create_procedural_road_material(mat, road_type)
        
        # Nœud texture principale
        img_texture = nodes.new(type='ShaderNodeTexImage')
        try:
            img = bpy.data.images.load(self.asphalt_texture_path)
            img_texture.image = img
        except:
            print(f"❌ Erreur chargement texture route")
            return self._create_procedural_road_material(mat, road_type)
        
        # Nœuds de mapping et coordonnées
        mapping = nodes.new(type='ShaderNodeMapping')
        coord = nodes.new(type='ShaderNodeTexCoord')
        
        # Configuration selon le type de route
        zone_config = self.texture_zones.get(road_type, self.texture_zones['road_center'])
        
        # Paramètres UV pour sélectionner la bonne zone de texture
        uv_offset_x, uv_offset_y = zone_config['uv_offset']
        uv_scale_x, uv_scale_y = zone_config['uv_scale']
        
        # Configuration du mapping pour sélectionner la zone
        mapping.inputs['Location'].default_value = (uv_offset_x, uv_offset_y, 0)
        mapping.inputs['Scale'].default_value = (uv_scale_x, uv_scale_y, 1)
        
        # Rotation pour les bords de route (ligne blanche parallèle)
        if road_type == 'road_border':
            mapping.inputs['Rotation'].default_value = (0, 0, 0)  # Ajuster si besoin
        
        # Normal map si disponible
        if os.path.exists(self.normal_map_path):
            normal_texture = nodes.new(type='ShaderNodeTexImage')
            normal_map = nodes.new(type='ShaderNodeNormalMap')
            
            try:
                normal_img = bpy.data.images.load(self.normal_map_path)
                normal_texture.image = normal_img
                normal_img.colorspace_settings.name = 'Non-Color'
                
                # Même mapping que la texture principale
                mapping_normal = nodes.new(type='ShaderNodeMapping')
                coord_normal = nodes.new(type='ShaderNodeTexCoord')
                
                mapping_normal.inputs['Location'].default_value = (uv_offset_x, uv_offset_y, 0)
                mapping_normal.inputs['Scale'].default_value = (uv_scale_x, uv_scale_y, 1)
                
                # Connexions normal map
                links.new(coord_normal.outputs['UV'], mapping_normal.inputs['Vector'])
                links.new(mapping_normal.outputs['Vector'], normal_texture.inputs['Vector'])
                links.new(normal_texture.outputs['Color'], normal_map.inputs['Color'])
                links.new(normal_map.outputs['Normal'], bsdf.inputs['Normal'])
                
                print(f"✅ Normal map ajoutée pour {road_type}")
            except:
                print(f"⚠️ Erreur chargement normal map")
        
        # Specular map si disponible
        if os.path.exists(self.specular_map_path):
            specular_texture = nodes.new(type='ShaderNodeTexImage')
            
            try:
                specular_img = bpy.data.images.load(self.specular_map_path)
                specular_texture.image = specular_img
                specular_img.colorspace_settings.name = 'Non-Color'
                
                # Même mapping que la texture principale
                mapping_spec = nodes.new(type='ShaderNodeMapping')
                coord_spec = nodes.new(type='ShaderNodeTexCoord')
                
                mapping_spec.inputs['Location'].default_value = (uv_offset_x, uv_offset_y, 0)
                mapping_spec.inputs['Scale'].default_value = (uv_scale_x, uv_scale_y, 1)
                
                # Connexions specular
                links.new(coord_spec.outputs['UV'], mapping_spec.inputs['Vector'])
                links.new(mapping_spec.outputs['Vector'], specular_texture.inputs['Vector'])
                links.new(specular_texture.outputs['Color'], bsdf.inputs['Specular'])
                
                print(f"✅ Specular map ajoutée pour {road_type}")
            except:
                print(f"⚠️ Erreur chargement specular map")
        
        # Paramètres matériau selon le type
        if road_type in ['road_center', 'road_border']:
            # Route asphalte
            bsdf.inputs['Roughness'].default_value = 0.9
            bsdf.inputs['Specular'].default_value = 0.2
            bsdf.inputs['Metallic'].default_value = 0.0
        else:
            # Trottoir béton/carrelage
            bsdf.inputs['Roughness'].default_value = 0.8
            bsdf.inputs['Specular'].default_value = 0.3
            bsdf.inputs['Metallic'].default_value = 0.0
        
        # Connexions principales
        links.new(coord.outputs['UV'], mapping.inputs['Vector'])
        links.new(mapping.outputs['Vector'], img_texture.inputs['Vector'])
        links.new(img_texture.outputs['Color'], bsdf.inputs['Base Color'])
        links.new(bsdf.outputs['BSDF'], output.inputs['Surface'])
        
        # Positionnement des nœuds
        output.location = (400, 0)
        bsdf.location = (200, 0)
        img_texture.location = (0, 100)
        mapping.location = (-200, 100)
        coord.location = (-400, 100)
        
        print(f"🛣️ Matériau route créé: {road_type} - {zone_config['description']}")
        return mat
    
    def _create_procedural_road_material(self, mat, road_type):
        """Matériau de route procédural de fallback"""
        nodes = mat.node_tree.nodes
        links = mat.node_tree.links
        nodes.clear()
        
        output = nodes.new(type='ShaderNodeOutputMaterial')
        bsdf = nodes.new(type='ShaderNodeBsdfPrincipled')
        
        # Couleurs selon le type
        if road_type in ['road_center', 'road_border']:
            # Asphalte gris foncé
            bsdf.inputs['Base Color'].default_value = (0.15, 0.15, 0.15, 1.0)
        else:
            # Trottoir gris clair
            bsdf.inputs['Base Color'].default_value = (0.6, 0.6, 0.6, 1.0)
        
        bsdf.inputs['Roughness'].default_value = 0.9
        bsdf.inputs['Specular'].default_value = 0.1
        
        links.new(bsdf.outputs['BSDF'], output.inputs['Surface'])
        
        print(f"🛣️ Matériau route procédural: {road_type}")
        return mat
    
    def create_sidewalk_material(self, sidewalk_type="concrete"):
        """Crée un matériau de trottoir spécifique"""
        if sidewalk_type == "concrete":
            return self.create_road_material("sidewalk_concrete", "Tokyo_Sidewalk_Concrete")
        else:
            return self.create_road_material("sidewalk_tiles", "Tokyo_Sidewalk_Tiles")
    
    def setup_road_texture_folders(self):
        """Crée la structure de dossiers pour les textures de routes"""
        road_folder = os.path.join(self.base_path, "roads")
        os.makedirs(road_folder, exist_ok=True)
        
        # Créer fichier README
        readme_path = os.path.join(road_folder, "README_ROADS.txt")
        with open(readme_path, 'w') as f:
            f.write("DOSSIER TEXTURES ROUTES TOKYO\n")
            f.write("=" * 30 + "\n\n")
            f.write("Fichiers nécessaires:\n")
            f.write("• asphalt_quad.jpg - Texture principale avec 4 zones:\n")
            f.write("  - Haut gauche: Centre route (asphalte uni)\n")
            f.write("  - Bas droite: Bords route (ligne blanche parallèle)\n")
            f.write("  - Haut droite: Trottoir béton\n")
            f.write("  - Bas gauche: Trottoir carrelage\n\n")
            f.write("• asphalt_normal.jpg - Normal map\n")
            f.write("• asphalt_specular.jpg - Specular map\n\n")
            f.write("Taille recommandée: 2048x2048 ou 4096x4096\n")
            f.write("Format: JPG, PNG, EXR\n")
        
        print(f"📁 Dossier routes créé: {road_folder}")
        return road_folder


# Instance globale du système
tokyo_texture_system = TokyoTextureSystem()

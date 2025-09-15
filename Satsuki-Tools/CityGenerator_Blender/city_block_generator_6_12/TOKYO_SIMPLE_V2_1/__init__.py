bl_info = {
    "name": "Tokyo City Generator v2.1.8",
    "author": "Tokyo Urban Designer", 
    "version": (2, 1, 8),
    "blender": (4, 0, 0),
    "location": "View3D > Sidebar > CityGen",
    "description": "Complete Tokyo city generator with 8 building types and fixed sidewalks",
    "category": "Add Mesh",
}

import bpy
from bpy.props import IntProperty, FloatProperty, EnumProperty, BoolProperty
from bpy.types import Operator, Panel
import bmesh
import mathutils
import random
import math

# ===================================================================
# PROPRIÉTÉS SIMPLES
# ===================================================================

class TokyoSimpleProperties(bpy.types.PropertyGroup):
    """Propriétés simplifiées - seulement l'essentiel !"""
    
    # PARAMÈTRES DE BASE (4 seulement !)
    city_size: IntProperty(
        name="City Size", 
        description="Size of the city (3=small, 7=large)",
        default=5, min=3, max=10
    )
    
    building_height: EnumProperty(
        name="Building Style",
        description="Overall building height style",
        items=[
            ('LOW', "Low Rise", "Small buildings (3-15m) - Residential style"),
            ('MIXED', "Mixed", "Varied heights (5-40m) - Realistic Tokyo"),
            ('HIGH', "High Rise", "Tall buildings (15-60m) - Business district"),
        ],
        default='MIXED'
    )
    
    density: FloatProperty(
        name="Density",
        description="How packed the city is",
        default=0.8, min=0.3, max=1.0, subtype='FACTOR'
    )
    
    use_textures: BoolProperty(
        name="Better Materials",
        description="Use improved materials (slower but prettier)",
        default=True
    )

# ===================================================================
# GÉNÉRATEUR SIMPLE ET EFFICACE
# ===================================================================

class TOKYO_SIMPLE_OT_generate(Operator):
    """Generate Tokyo city - Simple and effective!"""
    bl_idname = "tokyo_simple.generate"
    bl_label = "Generate Tokyo City"
    bl_options = {'REGISTER', 'UNDO'}
    
    def execute(self, context):
        props = context.scene.tokyo_simple
        
        # Nettoyer la scène
        self.clear_scene()
        
        # Générer la ville
        result = self.generate_tokyo_city(
            size=props.city_size,
            style=props.building_height,
            density=props.density,
            use_materials=props.use_textures
        )
        
        self.report({'INFO'}, 
            f"Tokyo city generated! {result['buildings']} buildings, {result['roads']} roads")
        
        return {'FINISHED'}
    
    def clear_scene(self):
        """Supprimer les objets Tokyo existants"""
        prefixes = ["Tokyo_Building_", "Tokyo_Road_", "Tokyo_Sidewalk_"]
        for obj in list(bpy.data.objects):
            if any(obj.name.startswith(prefix) for prefix in prefixes):
                bpy.data.objects.remove(obj, do_unlink=True)
    
    def generate_tokyo_city(self, size, style, density, use_materials):
        """Générateur principal - simple et efficace"""
        
        print(f"🏙️ Generating Tokyo city {size}x{size} - Style: {style}")
        
        block_size = 16.0  # Taille des blocs
        road_width = 4.0   # Largeur des routes
        
        buildings = []
        roads = []
        
        # ÉTAPE 1: Créer les routes AVANT les bâtiments
        roads = self.create_road_network(size, block_size, road_width)
        
        # ÉTAPE 2: Créer les bâtiments dans les espaces libres avec les vraies largeurs de routes
        main_road_width = road_width * 1.5  # 6.0
        secondary_road_width = road_width * 0.8  # 3.2
        buildings = self.create_buildings(size, block_size, main_road_width, secondary_road_width, style, density, use_materials)
        
        return {
            'buildings': len(buildings),
            'roads': len(roads)
        }
    
    def create_road_network(self, size, block_size, road_width):
        """Créer le réseau de routes varié avec trottoirs intelligents"""
        roads = []
        sidewalks = []
        
        # Largeurs de routes variées pour plus de réalisme
        main_road_width = road_width * 1.5  # Routes principales plus larges
        secondary_road_width = road_width * 0.8  # Routes secondaires plus étroites
        
        # Stocker les positions des intersections pour éviter les chevauchements
        intersections = []
        for i in range(size + 1):
            for j in range(size + 1):
                x = i * block_size - (size * block_size) / 2
                y = j * block_size - (size * block_size) / 2
                intersections.append((x, y))
        
        # Routes horizontales avec variation
        for i in range(size + 1):
            y = i * block_size - (size * block_size) / 2
            
            # Alterner entre routes principales et secondaires
            is_main_road = (i == 0 or i == size or i == size // 2)
            current_width = main_road_width if is_main_road else secondary_road_width
            
            # Créer la route
            bpy.ops.mesh.primitive_cube_add(
                size=1,
                location=(0, y, 0.05)
            )
            road = bpy.context.active_object
            road.scale = (size * block_size + current_width, current_width, 0.1)
            road.name = f"Tokyo_Road_H_{i}_{'Main' if is_main_road else 'Sec'}"
            
            bpy.ops.object.transform_apply(scale=True)
            self.apply_road_material(road, is_main_road)
            roads.append(road)
        
        # Routes verticales avec variation
        for i in range(size + 1):
            x = i * block_size - (size * block_size) / 2
            
            is_main_road = (i == 0 or i == size or i == size // 2)
            current_width = main_road_width if is_main_road else secondary_road_width
            
            # Créer la route
            bpy.ops.mesh.primitive_cube_add(
                size=1,
                location=(x, 0, 0.05)
            )
            road = bpy.context.active_object
            road.scale = (current_width, size * block_size + current_width, 0.1)
            road.name = f"Tokyo_Road_V_{i}_{'Main' if is_main_road else 'Sec'}"
            
            bpy.ops.object.transform_apply(scale=True)
            self.apply_road_material(road, is_main_road)
            roads.append(road)
        
        # Créer trottoirs intelligents qui évitent les intersections
        self.create_smart_sidewalks(size, block_size, main_road_width, secondary_road_width, intersections, sidewalks)
        
        # Ajouter les trottoirs aux intersections (coins)
        self.create_intersection_sidewalks(size, block_size, main_road_width, secondary_road_width, sidewalks)
        
        # Ajouter une seule diagonale utile pour les grandes villes
        if size >= 6:
            self.add_single_diagonal(size, block_size, roads)
        
        return roads + sidewalks
    
    def create_smart_sidewalks(self, size, block_size, main_road_width, secondary_road_width, intersections, sidewalks):
        """Créer des trottoirs qui évitent les chevauchements aux carrefours"""
        sidewalk_width = 1.5
        intersection_margin = 3.0  # Marge autour des intersections
        
        # Trottoirs horizontaux (le long des routes horizontales)
        for i in range(size + 1):
            y = i * block_size - (size * block_size) / 2
            is_main_road = (i == 0 or i == size or i == size // 2)
            current_width = main_road_width if is_main_road else secondary_road_width
            
            # Créer segments de trottoirs entre les intersections
            for j in range(size):
                segment_start_x = j * block_size - (size * block_size) / 2 + intersection_margin
                segment_end_x = (j + 1) * block_size - (size * block_size) / 2 - intersection_margin
                segment_center_x = (segment_start_x + segment_end_x) / 2
                segment_length = segment_end_x - segment_start_x
                
                if segment_length > 2:  # Seulement si le segment est assez long
                    for side in [-1, 1]:  # Deux côtés de la route
                        sidewalk_y = y + side * (current_width/2 + sidewalk_width/2)
                        
                        bpy.ops.mesh.primitive_cube_add(
                            size=1,
                            location=(segment_center_x, sidewalk_y, 0.15)
                        )
                        sidewalk = bpy.context.active_object
                        sidewalk.scale = (segment_length, sidewalk_width, 0.2)
                        sidewalk.name = f"Tokyo_Sidewalk_H_{i}_{j}_{side}"
                        
                        bpy.ops.object.transform_apply(scale=True)
                        self.apply_sidewalk_material(sidewalk)
                        sidewalks.append(sidewalk)
        
        # Trottoirs verticaux (le long des routes verticales)
        for i in range(size + 1):
            x = i * block_size - (size * block_size) / 2
            is_main_road = (i == 0 or i == size or i == size // 2)
            current_width = main_road_width if is_main_road else secondary_road_width
            
            # Créer segments de trottoirs entre les intersections
            for j in range(size):
                segment_start_y = j * block_size - (size * block_size) / 2 + intersection_margin
                segment_end_y = (j + 1) * block_size - (size * block_size) / 2 - intersection_margin
                segment_center_y = (segment_start_y + segment_end_y) / 2
                segment_length = segment_end_y - segment_start_y
                
                if segment_length > 2:  # Seulement si le segment est assez long
                    for side in [-1, 1]:
                        sidewalk_x = x + side * (current_width/2 + sidewalk_width/2)
                        
                        bpy.ops.mesh.primitive_cube_add(
                            size=1,
                            location=(sidewalk_x, segment_center_y, 0.15)
                        )
                        sidewalk = bpy.context.active_object
                        sidewalk.scale = (sidewalk_width, segment_length, 0.2)
                        sidewalk.name = f"Tokyo_Sidewalk_V_{i}_{j}_{side}"
                        
                        bpy.ops.object.transform_apply(scale=True)
                        self.apply_sidewalk_material(sidewalk)
                        sidewalks.append(sidewalk)
    
    def create_intersection_sidewalks(self, size, block_size, main_road_width, secondary_road_width, sidewalks):
        """Créer des trottoirs aux coins des intersections pour combler les espaces vides"""
        sidewalk_width = 1.5
        intersection_margin = 3.0
        
        # Créer des coins de trottoirs à chaque intersection
        for i in range(size + 1):
            for j in range(size + 1):
                x = j * block_size - (size * block_size) / 2
                y = i * block_size - (size * block_size) / 2
                
                # Déterminer les largeurs des routes à cette intersection
                is_main_road_h = (i == 0 or i == size or i == size // 2)
                is_main_road_v = (j == 0 or j == size or j == size // 2)
                
                current_width_h = main_road_width if is_main_road_h else secondary_road_width
                current_width_v = main_road_width if is_main_road_v else secondary_road_width
                
                # Créer 4 coins de trottoirs à chaque intersection
                corner_positions = [
                    (1, 1),   # Coin supérieur droit
                    (1, -1),  # Coin inférieur droit  
                    (-1, 1),  # Coin supérieur gauche
                    (-1, -1)  # Coin inférieur gauche
                ]
                
                for h_side, v_side in corner_positions:
                    # Position du coin
                    corner_x = x + h_side * (current_width_v/2 + sidewalk_width/2)
                    corner_y = y + v_side * (current_width_h/2 + sidewalk_width/2)
                    
                    # Créer le coin de trottoir
                    bpy.ops.mesh.primitive_cube_add(
                        size=1,
                        location=(corner_x, corner_y, 0.15)
                    )
                    corner_sidewalk = bpy.context.active_object
                    corner_sidewalk.scale = (sidewalk_width, sidewalk_width, 0.2)
                    corner_sidewalk.name = f"Tokyo_Sidewalk_Corner_{i}_{j}_{h_side}_{v_side}"
                    
                    bpy.ops.object.transform_apply(scale=True)
                    self.apply_sidewalk_material(corner_sidewalk)
                    sidewalks.append(corner_sidewalk)
    
    def add_single_diagonal(self, size, block_size, roads):
        """Ajouter une seule route diagonale utile"""
        # Une seule diagonale 45° qui traverse la ville
        start_x = -size * block_size / 2
        start_y = -size * block_size / 2
        end_x = size * block_size / 2
        end_y = size * block_size / 2
        
        center_x = (start_x + end_x) / 2
        center_y = (start_y + end_y) / 2
        length = math.sqrt((end_x - start_x)**2 + (end_y - start_y)**2)
        angle = math.atan2(end_y - start_y, end_x - start_x)
        
        bpy.ops.mesh.primitive_cube_add(size=1, location=(center_x, center_y, 0.05))
        diagonal_road = bpy.context.active_object
        diagonal_road.scale = (length, 3.0, 0.1)  # Largeur modérée
        diagonal_road.rotation_euler = (0, 0, angle)
        diagonal_road.name = "Tokyo_Road_Diagonal_Main"
        bpy.ops.object.transform_apply(scale=True)
        self.apply_road_material(diagonal_road, False)  # Route secondaire
        roads.append(diagonal_road)
    
    def create_buildings(self, size, block_size, main_road_width, secondary_road_width, style, density, use_materials):
        """Créer différents types de bâtiments avec formes variées"""
        buildings = []
        
        # Configuration des hauteurs selon le style
        height_configs = {
            'LOW': {'min': 3, 'max': 15, 'avg': 8},
            'MIXED': {'min': 5, 'max': 40, 'avg': 18},
            'HIGH': {'min': 15, 'max': 60, 'avg': 30}
        }
        
        config = height_configs[style]
        
        # Types de bâtiments disponibles
        building_types = [
            'residential',  # Immeubles résidentiels
            'office',       # Bureaux modernes  
            'commercial',   # Centres commerciaux
            'tower',        # Tours élancées
            'hotel',        # Hôtels
            'mixed_use',    # Usage mixte
            'warehouse',    # Entrepôts/usines
            'school'        # Écoles/institutions
        ]
        
        # Créer les bâtiments bloc par bloc
        for grid_x in range(size):
            for grid_y in range(size):
                
                # Position du centre du bloc
                center_x = grid_x * block_size - (size * block_size) / 2 + block_size / 2
                center_y = grid_y * block_size - (size * block_size) / 2 + block_size / 2
                
                # Déterminer la largeur de route à cette position
                # Les routes horizontales et verticales ont des largeurs différentes
                max_road_width = max(main_road_width, secondary_road_width)
                
                # Zone disponible pour les bâtiments - VRAIMENT proche des trottoirs
                sidewalk_width = 1.5  # Même valeur que dans create_smart_sidewalks
                building_margin = 0.3  # Marge minimale entre bâtiment et trottoir
                
                total_road_space = max_road_width + sidewalk_width * 2 + building_margin * 2
                available_width = block_size - total_road_space
                available_depth = block_size - total_road_space
                
                if available_width < 1 or available_depth < 1:
                    print(f"⚠️ Bloc {grid_x},{grid_y} trop petit: {available_width:.1f}x{available_depth:.1f}")
                    continue
                
                # Éviter seulement la diagonale principale si elle existe
                is_on_main_diagonal = False
                if size >= 6:
                    diag_tolerance = block_size / 4
                    if abs((center_y) - (center_x)) < diag_tolerance:
                        is_on_main_diagonal = True
                
                density_modifier = 0.7 if is_on_main_diagonal else 1.0
                buildings_per_block = max(2, int(10 * density * density_modifier))  # Plus de bâtiments
                
                print(f"📍 Bloc {grid_x},{grid_y}: {buildings_per_block} bâtiments sur {available_width:.1f}x{available_depth:.1f}m")
                
                # Déterminer le type de quartier selon la position
                center_distance = math.sqrt((grid_x - size/2)**2 + (grid_y - size/2)**2)
                max_distance = math.sqrt((size/2)**2 + (size/2)**2)
                center_factor = 1.0 - (center_distance / max_distance)
                
                for i in range(buildings_per_block):
                    
                    # Choisir le type de bâtiment selon la zone
                    building_type = self.choose_building_type(center_factor, style, grid_x, grid_y, size)
                    print(f"  🏢 Bâtiment {i+1}: {building_type} (center_factor: {center_factor:.2f})")
                    
                    # Placement en grille pour optimiser l'espace
                    if buildings_per_block == 1:
                        offset_x, offset_y = 0, 0
                    elif buildings_per_block <= 4:
                        row, col = i // 2, i % 2
                        offset_x = (col - 0.5) * available_width / 3
                        offset_y = (row - 0.5) * available_depth / 3
                    else:
                        row, col = i // 3, i % 3
                        offset_x = (col - 1) * available_width / 4
                        offset_y = (row - 1) * available_depth / 4
                    
                    # Ajouter variation
                    offset_x += random.uniform(-available_width/8, available_width/8)
                    offset_y += random.uniform(-available_depth/8, available_depth/8)
                    
                    building_x = center_x + offset_x
                    building_y = center_y + offset_y
                    
                    # Créer le bâtiment selon son type
                    building = self.create_building_by_type(
                        building_type, building_x, building_y, 
                        buildings_per_block, config, center_factor, 
                        style, grid_x, grid_y, i, use_materials
                    )
                    
                    if building:
                        buildings.append(building)
        
        return buildings
    
    def choose_building_type(self, center_factor, style, grid_x, grid_y, size):
        """Choisir le type de bâtiment selon la zone et le style"""
        
        # Centre-ville : plus de bureaux et tours
        if center_factor > 0.7:
            if style == 'HIGH':
                return random.choice(['tower', 'office', 'hotel', 'mixed_use'])
            else:
                return random.choice(['office', 'commercial', 'hotel'])
        
        # Zone intermédiaire : mixte
        elif center_factor > 0.4:
            if style == 'LOW':
                return random.choice(['residential', 'commercial', 'school'])
            else:
                return random.choice(['residential', 'office', 'commercial', 'mixed_use'])
        
        # Périphérie : plus résidentiel et industriel
        else:
            if grid_x == 0 or grid_x == size-1 or grid_y == 0 or grid_y == size-1:
                return random.choice(['warehouse', 'residential', 'school'])
            else:
                return random.choice(['residential', 'commercial'])
    
    def create_building_by_type(self, building_type, x, y, buildings_per_block, config, center_factor, style, grid_x, grid_y, i, use_materials):
        """Créer un bâtiment selon son type avec forme et matériau appropriés"""
        
        # Dimensions et hauteur selon le type
        if building_type == 'tower':
            # Tours élancées
            width = random.uniform(3, 5)
            depth = random.uniform(3, 5)
            height = config['avg'] * (1.5 + center_factor)
            shape = 'tower'
            
        elif building_type == 'office':
            # Bureaux modernes - rectangulaires
            width = random.uniform(4, 8)
            depth = random.uniform(6, 10)
            height = config['avg'] * (0.8 + center_factor * 0.6)
            shape = 'rectangular'
            
        elif building_type == 'residential':
            # Immeubles résidentiels - carrés ou rectangulaires
            width = random.uniform(4, 7)
            depth = random.uniform(4, 7)
            height = config['avg'] * 0.7
            shape = 'cube'
            
        elif building_type == 'commercial':
            # Centres commerciaux - larges et bas
            width = random.uniform(6, 10)
            depth = random.uniform(6, 10)
            height = random.uniform(8, 15)
            shape = 'wide'
            
        elif building_type == 'hotel':
            # Hôtels - hauts et élégants
            width = random.uniform(5, 8)
            depth = random.uniform(5, 8)
            height = config['avg'] * (1.0 + center_factor * 0.5)
            shape = 'elegant'
            
        elif building_type == 'mixed_use':
            # Usage mixte - forme complexe
            width = random.uniform(4, 7)
            depth = random.uniform(4, 7)
            height = config['avg'] * 0.9
            shape = 'complex'
            
        elif building_type == 'warehouse':
            # Entrepôts - larges et bas
            width = random.uniform(8, 12)
            depth = random.uniform(6, 10)
            height = random.uniform(6, 12)
            shape = 'industrial'
            
        elif building_type == 'school':
            # Écoles - modérées
            width = random.uniform(6, 9)
            depth = random.uniform(4, 7)
            height = random.uniform(8, 16)
            shape = 'institutional'
        
        else:
            # Par défaut
            width = random.uniform(4, 6)
            depth = random.uniform(4, 6)
            height = config['avg']
            shape = 'cube'
        
        # Ajuster selon la densité du bloc
        if buildings_per_block > 4:
            width *= 0.8
            depth *= 0.8
        elif buildings_per_block > 2:
            width *= 0.9
            depth *= 0.9
        
        # Créer la forme du bâtiment
        building = self.create_building_shape(x, y, width, depth, height, shape, building_type, grid_x, grid_y, i)
        
        # Appliquer le matériau selon le type
        if use_materials:
            self.apply_building_material_by_type(building, building_type, height)
        else:
            self.apply_basic_material(building)
        
        return building
    
    def create_building_shape(self, x, y, width, depth, height, shape, building_type, grid_x, grid_y, i):
        """Créer différentes formes de bâtiments"""
        
        if shape == 'tower':
            # Tour élancée - plus haute que large
            bpy.ops.mesh.primitive_cube_add(size=1, location=(x, y, height/2))
            building = bpy.context.active_object
            building.scale = (width, depth, height)
            
        elif shape == 'complex':
            # Forme complexe - deux cubes
            # Base
            bpy.ops.mesh.primitive_cube_add(size=1, location=(x, y, height*0.3))
            building = bpy.context.active_object
            building.scale = (width, depth, height*0.6)
            
            # Tour au-dessus (plus petite)
            if random.random() > 0.5:  # 50% de chance d'avoir une tour
                bpy.ops.mesh.primitive_cube_add(size=1, location=(x + width*0.2, y, height*0.8))
                tower = bpy.context.active_object
                tower.scale = (width*0.6, depth*0.6, height*0.8)
                tower.name = f"Tokyo_Building_Tower_{grid_x}_{grid_y}_{i}"
            
        elif shape == 'wide':
            # Bâtiment large (commercial)
            bpy.ops.mesh.primitive_cube_add(size=1, location=(x, y, height/2))
            building = bpy.context.active_object
            building.scale = (width, depth, height)
            
        else:
            # Forme standard (cube, rectangular, etc.)
            bpy.ops.mesh.primitive_cube_add(size=1, location=(x, y, height/2))
            building = bpy.context.active_object
            building.scale = (width, depth, height)
        
        building.name = f"Tokyo_Building_{building_type}_{grid_x}_{grid_y}_{i}"
        bpy.ops.object.transform_apply(scale=True)
        
        return building
    
    def apply_road_material(self, obj, is_main_road=False):
        """Matériau varié pour les routes selon leur importance"""
        mat_name = "Tokyo_Road_Main" if is_main_road else "Tokyo_Road_Secondary"
        mat = bpy.data.materials.new(name=mat_name)
        mat.use_nodes = True
        
        bsdf = mat.node_tree.nodes["Principled BSDF"]
        
        if is_main_road:
            # Routes principales - asphalte plus foncé et lisse
            bsdf.inputs['Base Color'].default_value = (0.12, 0.12, 0.12, 1.0)
            bsdf.inputs['Roughness'].default_value = 0.7
        else:
            # Routes secondaires - asphalte plus clair et texturé
            bsdf.inputs['Base Color'].default_value = (0.18, 0.18, 0.18, 1.0)
            bsdf.inputs['Roughness'].default_value = 0.95
        
        obj.data.materials.append(mat)
    
    def apply_sidewalk_material(self, obj):
        """Matériau spécifique pour les trottoirs"""
        mat = bpy.data.materials.new(name="Tokyo_Sidewalk")
        mat.use_nodes = True
        
        bsdf = mat.node_tree.nodes["Principled BSDF"]
        # Couleur béton claire pour les trottoirs
        bsdf.inputs['Base Color'].default_value = (0.7, 0.7, 0.75, 1.0)
        bsdf.inputs['Roughness'].default_value = 0.8
        # Removed Specular property for Blender 4.0+ compatibility
        obj.data.materials.append(mat)
    
    def apply_building_material_by_type(self, obj, building_type, height):
        """Appliquer des matériaux simplifiés et compatibles selon le type de bâtiment"""
        
        # Matériaux simplifiés pour éviter les erreurs de compatibilité
        if building_type == 'tower':
            # Tours modernes - métal brillant
            mat = bpy.data.materials.new(name=f"Tokyo_Tower_{int(height)}m")
            mat.use_nodes = True
            bsdf = mat.node_tree.nodes["Principled BSDF"]
            bsdf.inputs['Base Color'].default_value = (0.4, 0.5, 0.7, 1.0)
            bsdf.inputs['Metallic'].default_value = 0.8
            bsdf.inputs['Roughness'].default_value = 0.2
            
        elif building_type == 'office':
            # Bureaux - bleu professionnel
            mat = bpy.data.materials.new(name=f"Tokyo_Office_{int(height)}m")
            mat.use_nodes = True
            bsdf = mat.node_tree.nodes["Principled BSDF"]
            bsdf.inputs['Base Color'].default_value = (0.5, 0.6, 0.8, 1.0)
            bsdf.inputs['Metallic'].default_value = 0.6
            bsdf.inputs['Roughness'].default_value = 0.3
            
        elif building_type == 'residential':
            # Résidentiel - béton et brique
            color_variants = [
                (0.8, 0.7, 0.6, 1.0),  # Beige
                (0.7, 0.6, 0.5, 1.0),  # Brun clair
                (0.9, 0.8, 0.7, 1.0),  # Crème
                (0.6, 0.5, 0.4, 1.0),  # Brun foncé
            ]
            mat = bpy.data.materials.new(name=f"Tokyo_Residential_{int(height)}m")
            mat.use_nodes = True
            bsdf = mat.node_tree.nodes["Principled BSDF"]
            bsdf.inputs['Base Color'].default_value = random.choice(color_variants)
            bsdf.inputs['Metallic'].default_value = 0.1
            bsdf.inputs['Roughness'].default_value = 0.8
            
        elif building_type == 'commercial':
            # Commercial - couleurs vives
            commercial_colors = [
                (0.9, 0.3, 0.2, 1.0),  # Rouge
                (0.2, 0.7, 0.3, 1.0),  # Vert
                (0.9, 0.7, 0.1, 1.0),  # Jaune
                (0.3, 0.5, 0.9, 1.0),  # Bleu
            ]
            mat = bpy.data.materials.new(name=f"Tokyo_Commercial_{int(height)}m")
            mat.use_nodes = True
            bsdf = mat.node_tree.nodes["Principled BSDF"]
            bsdf.inputs['Base Color'].default_value = random.choice(commercial_colors)
            bsdf.inputs['Metallic'].default_value = 0.3
            bsdf.inputs['Roughness'].default_value = 0.6
            
        elif building_type == 'hotel':
            # Hôtels - élégant
            hotel_colors = [
                (0.9, 0.9, 0.8, 1.0),  # Crème luxe
                (0.7, 0.6, 0.5, 1.0),  # Brun élégant
                (0.8, 0.8, 0.9, 1.0),  # Gris-bleu chic
            ]
            mat = bpy.data.materials.new(name=f"Tokyo_Hotel_{int(height)}m")
            mat.use_nodes = True
            bsdf = mat.node_tree.nodes["Principled BSDF"]
            bsdf.inputs['Base Color'].default_value = random.choice(hotel_colors)
            bsdf.inputs['Metallic'].default_value = 0.4
            bsdf.inputs['Roughness'].default_value = 0.4
            
        elif building_type == 'mixed_use':
            # Usage mixte - neutre
            mat = bpy.data.materials.new(name=f"Tokyo_Mixed_{int(height)}m")
            mat.use_nodes = True
            bsdf = mat.node_tree.nodes["Principled BSDF"]
            bsdf.inputs['Base Color'].default_value = (0.6, 0.6, 0.7, 1.0)
            bsdf.inputs['Metallic'].default_value = 0.5
            bsdf.inputs['Roughness'].default_value = 0.5
            
        elif building_type == 'warehouse':
            # Entrepôts - industriel
            industrial_colors = [
                (0.4, 0.4, 0.4, 1.0),  # Gris métallique
                (0.5, 0.3, 0.2, 1.0),  # Rouille
                (0.3, 0.4, 0.3, 1.0),  # Vert industriel
            ]
            mat = bpy.data.materials.new(name=f"Tokyo_Warehouse_{int(height)}m")
            mat.use_nodes = True
            bsdf = mat.node_tree.nodes["Principled BSDF"]
            bsdf.inputs['Base Color'].default_value = random.choice(industrial_colors)
            bsdf.inputs['Metallic'].default_value = 0.7
            bsdf.inputs['Roughness'].default_value = 0.9
            
        elif building_type == 'school':
            # Écoles - institutionnel
            institutional_colors = [
                (0.9, 0.8, 0.6, 1.0),  # Beige institutionnel
                (0.8, 0.9, 0.8, 1.0),  # Vert pâle
                (0.8, 0.8, 0.9, 1.0),  # Bleu pâle
            ]
            mat = bpy.data.materials.new(name=f"Tokyo_School_{int(height)}m")
            mat.use_nodes = True
            bsdf = mat.node_tree.nodes["Principled BSDF"]
            bsdf.inputs['Base Color'].default_value = random.choice(institutional_colors)
            bsdf.inputs['Metallic'].default_value = 0.2
            bsdf.inputs['Roughness'].default_value = 0.7
            
        else:
            # Type par défaut
            mat = bpy.data.materials.new(name=f"Tokyo_Default_{int(height)}m")
            mat.use_nodes = True
            bsdf = mat.node_tree.nodes["Principled BSDF"]
            bsdf.inputs['Base Color'].default_value = (0.7, 0.7, 0.7, 1.0)
            bsdf.inputs['Roughness'].default_value = 0.7
        
        # Variation de couleur pour éviter l'uniformité
        if hasattr(bsdf.inputs['Base Color'], 'default_value'):
            base_color = list(bsdf.inputs['Base Color'].default_value)
            for i in range(3):  # RGB seulement
                variation = random.uniform(0.9, 1.1)
                base_color[i] = min(1.0, base_color[i] * variation)
            bsdf.inputs['Base Color'].default_value = base_color
        
        obj.data.materials.append(mat)
    
    def apply_building_material(self, obj, height, style):
        """Matériau adapté selon la hauteur et le style"""
        
        # Déterminer le type de bâtiment selon la hauteur
        if height > 35:
            mat_type = "skyscraper"
            base_color = (0.6, 0.7, 0.9, 1.0)  # Bleu moderne
            metallic = 0.7
            roughness = 0.3
        elif height > 20:
            mat_type = "office"
            base_color = (0.7, 0.7, 0.8, 1.0)  # Gris professionnel
            metallic = 0.3
            roughness = 0.6
        elif height > 10:
            mat_type = "apartment"
            base_color = (0.8, 0.75, 0.7, 1.0)  # Beige résidentiel
            metallic = 0.1
            roughness = 0.8
        else:
            mat_type = "house"
            base_color = (0.9, 0.8, 0.7, 1.0)  # Brun chaleureux
            metallic = 0.05
            roughness = 0.9
        
        # Variation de couleur pour éviter l'uniformité
        color_variation = [random.uniform(0.85, 1.15) for _ in range(3)]
        varied_color = tuple(min(1.0, base_color[i] * color_variation[i]) for i in range(3)) + (1.0,)
        
        mat = bpy.data.materials.new(name=f"Tokyo_{mat_type}_{int(height)}m")
        mat.use_nodes = True
        
        bsdf = mat.node_tree.nodes["Principled BSDF"]
        bsdf.inputs['Base Color'].default_value = varied_color
        bsdf.inputs['Metallic'].default_value = metallic
        bsdf.inputs['Roughness'].default_value = roughness
        
        obj.data.materials.append(mat)
    
    def apply_basic_material(self, obj):
        """Matériau basique uniforme"""
        mat = bpy.data.materials.new(name="Tokyo_Basic_Building")
        mat.use_nodes = True
        
        bsdf = mat.node_tree.nodes["Principled BSDF"]
        bsdf.inputs['Base Color'].default_value = (0.8, 0.8, 0.8, 1.0)
        bsdf.inputs['Roughness'].default_value = 0.7
        
        obj.data.materials.append(mat)

# ===================================================================
# INTERFACE ULTRA-SIMPLE
# ===================================================================

class TOKYO_SIMPLE_PT_panel(Panel):
    """Panneau simple - 4 paramètres maximum !"""
    bl_label = "Tokyo City Generator"
    bl_idname = "TOKYO_SIMPLE_PT_panel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Tokyo'
    
    def draw(self, context):
        layout = self.layout
        props = context.scene.tokyo_simple
        
        # En-tête simple
        box = layout.box()
        box.label(text="🏙️ Tokyo Generator v2.1.8 STABLE", icon='MESH_CUBE')
        
        # Les 4 paramètres essentiels
        main_box = layout.box()
        main_box.label(text="Settings", icon='SETTINGS')
        
        col = main_box.column(align=True)
        col.prop(props, "city_size")
        col.prop(props, "building_height")
        col.prop(props, "density", slider=True)
        col.prop(props, "use_textures")
        
        # Bouton de génération - GROS et visible
        layout.separator()
        row = layout.row()
        row.scale_y = 2.0
        row.operator("tokyo_simple.generate", text="🏗️ Generate Tokyo City", icon='MESH_CUBE')
        
        # Bouton de nettoyage
        layout.separator()
        clear_row = layout.row()
        clear_row.operator("tokyo_simple.clear", text="🗑️ Clear City", icon='TRASH')

class TOKYO_SIMPLE_OT_clear(Operator):
    """Clear all Tokyo objects"""
    bl_idname = "tokyo_simple.clear"
    bl_label = "Clear Tokyo City"
    bl_options = {'REGISTER', 'UNDO'}
    
    def execute(self, context):
        prefixes = ["Tokyo_Building_", "Tokyo_Road_", "Tokyo_Sidewalk_"]
        count = 0
        
        for obj in list(bpy.data.objects):
            if any(obj.name.startswith(prefix) for prefix in prefixes):
                bpy.data.objects.remove(obj, do_unlink=True)
                count += 1
        
        self.report({'INFO'}, f"Cleared {count} Tokyo objects")
        return {'FINISHED'}

# ===================================================================
# ENREGISTREMENT
# ===================================================================

classes = [
    TokyoSimpleProperties,
    TOKYO_SIMPLE_OT_generate,
    TOKYO_SIMPLE_OT_clear,
    TOKYO_SIMPLE_PT_panel,
]

def register():
    print("🏙️ Enregistrement Tokyo Simple v2.1...")
    
    for cls in classes:
        bpy.utils.register_class(cls)
    
    bpy.types.Scene.tokyo_simple = bpy.props.PointerProperty(type=TokyoSimpleProperties)
    
    print("✅ Tokyo Simple v2.1 enregistré - Interface simplifiée !")

def unregister():
    print("🔄 Désenregistrement Tokyo Simple v2.1...")
    
    del bpy.types.Scene.tokyo_simple
    
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)
    
    print("✅ Tokyo Simple v2.1 désenregistré !")

if __name__ == "__main__":
    register()
bl_info = {
    "name": "Tokyo City Generator v2.1.9 - Organic Diagonals",
    "blender": (4, 0, 0),
    "category": "Add Mesh",
    "version": (2, 1, 9),
    "author": "Tokyo Team",
    "description": "Générateur de ville organique avec routes diagonales courtes et blocs variés"
}

import bpy
import bmesh
import random
import math
from bpy.types import Operator, Panel
from bpy.props import IntProperty, FloatProperty, EnumProperty, BoolProperty

class TOKYO_OT_generate_organic_city(Operator):
    """Générateur de ville organique avec diagonales courtes"""
    bl_idname = "tokyo.generate_organic_city"
    bl_label = "Générer Ville Organique"
    bl_options = {'REGISTER', 'UNDO'}
    
    def execute(self, context):
        self.clear_scene()
        props = context.scene.tokyo_props
        
        result = self.generate_organic_tokyo_city(
            props.city_size,
            props.city_style, 
            props.density,
            props.use_materials
        )
        
        self.report({'INFO'}, f"Ville générée: {result['buildings']} bâtiments, {result['roads']} routes, {result['diagonals']} diagonales")
        return {'FINISHED'}
    
    def clear_scene(self):
        """Nettoyer la scène"""
        bpy.ops.object.select_all(action='DESELECT')
        for obj in bpy.data.objects:
            if any(keyword in obj.name for keyword in ["Tokyo_", "Building", "Road", "Sidewalk"]):
                bpy.data.objects.remove(obj, do_unlink=True)
    
    def generate_organic_tokyo_city(self, size, style, density, use_materials):
        """Générateur principal avec ordre optimisé"""
        
        print(f"🏙️ Generating Organic Tokyo city {size}x{size} - Style: {style}")
        
        # Configuration de base avec variation
        base_block_size = 18.0
        main_road_width = 6.0
        secondary_road_width = 3.5
        
        # ORDRE OPTIMISÉ DE GÉNÉRATION
        # 1. Routes principales (grille de base)
        roads = self.create_base_road_network(size, base_block_size, main_road_width, secondary_road_width)
        
        # 2. Routes diagonales courtes AVANT tout le reste
        diagonal_roads = self.create_short_diagonal_network(size, base_block_size, secondary_road_width)
        
        # 3. Trottoirs qui s'adaptent aux routes ET diagonales
        sidewalks = self.create_adaptive_sidewalks(size, base_block_size, main_road_width, secondary_road_width, diagonal_roads)
        
        # 4. Blocs organiques (non uniformes)
        block_zones = self.create_organic_blocks(size, base_block_size, diagonal_roads)
        
        # 5. Bâtiments dans les blocs organiques
        buildings = self.create_organic_buildings(block_zones, style, density, use_materials)
        
        return {
            'buildings': len(buildings),
            'roads': len(roads),
            'diagonals': len(diagonal_roads),
            'sidewalks': len(sidewalks)
        }
    
    def create_base_road_network(self, size, block_size, main_road_width, secondary_road_width):
        """Créer le réseau de routes de base (grille)"""
        roads = []
        
        # Routes horizontales
        for i in range(size + 1):
            y = i * block_size - (size * block_size) / 2
            is_main_road = (i == 0 or i == size or i == size // 2)
            current_width = main_road_width if is_main_road else secondary_road_width
            
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
        
        # Routes verticales
        for i in range(size + 1):
            x = i * block_size - (size * block_size) / 2
            is_main_road = (i == 0 or i == size or i == size // 2)
            current_width = main_road_width if is_main_road else secondary_road_width
            
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
        
        return roads
    
    def create_short_diagonal_network(self, size, block_size, road_width):
        """Créer des routes diagonales courtes entre intersections adjacentes"""
        diagonal_roads = []
        
        print(f"🔄 Création diagonales courtes pour grille {size}x{size}")
        
        # Paramètres des diagonales
        diagonal_width = road_width * 0.8  # Plus fines que les routes secondaires
        
        # Créer diagonales courtes aléatoires
        num_diagonals = min(size * 2, 12)  # Limite raisonnable
        
        for i in range(num_diagonals):
            # Choisir deux intersections adjacentes aléatoirement
            start_i = random.randint(0, size - 1)
            start_j = random.randint(0, size - 1)
            
            # Direction aléatoire (diagonal)
            directions = [
                (1, 1),   # Nord-Est
                (1, -1),  # Sud-Est
                (-1, 1),  # Nord-Ouest
                (-1, -1)  # Sud-Ouest
            ]
            
            dx, dy = random.choice(directions)
            end_i = start_i + dx
            end_j = start_j + dy
            
            # Vérifier que la destination est dans la grille
            if 0 <= end_i <= size and 0 <= end_j <= size:
                
                # Calculer positions réelles
                start_x = start_i * block_size - (size * block_size) / 2
                start_y = start_j * block_size - (size * block_size) / 2
                end_x = end_i * block_size - (size * block_size) / 2
                end_y = end_j * block_size - (size * block_size) / 2
                
                # Position et orientation du segment diagonal
                center_x = (start_x + end_x) / 2
                center_y = (start_y + end_y) / 2
                length = math.sqrt((end_x - start_x)**2 + (end_y - start_y)**2)
                angle = math.atan2(end_y - start_y, end_x - start_x)
                
                # Créer le segment diagonal
                bpy.ops.mesh.primitive_cube_add(size=1, location=(center_x, center_y, 0.06))
                diagonal = bpy.context.active_object
                diagonal.scale = (length * 0.9, diagonal_width, 0.1)  # Légèrement plus court pour ne pas toucher les intersections
                diagonal.rotation_euler = (0, 0, angle)
                diagonal.name = f"Tokyo_Diagonal_Short_{i}_{start_i}_{start_j}_to_{end_i}_{end_j}"
                
                bpy.ops.object.transform_apply(scale=True)
                self.apply_diagonal_material(diagonal)
                diagonal_roads.append(diagonal)
                
                print(f"   ↗️ Diagonale {i}: ({start_i},{start_j}) → ({end_i},{end_j})")
        
        return diagonal_roads
    
    def create_adaptive_sidewalks(self, size, block_size, main_road_width, secondary_road_width, diagonal_roads):
        """Créer des trottoirs qui s'adaptent aux routes ET aux diagonales"""
        sidewalks = []
        sidewalk_width = 1.2
        
        print(f"🚶 Création trottoirs adaptatifs")
        
        # Analyser les positions des diagonales pour adaptation
        diagonal_positions = []
        for diag in diagonal_roads:
            diagonal_positions.append({
                'center': (diag.location.x, diag.location.y),
                'angle': diag.rotation_euler.z,
                'width': diag.scale.y if hasattr(diag, 'scale') else 3.0
            })
        
        # Créer trottoirs pour chaque bloc en évitant les diagonales
        for i in range(size):
            for j in range(size):
                # Position du centre du bloc
                block_center_x = (i + 0.5) * block_size - (size * block_size) / 2
                block_center_y = (j + 0.5) * block_size - (size * block_size) / 2
                
                # Créer trottoirs organiques autour du bloc
                self.create_organic_block_sidewalks(
                    block_center_x, block_center_y, 
                    block_size, sidewalk_width, 
                    diagonal_positions, sidewalks, 
                    i, j
                )
        
        return sidewalks
    
    def create_organic_block_sidewalks(self, center_x, center_y, block_size, sidewalk_width, diagonal_positions, sidewalks, i, j):
        """Créer des trottoirs organiques autour d'un bloc"""
        
        # Vérifier s'il y a des diagonales qui traversent ce bloc
        block_has_diagonal = False
        for diag_pos in diagonal_positions:
            dist = math.sqrt((diag_pos['center'][0] - center_x)**2 + (diag_pos['center'][1] - center_y)**2)
            if dist < block_size * 0.7:  # Diagonale traverse le bloc
                block_has_diagonal = True
                break
        
        if block_has_diagonal:
            # Créer des trottoirs fragmentés pour s'adapter aux diagonales
            self.create_fragmented_sidewalks(center_x, center_y, block_size, sidewalk_width, sidewalks, i, j)
        else:
            # Trottoirs rectangulaires standard
            self.create_standard_block_sidewalks(center_x, center_y, block_size, sidewalk_width, sidewalks, i, j)
    
    def create_fragmented_sidewalks(self, center_x, center_y, block_size, sidewalk_width, sidewalks, i, j):
        """Créer des trottoirs fragmentés pour blocs avec diagonales"""
        
        # Créer 4 segments de trottoirs plus petits au lieu d'un grand rectangle
        margin = block_size * 0.4
        segment_size = block_size * 0.2
        
        positions = [
            (center_x - margin, center_y - margin),  # Sud-Ouest
            (center_x + margin, center_y - margin),  # Sud-Est
            (center_x - margin, center_y + margin),  # Nord-Ouest
            (center_x + margin, center_y + margin),  # Nord-Est
        ]
        
        for idx, (x, y) in enumerate(positions):
            bpy.ops.mesh.primitive_cube_add(size=1, location=(x, y, 0.02))
            sidewalk = bpy.context.active_object
            sidewalk.scale = (segment_size, segment_size, 0.05)
            sidewalk.name = f"Tokyo_Sidewalk_Organic_{i}_{j}_{idx}"
            
            bpy.ops.object.transform_apply(scale=True)
            self.apply_sidewalk_material(sidewalk)
            sidewalks.append(sidewalk)
    
    def create_standard_block_sidewalks(self, center_x, center_y, block_size, sidewalk_width, sidewalks, i, j):
        """Créer des trottoirs rectangulaires standard"""
        
        # Trottoir principal autour du bloc
        sidewalk_size = block_size * 0.8
        
        bpy.ops.mesh.primitive_cube_add(size=1, location=(center_x, center_y, 0.02))
        sidewalk = bpy.context.active_object
        sidewalk.scale = (sidewalk_size, sidewalk_size, 0.05)
        sidewalk.name = f"Tokyo_Sidewalk_Standard_{i}_{j}"
        
        bpy.ops.object.transform_apply(scale=True)
        self.apply_sidewalk_material(sidewalk)
        sidewalks.append(sidewalk)
    
    def create_organic_blocks(self, size, base_block_size, diagonal_roads):
        """Créer des zones de blocs organiques (non uniformes)"""
        block_zones = []
        
        print(f"🏗️ Création blocs organiques")
        
        for i in range(size):
            for j in range(size):
                # Position de base du bloc
                base_x = (i + 0.5) * base_block_size - (size * base_block_size) / 2
                base_y = (j + 0.5) * base_block_size - (size * base_block_size) / 2
                
                # Variation de taille pour éviter l'uniformité
                size_variation = random.uniform(0.7, 1.3)
                block_width = base_block_size * size_variation * random.uniform(0.8, 1.2)
                block_height = base_block_size * size_variation * random.uniform(0.8, 1.2)
                
                # Légère rotation pour plus d'organicité
                rotation = random.uniform(-0.1, 0.1)  # Petite rotation en radians
                
                # Vérifier si une diagonale traverse ce bloc
                has_diagonal = self.block_intersects_diagonal(base_x, base_y, base_block_size, diagonal_roads)
                
                if has_diagonal:
                    # Créer plusieurs sous-blocs plus petits
                    sub_blocks = self.create_sub_blocks(base_x, base_y, block_width, block_height, i, j)
                    block_zones.extend(sub_blocks)
                else:
                    # Bloc unique avec variation
                    block_zone = {
                        'center_x': base_x + random.uniform(-2, 2),  # Légère variation de position
                        'center_y': base_y + random.uniform(-2, 2),
                        'width': block_width,
                        'height': block_height,
                        'rotation': rotation,
                        'grid_i': i,
                        'grid_j': j,
                        'type': 'standard'
                    }
                    block_zones.append(block_zone)
        
        return block_zones
    
    def block_intersects_diagonal(self, block_x, block_y, block_size, diagonal_roads):
        """Vérifier si un bloc est traversé par une diagonale"""
        for diag in diagonal_roads:
            dist = math.sqrt((diag.location.x - block_x)**2 + (diag.location.y - block_y)**2)
            if dist < block_size * 0.6:
                return True
        return False
    
    def create_sub_blocks(self, base_x, base_y, block_width, block_height, i, j):
        """Créer des sous-blocs pour les zones avec diagonales"""
        sub_blocks = []
        
        # Créer 2-4 sous-blocs au lieu d'un grand
        num_sub_blocks = random.randint(2, 4)
        
        for k in range(num_sub_blocks):
            # Position aléatoire autour du centre
            offset_x = random.uniform(-block_width * 0.3, block_width * 0.3)
            offset_y = random.uniform(-block_height * 0.3, block_height * 0.3)
            
            sub_block = {
                'center_x': base_x + offset_x,
                'center_y': base_y + offset_y,
                'width': block_width * random.uniform(0.3, 0.6),
                'height': block_height * random.uniform(0.3, 0.6),
                'rotation': random.uniform(-0.2, 0.2),
                'grid_i': i,
                'grid_j': j,
                'type': 'sub_block',
                'sub_id': k
            }
            sub_blocks.append(sub_block)
        
        return sub_blocks
    
    def create_organic_buildings(self, block_zones, style, density, use_materials):
        """Créer des bâtiments dans les zones de blocs organiques"""
        buildings = []
        
        print(f"🏢 Création bâtiments organiques")
        
        # Types de bâtiments avec probabilités
        building_types = ['residential', 'office', 'commercial', 'tower', 'hotel', 'mixed_use', 'warehouse', 'school']
        
        for zone in block_zones:
            # Décider si ce bloc aura des bâtiments
            if random.random() > density:
                continue
            
            # Nombre de bâtiments selon la taille du bloc
            area = zone['width'] * zone['height']
            max_buildings = max(1, int(area / 80))  # Densité adaptative
            num_buildings = random.randint(1, max_buildings)
            
            for b in range(num_buildings):
                # Position dans le bloc
                offset_x = random.uniform(-zone['width'] * 0.3, zone['width'] * 0.3)
                offset_y = random.uniform(-zone['height'] * 0.3, zone['height'] * 0.3)
                
                x = zone['center_x'] + offset_x
                y = zone['center_y'] + offset_y
                
                # Taille et hauteur variables
                building_width = random.uniform(4, 12)
                building_depth = random.uniform(4, 12)
                building_height = self.get_organic_building_height(zone, style)
                
                # Type de bâtiment selon la zone
                building_type = self.choose_building_type_for_zone(zone, building_types)
                
                # Créer le bâtiment
                building = self.create_organic_building_shape(
                    x, y, building_width, building_depth, building_height, 
                    building_type, zone, b
                )
                
                # Appliquer matériau
                if use_materials:
                    self.apply_building_material_by_type(building, building_type, building_height)
                else:
                    self.apply_basic_material(building)
                
                buildings.append(building)
        
        return buildings
    
    def get_organic_building_height(self, zone, style):
        """Calculer la hauteur d'un bâtiment selon la zone et le style"""
        base_heights = {
            'traditional': (8, 25),
            'modern': (15, 45), 
            'mixed': (10, 35),
            'futuristic': (20, 60)
        }
        
        min_h, max_h = base_heights.get(style, (10, 30))
        
        # Variation selon le type de zone
        if zone['type'] == 'sub_block':
            # Bâtiments plus bas dans les sous-blocs
            max_h *= 0.7
        
        # Variation aléatoire
        height = random.uniform(min_h, max_h)
        
        # Quelques gratte-ciels aléatoires
        if random.random() < 0.1:  # 10% de chance
            height *= random.uniform(1.5, 2.5)
        
        return height
    
    def choose_building_type_for_zone(self, zone, building_types):
        """Choisir le type de bâtiment selon la zone"""
        
        # Probabilités selon la position dans la grille
        grid_center_dist = math.sqrt(zone['grid_i']**2 + zone['grid_j']**2)
        
        if grid_center_dist < 2:
            # Centre-ville : plus de bureaux et tours
            weights = [0.1, 0.3, 0.2, 0.25, 0.1, 0.03, 0.01, 0.01]
        elif grid_center_dist < 4:
            # Zone intermédiaire : mixte
            weights = [0.25, 0.2, 0.15, 0.1, 0.15, 0.1, 0.03, 0.02]
        else:
            # Périphérie : plus résidentiel
            weights = [0.4, 0.1, 0.1, 0.05, 0.05, 0.15, 0.1, 0.05]
        
        return random.choices(building_types, weights=weights)[0]
    
    def create_organic_building_shape(self, x, y, width, depth, height, building_type, zone, building_index):
        """Créer la forme organique du bâtiment"""
        
        # Position légèrement variée
        z = height / 2
        
        bpy.ops.mesh.primitive_cube_add(size=1, location=(x, y, z))
        building = bpy.context.active_object
        building.scale = (width, depth, height)
        building.rotation_euler = (0, 0, zone['rotation'] + random.uniform(-0.05, 0.05))
        building.name = f"Tokyo_Building_{building_type}_{zone['grid_i']}_{zone['grid_j']}_{building_index}"
        
        bpy.ops.object.transform_apply(scale=True)
        
        return building
    
    def apply_building_material_by_type(self, obj, building_type, height):
        """Appliquer des matériaux distinctifs selon le type"""
        
        # Couleurs très distinctes pour voir la différence
        colors = {
            'tower': (0.1, 0.3, 0.8, 1.0),       # Bleu foncé
            'office': (0.6, 0.7, 0.9, 1.0),      # Bleu clair
            'residential': (0.9, 0.6, 0.3, 1.0), # Orange
            'commercial': (0.9, 0.2, 0.2, 1.0),  # Rouge vif
            'hotel': (0.9, 0.9, 0.2, 1.0),       # Jaune
            'mixed_use': (0.3, 0.8, 0.3, 1.0),   # Vert
            'warehouse': (0.5, 0.5, 0.5, 1.0),   # Gris
            'school': (0.8, 0.4, 0.8, 1.0)       # Violet
        }
        
        color = colors.get(building_type, (0.7, 0.7, 0.7, 1.0))
        
        # Variation légère pour éviter l'uniformité
        varied_color = [
            min(1.0, color[0] * random.uniform(0.8, 1.2)),
            min(1.0, color[1] * random.uniform(0.8, 1.2)),
            min(1.0, color[2] * random.uniform(0.8, 1.2)),
            1.0
        ]
        
        mat = bpy.data.materials.new(name=f"Organic_{building_type}_{int(height)}")
        mat.use_nodes = True
        bsdf = mat.node_tree.nodes["Principled BSDF"]
        bsdf.inputs['Base Color'].default_value = varied_color
        bsdf.inputs['Metallic'].default_value = 0.3
        bsdf.inputs['Roughness'].default_value = 0.7
        
        obj.data.materials.append(mat)
    
    def apply_basic_material(self, obj):
        """Matériau basique"""
        mat = bpy.data.materials.new(name="Organic_Basic")
        mat.use_nodes = True
        bsdf = mat.node_tree.nodes["Principled BSDF"]
        bsdf.inputs['Base Color'].default_value = (0.8, 0.8, 0.8, 1.0)
        obj.data.materials.append(mat)
    
    def apply_road_material(self, obj, is_main_road=False):
        """Matériau pour routes"""
        color = (0.3, 0.3, 0.3, 1.0) if is_main_road else (0.4, 0.4, 0.4, 1.0)
        mat = bpy.data.materials.new(name=f"Road_{'Main' if is_main_road else 'Secondary'}")
        mat.use_nodes = True
        bsdf = mat.node_tree.nodes["Principled BSDF"]
        bsdf.inputs['Base Color'].default_value = color
        bsdf.inputs['Roughness'].default_value = 0.9
        obj.data.materials.append(mat)
    
    def apply_diagonal_material(self, obj):
        """Matériau distinctif pour diagonales"""
        mat = bpy.data.materials.new(name="Diagonal_Road")
        mat.use_nodes = True
        bsdf = mat.node_tree.nodes["Principled BSDF"]
        bsdf.inputs['Base Color'].default_value = (0.8, 0.3, 0.1, 1.0)  # Orange pour être visible
        bsdf.inputs['Roughness'].default_value = 0.8
        obj.data.materials.append(mat)
    
    def apply_sidewalk_material(self, obj):
        """Matériau pour trottoirs"""
        mat = bpy.data.materials.new(name="Sidewalk")
        mat.use_nodes = True
        bsdf = mat.node_tree.nodes["Principled BSDF"]
        bsdf.inputs['Base Color'].default_value = (0.7, 0.7, 0.6, 1.0)
        bsdf.inputs['Roughness'].default_value = 0.8
        obj.data.materials.append(mat)

# Propriétés pour l'interface
class TokyoProperties(bpy.types.PropertyGroup):
    city_size: IntProperty(
        name="Taille",
        description="Taille de la grille (NxN)",
        default=5,
        min=3,
        max=10
    )
    
    city_style: EnumProperty(
        name="Style",
        description="Style architectural",
        items=[
            ('traditional', "Traditionnel", "Style japonais classique"),
            ('modern', "Moderne", "Architecture contemporaine"),
            ('mixed', "Mixte", "Mélange de styles"),
            ('futuristic', "Futuriste", "Architecture avant-gardiste")
        ],
        default='modern'
    )
    
    density: FloatProperty(
        name="Densité",
        description="Densité des bâtiments",
        default=0.8,
        min=0.3,
        max=1.0
    )
    
    use_materials: BoolProperty(
        name="Matériaux colorés",
        description="Utiliser des matériaux colorés par type",
        default=True
    )

class TOKYO_PT_organic_panel(Panel):
    """Panneau pour le générateur organique"""
    bl_label = "Tokyo Organic City v2.1.9"
    bl_idname = "TOKYO_PT_organic_panel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Tokyo'
    
    def draw(self, context):
        layout = self.layout
        props = context.scene.tokyo_props
        
        # Titre avec emoji
        layout.label(text="🏙️ Générateur Organique", icon='MESH_CUBE')
        
        # Paramètres principaux
        layout.prop(props, "city_size")
        layout.prop(props, "city_style")
        layout.prop(props, "density")
        layout.prop(props, "use_materials")
        
        # Bouton de génération
        layout.separator()
        row = layout.row(align=True)
        row.scale_y = 1.5
        row.operator("tokyo.generate_organic_city", text="🏗️ Générer Ville Organique", icon='ADD')
        
        # Infos
        layout.separator()
        box = layout.box()
        box.label(text="✨ Nouveautés v2.1.9:")
        box.label(text="• Routes diagonales courtes")
        box.label(text="• Blocs non uniformes")
        box.label(text="• Trottoirs adaptatifs")
        box.label(text="• 8 types de bâtiments colorés")

# Enregistrement des classes
classes = [
    TokyoProperties,
    TOKYO_OT_generate_organic_city,
    TOKYO_PT_organic_panel
]

def register():
    for cls in classes:
        bpy.utils.register_class(cls)
    bpy.types.Scene.tokyo_props = bpy.props.PointerProperty(type=TokyoProperties)

def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)
    del bpy.types.Scene.tokyo_props

if __name__ == "__main__":
    register()
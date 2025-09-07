bl_info = {
    "name": "Tokyo City Generator 1.0.7",
    "author": "Tokyo Urban Designer", 
    "version": (1, 0, 7),
    "blender": (4, 0, 0),
    "location": "View3D > Sidebar > Tokyo Tab",
    "description": "Generate realistic Tokyo-style districts with complete urban network - no empty spaces",
    "category": "Add Mesh",
    "doc_url": "",
    "tracker_url": ""
}

import bpy
from bpy.props import IntProperty, FloatProperty, EnumProperty
from bpy.types import Operator, Panel
import bmesh
import mathutils
import random

# TOKYO 1.0.3 - FICHIER CORRIGÉ
# Bug résolu: Fichier vide → Contenu complet restauré

class TOKYO_OT_generate_district(Operator):
    """Generate Tokyo-style district"""
    bl_idname = "tokyo.generate_district"
    bl_label = "Generate Tokyo District"
    bl_options = {'REGISTER', 'UNDO'}
    
    def execute(self, context):
        # Récupérer les paramètres depuis la scène
        size = context.scene.tokyo_size
        density = context.scene.tokyo_density
        variety = context.scene.tokyo_variety
        organic = context.scene.tokyo_organic
        
        # Nettoyer la scène
        self.clear_scene()
        
        # Créer le district Tokyo
        self.create_tokyo_district(size, organic, density, variety)
        
        blocks_count = int(size * size * density)
        self.report({'INFO'}, f"Tokyo district {size}x{size} with {blocks_count} blocks generated!")
        return {'FINISHED'}
    
    def clear_scene(self):
        """Supprime tous les objets Tokyo existants"""
        for obj in bpy.data.objects:
            if obj.name.startswith(("TokyoSidewalk_", "TokyoStreet_", "TokyoBuilding_", "TokyoCrossing_", "TokyoBaseGround")):
                bpy.data.objects.remove(obj, do_unlink=True)
    
    def create_tokyo_district(self, size, organic_factor, block_density, building_variety):
        """Crée un district Tokyo complet"""
        print(f"🗾 Création district Tokyo {size}x{size}")
        
        # 1. DÉFINIR LES ZONES
        zones = self.define_tokyo_zones(size, block_density, building_variety)
        
        # 2. CRÉER LES BLOCS
        blocks = self.create_district_blocks(size, zones)
        
        # 3. CRÉER LES BÂTIMENTS
        buildings = self.create_tokyo_buildings(size, zones)
        
        # 4. CRÉER LE RÉSEAU URBAIN (routes, rues piétonnes, croisements)
        urban_network = self.create_urban_network(size, zones, organic_factor)
        
        print(f"✅ District créé: {len(blocks)} blocs-trottoirs, {len(buildings)} bâtiments, {len(urban_network)} éléments urbains")
        return {"blocks": blocks, "buildings": buildings, "urban_network": urban_network}
    
    def define_tokyo_zones(self, size, block_density, building_variety):
        """Définit les zones du district Tokyo avec contrôle de densité"""
        zones = {}
        center = size // 2
        total_blocks = size * size
        blocks_to_generate = int(total_blocks * block_density)
        
        # Créer liste de toutes les positions
        all_positions = [(x, y) for x in range(size) for y in range(size)]
        
        # Trier par priorité (centre d'abord, puis proche centre, puis périphérie)
        def priority_score(pos):
            x, y = pos
            dist_from_center = abs(x - center) + abs(y - center)
            return dist_from_center
        
        all_positions.sort(key=priority_score)
        
        # Sélectionner les blocs à générer selon la densité
        selected_positions = all_positions[:blocks_to_generate]
        
        # Assigner les zones selon le type de bâtiments voulu
        for x, y in selected_positions:
            dist_from_center = abs(x - center) + abs(y - center)
            
            if building_variety == 'RESIDENTIAL_ONLY':
                zones[(x, y)] = 'residential'
            elif building_variety == 'BUSINESS_ONLY':
                zones[(x, y)] = 'business'
            elif building_variety == 'NO_BUSINESS':
                if dist_from_center <= 1:
                    zones[(x, y)] = 'commercial'
                else:
                    zones[(x, y)] = 'residential'
            else:  # ALL
                if dist_from_center == 0:
                    zones[(x, y)] = 'business'
                elif dist_from_center == 1:
                    zones[(x, y)] = 'commercial'
                else:
                    zones[(x, y)] = 'residential'
        
        return zones
    
    def create_district_blocks(self, size, zones):
        """Crée les blocs-trottoirs du district selon les zones définies"""
        blocks = {}
        block_size = 20.0
        
        for (x, y), zone_type in zones.items():
            # Position du bloc avec variation aléatoire
            base_x = (x - size/2 + 0.5) * block_size
            base_y = (y - size/2 + 0.5) * block_size
            
            # Ajouter variation de position et taille pour plus de réalisme
            pos_x = base_x + random.uniform(-1.5, 1.5)
            pos_y = base_y + random.uniform(-1.5, 1.5)
            
            # Variation de taille selon la zone
            if zone_type == 'business':
                size_variation = random.uniform(0.85, 1.0)  # Blocs business plus réguliers
                height = 0.15  # Trottoirs surélevés
            elif zone_type == 'commercial':
                size_variation = random.uniform(0.75, 0.95)  # Variation moyenne
                height = 0.12  # Trottoirs moyens
            else:  # residential
                size_variation = random.uniform(0.6, 0.9)   # Plus de variation
                height = 0.08  # Trottoirs plus bas
            
            actual_size = block_size * size_variation
            
            # Créer le bloc-trottoir
            bpy.ops.mesh.primitive_cube_add(size=2.0, location=(pos_x, pos_y, height/2))
            block_obj = bpy.context.object
            # Appliquer la taille correcte avec variation
            block_obj.scale = (actual_size*0.9/2, actual_size*0.9/2, height/2)
            block_obj.name = f"TokyoSidewalk_{zone_type}_{x}_{y}"
            
            # Matériau de trottoir selon la zone
            material = self.create_sidewalk_material(self.determine_sidewalk_type(zone_type))
            block_obj.data.materials.append(material)
            blocks[(x, y)] = block_obj
        
        return blocks
    
    def create_tokyo_buildings(self, size, zones):
        """Crée les bâtiments sur chaque bloc selon la zone"""
        buildings = {}
        block_size = 20.0
        
        for (x, y), zone_type in zones.items():
            # Position avec variation organique
            pos_x = (x - size/2 + 0.5) * block_size + random.uniform(-1.0, 1.0)
            pos_y = (y - size/2 + 0.5) * block_size + random.uniform(-1.0, 1.0)
            
            # Hauteur et taille selon le type de zone avec plus de variation
            if zone_type == 'business':
                height = random.uniform(60, 160)
                # Gratte-ciels avec formes variées
                width_x = random.uniform(0.5, 0.8) * block_size
                width_y = random.uniform(0.5, 0.8) * block_size
                building_name = f"TokyoBuilding_Skyscraper_{x}_{y}"
            elif zone_type == 'commercial':
                height = random.uniform(12, 32)
                # Centres commerciaux plus carrés
                width_x = random.uniform(0.6, 0.85) * block_size
                width_y = random.uniform(0.6, 0.85) * block_size
                building_name = f"TokyoBuilding_Commercial_{x}_{y}"
            else:  # residential
                height = random.uniform(4, 20)
                # Maisons avec formes plus variées
                width_x = random.uniform(0.4, 0.7) * block_size
                width_y = random.uniform(0.4, 0.7) * block_size
                building_name = f"TokyoBuilding_House_{x}_{y}"
            
            # Créer le bâtiment
            bpy.ops.mesh.primitive_cube_add(size=2.0, location=(pos_x, pos_y, height/2))
            building_obj = bpy.context.object
            # Appliquer la taille avec variation
            building_obj.scale = (width_x/2, width_y/2, height/2)
            building_obj.name = building_name
            
            # Matériau selon le type
            material = self.create_building_material(zone_type)
            building_obj.data.materials.append(material)
            buildings[(x, y)] = building_obj
        
        return buildings
    
    def create_urban_network(self, size, zones, organic_factor):
        """Crée le réseau urbain : routes, rues piétonnes et croisements avec couverture complète"""
        network = {}
        block_size = 20.0
        
        # === ÉTAPE 1: CRÉER TOUTES LES ROUTES HORIZONTALES ===
        for y in range(size + 1):
            for x in range(size):
                road_type = self.determine_street_type(x, y, size, "horizontal", zones)
                element = self.create_street_element(x, y, size, road_type, "horizontal", block_size, organic_factor)
                if element:
                    network[f"street_h_{x}_{y}"] = element
        
        # === ÉTAPE 2: CRÉER TOUTES LES ROUTES VERTICALES ===
        for x in range(size + 1):
            for y in range(size):
                road_type = self.determine_street_type(x, y, size, "vertical", zones)
                element = self.create_street_element(x, y, size, road_type, "vertical", block_size, organic_factor)
                if element:
                    network[f"street_v_{x}_{y}"] = element
        
        # === ÉTAPE 3: CRÉER TOUS LES CROISEMENTS ===
        for x in range(size + 1):
            for y in range(size + 1):
                crossing = self.create_crossing(x, y, size, block_size, zones, organic_factor)
                if crossing:
                    network[f"crossing_{x}_{y}"] = crossing
        
        # === ÉTAPE 4: SOL DE BASE SIMPLE (seulement là où nécessaire) ===
        background_zones = self.create_simple_ground(size, zones, block_size)
        for key, element in background_zones.items():
            network[key] = element
        
        return network
    
    def determine_street_type(self, x, y, size, direction, zones):
        """Détermine le type de rue selon la position et les zones adjacentes"""
        center = size // 2
        distance_from_center = max(abs(x - center), abs(y - center))
        
        # Analyser les zones adjacentes pour déterminer le type de rue
        adjacent_zones = []
        if direction == "horizontal":
            if (x, y) in zones: adjacent_zones.append(zones[(x, y)])
            if (x, y-1) in zones: adjacent_zones.append(zones[(x, y-1)])
        else:  # vertical
            if (x, y) in zones: adjacent_zones.append(zones[(x, y)])
            if (x-1, y) in zones: adjacent_zones.append(zones[(x-1, y)])
        
        # Règles de détermination
        if distance_from_center <= 1:
            if 'business' in adjacent_zones:
                return "main_avenue"      # Avenue principale (business)
            else:
                return "secondary_road"   # Route secondaire
        elif distance_from_center <= 2:
            if 'commercial' in adjacent_zones:
                return "shopping_street"  # Rue commerçante
            else:
                return "local_street"     # Rue locale
        else:
            return "pedestrian_path"      # Chemin piéton
    
    def create_street_element(self, x, y, size, street_type, direction, block_size, organic_factor):
        """Crée un élément de rue selon le type"""
        
        # Paramètres selon le type de rue
        if street_type == "main_avenue":
            width = 8.0
            height = 0.02
            material_type = "asphalt_main"
        elif street_type == "secondary_road":
            width = 6.0
            height = 0.015
            material_type = "asphalt_secondary"
        elif street_type == "shopping_street":
            width = 5.0
            height = 0.01
            material_type = "paved_commercial"
        elif street_type == "local_street":
            width = 4.0
            height = 0.01
            material_type = "asphalt_local"
        else:  # pedestrian_path
            width = 2.5
            height = 0.005
            material_type = "pedestrian_stones"
        
        # Position selon la direction avec couverture raisonnée
        if direction == "horizontal":
            pos_x = (x - size/2 + 0.5) * block_size
            pos_y = (y - size/2) * block_size
            scale_x = block_size * 0.95 / 2  # Réajusté pour éviter trop de chevauchement
            scale_y = width / 2
            name = f"TokyoStreet_{street_type}_H_{x}_{y}"
        else:  # vertical
            pos_x = (x - size/2) * block_size
            pos_y = (y - size/2 + 0.5) * block_size
            scale_x = width / 2
            scale_y = block_size * 0.95 / 2  # Réajusté pour éviter trop de chevauchement
            name = f"TokyoStreet_{street_type}_V_{x}_{y}"
        
        # Variation organique
        if organic_factor > 0:
            curve_strength = organic_factor * 3.0
            pos_x += random.uniform(-curve_strength, curve_strength)
            pos_y += random.uniform(-curve_strength, curve_strength)
        
        # Créer l'élément
        bpy.ops.mesh.primitive_cube_add(size=2.0, location=(pos_x, pos_y, height/2))
        street_obj = bpy.context.object
        street_obj.scale = (scale_x, scale_y, height/2)
        street_obj.name = name
        
        # Matériau
        material = self.create_street_material(material_type)
        street_obj.data.materials.append(material)
        
        return street_obj
    
    def create_crossing(self, x, y, size, block_size, zones, organic_factor):
        """Crée un croisement à l'intersection"""
        pos_x = (x - size/2) * block_size
        pos_y = (y - size/2) * block_size
        
        # Variation organique
        if organic_factor > 0:
            pos_x += random.uniform(-1.0, 1.0)
            pos_y += random.uniform(-1.0, 1.0)
        
        # Taille du croisement (réduite pour plus de réalisme)
        crossing_size = 4.0  # Réduit pour éviter la domination visuelle
        height = 0.01        # Plus fin
        
        # Créer le croisement
        bpy.ops.mesh.primitive_cube_add(size=2.0, location=(pos_x, pos_y, height/2))
        crossing_obj = bpy.context.object
        crossing_obj.scale = (crossing_size/2, crossing_size/2, height/2)
        crossing_obj.name = f"TokyoCrossing_{x}_{y}"
        
        # Matériau de croisement
        material = self.create_street_material("crossing_asphalt")
        crossing_obj.data.materials.append(material)
        
        return crossing_obj
    
    def create_simple_ground(self, size, zones, block_size):
        """Crée un sol de base simple seulement où nécessaire"""
        ground = {}
        
        # Sol de base simple sous tout le district
        ground_size = size * block_size + 10  # Légèrement plus grand que le district
        height = 0.001  # Très fin
        
        # Un seul grand plan de sol
        pos_x = 0
        pos_y = 0
        
        bpy.ops.mesh.primitive_cube_add(size=2.0, location=(pos_x, pos_y, -height/2))
        ground_obj = bpy.context.object
        ground_obj.scale = (ground_size/2, ground_size/2, height/2)
        ground_obj.name = "TokyoBaseGround"
        
        # Matériau de sol simple
        material = self.create_simple_ground_material()
        ground_obj.data.materials.append(material)
        
        ground["base_ground"] = ground_obj
        return ground
    
    def create_simple_ground_material(self):
        """Crée un matériau simple pour le sol de base"""
        mat_name = "Tokyo_BaseGround"
        mat = bpy.data.materials.new(name=mat_name)
        mat.use_nodes = True
        
        # Couleur discrète
        color = (0.4, 0.4, 0.4, 1.0)  # Gris neutre
        roughness = 0.95
        
        mat.node_tree.nodes["Principled BSDF"].inputs[0].default_value = color
        mat.node_tree.nodes["Principled BSDF"].inputs[7].default_value = roughness
        return mat
    
    def create_street_material(self, material_type):
        """Crée un matériau pour les éléments de rue"""
        mat_name = f"Tokyo_Street_{material_type}"
        mat = bpy.data.materials.new(name=mat_name)
        mat.use_nodes = True
        
        if material_type == "asphalt_main":
            color = (0.1, 0.1, 0.1, 1.0)    # Asphalte principal - noir
            roughness = 0.9
        elif material_type == "asphalt_secondary":
            color = (0.15, 0.15, 0.15, 1.0)  # Asphalte secondaire - gris foncé
            roughness = 0.8
        elif material_type == "paved_commercial":
            color = (0.6, 0.55, 0.5, 1.0)   # Pavés commerciaux - beige
            roughness = 0.95
        elif material_type == "asphalt_local":
            color = (0.2, 0.2, 0.2, 1.0)    # Asphalte local - gris
            roughness = 0.7
        elif material_type == "pedestrian_stones":
            color = (0.7, 0.65, 0.6, 1.0)   # Pierres piétonnes - beige clair
            roughness = 0.85
        else:  # crossing_asphalt
            color = (0.12, 0.12, 0.12, 1.0) # Croisement - asphalte avec marquage
            roughness = 0.8
        
        mat.node_tree.nodes["Principled BSDF"].inputs[0].default_value = color
        mat.node_tree.nodes["Principled BSDF"].inputs[7].default_value = roughness
        return mat
    
    def determine_sidewalk_type(self, zone_type):
        """Détermine le type de trottoir selon la zone"""
        if zone_type == "business":
            return "modern_concrete"  # Trottoir béton moderne
        elif zone_type == "commercial":
            return "paved_stones"     # Trottoir pavé
        else:  # residential
            return "simple_concrete"  # Trottoir béton simple
    
    def create_building_material(self, zone_type):
        """Crée un matériau pour les bâtiments"""
        mat_name = f"Tokyo_{zone_type}_Building"
        mat = bpy.data.materials.new(name=mat_name)
        mat.use_nodes = True
        
        if zone_type == 'business':
            color = (0.8, 0.8, 0.9, 1.0)  # Gris métallique
            mat.node_tree.nodes["Principled BSDF"].inputs[6].default_value = 0.8  # Metallic
        elif zone_type == 'commercial':
            color = (0.9, 0.6, 0.3, 1.0)  # Orange
        else:  # residential
            color = (0.7, 0.9, 0.6, 1.0)  # Vert clair
        
        mat.node_tree.nodes["Principled BSDF"].inputs[0].default_value = color
        return mat
    
    def create_sidewalk_material(self, sidewalk_type):
        """Crée un matériau pour les trottoirs"""
        mat_name = f"Tokyo_Sidewalk_{sidewalk_type}"
        mat = bpy.data.materials.new(name=mat_name)
        mat.use_nodes = True
        
        if sidewalk_type == "modern_concrete":
            color = (0.85, 0.85, 0.85, 1.0)  # Béton moderne clair
            roughness = 0.4
        elif sidewalk_type == "paved_stones":
            color = (0.6, 0.55, 0.5, 1.0)    # Pavés beiges
            roughness = 0.9
        else:  # simple_concrete
            color = (0.7, 0.7, 0.7, 1.0)     # Béton simple
            roughness = 0.6
        
        mat.node_tree.nodes["Principled BSDF"].inputs[0].default_value = color
        mat.node_tree.nodes["Principled BSDF"].inputs[7].default_value = roughness
        return mat


# INTERFACE UTILISATEUR COMPATIBLE BLENDER 4.x
class TOKYO_PT_main_panel(Panel):
    """Panneau principal Tokyo"""
    bl_label = "Tokyo City Generator 1.0.7"
    bl_idname = "TOKYO_PT_main_panel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Tokyo'
    
    def draw(self, context):
        layout = self.layout
        
        # Titre avec icône
        row = layout.row()
        row.label(text="🗾 Tokyo District Generator", icon='WORLD')
        layout.separator()
        
        # Boîte pour les paramètres
        box = layout.box()
        box.label(text="⚙️ Configuration", icon='PREFERENCES')
        
        # District Size
        row = box.row()
        row.label(text="District Size:")
        row.prop(context.scene, "tokyo_size", text="")
        
        # Block Density  
        row = box.row()
        row.label(text="Block Density:")
        row.prop(context.scene, "tokyo_density", text="", slider=True)
        
        # Building Variety
        row = box.row()
        row.label(text="Building Variety:")
        row.prop(context.scene, "tokyo_variety", text="")
        
        # Organic Factor
        row = box.row()
        row.label(text="Organic Streets:")
        row.prop(context.scene, "tokyo_organic", text="", slider=True)
        
        layout.separator()
        
        # Bouton de génération
        layout.operator("tokyo.generate_district", text="🚀 Generate Tokyo District", icon='MESH_CUBE')
        
        layout.separator()
        
        # Informations
        box2 = layout.box()
        box2.label(text="📊 Building Types", icon='INFO')
        box2.label(text="• Business: Skyscrapers 15-40 floors")
        box2.label(text="• Commercial: Centers 3-8 floors") 
        box2.label(text="• Residential: Houses 1-5 floors")


# ENREGISTREMENT BLENDER
classes = [
    TOKYO_OT_generate_district,
    TOKYO_PT_main_panel,
]

# PROPRIÉTÉS DE SCÈNE pour l'interface
def init_scene_properties():
    """Initialise les propriétés de scène pour l'interface"""
    bpy.types.Scene.tokyo_size = IntProperty(
        name="District Size",
        description="Size of the district (3=3x3, 5=5x5)",
        default=3,
        min=3,
        max=7
    )
    
    bpy.types.Scene.tokyo_density = FloatProperty(
        name="Block Density",
        description="Percentage of blocks that will have buildings",
        default=1.0,
        min=0.3,
        max=1.0,
        subtype='PERCENTAGE'
    )
    
    bpy.types.Scene.tokyo_variety = EnumProperty(
        name="Building Variety",
        description="Types of buildings to generate",
        items=[
            ('ALL', 'All Types', 'Business + Commercial + Residential'),
            ('BUSINESS_ONLY', 'Business Only', 'Only skyscrapers'),
            ('NO_BUSINESS', 'No Business', 'Commercial + Residential only'),
            ('RESIDENTIAL_ONLY', 'Residential Only', 'Only houses')
        ],
        default='ALL'
    )
    
    bpy.types.Scene.tokyo_organic = FloatProperty(
        name="Organic Streets",
        description="How organic/curved the streets are",
        default=0.3,
        min=0.0,
        max=1.0,
        subtype='FACTOR'
    )

def clear_scene_properties():
    """Supprime les propriétés de scène"""
    del bpy.types.Scene.tokyo_size
    del bpy.types.Scene.tokyo_density  
    del bpy.types.Scene.tokyo_variety
    del bpy.types.Scene.tokyo_organic

def register():
    for cls in classes:
        bpy.utils.register_class(cls)
    init_scene_properties()
    print("🗾 Tokyo City Generator 1.0.7 registered!")

def unregister():
    clear_scene_properties()
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)
    print("🗾 Tokyo City Generator 1.0.7 unregistered!")

if __name__ == "__main__":
    register()
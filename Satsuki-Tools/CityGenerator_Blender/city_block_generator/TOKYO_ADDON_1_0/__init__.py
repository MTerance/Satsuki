bl_info = {
    "name": "Tokyo City Generator 1.0.3",
    "author": "Tokyo Urban Designer", 
    "version": (1, 0, 3),
    "blender": (4, 0, 0),
    "location": "View3D > Sidebar > Tokyo Tab",
    "description": "Generate realistic Tokyo-style districts with skyscrapers, commercial centers, and residential areas",
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
            if obj.name.startswith(("TokyoBlock_", "TokyoRoad_", "TokyoBuilding_")):
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
        
        print(f"✅ District créé: {len(blocks)} blocs, {len(buildings)} bâtiments")
        return {"blocks": blocks, "buildings": buildings}
    
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
        """Crée les blocs du district selon les zones définies"""
        blocks = {}
        block_size = 20.0
        
        for (x, y), zone_type in zones.items():
            # Position du bloc
            pos_x = (x - size/2 + 0.5) * block_size
            pos_y = (y - size/2 + 0.5) * block_size
            
            # Créer le mesh du bloc
            bpy.ops.mesh.primitive_cube_add(size=2.0, location=(pos_x, pos_y, 0.5))
            block_obj = bpy.context.object
            # Appliquer la taille correcte
            block_obj.scale = (block_size*0.9/2, block_size*0.9/2, 1.0)
            block_obj.name = f"TokyoBlock_{zone_type}_{x}_{y}"
            
            # Matériau selon la zone
            material = self.create_zone_material(zone_type)
            block_obj.data.materials.append(material)
            blocks[(x, y)] = block_obj
        
        return blocks
    
    def create_tokyo_buildings(self, size, zones):
        """Crée les bâtiments sur chaque bloc selon la zone"""
        buildings = {}
        block_size = 20.0
        
        for (x, y), zone_type in zones.items():
            # Position calculée de la même façon que les blocs
            pos_x = (x - size/2 + 0.5) * block_size
            pos_y = (y - size/2 + 0.5) * block_size
            
            # Hauteur selon le type de zone
            if zone_type == 'business':
                height = random.uniform(60, 160)
                building_name = f"TokyoBuilding_Skyscraper_{x}_{y}"
            elif zone_type == 'commercial':
                height = random.uniform(12, 32)
                building_name = f"TokyoBuilding_Commercial_{x}_{y}"
            else:  # residential
                height = random.uniform(4, 20)
                building_name = f"TokyoBuilding_House_{x}_{y}"
            
            # Créer le bâtiment
            bpy.ops.mesh.primitive_cube_add(size=2.0, location=(pos_x, pos_y, height/2))
            building_obj = bpy.context.object
            # Appliquer la taille correcte
            building_obj.scale = (block_size*0.7/2, block_size*0.7/2, height/2)
            building_obj.name = building_name
            
            # Matériau selon le type
            material = self.create_building_material(zone_type)
            building_obj.data.materials.append(material)
            buildings[(x, y)] = building_obj
        
        return buildings
    
    def create_zone_material(self, zone_type):
        """Crée un matériau pour les zones"""
        mat_name = f"Tokyo_{zone_type}_Zone"
        mat = bpy.data.materials.new(name=mat_name)
        mat.use_nodes = True
        
        if zone_type == 'business':
            color = (0.1, 0.1, 0.3, 1.0)  # Bleu foncé
        elif zone_type == 'commercial':
            color = (0.3, 0.1, 0.1, 1.0)  # Rouge foncé
        else:  # residential
            color = (0.1, 0.3, 0.1, 1.0)  # Vert foncé
        
        mat.node_tree.nodes["Principled BSDF"].inputs[0].default_value = color
        return mat
    
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


# INTERFACE UTILISATEUR COMPATIBLE BLENDER 4.x
class TOKYO_PT_main_panel(Panel):
    """Panneau principal Tokyo"""
    bl_label = "Tokyo City Generator 1.0.3"
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
    print("🗾 Tokyo City Generator 1.0.3 registered!")

def unregister():
    clear_scene_properties()
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)
    print("🗾 Tokyo City Generator 1.0.3 unregistered!")

if __name__ == "__main__":
    register()
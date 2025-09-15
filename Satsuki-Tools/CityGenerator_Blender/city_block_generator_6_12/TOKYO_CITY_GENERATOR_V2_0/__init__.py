bl_info = {
    "name": "Tokyo City Generator v2.0 UNIFIED",
    "author": "Tokyo Urban Designer",
    "version": (2, 0, 0),
    "blender": (4, 0, 0),
    "location": "View3D > Sidebar > Tokyo v2.0",
    "description": "Unified city generator with multiple algorithms: Tokyo Districts, Organic Cities, Rectangular Grids. Advanced multi-floor texture system included.",
    "category": "Add Mesh",
    "doc_url": "",
    "tracker_url": ""
}

import bpy
from bpy.props import IntProperty, FloatProperty, EnumProperty, BoolProperty, StringProperty
from bpy.types import Operator, Panel
import bmesh
import mathutils
import random
import os

# Import des modules unifiés
try:
    from . import core_unified
    from . import texture_system_v2
    from . import algorithms
    from . import ui_unified
    
    # Initialisation du système unifié
    from .texture_system_v2 import UnifiedTextureSystem
    from .algorithms import TokyoAlgorithm, OrganicAlgorithm, GridAlgorithm
    
    # Créer les instances globales
    unified_texture_system = UnifiedTextureSystem()
    
    # Algorithmes disponibles
    ALGORITHMS = {
        'TOKYO': TokyoAlgorithm(),
        'ORGANIC': OrganicAlgorithm(),
        'GRID': GridAlgorithm()
    }
    
    SYSTEM_AVAILABLE = True
    print("🎯 Tokyo City Generator v2.0 UNIFIED chargé avec succès")
    print(f"📊 Algorithmes disponibles: {list(ALGORITHMS.keys())}")
    print("🎨 Système de textures v2.0 initialisé")
    
except ImportError as e:
    SYSTEM_AVAILABLE = False
    unified_texture_system = None
    ALGORITHMS = {}
    print(f"⚠️ Erreur chargement Tokyo City Generator v2.0: {e}")
    print("🔄 Utilisation du mode de compatibilité")
except Exception as e:
    SYSTEM_AVAILABLE = False
    unified_texture_system = None
    ALGORITHMS = {}
    print(f"⚠️ Erreur système Tokyo City Generator v2.0: {e}")

# ===================================================================
# PROPRIÉTÉS UNIFIÉES
# ===================================================================

class TOKYO_V2_Properties(bpy.types.PropertyGroup):
    """Propriétés unifiées pour Tokyo City Generator v2.0"""
    
    # ALGORITHME DE GÉNÉRATION
    generation_mode: EnumProperty(
        name="Generation Mode",
        description="Select city generation algorithm",
        items=[
            ('TOKYO', "Tokyo Districts", "Realistic Tokyo-style districts with mixed zones"),
            ('ORGANIC', "Organic Cities", "Non-rectangular organic city layouts"),
            ('GRID', "Rectangular Grid", "Classic rectangular city blocks"),
        ],
        default='TOKYO'
    )
    
    # PARAMÈTRES COMMUNS
    city_size: IntProperty(
        name="City Size", 
        description="Size of the city grid",
        default=5, min=2, max=20
    )
    
    building_density: FloatProperty(
        name="Building Density",
        description="Density of buildings (0.1 = sparse, 1.0 = dense)",
        default=0.7, min=0.1, max=1.0
    )
    
    building_variety: FloatProperty(
        name="Building Variety",
        description="Variety in building types and sizes",
        default=0.8, min=0.0, max=1.0
    )
    
    # PARAMÈTRES SPÉCIALISÉS
    organic_factor: FloatProperty(
        name="Organic Factor",
        description="How organic/curved the layout should be (Organic mode only)",
        default=0.5, min=0.0, max=1.0
    )
    
    tokyo_district_type: EnumProperty(
        name="District Type",
        description="Type of Tokyo district to generate",
        items=[
            ('MIXED', "Mixed District", "Residential + Commercial + Business"),
            ('RESIDENTIAL', "Residential", "Mainly houses and apartments"),
            ('COMMERCIAL', "Commercial", "Shopping and retail areas"),
            ('BUSINESS', "Business", "Office buildings and skyscrapers"),
        ],
        default='MIXED'
    )
    
    # SYSTÈME DE TEXTURES V2.0
    use_advanced_textures: BoolProperty(
        name="Advanced Textures v2.0",
        description="Use the advanced multi-floor texture system",
        default=True
    )
    
    texture_base_path: StringProperty(
        name="Texture Path",
        description="Base path for texture files",
        default="C:/Users/sshom/Documents/assets/Tools/tokyo_textures",
        subtype='DIR_PATH'
    )
    
    # PARAMÈTRES AVANCÉS
    include_roads: BoolProperty(
        name="Include Roads",
        description="Generate roads and sidewalks",
        default=True
    )
    
    include_props: BoolProperty(
        name="Include Props",
        description="Add urban props (cars, trees, etc.)",
        default=False
    )
    
    seed: IntProperty(
        name="Random Seed",
        description="Seed for random generation (0 = random)",
        default=0, min=0
    )

# ===================================================================
# OPÉRATEUR PRINCIPAL UNIFIÉ
# ===================================================================

class TOKYO_V2_OT_generate_city(Operator):
    """Generate city with Tokyo City Generator v2.0"""
    bl_idname = "tokyo_v2.generate_city"
    bl_label = "Generate City v2.0"
    bl_options = {'REGISTER', 'UNDO'}
    
    def execute(self, context):
        if not SYSTEM_AVAILABLE:
            self.report({'ERROR'}, "Tokyo City Generator v2.0 system not available!")
            return {'CANCELLED'}
        
        props = context.scene.tokyo_v2
        
        # Configuration du seed
        if props.seed == 0:
            seed = random.randint(1, 10000)
        else:
            seed = props.seed
        random.seed(seed)
        
        # Sélection de l'algorithme
        algorithm = ALGORITHMS.get(props.generation_mode)
        if not algorithm:
            self.report({'ERROR'}, f"Algorithm {props.generation_mode} not available!")
            return {'CANCELLED'}
        
        # Nettoyer la scène
        self.clear_scene()
        
        # Configuration des paramètres
        generation_params = {
            'size': props.city_size,
            'density': props.building_density,
            'variety': props.building_variety,
            'organic_factor': props.organic_factor,
            'district_type': props.tokyo_district_type,
            'use_advanced_textures': props.use_advanced_textures,
            'texture_path': props.texture_base_path,
            'include_roads': props.include_roads,
            'include_props': props.include_props,
            'seed': seed
        }
        
        # Génération de la ville
        try:
            result = algorithm.generate(context, generation_params, unified_texture_system)
            
            # Rapport de succès
            mode_name = {
                'TOKYO': 'Tokyo District',
                'ORGANIC': 'Organic City', 
                'GRID': 'Grid City'
            }.get(props.generation_mode, 'City')
            
            stats = result.get('stats', {})
            buildings_count = stats.get('buildings', 0)
            blocks_count = stats.get('blocks', 0)
            
            texture_info = "with advanced textures v2.0" if props.use_advanced_textures else "with basic materials"
            
            self.report({'INFO'}, 
                f"{mode_name} {props.city_size}x{props.city_size} generated! "
                f"{buildings_count} buildings, {blocks_count} blocks, {texture_info} (seed: {seed})")
            
            return {'FINISHED'}
            
        except Exception as e:
            self.report({'ERROR'}, f"Generation failed: {str(e)}")
            return {'CANCELLED'}
    
    def clear_scene(self):
        """Supprime tous les objets de ville existants"""
        prefixes = [
            "TokyoBuilding_", "TokyoSidewalk_", "TokyoStreet_", "TokyoCrossing_",
            "OrganicBuilding_", "OrganicRoad_", "OrganicBlock_",
            "GridBuilding_", "GridStreet_", "GridBlock_",
            "CityBuilding_", "CityRoad_", "CityBlock_", "CityProp_"
        ]
        
        for obj in list(bpy.data.objects):
            if any(obj.name.startswith(prefix) for prefix in prefixes):
                bpy.data.objects.remove(obj, do_unlink=True)

# ===================================================================
# INTERFACE UNIFIÉE
# ===================================================================

class TOKYO_V2_PT_main_panel(Panel):
    """Panneau principal Tokyo City Generator v2.0"""
    bl_label = "Tokyo City Generator v2.0"
    bl_idname = "TOKYO_V2_PT_main_panel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Tokyo v2.0'
    
    def draw(self, context):
        layout = self.layout
        props = context.scene.tokyo_v2
        
        # En-tête avec statut
        if SYSTEM_AVAILABLE:
            layout.label(text="🎯 System Ready", icon='CHECKMARK')
        else:
            layout.label(text="⚠️ System Error", icon='ERROR')
            layout.operator("tokyo_v2.reload_system", text="Reload System")
            return
        
        # Sélection de l'algorithme
        layout.separator()
        layout.prop(props, "generation_mode", expand=True)
        
        # Paramètres communs
        box = layout.box()
        box.label(text="🏗️ Generation Parameters", icon='SETTINGS')
        box.prop(props, "city_size")
        box.prop(props, "building_density")
        box.prop(props, "building_variety")
        
        # Paramètres spécialisés selon l'algorithme
        if props.generation_mode == 'TOKYO':
            box = layout.box()
            box.label(text="🗾 Tokyo Districts", icon='WORLD')
            box.prop(props, "tokyo_district_type")
        
        elif props.generation_mode == 'ORGANIC':
            box = layout.box()
            box.label(text="🌿 Organic Parameters", icon='FORCE_CURVE')
            box.prop(props, "organic_factor")
        
        # Système de textures
        box = layout.box()
        box.label(text="🎨 Texture System v2.0", icon='MATERIAL')
        box.prop(props, "use_advanced_textures")
        if props.use_advanced_textures:
            box.prop(props, "texture_base_path")
        
        # Options avancées
        box = layout.box()
        box.label(text="⚙️ Advanced Options", icon='MODIFIER')
        box.prop(props, "include_roads")
        box.prop(props, "include_props")
        box.prop(props, "seed")
        
        # Bouton de génération
        layout.separator()
        row = layout.row(align=True)
        row.scale_y = 2.0
        row.operator("tokyo_v2.generate_city", text="🏙️ Generate City v2.0", icon='MESH_CUBE')

# ===================================================================
# ENREGISTREMENT
# ===================================================================

classes = [
    TOKYO_V2_Properties,
    TOKYO_V2_OT_generate_city,
    TOKYO_V2_PT_main_panel,
]

def register():
    print("🎯 Enregistrement Tokyo City Generator v2.0...")
    
    for cls in classes:
        bpy.utils.register_class(cls)
    
    # Enregistrer les propriétés
    bpy.types.Scene.tokyo_v2 = bpy.props.PointerProperty(type=TOKYO_V2_Properties)
    
    # Enregistrer les modules
    if SYSTEM_AVAILABLE:
        core_unified.register()
        ui_unified.register()
    
    print("✅ Tokyo City Generator v2.0 enregistré avec succès!")

def unregister():
    print("🔄 Désenregistrement Tokyo City Generator v2.0...")
    
    if SYSTEM_AVAILABLE:
        core_unified.unregister()
        ui_unified.unregister()
    
    # Désenregistrer les propriétés
    del bpy.types.Scene.tokyo_v2
    
    # Désenregistrer les classes
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)
    
    print("✅ Tokyo City Generator v2.0 désenregistré!")

if __name__ == "__main__":
    register()
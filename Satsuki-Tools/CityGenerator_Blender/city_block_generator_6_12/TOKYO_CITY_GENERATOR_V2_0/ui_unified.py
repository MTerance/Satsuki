"""
Interface utilisateur unifiée pour Tokyo City Generator v2.0
"""

import bpy
from bpy.types import Panel, Operator
from bpy.props import BoolProperty

class TOKYO_V2_PT_algorithm_panel(Panel):
    """Panneau de sélection d'algorithme"""
    bl_label = "Algorithm Selection"
    bl_idname = "TOKYO_V2_PT_algorithm_panel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Tokyo v2.0'
    bl_parent_id = "TOKYO_V2_PT_main_panel"
    
    def draw(self, context):
        layout = self.layout
        props = context.scene.tokyo_v2
        
        # Affichage des algorithmes avec icônes
        box = layout.box()
        box.label(text="🎯 Select Generation Algorithm", icon='MODIFIER')
        
        # Tokyo Districts
        row = box.row(align=True)
        if props.generation_mode == 'TOKYO':
            row.alert = True
        op = row.operator("tokyo_v2.set_mode", text="🗾 Tokyo Districts")
        op.mode = 'TOKYO'
        
        # Organic Cities
        row = box.row(align=True)
        if props.generation_mode == 'ORGANIC':
            row.alert = True
        op = row.operator("tokyo_v2.set_mode", text="🌿 Organic Cities")
        op.mode = 'ORGANIC'
        
        # Grid Cities
        row = box.row(align=True)
        if props.generation_mode == 'GRID':
            row.alert = True
        op = row.operator("tokyo_v2.set_mode", text="📐 Grid Cities")
        op.mode = 'GRID'
        
        # Description de l'algorithme sélectionné
        box.separator()
        descriptions = {
            'TOKYO': "Realistic Tokyo-style mixed districts\nwith varied building heights and zones",
            'ORGANIC': "Natural, curved city layouts\nwith non-rectangular patterns",
            'GRID': "Classic rectangular grid system\nwith uniform block distribution"
        }
        
        desc_box = box.box()
        desc_box.scale_y = 0.8
        for line in descriptions[props.generation_mode].split('\n'):
            desc_box.label(text=line, icon='INFO')

class TOKYO_V2_PT_parameters_panel(Panel):
    """Panneau des paramètres de génération"""
    bl_label = "Generation Parameters"
    bl_idname = "TOKYO_V2_PT_parameters_panel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Tokyo v2.0'
    bl_parent_id = "TOKYO_V2_PT_main_panel"
    
    def draw(self, context):
        layout = self.layout
        props = context.scene.tokyo_v2
        
        # Paramètres communs
        box = layout.box()
        box.label(text="🏗️ Basic Parameters", icon='SETTINGS')
        
        col = box.column(align=True)
        col.prop(props, "city_size", slider=True)
        col.prop(props, "building_density", slider=True)
        col.prop(props, "building_variety", slider=True)
        
        # Paramètres spécialisés selon l'algorithme
        if props.generation_mode == 'TOKYO':
            self.draw_tokyo_params(layout, props)
        elif props.generation_mode == 'ORGANIC':
            self.draw_organic_params(layout, props)
        elif props.generation_mode == 'GRID':
            self.draw_grid_params(layout, props)
    
    def draw_tokyo_params(self, layout, props):
        """Paramètres spécifiques à Tokyo"""
        box = layout.box()
        box.label(text="🗾 Tokyo District Settings", icon='WORLD')
        box.prop(props, "tokyo_district_type", expand=False)
        
        # Info sur le type de district
        district_info = {
            'MIXED': "🏘️ Varied heights and building types",
            'RESIDENTIAL': "🏠 Houses and low-rise apartments", 
            'COMMERCIAL': "🏪 Shopping centers and retail",
            'BUSINESS': "🏢 Office buildings and skyscrapers"
        }
        
        info_box = box.box()
        info_box.scale_y = 0.7
        info_box.label(text=district_info.get(props.tokyo_district_type, ""), icon='INFO')
    
    def draw_organic_params(self, layout, props):
        """Paramètres spécifiques à Organic"""
        box = layout.box()
        box.label(text="🌿 Organic Settings", icon='FORCE_CURVE')
        box.prop(props, "organic_factor", slider=True)
        
        # Indicateur visuel du facteur organique
        info_box = box.box()
        info_box.scale_y = 0.7
        if props.organic_factor < 0.3:
            info_box.label(text="📐 Almost rectangular layout", icon='INFO')
        elif props.organic_factor < 0.7:
            info_box.label(text="🌀 Moderately curved paths", icon='INFO')
        else:
            info_box.label(text="🌊 Highly organic curves", icon='INFO')
    
    def draw_grid_params(self, layout, props):
        """Paramètres spécifiques à Grid"""
        box = layout.box()
        box.label(text="📐 Grid Settings", icon='GRID')
        
        info_box = box.box()
        info_box.scale_y = 0.7
        info_box.label(text="📏 Perfect rectangular blocks", icon='INFO')
        info_box.label(text="🛣️ Regular street network", icon='INFO')

class TOKYO_V2_PT_textures_panel(Panel):
    """Panneau du système de textures"""
    bl_label = "Advanced Textures v2.0"
    bl_idname = "TOKYO_V2_PT_textures_panel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Tokyo v2.0'
    bl_parent_id = "TOKYO_V2_PT_main_panel"
    
    def draw(self, context):
        layout = self.layout
        props = context.scene.tokyo_v2
        
        # Système de textures principal
        box = layout.box()
        box.label(text="🎨 Multi-Floor Texture System", icon='MATERIAL')
        
        row = box.row(align=True)
        row.prop(props, "use_advanced_textures", text="Enable Advanced Textures")
        
        if props.use_advanced_textures:
            box.separator()
            box.prop(props, "texture_base_path")
            
            # Status du système de textures
            status_box = box.box()
            status_box.scale_y = 0.8
            
            # Vérifier si le chemin existe
            import os
            if os.path.exists(props.texture_base_path):
                status_box.label(text="✅ Texture path found", icon='CHECKMARK')
            else:
                status_box.label(text="⚠️ Texture path not found", icon='ERROR')
                status_box.label(text="Will use procedural materials", icon='INFO')
            
            # Info sur le système multi-étages
            info_box = box.box()
            info_box.scale_y = 0.7
            info_box.label(text="📏 4 floors per texture file", icon='INFO')
            info_box.label(text="🔄 Auto-repeat based on height", icon='INFO')
            info_box.label(text="🎯 Category-based selection", icon='INFO')
        else:
            # Mode procédural
            info_box = box.box()
            info_box.scale_y = 0.8
            info_box.label(text="🎨 Using procedural materials", icon='INFO')
            info_box.label(text="🚀 Faster generation", icon='INFO')

class TOKYO_V2_PT_advanced_panel(Panel):
    """Panneau des options avancées"""
    bl_label = "Advanced Options"
    bl_idname = "TOKYO_V2_PT_advanced_panel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Tokyo v2.0'
    bl_parent_id = "TOKYO_V2_PT_main_panel"
    bl_options = {'DEFAULT_CLOSED'}
    
    def draw(self, context):
        layout = self.layout
        props = context.scene.tokyo_v2
        
        # Infrastructure
        box = layout.box()
        box.label(text="🛣️ Infrastructure", icon='MOD_BUILD')
        
        col = box.column(align=True)
        col.prop(props, "include_roads")
        col.prop(props, "include_props")
        
        # Random seed
        box = layout.box()
        box.label(text="🎲 Randomization", icon='FORCE_TURBULENCE')
        box.prop(props, "seed")
        
        seed_box = box.box()
        seed_box.scale_y = 0.7
        if props.seed == 0:
            seed_box.label(text="🎲 Random seed each time", icon='INFO')
        else:
            seed_box.label(text=f"🔒 Fixed seed: {props.seed}", icon='INFO')

class TOKYO_V2_PT_generation_panel(Panel):
    """Panneau de génération"""
    bl_label = "Generate City"
    bl_idname = "TOKYO_V2_PT_generation_panel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Tokyo v2.0'
    bl_parent_id = "TOKYO_V2_PT_main_panel"
    
    def draw(self, context):
        layout = self.layout
        props = context.scene.tokyo_v2
        
        # Résumé de génération
        box = layout.box()
        box.label(text="📊 Generation Preview", icon='PREVIEW_RANGE')
        
        # Calculs approximatifs
        estimated_buildings = int(props.city_size * props.city_size * props.building_density * 3)
        estimated_blocks = props.city_size * props.city_size
        
        info_col = box.column(align=True)
        info_col.scale_y = 0.8
        info_col.label(text=f"🏗️ ~{estimated_buildings} buildings")
        info_col.label(text=f"🏘️ {estimated_blocks} blocks")
        info_col.label(text=f"🎯 {props.generation_mode} algorithm")
        
        # Bouton principal de génération
        layout.separator()
        row = layout.row(align=True)
        row.scale_y = 2.5
        
        # Icône selon l'algorithme
        icons = {
            'TOKYO': 'WORLD',
            'ORGANIC': 'FORCE_CURVE', 
            'GRID': 'GRID'
        }
        
        row.operator("tokyo_v2.generate_city", 
                    text=f"🏙️ Generate {props.generation_mode.title()} City", 
                    icon=icons.get(props.generation_mode, 'MESH_CUBE'))
        
        # Boutons utilitaires
        layout.separator()
        utils_row = layout.row(align=True)
        utils_row.operator("tokyo_v2.clear_scene", text="🗑️ Clear Scene", icon='TRASH')
        utils_row.operator("tokyo_v2.reload_system", text="🔄 Reload", icon='FILE_REFRESH')

# ===================================================================
# OPÉRATEURS UTILITAIRES
# ===================================================================

class TOKYO_V2_OT_set_mode(Operator):
    """Change generation mode"""
    bl_idname = "tokyo_v2.set_mode"
    bl_label = "Set Generation Mode"
    
    mode: bpy.props.StringProperty()
    
    def execute(self, context):
        context.scene.tokyo_v2.generation_mode = self.mode
        self.report({'INFO'}, f"Mode changed to {self.mode}")
        return {'FINISHED'}

class TOKYO_V2_OT_clear_scene(Operator):
    """Clear all city objects from scene"""
    bl_idname = "tokyo_v2.clear_scene"
    bl_label = "Clear Scene"
    bl_options = {'REGISTER', 'UNDO'}
    
    def execute(self, context):
        # Préfixes de tous les générateurs
        all_prefixes = [
            "TokyoBuilding_", "TokyoSidewalk_", "TokyoStreet_", "TokyoCrossing_",
            "OrganicBuilding_", "OrganicRoad_", "OrganicBlock_",
            "GridBuilding_", "GridStreet_", "GridBlock_",
            "CityBuilding_", "CityRoad_", "CityBlock_", "CityProp_"
        ]
        
        count = 0
        for obj in list(bpy.data.objects):
            if any(obj.name.startswith(prefix) for prefix in all_prefixes):
                bpy.data.objects.remove(obj, do_unlink=True)
                count += 1
        
        self.report({'INFO'}, f"Cleared {count} city objects from scene")
        return {'FINISHED'}

class TOKYO_V2_OT_reload_system(Operator):
    """Reload Tokyo City Generator v2.0 system"""
    bl_idname = "tokyo_v2.reload_system"
    bl_label = "Reload System"
    
    def execute(self, context):
        try:
            # Recharger les modules (nécessite restart de Blender en réalité)
            self.report({'INFO'}, "System reload requested. Restart Blender for full reload.")
            return {'FINISHED'}
        except Exception as e:
            self.report({'ERROR'}, f"Reload failed: {str(e)}")
            return {'CANCELLED'}

# ===================================================================
# ENREGISTREMENT
# ===================================================================

classes = [
    TOKYO_V2_PT_algorithm_panel,
    TOKYO_V2_PT_parameters_panel,
    TOKYO_V2_PT_textures_panel,
    TOKYO_V2_PT_advanced_panel,
    TOKYO_V2_PT_generation_panel,
    TOKYO_V2_OT_set_mode,
    TOKYO_V2_OT_clear_scene,
    TOKYO_V2_OT_reload_system,
]

def register():
    """Enregistrement de l'interface unifiée"""
    for cls in classes:
        bpy.utils.register_class(cls)
    print("🎨 Interface unifiée v2.0 enregistrée")

def unregister():
    """Désenregistrement de l'interface unifiée"""
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)
    print("🔄 Interface unifiée v2.0 désenregistrée")
import bpy
from bpy.types import Panel

class CITYGEN_PT_Panel(Panel):
    bl_label = "City Block Generator"
    bl_idname = "CITYGEN_PT_Panel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "CityGen"

    def draw(self, context):
        """Interface utilisateur simplifiée avec propriétés directes"""
        layout = self.layout
        scene = context.scene
        
        # Vérifier l'existence des propriétés directes
        required_props = ['citygen_width', 'citygen_length', 'citygen_max_floors', 'citygen_road_width']
        missing_props = [prop for prop in required_props if not hasattr(scene, prop)]
        
        if missing_props:
            layout.alert = True
            layout.label(text="Propriétés non initialisées", icon='ERROR')
            layout.label(text="Redémarrez Blender ou rechargez l'addon")
            return
        
        # Interface des paramètres de base
        layout.label(text="Paramètres de génération:", icon='SETTINGS')
        
        # Grille des paramètres
        grid = layout.grid_flow(columns=2, align=True)
        
        # Largeur et longueur
        grid.prop(scene, "citygen_width", text="Largeur")
        grid.prop(scene, "citygen_length", text="Longueur")
        
        # Étages et routes
        grid.prop(scene, "citygen_max_floors", text="Étages max")
        grid.prop(scene, "citygen_road_width", text="Routes")
        
        layout.separator()
        
        # Section génération
        layout.label(text="Actions:", icon='PLAY')
        col = layout.column(align=True)
        col.scale_y = 1.2
        col.operator("citygen.generate_city", text="Générer Quartier", icon='MESH_CUBE')
        col.operator("citygen.regenerate_roads_sidewalks", text="Régénérer Routes", icon='MOD_BUILD')
        
        layout.separator()
        
        # Section outils
        layout.label(text="Outils:", icon='TOOL_SETTINGS')
        col = layout.column(align=True)
        col.operator("citygen.diagnostic", text="Diagnostic", icon='CONSOLE')

classes = [CITYGEN_PT_Panel]

def register():
    for cls in classes:
        bpy.utils.register_class(cls)

def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)

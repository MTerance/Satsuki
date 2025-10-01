
import bpy
from bpy.types import Panel

class JPBG_PT_panel(Panel):
    bl_label = "JP Building Generator"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'JPBuild'
    bl_idname = "JPBG_PT_panel"

    def draw(self, context):
        layout = self.layout
        p = context.scene.jpbg

        row = layout.row(align=True)
        row.prop(p, "seed")
        row.operator("jpbg.random_seed", text="", icon='FILE_REFRESH')

        layout.prop(p, "building_type")
        col = layout.column(align=True)
        col.prop(p, "floors")
        col.prop(p, "floor_height")
        col.separator()
        col.prop(p, "footprint_x")
        col.prop(p, "footprint_y")
        layout.separator()

        box = layout.box()
        box.label(text="Parcelle")
        box.prop(p, "front_sidewalk")
        box.prop(p, "other_margin")

        layout.separator()
        layout.prop(p, "texture_category")

        layout.separator()
        layout.prop(p, "add_signage")
        layout.prop(p, "add_rooftop_units")
        layout.separator()
        layout.operator("jpbg.generate", icon='MOD_BUILD')

def register():
    bpy.utils.register_class(JPBG_PT_panel)

def unregister():
    bpy.utils.unregister_class(JPBG_PT_panel)

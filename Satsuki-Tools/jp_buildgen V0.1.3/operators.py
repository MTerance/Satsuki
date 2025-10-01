
import bpy
from bpy.types import Operator
from .core import generate_building

class JPBG_OT_generate(Operator):
    bl_idname = "jpbg.generate"
    bl_label = "Générer l'immeuble"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        props = context.scene.jpbg
        generate_building(context, props)
        self.report({'INFO'}, "Immeuble généré")
        return {'FINISHED'}

class JPBG_OT_random_seed(Operator):
    bl_idname = "jpbg.random_seed"
    bl_label = "Seed aléatoire"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        import random
        context.scene.jpbg.seed = random.randint(0, 999999)
        return {'FINISHED'}

def register():
    bpy.utils.register_class(JPBG_OT_generate)
    bpy.utils.register_class(JPBG_OT_random_seed)

def unregister():
    bpy.utils.unregister_class(JPBG_OT_random_seed)
    bpy.utils.unregister_class(JPBG_OT_generate)

"""
Version ultra-minimale pour tester l'enregistrement sans crash
"""
import bpy

class MinimalProperties(bpy.types.PropertyGroup):
    """Version ultra-basique pour test"""
    width = bpy.props.IntProperty(name="Largeur", default=5, min=1, max=50)
    length = bpy.props.IntProperty(name="Longueur", default=5, min=1, max=50)

class MINIMAL_OT_Test(bpy.types.Operator):
    bl_idname = "minimal.test"
    bl_label = "Test Minimal"
    bl_description = "Test basique"
    
    def execute(self, context):
        self.report({'INFO'}, "Test réussi!")
        return {'FINISHED'}

def register():
    print("=== TEST MINIMAL: Début enregistrement ===")
    try:
        bpy.utils.register_class(MinimalProperties)
        print("✅ MinimalProperties enregistrée")
        
        bpy.types.Scene.minimal_props = bpy.props.PointerProperty(type=MinimalProperties)
        print("✅ Lien Scene créé")
        
        bpy.utils.register_class(MINIMAL_OT_Test)
        print("✅ Opérateur enregistré")
        
        print("=== TEST MINIMAL: Succès complet ===")
        
    except Exception as e:
        print(f"❌ ERREUR TEST MINIMAL: {e}")
        import traceback
        print(f"Traceback: {traceback.format_exc()}")

def unregister():
    print("=== TEST MINIMAL: Désenregistrement ===")
    try:
        if hasattr(bpy.types.Scene, "minimal_props"):
            del bpy.types.Scene.minimal_props
        bpy.utils.unregister_class(MINIMAL_OT_Test)
        bpy.utils.unregister_class(MinimalProperties)
        print("✅ Désenregistrement réussi")
    except Exception as e:
        print(f"⚠️ Erreur désenregistrement: {e}")

if __name__ == "__main__":
    register()

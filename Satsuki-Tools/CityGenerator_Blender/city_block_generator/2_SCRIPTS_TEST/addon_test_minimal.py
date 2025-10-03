bl_info = {
    "name": "Test Minimal Properties",
    "version": (1, 0),
    "blender": (4, 0, 0),
    "category": "Development",
}

import bpy

class TestMinimalProps(bpy.types.PropertyGroup):
    test_int = bpy.props.IntProperty(default=5)

def register():
    print("=== TEST MINIMAL ADDON ===")
    try:
        bpy.utils.register_class(TestMinimalProps)
        print("✅ TestMinimalProps enregistrée")
        
        bpy.types.Scene.test_props = bpy.props.PointerProperty(type=TestMinimalProps)
        print("✅ Lien Scene créé")
        
        if hasattr(bpy.types, 'TestMinimalProps'):
            print("✅ TestMinimalProps accessible dans bpy.types")
        else:
            print("❌ TestMinimalProps NON accessible dans bpy.types")
            
    except Exception as e:
        print(f"❌ ERREUR TEST: {e}")
        import traceback
        print(traceback.format_exc())

def unregister():
    try:
        if hasattr(bpy.types.Scene, "test_props"):
            del bpy.types.Scene.test_props
        bpy.utils.unregister_class(TestMinimalProps)
        print("✅ Test désenregistré")
    except Exception as e:
        print(f"⚠️ Erreur désenregistrement test: {e}")

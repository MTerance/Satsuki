import bpy

class SimpleProps(bpy.types.PropertyGroup):
    test_int = bpy.props.IntProperty(default=5)

def register():
    print("=== DEBUT TEST SIMPLE ===")
    try:
        bpy.utils.register_class(SimpleProps)
        print("✅ SimpleProps enregistrée")
        
        if hasattr(bpy.types, 'SimpleProps'):
            print("✅ SimpleProps accessible")
        else:
            print("❌ SimpleProps NON accessible")
            
    except Exception as e:
        print(f"❌ ERREUR: {e}")
        import traceback
        print(traceback.format_exc())

def unregister():
    try:
        bpy.utils.unregister_class(SimpleProps)
    except:
        pass

if __name__ == "__main__":
    register()

bl_info = {
    "name": "City Block Generator",
    "author": "Assistant", 
    "version": (6, 14, 0),
    "blender": (4, 0, 0),
    "location": "View3D > Sidebar > CityGen Tab",
    "description": "Roads-first city generation with organic curves. Create road network first, then blocks, then buildings.",
    "category": "Add Mesh",
    "doc_url": "",
    "tracker_url": ""
}

import bpy
import traceback

try:
    from . import operators, ui
    modules_loaded = True
    print("✅ City Block Generator: Modules chargés")
except Exception as e:
    print(f"❌ Erreur import modules: {e}")
    modules_loaded = False

def register():
    """Enregistre l'addon"""
    try:
        print("🔧 Enregistrement City Block Generator v6.14.0...")
        
        if not modules_loaded:
            print("❌ Modules non chargés")
            return
        
        operators.register()
        ui.register()
        
        print("✅ City Block Generator enregistré")
        
    except Exception as e:
        print(f"❌ Erreur enregistrement: {e}")
        traceback.print_exc()

def unregister():
    """Désenregistre l'addon"""
    try:
        if modules_loaded:
            ui.unregister()
            operators.unregister()
        print("🔄 City Block Generator désenregistré")
    except Exception as e:
        print(f"❌ Erreur désenregistrement: {e}")

if __name__ == "__main__":
    register()

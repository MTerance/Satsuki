bl_info = {
    "name": "CityGen (1.7.33)",
    "author": "ChatGPT + User",
    "version": (1, 7, 33),
    "blender": (4, 5, 0),
    "location": "View3D > Sidebar > CityGen",
    "description": "Non-rectangular city generator with textures and props",
    "category": "Object",
}

if "bpy" in locals():
    import importlib
    importlib.reload(core)
    importlib.reload(operators)
    importlib.reload(panels)
    importlib.reload(properties)
else:
    from . import core, operators, panels, properties

import bpy

def register():
    core.register()
    operators.register()
    panels.register()
    properties.register()

def unregister():
    core.unregister()
    operators.unregister()
    panels.unregister()
    properties.unregister()

bl_info = {
    "name": "JP Building Generator",
    "author": "You + ChatGPT",
    "version": (0, 1, 4),
    "blender": (4, 5, 0),
    "location": "View3D > Sidebar > JPBuild",
    "description": "Generate modern Japanese-style buildings with parcel and texture categories.",
    "category": "Add Mesh",
}

import bpy
from . import properties, operators, panels, core

def register():
    properties.register()
    operators.register()
    panels.register()
    core.register()

def unregister():
    core.unregister()
    panels.unregister()
    operators.unregister()
    properties.unregister()

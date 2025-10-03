bl_info = {
    "name": "City Block Generator",
    "author": "Assistant",
    "version": (6, 13, 8),
    "blender": (4, 0, 0),
    "location": "View3D > Sidebar > CityGen",
    "description": "Generate procedural cities with variety",
    "category": "Add Mesh",
}

import bpy

class CITYGEN_OT_Generate(bpy.types.Operator):
    bl_idname = "citygen.generate"
    bl_label = "Generate City"
    bl_options = {'REGISTER', 'UNDO'}
    
    def execute(self, context):
        import random
        scene = context.scene
        width = scene.citygen_width
        length = scene.citygen_length
        variety = scene.citygen_variety
        
        colors_map = {
            'LOW': [(0.8,0.8,0.8,1.0), (0.7,0.7,0.7,1.0), (0.9,0.9,0.9,1.0)],
            'MEDIUM': [(0.85,0.82,0.75,1.0), (0.65,0.72,0.78,1.0), (0.75,0.78,0.70,1.0), (0.70,0.70,0.70,1.0), (0.82,0.75,0.72,1.0), (0.60,0.60,0.60,1.0)],
            'HIGH': [(0.85,0.82,0.75,1.0), (0.65,0.72,0.78,1.0), (0.75,0.78,0.70,1.0), (0.82,0.75,0.72,1.0), (0.70,0.72,0.75,1.0), (0.55,0.62,0.70,1.0), (0.45,0.45,0.45,1.0), (0.65,0.55,0.48,1.0)],
        }
        colors = colors_map.get(variety, colors_map['MEDIUM'])
        
        collection = bpy.data.collections.new(f"City_{width}x{length}")
        context.scene.collection.children.link(collection)
        
        for x in range(width):
            for y in range(length):
                for i in range(3):
                    pos_x = x*25 + random.uniform(2,18)
                    pos_y = y*25 + random.uniform(2,18)
                    height = random.uniform(6,18)
                    
                    bpy.ops.mesh.primitive_cube_add(location=(pos_x, pos_y, height))
                    obj = context.active_object
                    obj.scale = (random.uniform(4,8), random.uniform(4,8), height*2)
                    obj.name = f"Building_{x}_{y}_{i}"
                    
                    if obj.name in context.scene.collection.objects:
                        context.scene.collection.objects.unlink(obj)
                    collection.objects.link(obj)
                    
                    mat = bpy.data.materials.new(name=f"Mat_{x}_{y}_{i}")
                    mat.use_nodes = True
                    bsdf = mat.node_tree.nodes.get("Principled BSDF")
                    if bsdf:
                        bsdf.inputs['Base Color'].default_value = random.choice(colors)
                        bsdf.inputs['Roughness'].default_value = random.uniform(0.3, 0.7)
                    obj.data.materials.append(mat)
        
        self.report({'INFO'}, f"City {width}x{length} generated with {variety} variety")
        return {'FINISHED'}

class CITYGEN_PT_Panel(bpy.types.Panel):
    bl_label = "City Generator"
    bl_idname = "CITYGEN_PT_panel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "CityGen"
    
    def draw(self, context):
        layout = self.layout
        scene = context.scene
        
        layout.label(text="City Dimensions:")
        layout.prop(scene, "citygen_width")
        layout.prop(scene, "citygen_length")
        layout.prop(scene, "citygen_variety")
        
        layout.separator()
        layout.operator("citygen.generate", text="Generate City", icon='MESH_CUBE')

def register():
    bpy.utils.register_class(CITYGEN_OT_Generate)
    bpy.utils.register_class(CITYGEN_PT_Panel)
    
    bpy.types.Scene.citygen_width = bpy.props.IntProperty(name="Width", default=3, min=2, max=5)
    bpy.types.Scene.citygen_length = bpy.props.IntProperty(name="Length", default=3, min=2, max=5)
    bpy.types.Scene.citygen_variety = bpy.props.EnumProperty(
        name="Variety",
        items=[('LOW', 'Low', '3 colors'), ('MEDIUM', 'Medium', '6 colors'), ('HIGH', 'High', '8 colors')],
        default='MEDIUM'
    )

def unregister():
    bpy.utils.unregister_class(CITYGEN_PT_Panel)
    bpy.utils.unregister_class(CITYGEN_OT_Generate)
    del bpy.types.Scene.citygen_width
    del bpy.types.Scene.citygen_length
    del bpy.types.Scene.citygen_variety

if __name__ == "__main__":
    register()

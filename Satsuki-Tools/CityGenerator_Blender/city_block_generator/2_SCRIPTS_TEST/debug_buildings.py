import bpy

def debug_building_generation():
    """Script de débogage pour tester la génération d'un bâtiment simple"""
    print("=== DÉBOGAGE GÉNÉRATION BÂTIMENT ===")
    
    # Nettoyer la scène
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete(use_global=False)
    
    # Test direct de création de cube
    print("1. Test création cube simple...")
    try:
        bpy.ops.mesh.primitive_cube_add(size=2, location=(0, 0, 1))
        cube = bpy.context.object
        if cube:
            cube.name = "test_cube"
            print(f"   ✅ Cube test créé: {cube.name} à {cube.location}")
        else:
            print("   ❌ Échec création cube test")
    except Exception as e:
        print(f"   ❌ Erreur création cube: {e}")
    
    # Test avec matériau
    print("2. Test création matériau...")
    try:
        mat = bpy.data.materials.new(name="test_material")
        mat.use_nodes = True
        nodes = mat.node_tree.nodes
        nodes.clear()
        
        # Ajouter un nœud de sortie
        output = nodes.new('ShaderNodeOutputMaterial')
        output.location = (0, 0)
        
        # Ajouter un nœud Principled BSDF
        principled = nodes.new('ShaderNodeBsdfPrincipled')
        principled.location = (-300, 0)
        principled.inputs[0].default_value = (0, 1, 0, 1)  # Vert
        
        # Connecter
        mat.node_tree.links.new(principled.outputs[0], output.inputs[0])
        print(f"   ✅ Matériau créé: {mat.name}")
        
        # Appliquer au cube
        if cube and cube.data:
            cube.data.materials.append(mat)
            print(f"   ✅ Matériau appliqué au cube")
        
    except Exception as e:
        print(f"   ❌ Erreur matériau: {e}")
    
    print("=== FIN DÉBOGAGE ===")

if __name__ == "__main__":
    debug_building_generation()

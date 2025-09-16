import bpy

# Test de création d'un bâtiment simple pour diagnostic
def test_simple_building():
    """Test de création d'un bâtiment simple pour débogage"""
    print("=== TEST SIMPLE BÂTIMENT ===")
    
    # Nettoyer la scène
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete(use_global=False)
    
    try:
        # Créer un cube simple avec les bonnes dimensions
        print("1. Création cube primitif...")
        bpy.ops.mesh.primitive_cube_add(size=2, location=(0, 0, 1))
        cube = bpy.context.object
        
        if cube:
            print(f"✅ Cube créé: {cube.name}")
            print(f"Position: {cube.location}")
            print(f"Échelle: {cube.scale}")
            
            # Renommer
            cube.name = "TEST_Building"
            
            # Créer un matériau vert
            mat = bpy.data.materials.new(name="test_green")
            mat.use_nodes = True
            nodes = mat.node_tree.nodes
            nodes.clear()
            
            # Output node
            output = nodes.new('ShaderNodeOutputMaterial')
            output.location = (0, 0)
            
            # Principled BSDF
            principled = nodes.new('ShaderNodeBsdfPrincipled')
            principled.location = (-300, 0)
            principled.inputs[0].default_value = (0, 1, 0, 1)  # Vert
            
            # Connecter
            mat.node_tree.links.new(principled.outputs[0], output.inputs[0])
            
            # Appliquer
            cube.data.materials.append(mat)
            
            print(f"✅ Matériau vert appliqué")
            print(f"Le cube devrait être visible dans la vue 3D!")
            
            return True
        else:
            print("❌ Échec création cube")
            return False
            
    except Exception as e:
        print(f"❌ ERREUR: {e}")
        return False

# Exécuter le test
if __name__ == "__main__":
    result = test_simple_building()
    print(f"Résultat du test: {'SUCCÈS' if result else 'ÉCHEC'}")

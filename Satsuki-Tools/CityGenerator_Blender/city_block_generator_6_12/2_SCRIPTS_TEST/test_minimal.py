# Script de test MINIMAL pour identifier le problème - Exécuter dans Blender
import bpy

print("=== TEST MINIMAL BÂTIMENTS ===")

# 1. Nettoyer la scène
bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete(use_global=False)

# 2. Créer un cube simple directement pour vérifier que Blender fonctionne
print("Test création cube direct...")
bpy.ops.mesh.primitive_cube_add(location=(0, 0, 1))
test_cube = bpy.context.active_object
test_cube.name = "TestCube_Direct"
print(f"✅ Cube direct créé: {test_cube.name}")

# 3. Test de la fonction create_cube_with_center_bottom_origin
try:
    print("Test fonction create_cube_with_center_bottom_origin...")
    from city_block_generator_6_12.generator import create_cube_with_center_bottom_origin
    
    result_cube = create_cube_with_center_bottom_origin(2, 2, 4, (5, 5, 0))
    if result_cube:
        print(f"✅ Cube créé par fonction: {result_cube.name} à {result_cube.location}")
    else:
        print("❌ Fonction create_cube_with_center_bottom_origin a retourné None")
        
except Exception as e:
    print(f"❌ Erreur fonction create_cube: {e}")
    import traceback
    traceback.print_exc()

# 4. Test direct de generate_rectangular_building
try:
    print("Test fonction generate_rectangular_building...")
    from city_block_generator_6_12.generator import generate_rectangular_building, create_material
    
    # Créer un matériau simple
    test_mat = create_material("TestMat", (0, 1, 0))
    if test_mat:
        print(f"✅ Matériau créé: {test_mat.name}")
        
        # Tester la génération de bâtiment
        result_building = generate_rectangular_building(10, 10, 4, 4, 8, test_mat, 1)
        if result_building:
            print(f"✅ Bâtiment créé: {result_building.name} à {result_building.location}")
        else:
            print("❌ generate_rectangular_building a retourné None")
    else:
        print("❌ Impossible de créer le matériau")
        
except Exception as e:
    print(f"❌ Erreur génération bâtiment: {e}")
    import traceback
    traceback.print_exc()

# 5. Compter les objets
print("\nObjets dans la scène:")
all_objects = bpy.context.scene.objects
for obj in all_objects:
    print(f"  - {obj.name} à {obj.location}")

print(f"Total: {len(all_objects)} objets")
print("=== FIN TEST MINIMAL ===")

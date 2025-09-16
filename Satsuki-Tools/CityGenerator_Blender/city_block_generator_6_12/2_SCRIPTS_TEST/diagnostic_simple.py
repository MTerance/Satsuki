# Script de diagnostic simple - Exécuter dans Blender
import bpy

print("=== DIAGNOSTIC SIMPLE GÉNÉRATION BÂTIMENTS ===")

# 1. Tester la création d'un cube simple
print("\n1. Test création cube simple...")
try:
    bpy.ops.mesh.primitive_cube_add(location=(0, 0, 1))
    cube = bpy.context.active_object
    cube.name = "Test_Cube"
    print(f"✅ Cube créé: {cube.name}")
except Exception as e:
    print(f"❌ Échec création cube: {e}")

# 2. Vérifier les propriétés de l'addon
print("\n2. Vérification propriétés addon...")
scene = bpy.context.scene
props_status = {
    'citygen_width': getattr(scene, 'citygen_width', 'MANQUANT'),
    'citygen_length': getattr(scene, 'citygen_length', 'MANQUANT'), 
    'citygen_max_floors': getattr(scene, 'citygen_max_floors', 'MANQUANT'),
    'citygen_buildings_per_block': getattr(scene, 'citygen_buildings_per_block', 'MANQUANT'),
    'citygen_seamless_roads': getattr(scene, 'citygen_seamless_roads', 'MANQUANT'),
    'citygen_building_variety': getattr(scene, 'citygen_building_variety', 'MANQUANT'),
    'citygen_height_variation': getattr(scene, 'citygen_height_variation', 'MANQUANT')
}

for prop, value in props_status.items():
    print(f"  {prop}: {value}")

# 3. Test import du générateur
print("\n3. Test import générateur...")
try:
    addon_name = "city_block_generator_6_12"
    if addon_name in bpy.context.preferences.addons:
        print(f"✅ Addon {addon_name} activé")
        
        from city_block_generator_6_12.generator import generate_city
        print("✅ Import generate_city réussi")
        
        # Test d'appel simple avec debug
        print("\n4. Test appel generate_city...")
        result = generate_city(bpy.context, regen_only=False)
        print(f"Résultat generate_city: {result}")
        
    else:
        print(f"❌ Addon {addon_name} non activé")
        
except Exception as e:
    print(f"❌ Erreur import/test: {e}")
    import traceback
    traceback.print_exc()

# 4. Compter les objets après test
print("\n5. Objets dans la scène après test:")
all_objects = bpy.context.scene.objects
for obj_type in ['Road', 'Building', 'Sidewalk', 'Test']:
    objects = [obj for obj in all_objects if obj_type in obj.name]
    print(f"  {obj_type}: {len(objects)}")

print(f"\nTotal objets: {len(all_objects)}")
print("=== FIN DIAGNOSTIC ===")

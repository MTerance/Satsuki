# Test de l'origine centre bas pour City Block Generator
# À exécuter dans la console Python de Blender

import bpy

print("🧪 TEST ORIGINE CENTRE BAS - CITY BLOCK GENERATOR")
print("="*60)

# Supprimer tous les objets existants
bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete(use_global=False)

# Test 1: Créer un cube avec la nouvelle fonction
print("\n1️⃣ Test création cube avec origine centre bas:")
try:
    # Importer les fonctions du module
    import sys
    if "city_block_generator_6_12" in sys.modules:
        from city_block_generator_6_12.generator import create_cube_with_center_bottom_origin, set_origin_to_center_bottom
        
        # Créer un cube test
        cube = create_cube_with_center_bottom_origin(4, 6, 8, (0, 0, 0))
        
        if cube:
            print(f"   ✅ Cube créé: {cube.name}")
            print(f"   📍 Position: x={cube.location.x}, y={cube.location.y}, z={cube.location.z}")
            print(f"   📏 Dimensions: {cube.dimensions.x:.2f} x {cube.dimensions.y:.2f} x {cube.dimensions.z:.2f}")
            
            # Vérifier que l'origine est au centre bas
            mesh = cube.data
            if mesh.vertices:
                z_coords = [v.co.z for v in mesh.vertices]
                z_min = min(z_coords)
                z_max = max(z_coords)
                print(f"   📐 Z mesh: min={z_min:.3f}, max={z_max:.3f}")
                
                if abs(z_min) < 0.001:  # Z minimum proche de 0
                    print("   ✅ Origine correctement placée au centre bas")
                else:
                    print("   ❌ Origine incorrecte")
        else:
            print("   ❌ Échec création cube")
            
    else:
        print("   ❌ Module city_block_generator_6_12 non chargé")

except Exception as e:
    print(f"   ❌ Erreur: {e}")

# Test 2: Générer une petite ville
print("\n2️⃣ Test génération ville 2x2:")
try:
    if hasattr(bpy.context.scene, 'citygen_props'):
        props = bpy.context.scene.citygen_props
        
        # Configurer pour un test simple
        props.width = 2
        props.length = 2
        props.max_floors = 3
        props.road_width = 2.0
        props.sidewalk_width = 0.5
        
        # Générer la ville
        from city_block_generator_6_12.generator import generate_city
        success = generate_city(bpy.context)
        
        if success:
            print("   ✅ Ville générée avec succès")
            
            # Analyser les objets créés
            objects_by_type = {
                'buildings': [],
                'roads': [],
                'sidewalks': []
            }
            
            for obj in bpy.data.objects:
                if obj.name.startswith('batiment'):
                    objects_by_type['buildings'].append(obj)
                elif obj.name.startswith('road'):
                    objects_by_type['roads'].append(obj)
                elif obj.name.startswith('sidewalk'):
                    objects_by_type['sidewalks'].append(obj)
            
            print(f"   📊 Objets créés:")
            print(f"      • Bâtiments: {len(objects_by_type['buildings'])}")
            print(f"      • Routes: {len(objects_by_type['roads'])}")
            print(f"      • Trottoirs: {len(objects_by_type['sidewalks'])}")
            
            # Vérifier les positions des bâtiments
            print(f"   📍 Positions des bâtiments:")
            for i, building in enumerate(objects_by_type['buildings'][:3]):  # Premiers 3 seulement
                loc = building.location
                dim = building.dimensions
                print(f"      • {building.name}: pos=({loc.x:.2f}, {loc.y:.2f}, {loc.z:.2f}), dim=({dim.x:.2f}, {dim.y:.2f}, {dim.z:.2f})")
                
                # Vérifier que le bâtiment est au-dessus du sol
                if loc.z > 0:
                    print(f"        ✅ Au-dessus du sol (z={loc.z:.3f})")
                else:
                    print(f"        ❌ Sous le sol (z={loc.z:.3f})")
                    
        else:
            print("   ❌ Échec génération ville")
    else:
        print("   ❌ Propriétés citygen_props non disponibles")
        
except Exception as e:
    print(f"   ❌ Erreur: {e}")
    import traceback
    traceback.print_exc()

# Test 3: Vérification de l'alignement
print("\n3️⃣ Test alignement des objets:")
try:
    roads = [obj for obj in bpy.data.objects if obj.name.startswith('road')]
    sidewalks = [obj for obj in bpy.data.objects if obj.name.startswith('sidewalk')]
    buildings = [obj for obj in bpy.data.objects if obj.name.startswith('batiment')]
    
    print(f"   📏 Vérification des hauteurs Z:")
    
    # Routes doivent être au niveau le plus bas
    if roads:
        road_z = roads[0].location.z
        print(f"      • Routes: z={road_z:.3f} (plus bas)")
        
    # Trottoirs légèrement au-dessus
    if sidewalks:
        sidewalk_z = sidewalks[0].location.z
        print(f"      • Trottoirs: z={sidewalk_z:.3f} (au-dessus routes)")
        
    # Bâtiments encore au-dessus
    if buildings:
        building_z = buildings[0].location.z
        print(f"      • Bâtiments: z={building_z:.3f} (au-dessus trottoirs)")
        
        # Vérifier l'ordre des hauteurs
        if roads and sidewalks and buildings:
            if road_z < sidewalk_z < building_z:
                print("   ✅ Ordre des hauteurs correct: routes < trottoirs < bâtiments")
            else:
                print("   ❌ Ordre des hauteurs incorrect")
    
except Exception as e:
    print(f"   ❌ Erreur: {e}")

print("\n" + "="*60)
print("🏁 TEST TERMINÉ")
print("\n💡 Instructions:")
print("   1. Vérifiez la vue 3D pour voir les objets")
print("   2. Tous les objets devraient avoir leur origine au centre bas")
print("   3. Les bâtiments doivent être alignés sur les trottoirs")
print("   4. Les routes doivent s'aligner parfaitement")
print("="*60)

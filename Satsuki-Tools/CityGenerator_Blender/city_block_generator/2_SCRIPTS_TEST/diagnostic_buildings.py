# Script de diagnostic spécialisé pour les bâtiments - Exécuter dans Blender
import bpy

print("=== DIAGNOSTIC SPÉCIALISÉ BÂTIMENTS ===")

# Test direct de génération de bâtiment simple
try:
    print("\n1. Test import direct des fonctions...")
    from city_block_generator.generator import (
        generate_rectangular_building, 
        create_material,
        create_cube_with_center_bottom_origin
    )
    print("✅ Import des fonctions réussi")
    
    print("\n2. Test création matériau...")
    test_mat = create_material("TestBuildingMat", (0.5, 1.0, 0.0))
    if test_mat:
        print(f"✅ Matériau créé: {test_mat.name}")
    else:
        print("❌ Échec création matériau")
        
    print("\n3. Test création cube direct...")
    test_cube = create_cube_with_center_bottom_origin(4, 4, 8, (5, 5, 0))
    if test_cube:
        print(f"✅ Cube créé: {test_cube.name} à {test_cube.location}")
    else:
        print("❌ Échec création cube")
        
    print("\n4. Test génération bâtiment rectangulaire...")
    test_building = generate_rectangular_building(10, 10, 6, 6, 12, test_mat, 999)
    if test_building:
        print(f"✅ Bâtiment créé: {test_building.name} à {test_building.location}")
    else:
        print("❌ Échec génération bâtiment")
        
except Exception as e:
    print(f"❌ Erreur lors des tests: {e}")
    import traceback
    traceback.print_exc()

print("\n5. Test génération complète avec debug...")
try:
    # Supprimer les objets existants
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete(use_global=False)
    
    # Configurer les paramètres
    scene = bpy.context.scene
    scene.citygen_width = 2
    scene.citygen_length = 2
    scene.citygen_max_floors = 6
    scene.citygen_buildings_per_block = 1
    scene.citygen_seamless_roads = False  # Pour avoir des trottoirs
    scene.citygen_building_variety = 'LOW'  # Simple pour debug
    scene.citygen_height_variation = 0.0   # Pas de variation
    
    print(f"Configuration: {scene.citygen_width}x{scene.citygen_length}, {scene.citygen_buildings_per_block} bât/bloc")
    
    # Appel direct avec debug forcé
    from city_block_generator.generator import generate_city
    
    print("\n🚀 APPEL generate_city avec regen_only=False...")
    result = generate_city(bpy.context, regen_only=False)
    print(f"Résultat generate_city: {result}")
    
    # Compter les objets après génération
    print("\n6. Analyse des objets créés...")
    all_objects = bpy.context.scene.objects
    roads = [obj for obj in all_objects if 'Road' in obj.name or 'road' in obj.name.lower()]
    buildings = [obj for obj in all_objects if 'Building' in obj.name or 'batiment' in obj.name.lower()]
    sidewalks = [obj for obj in all_objects if 'Sidewalk' in obj.name or 'trottoir' in obj.name.lower()]
    
    print(f"📊 RÉSULTATS FINAUX:")
    print(f"  🛣️ Routes: {len(roads)} - {[r.name for r in roads[:3]]}")
    print(f"  🏢 Bâtiments: {len(buildings)} - {[b.name for b in buildings[:3]]}")
    print(f"  🟦 Trottoirs: {len(sidewalks)} - {[s.name for s in sidewalks[:3]]}")
    print(f"  📦 Total: {len(all_objects)} objets")
    
    if len(buildings) == 0:
        print("\n🚨 AUCUN BÂTIMENT GÉNÉRÉ!")
        print("💡 Vérifiez la console Python pour voir les messages de debug détaillés")
        print("💡 Recherchez les messages commençant par '🏠 SECTION BÂTIMENT'")
    else:
        print(f"\n✅ SUCCÈS! {len(buildings)} bâtiment(s) généré(s)")
        
except Exception as e:
    print(f"❌ Erreur génération complète: {e}")
    import traceback
    traceback.print_exc()

print("\n=== FIN DIAGNOSTIC SPÉCIALISÉ ===")

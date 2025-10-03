# Script de test de génération corrigé - Exécuter dans Blender
import bpy

print("=== TEST GÉNÉRATION AVEC BÂTIMENTS VARIÉS ===")

# 1. Recharger l'addon avec force
addon_name = "city_block_generator"
if addon_name in bpy.context.preferences.addons:
    print("Rechargement de l'addon...")
    bpy.ops.preferences.addon_disable(module=addon_name)
    
import sys
modules_to_remove = [m for m in sys.modules if addon_name in m]
for m in modules_to_remove:
    del sys.modules[m]

bpy.ops.preferences.addon_enable(module=addon_name)

# 2. Supprimer tous les objets de la scène
bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete(use_global=False)

# 3. Configuration de test avec variété
scene = bpy.context.scene
scene.citygen_width = 3
scene.citygen_length = 3  
scene.citygen_max_floors = 8
scene.citygen_road_width = 4.0
scene.citygen_buildings_per_block = 2  # 2 bâtiments par bloc
scene.citygen_seamless_roads = True    # Routes collées
scene.citygen_building_variety = 'HIGH'  # Variété élevée
scene.citygen_height_variation = 0.8   # Variation importante

print("✅ Configuration appliquée:")
print(f"  - Grille: {scene.citygen_width}x{scene.citygen_length}")
print(f"  - Bâtiments par bloc: {scene.citygen_buildings_per_block}")
print(f"  - Variété: {scene.citygen_building_variety}")
print(f"  - Variation hauteur: {scene.citygen_height_variation}")
print(f"  - Routes collées: {scene.citygen_seamless_roads}")

# 4. Générer la ville
print("\n🏗️ GÉNÉRATION DE LA VILLE...")
try:
    bpy.ops.citygen.generate_quarter()
    print("✅ Génération terminée!")
    
    # 5. Compter les objets créés
    all_objects = bpy.context.scene.objects
    roads = [obj for obj in all_objects if 'Road' in obj.name]
    buildings = [obj for obj in all_objects if 'Building' in obj.name]
    sidewalks = [obj for obj in all_objects if 'Sidewalk' in obj.name]
    
    print(f"\n📊 RÉSULTATS:")
    print(f"  🛣️ Routes: {len(roads)}")
    print(f"  🏢 Bâtiments: {len(buildings)}")
    print(f"  🟦 Trottoirs: {len(sidewalks)}")
    print(f"  📦 Total objets: {len(all_objects)}")
    
    if len(buildings) > 0:
        print(f"  ✅ SUCCÈS! Bâtiments générés avec variété!")
        print(f"  🎯 Attendu: {scene.citygen_width * scene.citygen_length * scene.citygen_buildings_per_block} bâtiments")
        print(f"  📈 Obtenu: {len(buildings)} bâtiments")
        
        # Analyser les types de bâtiments
        building_types = {}
        for building in buildings:
            if hasattr(building, 'name'):
                # Extraire le type du nom si possible
                name = building.name
                if 'Tower' in name:
                    building_types['Tower'] = building_types.get('Tower', 0) + 1
                elif 'L_Shape' in name:
                    building_types['L_Shape'] = building_types.get('L_Shape', 0) + 1
                elif 'U_Shape' in name:
                    building_types['U_Shape'] = building_types.get('U_Shape', 0) + 1
                else:
                    building_types['Rectangular'] = building_types.get('Rectangular', 0) + 1
        
        print(f"  🎨 Types de bâtiments détectés:")
        for type_name, count in building_types.items():
            print(f"    - {type_name}: {count}")
            
    else:
        print(f"  ❌ PROBLÈME: Aucun bâtiment généré!")
        print(f"  🔍 Vérifiez la console Python de Blender pour les erreurs")
        
except Exception as e:
    print(f"❌ ERREUR lors de la génération: {e}")
    import traceback
    traceback.print_exc()

print("\n🎯 Test terminé. Vérifiez la vue 3D pour voir les résultats!")

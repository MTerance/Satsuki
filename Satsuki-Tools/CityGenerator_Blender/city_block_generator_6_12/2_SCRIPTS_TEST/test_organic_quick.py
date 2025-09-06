# Script de test rapide pour le mode organique
import bpy

# Configuration de test pour le mode organique
scene = bpy.context.scene

print("=== TEST MODE ORGANIQUE ===")

# Paramètres de base
scene.citygen_width = 3
scene.citygen_length = 3
scene.citygen_max_floors = 6
scene.citygen_road_width = 4.0
scene.citygen_buildings_per_block = 1

# Paramètres organiques
scene.citygen_organic_mode = True
scene.citygen_polygon_min_sides = 4
scene.citygen_polygon_max_sides = 6
scene.citygen_road_curve_intensity = 0.7
scene.citygen_block_size_variation = 0.4

print(f"Configuration:")
print(f"  - Grille: {scene.citygen_width}x{scene.citygen_length}")
print(f"  - Mode organique: {scene.citygen_organic_mode}")
print(f"  - Côtés blocs: {scene.citygen_polygon_min_sides}-{scene.citygen_polygon_max_sides}")
print(f"  - Intensité courbes: {scene.citygen_road_curve_intensity}")
print(f"  - Variation blocs: {scene.citygen_block_size_variation}")

print("Lancement de la génération organique...")

# Appeler l'opérateur de génération
try:
    bpy.ops.citygen.generate_city()
    print("✅ Génération terminée avec succès")
except Exception as e:
    print(f"❌ Erreur: {e}")

# Compter les objets créés
all_objects = bpy.context.scene.objects
buildings = [obj for obj in all_objects if 'building' in obj.name.lower() or 'organic' in obj.name.lower()]
blocks = [obj for obj in all_objects if 'polygonal' in obj.name.lower() or 'block' in obj.name.lower()]
roads = [obj for obj in all_objects if 'road' in obj.name.lower() or 'route' in obj.name.lower()]

print(f"\nRésultats:")
print(f"  📦 Blocs polygonaux: {len(blocks)}")
print(f"  🏢 Bâtiments: {len(buildings)}")
print(f"  🛣️ Routes: {len(roads)}")
print(f"  📊 Total objets: {len(all_objects)}")

if len(blocks) > 0:
    print("\n✅ MODE ORGANIQUE FONCTIONNE!")
    print("Vous devriez voir des blocs polygonaux avec des bâtiments verts")
else:
    print("\n❌ MODE ORGANIQUE A UN PROBLÈME")
    print("Aucun bloc polygonal détecté")

# Script de rechargement forcé avec variété de bâtiments - À exécuter dans Blender
import bpy
import sys

print("=== FORCE RELOAD CITY BLOCK GENERATOR AVEC VARIÉTÉ ===")

# 1. Désactiver l'addon
addon_name = "city_block_generator_6_12"
if addon_name in bpy.context.preferences.addons:
    print("Désactivation de l'addon...")
    bpy.ops.preferences.addon_disable(module=addon_name)

# 2. Nettoyer le cache Python
print("Nettoyage du cache Python...")
modules_to_remove = [m for m in sys.modules if addon_name in m]
for m in modules_to_remove:
    print(f"  Suppression du module: {m}")
    del sys.modules[m]

# 3. Supprimer toutes les anciennes propriétés
print("Nettoyage de toutes les propriétés...")
scene = bpy.context.scene

all_props = ['citygen_props', 'citygen_width', 'citygen_length', 'citygen_max_floors', 
             'citygen_road_width', 'citygen_buildings_per_block', 'citygen_seamless_roads',
             'citygen_building_variety', 'citygen_height_variation']

for prop in all_props:
    if hasattr(scene, prop):
        print(f"  Suppression de {prop}")
        delattr(scene, prop)

# 4. Réactiver l'addon
print("Réactivation de l'addon...")
try:
    bpy.ops.preferences.addon_enable(module=addon_name)
    print("✓ Addon réactivé")
except Exception as e:
    print(f"✗ Erreur lors de la réactivation: {e}")

# 5. Configuration de test avec variété
print("Configuration de test avec variété...")
if hasattr(scene, 'citygen_width'):
    scene.citygen_width = 3
    scene.citygen_length = 3
    scene.citygen_max_floors = 8
    scene.citygen_road_width = 4.0
    scene.citygen_buildings_per_block = 2
    scene.citygen_seamless_roads = True
    scene.citygen_building_variety = 'HIGH'  # Variété élevée pour tester
    scene.citygen_height_variation = 0.7     # Variation importante
    
    print("✅ Configuration appliquée:")
    print(f"  - Grille: {scene.citygen_width}x{scene.citygen_length}")
    print(f"  - Bâtiments par bloc: {scene.citygen_buildings_per_block}")
    print(f"  - Variété des formes: {scene.citygen_building_variety}")
    print(f"  - Variation des hauteurs: {scene.citygen_height_variation}")
    print(f"  - Routes collées: {scene.citygen_seamless_roads}")
else:
    print("⚠️ Propriétés non encore disponibles - vérifiez l'enregistrement de l'addon")

print("✅ RECHARGEMENT FORCÉ TERMINÉ!")
print("🎯 Testez maintenant la génération avec variété élevée!")
print("🏗️ Vous devriez voir: tours, bâtiments en L/U, hauteurs variées...")

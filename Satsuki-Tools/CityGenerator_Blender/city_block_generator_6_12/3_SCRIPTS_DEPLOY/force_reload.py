# Script pour forcer le rechargement complet de l'addon

import bpy
import sys
import importlib

def force_reload_addon():
    """Force le rechargement complet de l'addon City Block Generator"""
    
    print("=== FORCE RELOAD CITY BLOCK GENERATOR ===")
    
    # 1. Désactiver l'addon s'il est actif
    addon_name = "city_block_generator_6_12"
    if addon_name in bpy.context.preferences.addons:
        print("Désactivation de l'addon...")
        bpy.ops.preferences.addon_disable(module=addon_name)
    
    # 2. Supprimer tous les modules de l'addon du cache Python
    print("Nettoyage du cache Python...")
    modules_to_remove = []
    for module_name in sys.modules:
        if addon_name in module_name:
            modules_to_remove.append(module_name)
    
    for module_name in modules_to_remove:
        print(f"  Suppression du module: {module_name}")
        del sys.modules[module_name]
    
    # 3. Supprimer les anciennes propriétés si elles existent
    print("Nettoyage des anciennes propriétés...")
    scene = bpy.context.scene
    
    # Supprimer les anciennes propriétés citygen_props si elles existent
    if hasattr(scene, 'citygen_props'):
        print("  Suppression des anciennes propriétés citygen_props")
        del scene.citygen_props
    
    # 4. Initialiser les nouvelles propriétés directes
    print("Initialisation des nouvelles propriétés...")
    scene.citygen_width = 5
    scene.citygen_length = 5 
    scene.citygen_max_floors = 8
    scene.citygen_road_width = 4.0
    scene.citygen_buildings_per_block = 1
    scene.citygen_seamless_roads = True
    
    print(f"  citygen_width: {scene.citygen_width}")
    print(f"  citygen_length: {scene.citygen_length}")
    print(f"  citygen_max_floors: {scene.citygen_max_floors}")
    print(f"  citygen_road_width: {scene.citygen_road_width}")
    print(f"  citygen_buildings_per_block: {scene.citygen_buildings_per_block}")
    print(f"  citygen_seamless_roads: {scene.citygen_seamless_roads}")    # 5. Réactiver l'addon
    print("Réactivation de l'addon...")
    try:
        bpy.ops.preferences.addon_enable(module=addon_name)
        print("✓ Addon réactivé avec succès")
    except Exception as e:
        print(f"✗ Erreur lors de la réactivation: {e}")
        return False
    
    # 6. Vérification finale
    print("Vérification finale...")
    if addon_name in bpy.context.preferences.addons:
        print("✓ Addon correctement chargé")
        return True
    else:
        print("✗ Addon non trouvé après réactivation")
        return False

# Script principal
if __name__ == "__main__":
    force_reload_addon()

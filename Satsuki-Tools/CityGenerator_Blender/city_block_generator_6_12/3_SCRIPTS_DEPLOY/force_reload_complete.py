# Script de rechargement forcé - À exécuter dans la console Blender
import bpy
import sys
import importlib

def force_reload_citygen():
    """Force le rechargement complet avec nouvelles propriétés"""
    
    print("=== FORCE RELOAD CITY BLOCK GENERATOR ===")
    
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
    
    # 3. Supprimer les anciennes propriétés
    print("Nettoyage des anciennes propriétés...")
    scene = bpy.context.scene
    
    # Supprimer les anciennes propriétés si elles existent
    old_props = ['citygen_props']
    for prop in old_props:
        if hasattr(scene, prop):
            print(f"  Suppression de {prop}")
            delattr(scene, prop)
    
    # Supprimer les nouvelles propriétés pour les réinitialiser
    new_props = ['citygen_width', 'citygen_length', 'citygen_max_floors', 
                 'citygen_road_width', 'citygen_buildings_per_block', 'citygen_seamless_roads']
    for prop in new_props:
        if hasattr(scene, prop):
            print(f"  Suppression de {prop} pour réinitialisation")
            delattr(scene, prop)
    
    # 4. Réactiver l'addon
    print("Réactivation de l'addon...")
    try:
        bpy.ops.preferences.addon_enable(module=addon_name)
        print("✓ Addon réactivé")
    except Exception as e:
        print(f"✗ Erreur lors de la réactivation: {e}")
        return False
    
    # 5. Vérifier les nouvelles propriétés
    print("Vérification des propriétés...")
    for prop in new_props:
        if hasattr(scene, prop):
            value = getattr(scene, prop)
            print(f"  ✓ {prop}: {value}")
        else:
            print(f"  ✗ {prop}: MANQUANT")
    
    # 6. Configuration de test
    print("Configuration de test...")
    scene.citygen_width = 3
    scene.citygen_length = 3
    scene.citygen_max_floors = 6
    scene.citygen_road_width = 4.0
    scene.citygen_buildings_per_block = 2
    scene.citygen_seamless_roads = True
    
    print("✅ RECHARGEMENT FORCÉ TERMINÉ!")
    print("L'addon est prêt avec les nouvelles fonctionnalités.")
    return True

# Exécuter le rechargement
if __name__ == "__main__":
    force_reload_citygen()

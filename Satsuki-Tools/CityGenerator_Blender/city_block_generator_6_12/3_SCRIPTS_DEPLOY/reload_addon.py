# Script de rechargement pour le développement
# Exécutez ce script dans Blender pour recharger l'addon après modifications

import bpy
import importlib
import sys
import os

# Nom du module de l'addon
addon_name = "city_block_generator_6_12"

def reload_addon():
    """Recharge complètement l'addon City Block Generator"""
    try:
        print("=== Rechargement de l'addon City Block Generator ===")
        
        # Désactiver l'addon s'il est actif
        if addon_name in bpy.context.preferences.addons:
            print("Désactivation de l'addon...")
            bpy.ops.preferences.addon_disable(module=addon_name)
        
        # Supprimer les modules du cache Python
        modules_to_remove = []
        for module_name in sys.modules.keys():
            if addon_name in module_name:
                modules_to_remove.append(module_name)
        
        for module_name in modules_to_remove:
            print(f"Suppression du module: {module_name}")
            del sys.modules[module_name]
        
        # Réactiver l'addon
        print("Réactivation de l'addon...")
        bpy.ops.preferences.addon_enable(module=addon_name)
        
        print("=== Rechargement terminé avec succès ===")
        
    except Exception as e:
        print(f"Erreur lors du rechargement: {e}")
        import traceback
        traceback.print_exc()

# Exécuter le rechargement
if __name__ == "__main__":
    reload_addon()
else:
    print("Le script n'est pas exécuté dans Blender.")

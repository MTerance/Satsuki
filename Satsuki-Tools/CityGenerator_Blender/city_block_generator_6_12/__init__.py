bl_info = {
    "name": "City Block Generator",
    "author": "Shomaa", 
    "version": (7, 1, 0),  # Version FINALE - erreur calculate_height_with_variation corrigée
    "blender": (4, 0, 0),
    "location": "View3D > Sidebar > CityGen Tab",
    "description": "Generate city blocks with diagonal roads, intersections, green apple buildings and pale pink roads. Includes auto-deployment tools.",
    "category": "Add Mesh",
    "doc_url": "",
    "tracker_url": ""
}

import bpy
import traceback

try:
    from . import operators, ui
    # Ne pas importer generator.py automatiquement pour éviter les crashes
    modules_loaded = True
    print("✅ Modules operators et ui chargés avec succès")
except Exception as e:
    print(f"ERREUR CRITIQUE lors de l'import des modules: {str(e)}")
    print(f"Traceback: {traceback.format_exc()}")
    modules_loaded = False

def register():
    """Enregistre l'addon avec gestion d'erreurs robuste"""
    try:
        print("=== Début d'enregistrement de l'addon City Block Generator ===")
        
        if not modules_loaded:
            print("ERREUR: Modules non chargés, impossible d'enregistrer l'addon")
            return
        
        # Enregistrer les modules dans l'ordre correct
        try:
            operators.register()
            print("Module operators enregistré avec succès")
        except Exception as e:
            print(f"ERREUR lors de l'enregistrement du module operators: {str(e)}")
            print(f"Traceback: {traceback.format_exc()}")
        
        try:
            ui.register()
            print("Module ui enregistré avec succès")
        except Exception as e:
            print(f"ERREUR lors de l'enregistrement du module ui: {str(e)}")
            print(f"Traceback: {traceback.format_exc()}")
        
        print("=== City Block Generator: Addon enregistré avec succès ===")
        
    except Exception as e:
        print(f"ERREUR CRITIQUE lors de l'enregistrement de l'addon: {str(e)}")
        print(f"Traceback: {traceback.format_exc()}")

def unregister():
    """Désenregistre l'addon avec gestion d'erreurs robuste"""
    try:
        print("=== Début de désenregistrement de l'addon City Block Generator ===")
        
        if not modules_loaded:
            print("AVERTISSEMENT: Modules non chargés lors du désenregistrement")
            return
        
        # Désenregistrer les modules dans l'ordre inverse
        try:
            ui.unregister()
            print("Module ui désenregistré avec succès")
        except Exception as e:
            print(f"ERREUR lors du désenregistrement du module ui: {str(e)}")
        
        try:
            operators.unregister()
            print("Module operators désenregistré avec succès")
        except Exception as e:
            print(f"ERREUR lors du désenregistrement du module operators: {str(e)}")
        
        print("=== City Block Generator: Addon désenregistré avec succès ===")
        
    except Exception as e:
        print(f"ERREUR CRITIQUE lors du désenregistrement de l'addon: {str(e)}")
        print(f"Traceback: {traceback.format_exc()}")
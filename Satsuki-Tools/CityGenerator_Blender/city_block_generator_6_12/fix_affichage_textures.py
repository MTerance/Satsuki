# SOLUTION IMMÉDIATE - Changer le mode d'affichage pour voir les textures
# À copier-coller dans la console Blender

import bpy

def activer_affichage_textures():
    print("🎨 Activation de l'affichage des textures...")
    
    # Parcourir toutes les vues 3D
    for area in bpy.context.screen.areas:
        if area.type == 'VIEW_3D':
            for space in area.spaces:
                if space.type == 'VIEW_3D':
                    # Changer en mode Material Preview
                    space.shading.type = 'MATERIAL'
                    print(f"✅ Mode changé vers: {space.shading.type}")
    
    print("🎯 Les textures devraient maintenant être visibles !")
    print("💡 Si ce n'est pas le cas, essayez le mode RENDERED (plus lent)")

# Exécuter
activer_affichage_textures()

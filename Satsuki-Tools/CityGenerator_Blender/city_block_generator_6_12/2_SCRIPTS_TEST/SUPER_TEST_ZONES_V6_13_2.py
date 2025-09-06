"""
SUPER TEST ZONES V6.13.2
Test très simple pour voir exactement le comportement des zones
Instructions: Exécuter dans Blender (Script Editor → Run Script)
"""

import bpy

def super_test_zones():
    """Test ultra-simple et direct"""
    print("🔥🔥🔥 === SUPER TEST ZONES V6.13.2 === 🔥🔥🔥")
    
    # Nettoyer d'abord
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete(use_global=False)
    
    # Configuration simple
    scene = bpy.context.scene
    scene.citygen_width = 3       # Grille 3x3 pour test simple
    scene.citygen_length = 3
    scene.citygen_organic_mode = True
    scene.citygen_road_first_method = True
    
    print(f"📊 Paramètres: grille {scene.citygen_width}x{scene.citygen_length}")
    print(f"🎯 ZONES ATTENDUES: {scene.citygen_width * scene.citygen_length} = 9 zones")
    
    # Lancer et capturer TOUS les logs
    print("🚀 === DÉBUT GÉNÉRATION - FOCUS ZONES ===")
    
    result = bpy.ops.citygen.generate_city()
    
    print("🔍 === FIN GÉNÉRATION - ANALYSE RÉSULTATS ===")
    print(f"📊 Résultat opération: {result}")
    
    # Compter les objets créés
    print("🔢 Objets créés dans la scène:")
    for obj in bpy.context.scene.objects:
        print(f"   - {obj.name}: {obj.type}")
    
    print("🎯 Test terminé - Recherchez dans les logs ci-dessus le nombre de zones!")

# Exécuter automatiquement
super_test_zones()

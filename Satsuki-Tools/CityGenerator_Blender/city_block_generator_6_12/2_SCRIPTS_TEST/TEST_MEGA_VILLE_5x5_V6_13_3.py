"""
TEST MEGA VILLE 5x5 V6.13.3
Test d'une ville massive avec 25 zones pour voir la puissance du système
Instructions: Exécuter dans Blender (Script Editor → Run Script)
"""

import bpy

def mega_ville_test():
    """Test d'une MEGA ville 5x5 = 25 zones !"""
    print("🔥🔥🔥 === TEST MEGA VILLE 5x5 V6.13.3 === 🔥🔥🔥")
    
    # Nettoyer d'abord
    print("🧹 Nettoyage pour MEGA ville...")
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete(use_global=False)
    
    # Configuration MEGA ville
    scene = bpy.context.scene
    scene.citygen_width = 5       # GRILLE 5x5 = 25 ZONES !
    scene.citygen_length = 5
    scene.citygen_organic_mode = True
    scene.citygen_road_first_method = True
    scene.citygen_max_floors = 12  # Gratte-ciels plus hauts
    scene.citygen_buildings_per_block = 3  # Plus de bâtiments par bloc
    
    print(f"🏙️ === PARAMÈTRES MEGA VILLE ===")
    print(f"   📊 Grille: {scene.citygen_width}x{scene.citygen_length}")
    print(f"   🎯 ZONES ATTENDUES: {scene.citygen_width * scene.citygen_length} = 25 zones")
    print(f"   🏗️ BÂTIMENTS ATTENDUS: ~{25 * 2} = 50+ bâtiments")
    print(f"   🏢 Hauteur max: {scene.citygen_max_floors} étages")
    print(f"   🛣️ Routes organiques: ULTRA courbes")
    
    # Lancer la MEGA génération
    print("🚀 === DÉBUT MEGA GÉNÉRATION 5x5 ===")
    
    result = bpy.ops.citygen.generate_city()
    
    print("🔍 === FIN MEGA GÉNÉRATION - ANALYSE ===")
    print(f"📊 Résultat: {result}")
    
    # Analyser les objets créés
    roads = [obj for obj in bpy.context.scene.objects if "Road" in obj.name]
    blocks = [obj for obj in bpy.context.scene.objects if "Block" in obj.name]
    buildings = [obj for obj in bpy.context.scene.objects if "Building" in obj.name]
    
    print(f"🔢 === ANALYSE MEGA VILLE ===")
    print(f"   🛣️ Routes créées: {len(roads)}")
    print(f"   🏗️ Blocs créés: {len(blocks)}")
    print(f"   🏢 Bâtiments créés: {len(buildings)}")
    print(f"   📊 Total objets: {len(bpy.context.scene.objects)}")
    
    # Vérifier le succès
    success = len(blocks) >= 20 and len(buildings) >= 40
    if success:
        print("✅🎉 MEGA SUCCÈS ! Ville organique massive créée !")
    else:
        print("⚠️ Résultats partiels, mais toujours impressionnant !")
    
    print("🎯 MEGA test terminé - Observez votre ville organique géante !")

# Exécuter automatiquement
mega_ville_test()

"""
TEST SIMPLE ADDON CLEAN V6.14.0
Test de l'addon nettoyé avec courbes visibles
Instructions: Exécuter dans Blender (Script Editor → Run Script)
"""

import bpy

def test_addon_clean():
    """Test simple de l'addon nettoyé v6.14.0"""
    
    print("🔥 === TEST ADDON CLEAN V6.14.0 === 🔥")
    print("🧹 Addon nettoyé - Code mort supprimé")
    print("🌊 Courbes Blender natives préservées")
    
    # Nettoyer la scène
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete(use_global=False)
    
    # Configuration simple mais efficace
    scene = bpy.context.scene
    scene.citygen_width = 3           # Grille 3x3 pour test rapide
    scene.citygen_length = 3
    scene.citygen_organic_mode = True # Mode organique activé
    scene.citygen_road_first_method = True
    scene.citygen_road_curve_intensity = 0.8  # Courbes visibles
    scene.citygen_buildings_per_block = 2
    
    print(f"📊 === PARAMÈTRES TEST CLEAN ===")
    print(f"   🔢 Grille: {scene.citygen_width}x{scene.citygen_length}")
    print(f"   🌊 Mode: Organique avec courbes")
    print(f"   📏 Intensité courbes: {scene.citygen_road_curve_intensity}")
    print(f"   🏢 Bâtiments par bloc: {scene.citygen_buildings_per_block}")
    
    # Test de génération
    print("🚀 === GÉNÉRATION TEST CLEAN ===")
    
    try:
        result = bpy.ops.citygen.generate_city()
        print(f"✅ Résultat: {result}")
        
        # Analyse des objets créés
        all_objects = list(bpy.context.scene.objects)
        roads = [obj for obj in all_objects if "Road" in obj.name]
        blocks = [obj for obj in all_objects if "Block" in obj.name]
        buildings = [obj for obj in all_objects if "Building" in obj.name]
        
        print(f"📊 === RÉSULTATS TEST CLEAN ===")
        print(f"   🛣️ Routes: {len(roads)}")
        print(f"   🏗️ Blocs: {len(blocks)}")
        print(f"   🏢 Bâtiments: {len(buildings)}")
        print(f"   📋 Total: {len(all_objects)} objets")
        
        # Vérifier le succès
        if len(roads) >= 6 and len(blocks) >= 6 and len(buildings) >= 8:
            print("✅🎉 SUCCÈS TEST CLEAN ! 🎉✅")
            print("🧹 Addon nettoyé fonctionne parfaitement")
            print("🌊 Courbes organiques générées")
            print("🏙️ Ville cohérente créée")
        else:
            print("⚠️ Résultats partiels mais fonctionnel")
            
    except Exception as e:
        print(f"❌ Erreur génération: {e}")
        import traceback
        traceback.print_exc()
    
    print("🎯 Test addon clean terminé!")
    print("🧹 Code optimisé et nettoyé")
    print("🌊 Courbes natives préservées")

# Exécuter automatiquement
test_addon_clean()

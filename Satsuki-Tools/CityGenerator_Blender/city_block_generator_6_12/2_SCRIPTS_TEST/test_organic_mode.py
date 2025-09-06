#!/usr/bin/env python3
"""
Script de test pour le mode organique de City Block Generator
À exécuter dans Blender pour tester les nouvelles fonctionnalités organiques
"""

import bpy

def test_organic_mode():
    """Test du mode organique avec différents paramètres"""
    try:
        print("=== TEST MODE ORGANIQUE CITY BLOCK GENERATOR ===")
        
        # Accéder à la scène
        scene = bpy.context.scene
        
        # Configuration du mode organique
        scene.citygen_width = 2
        scene.citygen_length = 2
        scene.citygen_max_floors = 4
        scene.citygen_road_width = 3.0
        scene.citygen_buildings_per_block = 1
        scene.citygen_seamless_roads = False
        scene.citygen_building_variety = 'HIGH'
        scene.citygen_height_variation = 0.5
        
        # === ACTIVATION MODE ORGANIQUE ===
        scene.citygen_organic_mode = True
        scene.citygen_polygon_min_sides = 4
        scene.citygen_polygon_max_sides = 6
        scene.citygen_road_curve_intensity = 0.7
        scene.citygen_block_size_variation = 0.4
        
        print("🌿 Configuration mode organique:")
        print(f"   - Mode organique: {scene.citygen_organic_mode}")
        print(f"   - Côtés polygones: {scene.citygen_polygon_min_sides}-{scene.citygen_polygon_max_sides}")
        print(f"   - Intensité courbes: {scene.citygen_road_curve_intensity}")
        print(f"   - Variation blocs: {scene.citygen_block_size_variation}")
        print(f"   - Grille: {scene.citygen_width}x{scene.citygen_length}")
        print(f"   - Variété bâtiments: {scene.citygen_building_variety}")
        
        # Tenter la génération
        print("\n🚀 Test de génération en mode organique...")
        bpy.ops.citygen.generate_city()
        
        # Compter les objets créés
        all_objects = bpy.context.scene.objects
        buildings = [obj for obj in all_objects if 'building' in obj.name.lower() or 'batiment' in obj.name.lower()]
        roads = [obj for obj in all_objects if 'road' in obj.name.lower() or 'route' in obj.name.lower()]
        blocks = [obj for obj in all_objects if 'block' in obj.name.lower() or 'bloc' in obj.name.lower()]
        
        print(f"\n✅ RÉSULTATS:")
        print(f"   🏢 Bâtiments créés: {len(buildings)}")
        print(f"   🛣️  Routes créées: {len(roads)}")
        print(f"   🧱 Blocs créés: {len(blocks)}")
        print(f"   📊 Total objets: {len(all_objects)}")
        
        if buildings and (roads or blocks):
            print("🎉 TEST RÉUSSI: Mode organique fonctionnel!")
            return True
        else:
            print("❌ TEST ÉCHOUÉ: Pas assez d'objets créés")
            return False
            
    except Exception as e:
        print(f"❌ ERREUR pendant le test: {e}")
        import traceback
        print(f"Traceback: {traceback.format_exc()}")
        return False

def test_standard_vs_organic():
    """Compare les modes standard et organique"""
    print("\n=== COMPARAISON MODES STANDARD vs ORGANIQUE ===")
    
    scene = bpy.context.scene
    scene.citygen_width = 2
    scene.citygen_length = 2
    
    # Test mode standard
    scene.citygen_organic_mode = False
    print("🏙️ Test mode STANDARD...")
    bpy.ops.citygen.generate_city()
    standard_objects = len(bpy.context.scene.objects)
    
    # Attendre un peu puis tester mode organique
    bpy.ops.mesh.primitive_cube_add()  # Dummy operation pour séparer
    
    scene.citygen_organic_mode = True
    print("🌿 Test mode ORGANIQUE...")
    bpy.ops.citygen.generate_city()
    organic_objects = len(bpy.context.scene.objects)
    
    print(f"📊 COMPARAISON:")
    print(f"   Standard: {standard_objects} objets")
    print(f"   Organique: {organic_objects} objets")

if __name__ == "__main__":
    # Exécuter les tests
    test_organic_mode()
    test_standard_vs_organic()

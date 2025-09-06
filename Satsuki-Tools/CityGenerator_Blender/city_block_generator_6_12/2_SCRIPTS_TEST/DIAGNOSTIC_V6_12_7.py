"""
DIAGNOSTIC SIMPLE V6.12.7
Test pour vérifier que notre fonction corrigée fonctionne
"""

import bpy

def test_zone_function():
    """Test direct de la fonction identify_block_zones_from_roads_rf"""
    
    print("🔥 === TEST DIAGNOSTIC V6.12.7 ===")
    
    # Nettoyer la scène
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete(use_global=False)
    
    # Importer le module generator
    import sys
    import os
    
    # Assurer que le module est chargé
    addon_path = bpy.utils.user_resource('SCRIPTS', path="addons")
    sys.path.append(os.path.join(addon_path, "city_block_generator_6_12"))
    
    try:
        from city_block_generator_6_12 import generator
        
        print("✅ Module generator importé")
        
        # Test direct de la fonction
        print("🧪 Test direct identify_block_zones_from_roads_rf...")
        
        # Paramètres de test
        road_network = []  # Pas important pour notre test
        width = 3
        length = 3
        road_width = 2.0
        
        # Appel direct de la fonction
        zones = generator.identify_block_zones_from_roads_rf(road_network, width, length, road_width)
        
        print(f"🎯 RÉSULTAT: {len(zones)} zones retournées")
        print(f"   Attendu: {width * length} = {width * length} zones")
        
        if len(zones) == width * length:
            print("🎉 SUCCÈS ! La fonction fonctionne correctement")
            
            # Créer des marqueurs visuels pour chaque zone
            for i, zone in enumerate(zones):
                bpy.ops.mesh.primitive_cube_add(
                    size=1.0,
                    location=(zone['x'], zone['y'], 5.0)
                )
                marker = bpy.context.object
                marker.name = f"ZONE_MARKER_{i}"
                marker.scale = (zone['width']/2, zone['height']/2, 0.5)
                
                # Couleur selon type
                mat = bpy.data.materials.new(f"ZoneMat_{i}")
                mat.use_nodes = True
                if zone['zone_type'] == 'residential':
                    color = (0.5, 1.0, 0.5)  # Vert
                elif zone['zone_type'] == 'commercial':
                    color = (1.0, 0.5, 0.5)  # Rouge  
                else:
                    color = (0.5, 0.5, 1.0)  # Bleu
                
                bsdf = mat.node_tree.nodes.get("Principled BSDF")
                if bsdf:
                    bsdf.inputs[0].default_value = (*color, 1.0)
                
                marker.data.materials.append(mat)
            
            print(f"✅ {len(zones)} marqueurs visuels créés")
        else:
            print(f"❌ ÉCHEC ! Attendu {width * length}, reçu {len(zones)}")
            
    except Exception as e:
        print(f"❌ ERREUR import/test: {e}")
        import traceback
        print(f"Traceback: {traceback.format_exc()}")

if __name__ == "__main__":
    test_zone_function()

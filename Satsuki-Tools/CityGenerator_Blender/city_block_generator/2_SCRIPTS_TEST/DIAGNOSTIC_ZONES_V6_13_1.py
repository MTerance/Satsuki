"""
DIAGNOSTIC ZONES V6.13.1
Test spécifique pour la fonction identify_block_zones_from_roads_rf
"""

import bpy

def test_zone_identification():
    """Test exclusif de l'identification des zones"""
    print("🔥🔥🔥 === DIAGNOSTIC ZONES V6.13.1 === 🔥🔥🔥")
    
    try:
        # Nettoyer la scène
        print("🧹 Nettoyage scène...")
        bpy.ops.object.select_all(action='SELECT')
        bpy.ops.object.delete(use_global=False)
        print("✅ Scène nettoyée")
        
        # Importer l'addon et ses fonctions
        print("🔌 Import addon...")
        import city_block_generator.generator as gen
        print("✅ Addon importé")
        
        # Tester la fonction zones avec les paramètres typiques
        print("🎯 Test identification zones...")
        
        # Paramètres de test (grille 5x5 classique)
        width = 5
        length = 5
        road_width = 2.0
        road_network = {}  # Vide pour ce test - on teste juste la logique de grille
        
        print(f"   📊 Paramètres test: {width}x{length} grille, road_width={road_width}")
        print(f"   🎯 ATTENDU: {width * length} = {width * length} zones")
        
        # Appeler directement la fonction problématique
        print("🔥 Appel direct identify_block_zones_from_roads_rf...")
        block_zones = gen.identify_block_zones_from_roads_rf(road_network, width, length, road_width)
        
        # Analyser les résultats
        print(f"🔍 === RÉSULTATS ANALYSE === 🔍")
        print(f"   📊 Zones créées: {len(block_zones)}")
        print(f"   ✅ SUCCÈS: {len(block_zones) == width * length}")
        
        if len(block_zones) == 0:
            print("❌ AUCUNE ZONE CRÉÉE - PROBLÈME MAJEUR!")
        elif len(block_zones) == 1:
            print("❌ UNE SEULE ZONE - C'EST LE PROBLÈME!")
            print(f"   Zone unique: {block_zones[0]}")
        elif len(block_zones) < width * length:
            print(f"⚠️ ZONES MANQUANTES: {len(block_zones)}/{width * length}")
        else:
            print(f"✅ NOMBRE CORRECT DE ZONES: {len(block_zones)}")
        
        # Afficher quelques zones pour analyse
        if len(block_zones) > 0:
            print(f"🔍 Analyse des premières zones:")
            for i, zone in enumerate(block_zones[:5]):  # 5 premières
                print(f"   Zone {i}: pos=({zone['x']:.1f}, {zone['y']:.1f}), taille={zone['width']:.1f}x{zone['height']:.1f}, type={zone['zone_type']}")
        
        print("🎯 Diagnostic zones terminé !")
        
    except Exception as e:
        print(f"❌ ERREUR dans diagnostic zones: {e}")
        import traceback
        print(f"Traceback: {traceback.format_exc()}")

if __name__ == "__main__":
    test_zone_identification()

"""
TEST ULTRA-SÉCURISÉ V6.13.0
Test minimaliste pour éviter les crashes
"""

import bpy

def test_simple_generation():
    """Test ultra-simple pour identifier le problème"""
    print("🔥 === TEST ULTRA-SÉCURISÉ V6.13.0 ===")
    
    try:
        # Nettoyer la scène
        print("🧹 Nettoyage scène...")
        bpy.ops.object.select_all(action='SELECT')
        bpy.ops.object.delete(use_global=False)
        print("✅ Scène nettoyée")
        
        # Test 1: Création d'un simple cube
        print("🔨 Test création cube...")
        bpy.ops.mesh.primitive_cube_add(size=2.0, location=(0, 0, 1))
        cube = bpy.context.object
        cube.name = "TEST_CUBE_V6130"
        print("✅ Cube créé avec succès")
        
        # Test 2: Test de l'addon sans génération
        print("🔌 Test addon présent...")
        try:
            # Vérifier que l'addon est chargé
            import city_block_generator_6_12
            print("✅ Addon trouvé")
            
            # Vérifier l'opérateur
            if hasattr(bpy.ops, 'citygen'):
                print("✅ Opérateur citygen présent")
            else:
                print("❌ Opérateur citygen manquant")
                
        except Exception as e:
            print(f"❌ Erreur addon: {e}")
        
        print("🎯 Test sécurisé terminé - Pas de crash !")
        
    except Exception as e:
        print(f"❌ ERREUR dans test sécurisé: {e}")
        import traceback
        print(f"Traceback: {traceback.format_exc()}")

if __name__ == "__main__":
    test_simple_generation()

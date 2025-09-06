"""
TEST ZONES SPÉCIFIQUE V6.13.2
Test pour diagnostiquer précisément le problème d'identification des zones
"""

import bpy

def test_zone_generation_only():
    """Test qui se concentre uniquement sur la génération de zones"""
    print("🔥🔥🔥 === TEST ZONES SPÉCIFIQUE V6.13.2 === 🔥🔥🔥")
    
    try:
        # Nettoyer la scène
        print("🧹 Nettoyage scène...")
        bpy.ops.object.select_all(action='SELECT')
        bpy.ops.object.delete(use_global=False)
        print("✅ Scène nettoyée")
        
        # Vérifier que l'addon est présent
        print("🔌 Vérification addon...")
        if not hasattr(bpy.ops, 'citygen'):
            print("❌ Addon non trouvé!")
            return
        print("✅ Addon trouvé")
        
        # Configurer les paramètres pour un test simple
        print("⚙️ Configuration test zones...")
        scene = bpy.context.scene
        
        # Paramètres de test - grille 3x3 pour commencer simple
        scene.city_width = 3
        scene.city_length = 3
        scene.road_width = 2.0
        scene.force_organic_roads = True  # Activer les routes organiques
        scene.method_roads_first = True   # Méthode roads-first
        
        print(f"   📊 Grille configurée: {scene.city_width}x{scene.city_length}")
        print(f"   🎯 Zones attendues: {scene.city_width * scene.city_length} = {scene.city_width * scene.city_length}")
        
        # Lancer la génération et observer les logs de zones
        print("🚀 Lancement génération avec focus sur zones...")
        result = bpy.ops.citygen.generate_city()
        
        if result == {'FINISHED'}:
            print("✅ Génération terminée - vérifiez les logs ci-dessus pour le nombre de zones")
        else:
            print(f"⚠️ Génération résultat: {result}")
        
        print("🎯 Test zones terminé - Analysez les logs!")
        
    except Exception as e:
        print(f"❌ ERREUR dans test zones: {e}")
        import traceback
        print(f"Traceback: {traceback.format_exc()}")

if __name__ == "__main__":
    test_zone_generation_only()

"""
SCRIPT D'INSTALLATION ET TEST AUTOMATIQUE
À exécuter dans Blender pour installer et tester l'addon corrigé
"""

import bpy
import os
import sys

def install_and_test_addon():
    """Installe et teste l'addon automatiquement"""
    print("🔧 === INSTALLATION ET TEST AUTOMATIQUE ===")
    
    # 1. Désactiver l'ancien addon s'il existe
    try:
        bpy.ops.preferences.addon_disable(module="city_block_generator")
        print("✅ Ancien addon désactivé")
    except:
        print("ℹ️ Aucun ancien addon à désactiver")
    
    # 2. Supprimer les anciens objets
    try:
        bpy.ops.object.select_all(action='SELECT')
        bpy.ops.object.delete(use_global=False)
        print("✅ Scène nettoyée")
    except:
        print("ℹ️ Scène déjà vide")
    
    # 3. Réactiver l'addon
    try:
        bpy.ops.preferences.addon_enable(module="city_block_generator")
        print("✅ Addon réactivé")
    except Exception as e:
        print(f"❌ Erreur activation addon: {e}")
        return False
    
    # 4. Lancer le test de génération
    try:
        print("🏙️ Génération ville de test 3x3...")
        
        # Configurer les paramètres
        scene = bpy.context.scene
        scene.citygen_width = 3
        scene.citygen_length = 3
        scene.citygen_organic_mode = True
        scene.citygen_road_first_method = True
        scene.citygen_enable_debug = True
        
        # Lancer la génération
        bpy.ops.citygen.generate_city()
        
        print("✅ Génération terminée !")
        
        # 5. Compter les objets créés
        roads = [obj for obj in bpy.context.scene.objects if "Road" in obj.name]
        buildings = [obj for obj in bpy.context.scene.objects if "Building" in obj.name or "batiment" in obj.name]
        
        print(f"📊 Résultats:")
        print(f"   🛣️ Routes: {len(roads)}")
        print(f"   🏢 Bâtiments: {len(buildings)}")
        
        if len(buildings) >= 15:  # Pour 3x3 on devrait avoir ~18+ bâtiments
            print("🎉 SUCCÈS ! Ville générée avec succès !")
            return True
        else:
            print("⚠️ Nombre de bâtiments insuffisant...")
            return False
            
    except Exception as e:
        print(f"❌ Erreur génération: {e}")
        import traceback
        print(f"Traceback: {traceback.format_exc()}")
        return False

if __name__ == "__main__":
    install_and_test_addon()

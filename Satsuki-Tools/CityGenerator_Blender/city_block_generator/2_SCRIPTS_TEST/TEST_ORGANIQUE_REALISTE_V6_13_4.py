"""
TEST ORGANIQUE RÉALISTE V6.13.4
Test du nouveau système organique réaliste - garde la logique urbaine
Instructions: Exécuter dans Blender (Script Editor → Run Script)
"""

import bpy

def test_organique_realiste():
    """Test du système organique réaliste (pas chaotique)"""
    print("🔥🔥🔥 === TEST ORGANIQUE RÉALISTE V6.13.4 === 🔥🔥🔥")
    print("🎯 Objectif: Routes organiques mais avec logique urbaine")
    
    # Nettoyer d'abord
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete(use_global=False)
    
    # Configuration pour système réaliste
    scene = bpy.context.scene
    scene.citygen_width = 4       # Grille 4x4 pour test
    scene.citygen_length = 4
    scene.citygen_organic_mode = True
    scene.citygen_road_first_method = True
    scene.citygen_road_curve_intensity = 0.3  # Intensité modérée
    scene.citygen_buildings_per_block = 2  # Optimisé
    
    print(f"🏙️ === PARAMÈTRES ORGANIQUE RÉALISTE ===")
    print(f"   📊 Grille: {scene.citygen_width}x{scene.citygen_length}")
    print(f"   🌿 Courbes: Légères (intensité={scene.citygen_road_curve_intensity})")
    print(f"   🎯 ATTENDU: Routes légèrement courbes mais ordonnées")
    print(f"   🏗️ Zones: {scene.citygen_width * scene.citygen_length} = 16 zones")
    
    # Lancer génération réaliste
    print("🚀 === DÉBUT GÉNÉRATION ORGANIQUE RÉALISTE ===")
    
    result = bpy.ops.citygen.generate_city()
    
    print("🔍 === FIN GÉNÉRATION - ANALYSE RÉALISTE ===")
    print(f"📊 Résultat: {result}")
    
    # Analyser les résultats
    roads = [obj for obj in bpy.context.scene.objects if "Road" in obj.name]
    blocks = [obj for obj in bpy.context.scene.objects if "Block" in obj.name]
    buildings = [obj for obj in bpy.context.scene.objects if "Building" in obj.name]
    
    print(f"🔢 === ANALYSE ORGANIQUE RÉALISTE ===")
    print(f"   🛣️ Routes: {len(roads)} (devraient être légèrement courbes)")
    print(f"   🏗️ Blocs: {len(blocks)} (distribution ordonnée)")
    print(f"   🏢 Bâtiments: {len(buildings)} (bien répartis)")
    print(f"   📊 Total: {len(bpy.context.scene.objects)} objets")
    
    # Vérifier le succès
    success = len(blocks) >= 12 and len(buildings) >= 20
    if success:
        print("✅🎉 SUCCÈS ORGANIQUE RÉALISTE !")
        print("🌟 Les routes devraient être organiques MAIS ordonnées")
        print("🏙️ Aspect de vraie ville avec caractère naturel")
    else:
        print("⚠️ Résultats partiels - vérifiez les logs")
    
    print("🎯 Test organique réaliste terminé!")
    print("👀 Observez: les routes ont des courbes mais gardent la logique urbaine")

# Exécuter automatiquement
test_organique_realiste()

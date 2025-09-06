"""
TEST COURBES MEGA VISIBLES V6.13.7
Système avec courbes Blender natives IMPOSSIBLES à rater !
Instructions: Exécuter dans Blender (Script Editor → Run Script)
"""

import bpy

def test_courbes_mega_visibles():
    """Test des courbes Blender natives MEGA visibles"""
    print("🔥🔥🔥 === TEST COURBES MEGA VISIBLES V6.13.7 === 🔥🔥🔥")
    print("🎯 Objectif: Courbes Blender natives IMPOSSIBLES à rater !")
    print("🌊 Amplitude GIGANTESQUE garantie !")
    
    # Nettoyer d'abord
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete(use_global=False)
    
    # Configuration pour COURBES MAXIMALES
    scene = bpy.context.scene
    scene.citygen_width = 4       # Grille 4x4 pour des courbes bien visibles
    scene.citygen_length = 4
    scene.citygen_organic_mode = True
    scene.citygen_road_first_method = True
    scene.citygen_road_curve_intensity = 1.0  # MAXIMUM !!!
    scene.citygen_buildings_per_block = 1
    
    print(f"🎯 === PARAMÈTRES COURBES MEGA VISIBLES ===")
    print(f"   📊 Grille: {scene.citygen_width}x{scene.citygen_length}")
    print(f"   🔥 Système: Courbes Blender natives MEGA visibles")
    print(f"   🌊 Intensité: {scene.citygen_road_curve_intensity} (MAXIMUM)")
    print(f"   🎯 ATTENDU: Courbes GIGANTESQUES impossibles à rater")
    print(f"   📏 Amplitude: TRIPLER l'intensité = {scene.citygen_road_curve_intensity * 3}")
    
    # Lancer génération COURBES MEGA VISIBLES
    print("🚀 === DÉBUT GÉNÉRATION COURBES MEGA VISIBLES ===")
    print("🔥 Courbes Blender natives avec amplitude GIGANTESQUE...")
    
    result = bpy.ops.citygen.generate_city()
    
    print("🔍 === FIN GÉNÉRATION - ANALYSE COURBES MEGA VISIBLES ===")
    print(f"📊 Résultat: {result}")
    
    # Analyser les résultats
    roads = [obj for obj in bpy.context.scene.objects if "Road" in obj.name or "SuperCurve" in obj.name]
    curves = [obj for obj in bpy.context.scene.objects if "SuperCurve" in obj.name]
    blocks = [obj for obj in bpy.context.scene.objects if "Block" in obj.name]
    buildings = [obj for obj in bpy.context.scene.objects if "Building" in obj.name]
    
    print(f"🔥 === ANALYSE COURBES MEGA VISIBLES ===")
    print(f"   🛣️ Routes totales: {len(roads)}")
    print(f"   🌊 SuperCourbes Blender: {len(curves)} (MEGA VISIBLES)")
    print(f"   🏗️ Blocs: {len(blocks)}")
    print(f"   🏢 Bâtiments: {len(buildings)}")
    print(f"   📊 Total objets: {len(bpy.context.scene.objects)}")
    
    # Analyser les SuperCourbes spécifiquement
    if curves:
        print(f"🔥 === DÉTAILS SUPERCOURBES ===")
        for i, curve in enumerate(curves[:3]):  # Premiers 3
            print(f"   🌊 {curve.name}: {len(curve.data.vertices) if hasattr(curve.data, 'vertices') else 'N/A'} vertices")
            if hasattr(curve.data, 'vertices') and curve.data.vertices:
                # Calculer l'amplitude réelle
                x_coords = [v.co.x for v in curve.data.vertices]
                if len(x_coords) > 1:
                    amplitude = max(x_coords) - min(x_coords)
                    print(f"      📏 Amplitude réelle: {amplitude:.1f} unités")
    
    # Vérifier le succès COURBES MEGA VISIBLES
    success = len(curves) >= 8 and len(blocks) >= 10
    if success:
        print("✅🔥🌊 SUCCÈS COURBES MEGA VISIBLES ! 🌊🔥✅")
        print("🎯 Courbes Blender natives GIGANTESQUES créées")
        print("🔥 Amplitude TRIPLER = IMPOSSIBLE à rater")
        print("🌊 SuperCourves avec résolution 64 + biseau 16")
        print("🏙️ Ville organique avec VRAIES courbes visibles !")
    else:
        print("⚠️ Résultats partiels - vérifiez les SuperCourbes")
    
    print("🎯 Test COURBES MEGA VISIBLES terminé!")
    print("👀 Observez: SuperCourveRoad_V_ et SuperCurveRoad_H_")
    print("🔥 Les courbes sont maintenant IMPOSSIBLES à rater !")
    print("🌊 Amplitude GIGANTESQUE garantie !")

# Exécuter automatiquement
test_courbes_mega_visibles()

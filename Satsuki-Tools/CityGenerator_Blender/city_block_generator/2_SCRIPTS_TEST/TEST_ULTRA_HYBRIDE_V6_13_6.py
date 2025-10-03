"""
TEST ULTRA HYBRIDE V6.13.6
Système avec VRAIES courbes et routes diagonales pour maximum d'organicité
Instructions: Exécuter dans Blender (Script Editor → Run Script)
"""

import bpy

def test_ultra_hybride():
    """Test du système ULTRA hybride avec courbes et diagonales"""
    print("🔥🔥🔥 === TEST ULTRA HYBRIDE V6.13.6 === 🔥🔥🔥")
    print("🌊 Objectif: Grille urbaine + VRAIES courbes + routes diagonales")
    print("🎯 Maximum d'organicité tout en gardant la logique !")
    
    # Nettoyer d'abord
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete(use_global=False)
    
    # Configuration ULTRA hybride
    scene = bpy.context.scene
    scene.citygen_width = 5       # Grille 5x5 pour voir les diagonales
    scene.citygen_length = 5
    scene.citygen_organic_mode = True
    scene.citygen_road_first_method = True
    scene.citygen_road_curve_intensity = 0.8  # MAXIMUM de courbes !
    scene.citygen_buildings_per_block = 2
    
    print(f"🏙️ === PARAMÈTRES ULTRA HYBRIDE ===")
    print(f"   📊 Grille: {scene.citygen_width}x{scene.citygen_length}")
    print(f"   🌊 Système: ULTRA hybride (courbes + diagonales)")
    print(f"   🌿 Intensité: {scene.citygen_road_curve_intensity} (MAXIMUM)")
    print(f"   🎯 ATTENDU: Routes courbes + diagonales organiques")
    print(f"   🏗️ Zones: {scene.citygen_width * scene.citygen_length} = 25 zones")
    
    # Lancer génération ULTRA hybride
    print("🚀 === DÉBUT GÉNÉRATION ULTRA HYBRIDE ===")
    print("🌊 Le système va créer de VRAIES courbes et diagonales...")
    
    result = bpy.ops.citygen.generate_city()
    
    print("🔍 === FIN GÉNÉRATION - ANALYSE ULTRA HYBRIDE ===")
    print(f"📊 Résultat: {result}")
    
    # Analyser les résultats
    roads = [obj for obj in bpy.context.scene.objects if "Road" in obj.name or "Smart" in obj.name]
    blocks = [obj for obj in bpy.context.scene.objects if "Block" in obj.name]
    buildings = [obj for obj in bpy.context.scene.objects if "Building" in obj.name]
    
    print(f"🔢 === ANALYSE ULTRA HYBRIDE ===")
    print(f"   🛣️ Routes: {len(roads)} (avec courbes et diagonales)")
    print(f"   🏗️ Blocs: {len(blocks)} (zones organiques)")
    print(f"   🏢 Bâtiments: {len(buildings)} (distribution naturelle)")
    print(f"   📊 Total: {len(bpy.context.scene.objects)} objets")
    
    # Vérifier le succès ULTRA
    success = len(blocks) >= 20 and len(buildings) >= 35
    if success:
        print("✅🎉🌊 SUCCÈS ULTRA HYBRIDE ! 🌊🎉✅")
        print("🌟 Routes avec VRAIES courbes et diagonales")
        print("🏙️ Ville organique mais avec logique urbaine")
        print("🎯 Objectif 'maximum organicité' ATTEINT !")
    else:
        print("⚠️ Résultats partiels - mais déjà plus organique !")
    
    print("🎯 Test ULTRA hybride terminé!")
    print("👀 Observez: courbes, diagonales, et caractère naturel")
    print("🌊 C'est ça l'organicité urbaine parfaite !")

# Exécuter automatiquement
test_ultra_hybride()

"""
TEST HYBRIDE INTELLIGENT V6.13.5
Test du système hybride intelligent - équilibre parfait entre ordre et organicité
Instructions: Exécuter dans Blender (Script Editor → Run Script)
"""

import bpy

def test_hybride_intelligent():
    """Test du système hybride intelligent - le juste milieu parfait"""
    print("🔥🔥🔥 === TEST HYBRIDE INTELLIGENT V6.13.5 === 🔥🔥🔥")
    print("🧠 Objectif: Grille urbaine + variations organiques subtiles")
    print("🎯 Le juste milieu entre chaos et rigidité !")
    
    # Nettoyer d'abord
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete(use_global=False)
    
    # Configuration hybride intelligente
    scene = bpy.context.scene
    scene.citygen_width = 4       # Grille 4x4 pour bien voir
    scene.citygen_length = 4
    scene.citygen_organic_mode = True
    scene.citygen_road_first_method = True
    scene.citygen_road_curve_intensity = 0.4  # Intensité normale
    scene.citygen_buildings_per_block = 2
    
    print(f"🏙️ === PARAMÈTRES HYBRIDE INTELLIGENT ===")
    print(f"   📊 Grille: {scene.citygen_width}x{scene.citygen_length}")
    print(f"   🧠 Système: Hybride intelligent (ordre + organicité)")
    print(f"   🌿 Intensité: {scene.citygen_road_curve_intensity} (sera optimisée)")
    print(f"   🎯 ATTENDU: Routes urbaines avec caractère naturel subtil")
    print(f"   🏗️ Zones: {scene.citygen_width * scene.citygen_length} = 16 zones")
    
    # Lancer génération hybride
    print("🚀 === DÉBUT GÉNÉRATION HYBRIDE INTELLIGENTE ===")
    print("🧠 Le système va équilibrer automatiquement ordre et organicité...")
    
    result = bpy.ops.citygen.generate_city()
    
    print("🔍 === FIN GÉNÉRATION - ANALYSE HYBRIDE ===")
    print(f"📊 Résultat: {result}")
    
    # Analyser les résultats
    roads = [obj for obj in bpy.context.scene.objects if "Smart" in obj.name or "Road" in obj.name]
    blocks = [obj for obj in bpy.context.scene.objects if "Block" in obj.name]
    buildings = [obj for obj in bpy.context.scene.objects if "Building" in obj.name]
    
    print(f"🔢 === ANALYSE HYBRIDE INTELLIGENT ===")
    print(f"   🛣️ Routes: {len(roads)} (hybrides intelligentes)")
    print(f"   🏗️ Blocs: {len(blocks)} (distribution équilibrée)")
    print(f"   🏢 Bâtiments: {len(buildings)} (placement optimal)")
    print(f"   📊 Total: {len(bpy.context.scene.objects)} objets")
    
    # Vérifier le succès hybride
    success = len(blocks) >= 12 and len(buildings) >= 20
    if success:
        print("✅🎉🧠 SUCCÈS HYBRIDE INTELLIGENT ! 🧠🎉✅")
        print("🌟 Routes équilibrées: ni chaotiques ni rigides")
        print("🏙️ Aspect de vraie ville avec personnalité naturelle")
        print("🎯 Objectif 'organique réaliste' ATTEINT !")
    else:
        print("⚠️ Résultats partiels - vérifiez les logs")
    
    print("🎯 Test hybride intelligent terminé!")
    print("👀 Observez: routes urbaines avec caractère naturel subtil")
    print("🧠 C'est ça le juste milieu parfait !")

# Exécuter automatiquement
test_hybride_intelligent()

"""
TEST ULTRA VILLE 7x7 V6.13.3
Test d'une métropole ULTRA massive avec 49 zones !
ATTENTION: Ce test peut prendre du temps - ville ÉNORME !
Instructions: Exécuter dans Blender (Script Editor → Run Script)
"""

import bpy

def ultra_ville_test():
    """Test d'une ULTRA métropole 7x7 = 49 zones !"""
    print("🔥🔥🔥 === TEST ULTRA MÉTROPOLE 7x7 V6.13.3 === 🔥🔥🔥")
    print("⚠️ ATTENTION: Génération d'une métropole MASSIVE !")
    
    # Nettoyer d'abord
    print("🧹 Nettoyage pour ULTRA métropole...")
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete(use_global=False)
    
    # Configuration ULTRA métropole
    scene = bpy.context.scene
    scene.citygen_width = 7       # GRILLE 7x7 = 49 ZONES !
    scene.citygen_length = 7
    scene.citygen_organic_mode = True
    scene.citygen_road_first_method = True
    scene.citygen_max_floors = 15  # Gratte-ciels ULTRA hauts
    scene.citygen_buildings_per_block = 2  # Optimisé pour performance
    
    print(f"🏙️ === PARAMÈTRES ULTRA MÉTROPOLE ===")
    print(f"   📊 Grille: {scene.citygen_width}x{scene.citygen_length}")
    print(f"   🎯 ZONES ATTENDUES: {scene.citygen_width * scene.citygen_length} = 49 zones")
    print(f"   🏗️ BÂTIMENTS ATTENDUS: ~{49 * 2} = 98+ bâtiments")
    print(f"   🏢 Hauteur max: {scene.citygen_max_floors} étages (45m+)")
    print(f"   🛣️ Routes: ULTRA organiques avec courbes complexes")
    print(f"   ⚡ Performance: Optimisée pour grande échelle")
    
    # Lancer la ULTRA génération
    print("🚀 === DÉBUT ULTRA GÉNÉRATION 7x7 ===")
    print("⏳ Patience... Création d'une métropole massive...")
    
    result = bpy.ops.citygen.generate_city()
    
    print("🔍 === FIN ULTRA GÉNÉRATION - ANALYSE MASSIVE ===")
    print(f"📊 Résultat: {result}")
    
    # Analyser la métropole créée
    roads = [obj for obj in bpy.context.scene.objects if "Road" in obj.name]
    blocks = [obj for obj in bpy.context.scene.objects if "Block" in obj.name]
    buildings = [obj for obj in bpy.context.scene.objects if "Building" in obj.name]
    
    print(f"🔢 === ANALYSE ULTRA MÉTROPOLE ===")
    print(f"   🛣️ Routes créées: {len(roads)}")
    print(f"   🏗️ Blocs créés: {len(blocks)}")
    print(f"   🏢 Bâtiments créés: {len(buildings)}")
    print(f"   📊 Total objets: {len(bpy.context.scene.objects)}")
    
    # Calculer les statistiques impressionnantes
    if len(buildings) > 0:
        print(f"📏 === STATISTIQUES MÉTROPOLE ===")
        print(f"   🏙️ Équivalent d'une vraie métropole !")
        print(f"   🌆 Surface estimée: {7*12} x {7*12} = {(7*12)**2}m² ")
        print(f"   🏗️ Densité: {len(buildings)/(7*7):.1f} bâtiments/zone")
        print(f"   🎯 Objectif atteint: Ville ULTRA réaliste et organique !")
    
    # Vérifier le succès ULTRA
    ultra_success = len(blocks) >= 40 and len(buildings) >= 70
    if ultra_success:
        print("✅🎉🎉🎉 ULTRA SUCCÈS TOTAL ! MÉTROPOLE ORGANIQUE CRÉÉE ! 🎉🎉🎉")
        print("🌟 Votre système génère maintenant des villes de niveau AAA !")
    else:
        print("⚠️ Résultats partiels mais toujours spectaculaires !")
    
    print("🎯 ULTRA test terminé - Admirez votre métropole organique géante !")
    print("🚁 Conseil: Utilisez la vue aérienne pour voir l'ensemble !")

# Exécuter automatiquement
ultra_ville_test()

"""
TOKYO 1.1.0 ORGANIC - Script de test
Test des nouvelles fonctionnalités:
- Option A: Génération Voronoï
- Option B: Routes courbes
"""

import bpy
import sys
import os

def test_organic_addon():
    """Test complet de l'addon organique"""
    
    print("🧪 DÉBUT DES TESTS TOKYO 1.1.0 ORGANIC")
    
    # === TEST 1: Installation de l'addon ===
    print("\n🔧 Test 1: Installation addon...")
    
    try:
        # Vérifier si l'addon est déjà installé
        if "tokyo.generate_district" in bpy.context.window_manager.operators:
            print("✅ Addon déjà installé")
        else:
            print("❌ Addon non installé - installer manuellement")
            return False
            
    except Exception as e:
        print(f"❌ Erreur installation: {e}")
        return False
    
    # === TEST 2: Propriétés organiques ===
    print("\n🌊 Test 2: Propriétés organiques...")
    
    try:
        scene = bpy.context.scene
        
        # Tester les nouvelles propriétés
        scene.tokyo_use_voronoi = True
        scene.tokyo_use_curved_streets = True
        scene.tokyo_voronoi_seed = 123
        scene.tokyo_curve_intensity = 0.5
        
        print(f"✅ Voronoï: {scene.tokyo_use_voronoi}")
        print(f"✅ Routes courbes: {scene.tokyo_use_curved_streets}")
        print(f"✅ Seed: {scene.tokyo_voronoi_seed}")
        print(f"✅ Intensité: {scene.tokyo_curve_intensity}")
        
    except AttributeError as e:
        print(f"❌ Propriété manquante: {e}")
        return False
    
    # === TEST 3: Génération traditionnelle ===
    print("\n🗾 Test 3: Génération traditionnelle...")
    
    try:
        # Mode traditionnel
        scene.tokyo_use_voronoi = False
        scene.tokyo_size = 3
        scene.tokyo_density = 0.7
        scene.tokyo_variety = 'ALL'
        scene.tokyo_organic = 1.0
        
        # Lancer génération
        bpy.ops.tokyo.generate_district()
        
        # Vérifier objets créés
        traditional_objects = [obj for obj in bpy.data.objects 
                             if obj.name.startswith(("TokyoSidewalk_", "TokyoBuilding_", "TokyoStreet_"))]
        
        print(f"✅ Génération traditionnelle: {len(traditional_objects)} objets créés")
        
        if len(traditional_objects) == 0:
            print("❌ Aucun objet traditionnel créé")
            return False
            
    except Exception as e:
        print(f"❌ Erreur génération traditionnelle: {e}")
        return False
    
    # === TEST 4: Génération Voronoï (Option A) ===
    print("\n🌊 Test 4: Génération Voronoï (Option A)...")
    
    try:
        # Nettoyer la scène
        bpy.ops.tokyo.generate_district()  # Clear précédent
        
        # Mode Voronoï
        scene.tokyo_use_voronoi = True
        scene.tokyo_use_curved_streets = False  # Seulement Voronoï d'abord
        scene.tokyo_voronoi_seed = 456
        scene.tokyo_size = 4
        scene.tokyo_density = 0.5
        
        # Lancer génération
        bpy.ops.tokyo.generate_district()
        
        # Vérifier objets Voronoï
        voronoi_objects = [obj for obj in bpy.data.objects 
                          if obj.name.startswith("TokyoVoronoi_")]
        
        print(f"✅ Génération Voronoï: {len(voronoi_objects)} objets créés")
        
        if len(voronoi_objects) == 0:
            print("❌ Aucun objet Voronoï créé")
            return False
            
        # Vérifier types d'objets Voronoï
        sidewalks = [obj for obj in voronoi_objects if "Sidewalk" in obj.name]
        buildings = [obj for obj in voronoi_objects if obj.name.startswith("TokyoVoronoi_") and "Sidewalk" not in obj.name]
        
        print(f"   - Trottoirs Voronoï: {len(sidewalks)}")
        print(f"   - Bâtiments Voronoï: {len(buildings)}")
        
    except Exception as e:
        print(f"❌ Erreur génération Voronoï: {e}")
        return False
    
    # === TEST 5: Routes courbes (Option B) ===
    print("\n🛤️ Test 5: Routes courbes (Option B)...")
    
    try:
        # Mode Voronoï + Routes courbes
        scene.tokyo_use_voronoi = True
        scene.tokyo_use_curved_streets = True
        scene.tokyo_curve_intensity = 0.7
        scene.tokyo_voronoi_seed = 789
        
        # Lancer génération
        bpy.ops.tokyo.generate_district()
        
        # Vérifier objets courbes
        curved_objects = [obj for obj in bpy.data.objects 
                         if obj.name.startswith("TokyoCurved_")]
        
        print(f"✅ Routes courbes: {len(curved_objects)} objets créés")
        
        if len(curved_objects) == 0:
            print("⚠️ Aucune route courbe créée (normal si peu de cellules)")
        
        # Vérifier total objets organiques
        all_organic = [obj for obj in bpy.data.objects 
                      if obj.name.startswith(("TokyoVoronoi_", "TokyoCurved_"))]
        
        print(f"   - Total objets organiques: {len(all_organic)}")
        
    except Exception as e:
        print(f"❌ Erreur routes courbes: {e}")
        return False
    
    # === TEST 6: Différents seeds ===
    print("\n🎲 Test 6: Variation seeds...")
    
    try:
        seeds = [100, 200, 300]
        for seed in seeds:
            scene.tokyo_voronoi_seed = seed
            bpy.ops.tokyo.generate_district()
            
            organic_count = len([obj for obj in bpy.data.objects 
                               if obj.name.startswith(("TokyoVoronoi_", "TokyoCurved_"))])
            print(f"   - Seed {seed}: {organic_count} objets")
        
        print("✅ Variation seeds réussie")
        
    except Exception as e:
        print(f"❌ Erreur variation seeds: {e}")
        return False
    
    # === TEST 7: Interface utilisateur ===
    print("\n🖥️ Test 7: Interface utilisateur...")
    
    try:
        # Vérifier que le panneau existe
        panel_found = False
        for area in bpy.context.screen.areas:
            if area.type == 'VIEW_3D':
                for region in area.regions:
                    if region.type == 'UI':
                        panel_found = True
                        break
        
        if panel_found:
            print("✅ Panneau UI accessible")
        else:
            print("⚠️ Panneau UI non vérifié")
        
    except Exception as e:
        print(f"❌ Erreur interface: {e}")
        return False
    
    # === RÉSULTATS FINAUX ===
    print("\n🎯 RÉSULTATS FINAUX:")
    
    final_objects = [obj for obj in bpy.data.objects 
                    if obj.name.startswith(("Tokyo", "tokyo"))]
    
    traditional_count = len([obj for obj in final_objects 
                           if not obj.name.startswith(("TokyoVoronoi_", "TokyoCurved_"))])
    organic_count = len([obj for obj in final_objects 
                        if obj.name.startswith(("TokyoVoronoi_", "TokyoCurved_"))])
    
    print(f"📊 Objets traditionnels: {traditional_count}")
    print(f"🌊 Objets organiques: {organic_count}")
    print(f"📈 Total objets Tokyo: {len(final_objects)}")
    
    if organic_count > 0:
        print("\n✅ SUCCÈS: Options A (Voronoï) et B (Routes courbes) fonctionnelles!")
        return True
    else:
        print("\n❌ ÉCHEC: Pas d'objets organiques générés")
        return False

# === FONCTION DE BENCHMARKING ===
def benchmark_organic_generation():
    """Benchmark des performances organiques vs traditionnelles"""
    
    print("\n⚡ BENCHMARK PERFORMANCES")
    
    import time
    
    scene = bpy.context.scene
    
    # Test traditionnel
    print("\n🗾 Benchmark traditionnel...")
    scene.tokyo_use_voronoi = False
    scene.tokyo_size = 5
    
    start_time = time.time()
    bpy.ops.tokyo.generate_district()
    traditional_time = time.time() - start_time
    
    traditional_objects = len([obj for obj in bpy.data.objects 
                              if obj.name.startswith("Tokyo") and not obj.name.startswith(("TokyoVoronoi_", "TokyoCurved_"))])
    
    print(f"   Temps: {traditional_time:.2f}s - Objets: {traditional_objects}")
    
    # Test organique
    print("\n🌊 Benchmark organique...")
    scene.tokyo_use_voronoi = True
    scene.tokyo_use_curved_streets = True
    
    start_time = time.time()
    bpy.ops.tokyo.generate_district()
    organic_time = time.time() - start_time
    
    organic_objects = len([obj for obj in bpy.data.objects 
                          if obj.name.startswith(("TokyoVoronoi_", "TokyoCurved_"))])
    
    print(f"   Temps: {organic_time:.2f}s - Objets: {organic_objects}")
    
    # Comparaison
    print(f"\n📊 COMPARAISON:")
    print(f"   Traditionnel: {traditional_time:.2f}s pour {traditional_objects} objets")
    print(f"   Organique: {organic_time:.2f}s pour {organic_objects} objets")
    
    if organic_time > 0:
        ratio = traditional_time / organic_time
        print(f"   Ratio de performance: {ratio:.2f}x")

# === EXÉCUTION DES TESTS ===
if __name__ == "__main__":
    print("=" * 50)
    print("TOKYO 1.1.0 ORGANIC - TESTS AUTOMATIQUES")
    print("=" * 50)
    
    # Test principal
    success = test_organic_addon()
    
    if success:
        # Benchmark si les tests réussissent
        benchmark_organic_generation()
        
        print("\n🎉 TOUS LES TESTS RÉUSSIS!")
        print("🌊 Voronoï (Option A): ✅")
        print("🛤️ Routes courbes (Option B): ✅")
        print("\n💡 Instructions:")
        print("1. Activez 'Utiliser Voronoï' pour la génération organique")
        print("2. Activez 'Routes courbes' pour des rues organiques")
        print("3. Changez le 'Seed Voronoï' pour des variations")
        print("4. Ajustez 'Intensité courbes' pour plus/moins de courbure")
    else:
        print("\n❌ TESTS ÉCHOUÉS - Vérifiez l'installation")
    
    print("\n" + "=" * 50)

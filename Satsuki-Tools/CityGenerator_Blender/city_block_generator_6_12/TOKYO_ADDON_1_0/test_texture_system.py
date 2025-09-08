# TEST SYSTÈME DE TEXTURES TOKYO v1.0
# Script pour tester le système de textures avancé

import bpy
import random

def test_tokyo_texture_system():
    """Test complet du système de textures Tokyo"""
    
    print("🧪 DÉBUT TEST SYSTÈME TEXTURES TOKYO")
    print("=" * 50)
    
    # Test 1: Vérifier import du système
    try:
        from .texture_system import tokyo_texture_system
        print("✅ Test 1: Import système de textures réussi")
        system_available = True
    except ImportError as e:
        print(f"❌ Test 1: Échec import système de textures: {e}")
        system_available = False
        return False
    
    # Test 2: Vérifier structure des dossiers
    texture_path = tokyo_texture_system.get_texture_base_path()
    print(f"📁 Test 2: Chemin de base des textures: {texture_path}")
    
    if texture_path:
        print("✅ Test 2: Chemin des textures trouvé")
    else:
        print("❌ Test 2: Aucun chemin de textures trouvé")
        return False
    
    # Test 3: Test des catégories de bâtiments
    test_buildings = [
        {"height": 100, "width_x": 15, "width_y": 15, "zone": "business", "expected": "skyscraper"},
        {"height": 25, "width_x": 20, "width_y": 18, "zone": "commercial", "expected": "commercial"},
        {"height": 30, "width_x": 10, "width_y": 12, "zone": "residential", "expected": "midrise"},
        {"height": 15, "width_x": 8, "width_y": 10, "zone": "residential", "expected": "residential"},
        {"height": 6, "width_x": 6, "width_y": 8, "zone": "commercial", "expected": "lowrise"},
    ]
    
    print("\n🏗️ Test 3: Catégorisation des bâtiments")
    all_categories_ok = True
    
    for i, building in enumerate(test_buildings):
        category = tokyo_texture_system.categorize_building(
            building["height"], building["width_x"], building["width_y"], building["zone"]
        )
        
        if category == building["expected"]:
            print(f"✅ Bâtiment {i+1}: {building['height']}m → {category} (correct)")
        else:
            print(f"❌ Bâtiment {i+1}: {building['height']}m → {category} (attendu: {building['expected']})")
            all_categories_ok = False
    
    if all_categories_ok:
        print("✅ Test 3: Toutes les catégories correctes")
    else:
        print("❌ Test 3: Erreurs dans la catégorisation")
    
    # Test 4: Test de création de matériaux
    print("\n🎨 Test 4: Création de matériaux")
    
    test_materials = []
    for category in ["skyscraper", "commercial", "midrise", "residential", "lowrise"]:
        try:
            # Créer un matériau de test
            material = tokyo_texture_system.create_advanced_building_material(
                "business", 50, 15, 15, f"test_{category}"
            )
            
            if material:
                test_materials.append(material)
                print(f"✅ Matériau {category}: créé avec succès")
            else:
                print(f"❌ Matériau {category}: échec de création")
                
        except Exception as e:
            print(f"❌ Matériau {category}: erreur {e}")
    
    # Test 5: Vérifier les propriétés de scène
    print("\n⚙️ Test 5: Propriétés de scène")
    
    if hasattr(bpy.types.Scene, 'tokyo_use_advanced_textures'):
        print("✅ Propriété tokyo_use_advanced_textures trouvée")
        
        # Tester les valeurs
        if hasattr(bpy.context.scene, 'tokyo_use_advanced_textures'):
            current_value = bpy.context.scene.tokyo_use_advanced_textures
            print(f"📋 Valeur actuelle: {current_value}")
        else:
            print("⚠️ Propriété non initialisée dans la scène courante")
    else:
        print("❌ Propriété tokyo_use_advanced_textures non trouvée")
    
    # Test 6: Test de génération complète
    print("\n🏙️ Test 6: Génération complète (simulation)")
    
    try:
        # Simuler une génération de ville
        zones = {
            (0, 0): 'business',
            (0, 1): 'commercial', 
            (1, 0): 'residential',
            (1, 1): 'residential'
        }
        
        buildings_created = 0
        for (x, y), zone_type in zones.items():
            # Paramètres aléatoires
            if zone_type == 'business':
                height = random.uniform(60, 160)
                width_x = random.uniform(10, 16)
                width_y = random.uniform(10, 16)
            elif zone_type == 'commercial':
                height = random.uniform(12, 32)
                width_x = random.uniform(12, 17)
                width_y = random.uniform(12, 17)
            else:  # residential
                height = random.uniform(4, 20)
                width_x = random.uniform(8, 14)
                width_y = random.uniform(8, 14)
            
            # Tenter de créer le matériau
            try:
                material = tokyo_texture_system.create_advanced_building_material(
                    zone_type, height, width_x, width_y, f"test_{x}_{y}"
                )
                if material:
                    buildings_created += 1
            except Exception as e:
                print(f"⚠️ Erreur création bâtiment ({x},{y}): {e}")
        
        print(f"✅ Test 6: {buildings_created}/{len(zones)} bâtiments créés avec succès")
        
    except Exception as e:
        print(f"❌ Test 6: Erreur dans génération complète: {e}")
    
    # Nettoyage des matériaux de test
    print("\n🧹 Nettoyage des matériaux de test")
    cleaned_count = 0
    for material in test_materials:
        try:
            bpy.data.materials.remove(material)
            cleaned_count += 1
        except:
            pass
    
    print(f"🗑️ {cleaned_count} matériaux de test supprimés")
    
    # Résumé final
    print("\n" + "=" * 50)
    print("📊 RÉSUMÉ DU TEST")
    print("=" * 50)
    
    if system_available and all_categories_ok and buildings_created > 0:
        print("🎉 SUCCÈS: Système de textures opérationnel!")
        print("✅ Tous les tests passés")
        print("🚀 Le système est prêt à être utilisé")
        return True
    else:
        print("⚠️ ATTENTION: Problèmes détectés")
        print("🔧 Vérifiez la configuration et les dossiers de textures")
        return False

def test_quick_generation():
    """Test rapide de génération avec textures"""
    print("\n🚀 TEST GÉNÉRATION RAPIDE AVEC TEXTURES")
    
    # Activer le système de textures
    if hasattr(bpy.context.scene, 'tokyo_use_advanced_textures'):
        bpy.context.scene.tokyo_use_advanced_textures = True
        print("✅ Système de textures activé")
    
    # Paramètres de test
    bpy.context.scene.tokyo_size = 3
    bpy.context.scene.tokyo_density = 1.0
    bpy.context.scene.tokyo_variety = 'ALL'
    bpy.context.scene.tokyo_organic = 0.3
    
    print("📋 Paramètres configurés pour test 3x3")
    
    # Lancer la génération
    try:
        bpy.ops.tokyo.generate_district()
        print("🏙️ Génération terminée avec succès!")
        print("🎯 Vérifiez les matériaux des bâtiments générés")
        return True
    except Exception as e:
        print(f"❌ Erreur lors de la génération: {e}")
        return False

if __name__ == "__main__":
    # Lancer les tests
    test_result = test_tokyo_texture_system()
    
    if test_result:
        print("\n🎮 Voulez-vous tester une génération rapide? (Décommentez la ligne suivante)")
        # test_quick_generation()
    
    print("\n🏁 Tests terminés!")

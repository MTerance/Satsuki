# TEST MODES ET ALIGNEMENT - City Block Generator
# À exécuter dans l'éditeur de texte de Blender

import bpy

def test_all_modes():
    """Test de tous les modes disponibles avec alignement."""
    
    print("=== TEST COMPLET MODES ET ALIGNEMENT ===")
    
    # Vérifier l'addon
    if not hasattr(bpy.context.scene, 'citygen_props'):
        print("❌ Addon City Block Generator non activé")
        return False
    
    props = bpy.context.scene.citygen_props
    
    # Test 1: Mode Normal (sans districts)
    print("\n🔹 TEST 1: Mode Normal")
    test_normal_mode(props)
    
    # Test 2: Mode District Commercial
    print("\n🔹 TEST 2: Mode District - Dominante Commerciale") 
    test_commercial_district(props)
    
    # Test 3: Mode District Résidentiel
    print("\n🔹 TEST 3: Mode District - Dominante Résidentielle")
    test_residential_district(props)
    
    # Test 4: Mode District Industriel
    print("\n🔹 TEST 4: Mode District - Dominante Industrielle")
    test_industrial_district(props)
    
    return True

def test_normal_mode(props):
    """Test du mode normal sans districts."""
    
    # Nettoyer la scène
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete(use_global=False)
    
    # Configuration mode normal
    props.width = 4
    props.length = 4  
    props.max_floors = 8
    props.block_variety = 'MEDIUM'
    props.base_block_size = 10.0
    props.district_mode = False  # ← MODE NORMAL
    
    print(f"  Configuration: {props.width}x{props.length}, variété {props.block_variety}")
    print(f"  Mode district: {props.district_mode}")
    
    # Générer et analyser
    generate_and_analyze("Mode Normal")

def test_commercial_district(props):
    """Test du mode district avec dominante commerciale."""
    
    # Nettoyer la scène
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete(use_global=False)
    
    # Configuration district commercial
    props.width = 5
    props.length = 5
    props.max_floors = 15
    props.block_variety = 'HIGH'
    props.base_block_size = 12.0
    props.district_mode = True  # ← MODE DISTRICT ACTIVÉ
    props.commercial_ratio = 0.6  # ← 60% COMMERCIAL
    props.residential_ratio = 0.3
    props.industrial_ratio = 0.1
    
    print(f"  Configuration: {props.width}x{props.length}, variété {props.block_variety}")
    print(f"  Mode district: {props.district_mode}")
    print(f"  Ratios: C={props.commercial_ratio}, R={props.residential_ratio}, I={props.industrial_ratio}")
    
    # Générer et analyser
    generate_and_analyze("District Commercial")

def test_residential_district(props):
    """Test du mode district avec dominante résidentielle."""
    
    # Nettoyer la scène  
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete(use_global=False)
    
    # Configuration district résidentiel
    props.width = 6
    props.length = 6
    props.max_floors = 10
    props.block_variety = 'HIGH'
    props.base_block_size = 10.0
    props.district_mode = True  # ← MODE DISTRICT ACTIVÉ
    props.commercial_ratio = 0.2
    props.residential_ratio = 0.7  # ← 70% RÉSIDENTIEL
    props.industrial_ratio = 0.1
    
    print(f"  Configuration: {props.width}x{props.length}, variété {props.block_variety}")
    print(f"  Mode district: {props.district_mode}")
    print(f"  Ratios: C={props.commercial_ratio}, R={props.residential_ratio}, I={props.industrial_ratio}")
    
    # Générer et analyser
    generate_and_analyze("District Résidentiel")

def test_industrial_district(props):
    """Test du mode district avec dominante industrielle."""
    
    # Nettoyer la scène
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete(use_global=False)
    
    # Configuration district industriel
    props.width = 4
    props.length = 5
    props.max_floors = 6
    props.block_variety = 'EXTREME'
    props.base_block_size = 15.0
    props.district_mode = True  # ← MODE DISTRICT ACTIVÉ
    props.commercial_ratio = 0.1
    props.residential_ratio = 0.3
    props.industrial_ratio = 0.6  # ← 60% INDUSTRIEL
    
    print(f"  Configuration: {props.width}x{props.length}, variété {props.block_variety}")
    print(f"  Mode district: {props.district_mode}")
    print(f"  Ratios: C={props.commercial_ratio}, R={props.residential_ratio}, I={props.industrial_ratio}")
    
    # Générer et analyser
    generate_and_analyze("District Industriel")

def generate_and_analyze(mode_name):
    """Génère et analyse le résultat."""
    
    try:
        result = bpy.ops.citygen.generate_city()
        if result == {'FINISHED'}:
            print(f"  ✅ {mode_name} généré avec succès")
            analyze_quick(mode_name)
        else:
            print(f"  ❌ Échec génération {mode_name}")
    except Exception as e:
        print(f"  ❌ Erreur {mode_name}: {e}")

def analyze_quick(mode_name):
    """Analyse rapide des objets générés."""
    
    # Compter les objets
    roads = [obj for obj in bpy.context.scene.objects if 'road' in obj.name.lower()]
    sidewalks = [obj for obj in bpy.context.scene.objects if 'sidewalk' in obj.name.lower()]
    buildings = [obj for obj in bpy.context.scene.objects if 'batiment' in obj.name.lower()]
    
    print(f"    📊 Objets: {len(buildings)} bâtiments, {len(roads)} routes, {len(sidewalks)} trottoirs")
    
    # Analyser les matériaux (indicateur de districts)
    materials = set()
    for obj in bpy.context.scene.objects:
        if obj.data and hasattr(obj.data, 'materials'):
            for mat in obj.data.materials:
                if mat:
                    materials.add(mat.name)
    
    district_materials = [mat for mat in materials if 'District' in mat]
    if district_materials:
        print(f"    🎨 Matériaux districts: {', '.join(district_materials)}")
    else:
        print(f"    🎨 Matériaux standard: {len(materials)} total")
    
    print(f"    💡 Regardez la vue 3D pour voir le style {mode_name}")

# Interface utilisateur simple
def quick_test_alignment():
    """Test rapide d'alignement seulement."""
    
    print("=== TEST ALIGNEMENT RAPIDE ===")
    
    if not hasattr(bpy.context.scene, 'citygen_props'):
        print("❌ Addon non activé")
        return False
    
    props = bpy.context.scene.citygen_props
    
    # Configuration simple pour alignement
    props.width = 3
    props.length = 3
    props.max_floors = 5
    props.block_variety = 'UNIFORM'
    props.base_block_size = 10.0
    props.district_mode = False
    
    # Nettoyer et générer
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete(use_global=False)
    
    try:
        result = bpy.ops.citygen.generate_city()
        if result == {'FINISHED'}:
            print("✅ Test alignement réussi")
            return True
        else:
            print("❌ Échec test alignement")
            return False
    except Exception as e:
        print(f"❌ Erreur: {e}")
        return False

# Choisir le test à exécuter
print("🎯 TESTS DISPONIBLES:")
print("1. test_all_modes() - Test complet de tous les modes")
print("2. quick_test_alignment() - Test rapide alignement seulement")
print("\nCopiez-collez l'une de ces lignes pour exécuter:")
print("success = test_all_modes()")
print("success = quick_test_alignment()")

# Exécution par défaut (changez selon vos besoins)
success = quick_test_alignment()
if success:
    print("\n🎉 Test terminé ! Vérifiez la vue 3D")
else:
    print("\n❌ Test échoué")
# Choisir le test à exécuter
print("🎯 TESTS DISPONIBLES:")
print("1. test_all_modes() - Test complet de tous les modes")
print("2. quick_test_alignment() - Test rapide alignement seulement")
print("\nCopiez-collez l'une de ces lignes pour exécuter:")
print("success = test_all_modes()")
print("success = quick_test_alignment()")

# Exécution par défaut (changez selon vos besoins)
success = quick_test_alignment()
if success:
    print("\n🎉 Test terminé ! Vérifiez la vue 3D")
else:
    print("\n❌ Test échoué")

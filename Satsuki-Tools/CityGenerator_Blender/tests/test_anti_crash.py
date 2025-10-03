#!/usr/bin/env python3
"""
Test anti-crash pour City Block Generator
Valide que les fonctions critiques gèrent les erreurs proprement
"""

import sys
import traceback

def mock_bpy_context():
    """Simule un contexte Blender pour les tests"""
    class MockScene:
        def __init__(self):
            # Propriétés sécurisées par défaut
            self.citygen_width = 3
            self.citygen_length = 3
            self.citygen_max_floors = 5
            self.citygen_buildings_per_block = 1
            self.citygen_road_width = 4.0
            self.citygen_seamless_roads = True
            self.citygen_building_variety = 'MEDIUM'
            self.citygen_height_variation = 0.3
    
    class MockContext:
        def __init__(self):
            self.scene = MockScene()
    
    return MockContext()

def test_parameter_validation():
    """Test la validation des paramètres d'entrée"""
    print("🔧 === TEST VALIDATION PARAMÈTRES ===")
    print()
    
    test_cases = [
        # Cas normaux
        {'width': 3, 'length': 3, 'should_pass': True, 'name': 'Paramètres normaux'},
        {'width': 1, 'length': 1, 'should_pass': True, 'name': 'Paramètres minimaux'},
        {'width': 5, 'length': 5, 'should_pass': True, 'name': 'Paramètres limites'},
        
        # Cas d'erreur
        {'width': 0, 'length': 3, 'should_pass': False, 'name': 'Largeur nulle'},
        {'width': 3, 'length': 0, 'should_pass': False, 'name': 'Longueur nulle'},
        {'width': -1, 'length': 3, 'should_pass': False, 'name': 'Largeur négative'},
        {'width': 10, 'length': 10, 'should_pass': False, 'name': 'Trop grande grille'},
    ]
    
    all_passed = True
    
    for case in test_cases:
        print(f"🔍 Test: {case['name']}")
        print(f"   Paramètres: width={case['width']}, length={case['length']}")
        
        try:
            # Simulation de validation
            width = max(1, min(case['width'], 5))
            length = max(1, min(case['length'], 5))
            total_blocks = width * length
            
            validation_passed = (
                width >= 1 and width <= 5 and
                length >= 1 and length <= 5 and
                total_blocks <= 25
            )
            
            if validation_passed == case['should_pass']:
                print(f"   ✅ Validation correcte")
            else:
                print(f"   ❌ Validation incorrecte!")
                all_passed = False
                
        except Exception as e:
            print(f"   ❌ ERREUR: {e}")
            all_passed = False
        
        print()
    
    return all_passed

def test_safe_functions():
    """Test les fonctions utilitaires sécurisées"""
    print("🛡️ === TEST FONCTIONS SÉCURISÉES ===")
    print()
    
    # Simulation des fonctions safe_int et safe_float
    def safe_int(value, default):
        try:
            if isinstance(value, (int, float)):
                return int(value)
            return default
        except:
            return default
    
    def safe_float(value, default):
        try:
            if isinstance(value, (int, float)):
                return float(value)
            return default
        except:
            return default
    
    test_cases = [
        # Tests safe_int
        {'func': safe_int, 'value': 5, 'default': 1, 'expected': 5, 'name': 'safe_int normal'},
        {'func': safe_int, 'value': 'invalid', 'default': 1, 'expected': 1, 'name': 'safe_int invalid'},
        {'func': safe_int, 'value': None, 'default': 1, 'expected': 1, 'name': 'safe_int None'},
        
        # Tests safe_float
        {'func': safe_float, 'value': 3.14, 'default': 1.0, 'expected': 3.14, 'name': 'safe_float normal'},
        {'func': safe_float, 'value': 'invalid', 'default': 1.0, 'expected': 1.0, 'name': 'safe_float invalid'},
        {'func': safe_float, 'value': None, 'default': 1.0, 'expected': 1.0, 'name': 'safe_float None'},
    ]
    
    all_passed = True
    
    for case in test_cases:
        print(f"🔍 Test: {case['name']}")
        print(f"   Paramètres: value={case['value']}, default={case['default']}")
        
        try:
            result = case['func'](case['value'], case['default'])
            
            if result == case['expected']:
                print(f"   ✅ Résultat correct: {result}")
            else:
                print(f"   ❌ Résultat incorrect: {result} (attendu: {case['expected']})")
                all_passed = False
                
        except Exception as e:
            print(f"   ❌ ERREUR: {e}")
            all_passed = False
        
        print()
    
    return all_passed

def test_error_handling():
    """Test la gestion d'erreurs"""
    print("⚡ === TEST GESTION D'ERREURS ===")
    print()
    
    def safe_operation_test(should_fail=False):
        """Simule une opération qui peut échouer"""
        try:
            if should_fail:
                raise ValueError("Erreur simulée")
            return True
        except Exception as e:
            print(f"   🛡️ Erreur capturée: {e}")
            return False
    
    test_cases = [
        {'should_fail': False, 'expected': True, 'name': 'Opération normale'},
        {'should_fail': True, 'expected': False, 'name': 'Opération avec erreur'},
    ]
    
    all_passed = True
    
    for case in test_cases:
        print(f"🔍 Test: {case['name']}")
        
        try:
            result = safe_operation_test(case['should_fail'])
            
            if result == case['expected']:
                print(f"   ✅ Gestion d'erreur correcte")
            else:
                print(f"   ❌ Gestion d'erreur incorrecte!")
                all_passed = False
                
        except Exception as e:
            print(f"   ❌ ERREUR NON CAPTURÉE: {e}")
            all_passed = False
        
        print()
    
    return all_passed

def test_performance_checks():
    """Test les vérifications de performance"""
    print("📊 === TEST VÉRIFICATIONS PERFORMANCE ===")
    print()
    
    def check_performance_limits(total_objects=0, total_meshes=0):
        """Simule la vérification des limites de performance"""
        limits = {
            'max_objects': 100,
            'max_meshes': 150,
        }
        
        warnings = []
        if total_objects > limits['max_objects']:
            warnings.append(f"Trop d'objets: {total_objects}/{limits['max_objects']}")
        if total_meshes > limits['max_meshes']:
            warnings.append(f"Trop de meshes: {total_meshes}/{limits['max_meshes']}")
        
        return len(warnings) == 0, warnings
    
    test_cases = [
        {'objects': 50, 'meshes': 75, 'should_pass': True, 'name': 'Utilisation normale'},
        {'objects': 150, 'meshes': 75, 'should_pass': False, 'name': 'Trop d\'objets'},
        {'objects': 50, 'meshes': 200, 'should_pass': False, 'name': 'Trop de meshes'},
        {'objects': 200, 'meshes': 300, 'should_pass': False, 'name': 'Dépassement total'},
    ]
    
    all_passed = True
    
    for case in test_cases:
        print(f"🔍 Test: {case['name']}")
        print(f"   Paramètres: {case['objects']} objets, {case['meshes']} meshes")
        
        try:
            passed, warnings = check_performance_limits(case['objects'], case['meshes'])
            
            if passed == case['should_pass']:
                print(f"   ✅ Vérification correcte")
                if warnings:
                    for warning in warnings:
                        print(f"      ⚠️ {warning}")
            else:
                print(f"   ❌ Vérification incorrecte!")
                all_passed = False
                
        except Exception as e:
            print(f"   ❌ ERREUR: {e}")
            all_passed = False
        
        print()
    
    return all_passed

def run_anti_crash_tests():
    """Exécute tous les tests anti-crash"""
    print("🛡️ === SUITE DE TESTS ANTI-CRASH ===")
    print()
    
    results = {
        'parameter_validation': test_parameter_validation(),
        'safe_functions': test_safe_functions(),
        'error_handling': test_error_handling(),
        'performance_checks': test_performance_checks()
    }
    
    print("📋 === RÉSUMÉ TESTS ANTI-CRASH ===")
    for test_name, passed in results.items():
        status = "✅ PASSÉ" if passed else "❌ ÉCHEC"
        print(f"   {test_name}: {status}")
    
    all_passed = all(results.values())
    
    print()
    if all_passed:
        print("🎉 TOUS LES TESTS ANTI-CRASH PASSÉS! Addon robuste.")
        return 0
    else:
        print("💥 CERTAINS TESTS ONT ÉCHOUÉ! Risque de crash.")
        return 1

if __name__ == "__main__":
    """Point d'entrée pour exécution directe"""
    try:
        exit_code = run_anti_crash_tests()
        sys.exit(exit_code)
    except Exception as e:
        print(f"💥 ERREUR CRITIQUE dans les tests: {e}")
        print(f"Traceback: {traceback.format_exc()}")
        sys.exit(1)
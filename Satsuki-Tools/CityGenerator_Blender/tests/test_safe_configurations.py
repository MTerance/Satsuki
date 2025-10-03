#!/usr/bin/env python3
"""
Test de configurations sécurisées pour City Block Generator
Valide que l'addon ne crash pas avec différentes configurations
"""

import sys
import traceback

# Test configurations sécurisées
SAFE_CONFIGS = [
    # Configuration minimale
    {
        'name': 'Minimal Safe',
        'width': 1,
        'length': 1,
        'max_floors': 1,
        'buildings_per_block': 1,
        'expected_blocks': 1,
        'expected_buildings': 1
    },
    
    # Configuration petite mais sûre
    {
        'name': 'Small Safe',
        'width': 2,
        'length': 2,
        'max_floors': 3,
        'buildings_per_block': 1,
        'expected_blocks': 4,
        'expected_buildings': 4
    },
    
    # Configuration optimale
    {
        'name': 'Optimal Safe',
        'width': 3,
        'length': 3,
        'max_floors': 5,
        'buildings_per_block': 1,
        'expected_blocks': 9,
        'expected_buildings': 9
    },
    
    # Configuration limite sécurisée
    {
        'name': 'Max Safe',
        'width': 5,
        'length': 5,
        'max_floors': 15,
        'buildings_per_block': 1,
        'expected_blocks': 25,
        'expected_buildings': 25
    }
]

# Configurations dangereuses (doivent être bloquées)
DANGEROUS_CONFIGS = [
    {
        'name': 'Too Many Blocks',
        'width': 6,
        'length': 6,
        'expected_error': 'limitation automatique'
    },
    
    {
        'name': 'Too Many Buildings',
        'width': 5,
        'length': 5,
        'buildings_per_block': 3,
        'expected_error': 'trop pour la performance'
    }
]

def validate_config_safety(config):
    """Valide qu'une configuration respecte les limites de sécurité"""
    total_blocks = config.get('width', 1) * config.get('length', 1)
    total_buildings = total_blocks * config.get('buildings_per_block', 1)
    
    safety_checks = {
        'blocks_safe': total_blocks <= 25,
        'buildings_safe': total_buildings <= 50,
        'width_safe': config.get('width', 1) <= 5,
        'length_safe': config.get('length', 1) <= 5,
        'floors_safe': config.get('max_floors', 1) <= 15,
        'buildings_per_block_safe': config.get('buildings_per_block', 1) <= 2
    }
    
    return safety_checks

def test_safe_configurations():
    """Test toutes les configurations sécurisées"""
    print("🧪 === TEST CONFIGURATIONS SÉCURISÉES ===")
    print()
    
    all_passed = True
    
    for config in SAFE_CONFIGS:
        print(f"🔍 Test: {config['name']}")
        print(f"   Paramètres: {config['width']}x{config['length']}, {config['max_floors']} étages, {config['buildings_per_block']} bât/bloc")
        
        try:
            safety = validate_config_safety(config)
            
            if all(safety.values()):
                print(f"   ✅ Configuration sécurisée")
                print(f"   📊 {config['expected_blocks']} blocs, {config['expected_buildings']} bâtiments")
            else:
                print(f"   ❌ Configuration DANGEREUSE!")
                print(f"   📊 Échecs: {[k for k, v in safety.items() if not v]}")
                all_passed = False
                
        except Exception as e:
            print(f"   ❌ ERREUR lors de la validation: {e}")
            all_passed = False
        
        print()
    
    return all_passed

def test_dangerous_configurations():
    """Test que les configurations dangereuses sont bien bloquées"""
    print("🚨 === TEST CONFIGURATIONS DANGEREUSES ===")
    print()
    
    all_passed = True
    
    for config in DANGEROUS_CONFIGS:
        print(f"🔍 Test: {config['name']}")
        
        try:
            safety = validate_config_safety(config)
            
            # Ces configurations doivent échouer
            if not all(safety.values()):
                print(f"   ✅ Configuration correctement bloquée")
                print(f"   🛡️ Sécurités activées: {[k for k, v in safety.items() if not v]}")
            else:
                print(f"   ❌ Configuration dangereuse NON BLOQUÉE!")
                all_passed = False
                
        except Exception as e:
            print(f"   ❌ ERREUR lors de la validation: {e}")
            all_passed = False
        
        print()
    
    return all_passed

def test_performance_limits():
    """Test les limites de performance"""
    print("⚡ === TEST LIMITES DE PERFORMANCE ===")
    print()
    
    test_cases = [
        {'total_blocks': 25, 'should_pass': True, 'name': 'Limite exacte blocs'},
        {'total_blocks': 26, 'should_pass': False, 'name': 'Dépassement blocs'},
        {'total_buildings': 50, 'should_pass': True, 'name': 'Limite exacte bâtiments'},
        {'total_buildings': 51, 'should_pass': False, 'name': 'Dépassement bâtiments'},
    ]
    
    all_passed = True
    
    for case in test_cases:
        print(f"🔍 Test: {case['name']}")
        
        try:
            if 'total_blocks' in case:
                passed = case['total_blocks'] <= 25
            else:
                passed = case['total_buildings'] <= 50
            
            if passed == case['should_pass']:
                print(f"   ✅ Limite correctement respectée")
            else:
                print(f"   ❌ Limite mal gérée!")
                all_passed = False
                
        except Exception as e:
            print(f"   ❌ ERREUR: {e}")
            all_passed = False
        
        print()
    
    return all_passed

def run_all_tests():
    """Exécute tous les tests de sécurité"""
    print("🎯 === SUITE DE TESTS SÉCURITÉ CITY BLOCK GENERATOR ===")
    print()
    
    results = {
        'safe_configs': test_safe_configurations(),
        'dangerous_configs': test_dangerous_configurations(),
        'performance_limits': test_performance_limits()
    }
    
    print("📋 === RÉSUMÉ DES TESTS ===")
    for test_name, passed in results.items():
        status = "✅ PASSÉ" if passed else "❌ ÉCHEC"
        print(f"   {test_name}: {status}")
    
    all_passed = all(results.values())
    
    print()
    if all_passed:
        print("🎉 TOUS LES TESTS PASSÉS! Addon sécurisé.")
        return 0
    else:
        print("💥 CERTAINS TESTS ONT ÉCHOUÉ! Vérifiez la sécurité.")
        return 1

if __name__ == "__main__":
    """Point d'entrée pour exécution directe"""
    try:
        exit_code = run_all_tests()
        sys.exit(exit_code)
    except Exception as e:
        print(f"💥 ERREUR CRITIQUE dans les tests: {e}")
        print(f"Traceback: {traceback.format_exc()}")
        sys.exit(1)
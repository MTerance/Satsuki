#!/usr/bin/env python3
"""
Suite de tests complète pour City Block Generator
Exécute tous les tests de sécurité, performance et robustesse
"""

import sys
import os
import subprocess
import traceback

def run_test_script(script_name):
    """Exécute un script de test et retourne le résultat"""
    try:
        print(f"🚀 Exécution de {script_name}...")
        result = subprocess.run([sys.executable, script_name], 
                              capture_output=True, text=True, cwd='.')
        
        print("📄 SORTIE:")
        print(result.stdout)
        
        if result.stderr:
            print("⚠️ ERREURS:")
            print(result.stderr)
        
        success = result.returncode == 0
        print(f"📊 Résultat: {'✅ SUCCÈS' if success else '❌ ÉCHEC'} (code: {result.returncode})")
        print("=" * 60)
        
        return success
        
    except Exception as e:
        print(f"💥 ERREUR lors de l'exécution de {script_name}: {e}")
        print("=" * 60)
        return False

def check_test_files():
    """Vérifie que tous les fichiers de test existent"""
    test_files = [
        'test_safe_configurations.py',
        'test_anti_crash.py'
    ]
    
    missing_files = []
    for test_file in test_files:
        if not os.path.exists(test_file):
            missing_files.append(test_file)
    
    if missing_files:
        print(f"❌ Fichiers de test manquants: {missing_files}")
        return False
    
    print(f"✅ Tous les fichiers de test trouvés: {test_files}")
    return True

def run_comprehensive_tests():
    """Exécute la suite complète de tests"""
    print("🎯 === SUITE COMPLÈTE DE TESTS CITY BLOCK GENERATOR ===")
    print()
    
    # Vérifier les fichiers de test
    if not check_test_files():
        print("💥 Impossible de continuer sans tous les fichiers de test")
        return 1
    
    print()
    
    # Liste des tests à exécuter
    test_scripts = [
        'test_safe_configurations.py',
        'test_anti_crash.py'
    ]
    
    results = {}
    
    # Exécuter chaque test
    for script in test_scripts:
        print(f"📋 === TEST: {script} ===")
        results[script] = run_test_script(script)
        print()
    
    # Résumé final
    print("🏆 === RÉSUMÉ FINAL DES TESTS ===")
    all_passed = True
    
    for script, passed in results.items():
        status = "✅ PASSÉ" if passed else "❌ ÉCHEC"
        print(f"   {script}: {status}")
        if not passed:
            all_passed = False
    
    print()
    
    if all_passed:
        print("🎉 FÉLICITATIONS! Tous les tests sont passés.")
        print("🛡️ L'addon City Block Generator est sécurisé et robuste.")
        print()
        print("✅ Prêt pour la production:")
        print("   - Configurations sécurisées validées")
        print("   - Protection anti-crash activée")
        print("   - Limites de performance respectées")
        print("   - Gestion d'erreurs robuste")
        return 0
    else:
        print("⚠️ ATTENTION! Certains tests ont échoué.")
        print("🔧 Vérifiez les problèmes signalés avant utilisation.")
        print()
        print("❌ Actions nécessaires:")
        for script, passed in results.items():
            if not passed:
                print(f"   - Corriger les problèmes dans {script}")
        return 1

def generate_test_report():
    """Génère un rapport de test"""
    report_file = "test_report.txt"
    
    try:
        with open(report_file, 'w', encoding='utf-8') as f:
            f.write("RAPPORT DE TESTS - CITY BLOCK GENERATOR\n")
            f.write("=" * 50 + "\n\n")
            f.write(f"Date: {__import__('datetime').datetime.now()}\n")
            f.write("Version: 6.13.7\n\n")
            
            f.write("TESTS EXÉCUTÉS:\n")
            f.write("- test_safe_configurations.py: Tests de configurations sécurisées\n")
            f.write("- test_anti_crash.py: Tests de robustesse anti-crash\n\n")
            
            f.write("SÉCURITÉS IMPLÉMENTÉES:\n")
            f.write("- Limites de grille: max 5x5 (25 blocs)\n")
            f.write("- Limites de bâtiments: max 50 par génération\n")
            f.write("- Validation des paramètres d'entrée\n")
            f.write("- Gestion d'erreurs avec try-catch\n")
            f.write("- Avertissements dans l'interface utilisateur\n")
            f.write("- Limites de performance pour éviter les crashes\n\n")
            
            f.write("RECOMMANDATIONS:\n")
            f.write("- Utiliser des grilles 3x3 ou plus petites pour de meilleures performances\n")
            f.write("- Éviter plus de 1-2 bâtiments par bloc\n")
            f.write("- Surveiller les avertissements dans l'interface\n")
            f.write("- Sauvegarder avant de générer de grandes villes\n")
        
        print(f"📄 Rapport de test généré: {report_file}")
        
    except Exception as e:
        print(f"⚠️ Impossible de générer le rapport: {e}")

if __name__ == "__main__":
    """Point d'entrée principal"""
    try:
        exit_code = run_comprehensive_tests()
        
        # Générer le rapport même en cas d'échec
        generate_test_report()
        
        sys.exit(exit_code)
        
    except KeyboardInterrupt:
        print("\n🛑 Tests interrompus par l'utilisateur")
        sys.exit(1)
        
    except Exception as e:
        print(f"💥 ERREUR CRITIQUE: {e}")
        print(f"Traceback: {traceback.format_exc()}")
        sys.exit(1)
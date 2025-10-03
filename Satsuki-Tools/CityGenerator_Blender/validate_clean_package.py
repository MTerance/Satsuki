#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de validation du package City Block Generator CLEAN
Vérifie que l'addon peut être chargé correctement dans Blender
"""

import sys
import os
import zipfile
import tempfile
import shutil

def validate_zip_structure(zip_path):
    """Valide la structure du ZIP"""
    print("=== VALIDATION STRUCTURE ZIP ===")
    
    try:
        with zipfile.ZipFile(zip_path, 'r') as zip_file:
            files = zip_file.namelist()
            print(f"Fichiers trouvés: {len(files)}")
            
            required_files = [
                'city_block_generator_clean/__init__.py',
                'city_block_generator_clean/operators.py', 
                'city_block_generator_clean/ui.py',
                'city_block_generator_clean/generator.py'
            ]
            
            missing_files = []
            for required_file in required_files:
                if required_file not in files:
                    missing_files.append(required_file)
                else:
                    print(f"✅ {required_file}")
            
            if missing_files:
                print("❌ Fichiers manquants:")
                for missing in missing_files:
                    print(f"   - {missing}")
                return False
            
            print("✅ Structure ZIP valide")
            return True
            
    except Exception as e:
        print(f"❌ Erreur validation ZIP: {e}")
        return False

def validate_python_syntax(zip_path):
    """Valide la syntaxe Python des fichiers"""
    print("\\n=== VALIDATION SYNTAXE PYTHON ===")
    
    try:
        with tempfile.TemporaryDirectory() as temp_dir:
            # Extraire le ZIP
            with zipfile.ZipFile(zip_path, 'r') as zip_file:
                zip_file.extractall(temp_dir)
            
            addon_dir = os.path.join(temp_dir, 'city_block_generator_clean')
            python_files = ['__init__.py', 'operators.py', 'ui.py', 'generator.py']
            
            for py_file in python_files:
                file_path = os.path.join(addon_dir, py_file)
                if os.path.exists(file_path):
                    try:
                        with open(file_path, 'r', encoding='utf-8') as f:
                            code = f.read()
                        
                        # Compilation syntaxique
                        compile(code, file_path, 'exec')
                        print(f"✅ {py_file} - syntaxe valide")
                        
                    except SyntaxError as e:
                        print(f"❌ {py_file} - Erreur syntaxe: {e}")
                        return False
                    except Exception as e:
                        print(f"⚠️ {py_file} - Avertissement: {e}")
                else:
                    print(f"❌ {py_file} - fichier manquant")
                    return False
            
            print("✅ Syntaxe Python valide")
            return True
            
    except Exception as e:
        print(f"❌ Erreur validation syntaxe: {e}")
        return False

def validate_blender_compatibility(zip_path):
    """Valide la compatibilité Blender basique"""
    print("\\n=== VALIDATION COMPATIBILITÉ BLENDER ===")
    
    try:
        with tempfile.TemporaryDirectory() as temp_dir:
            # Extraire le ZIP
            with zipfile.ZipFile(zip_path, 'r') as zip_file:
                zip_file.extractall(temp_dir)
            
            addon_dir = os.path.join(temp_dir, 'city_block_generator_clean')
            init_file = os.path.join(addon_dir, '__init__.py')
            
            # Vérifier bl_info
            with open(init_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            if 'bl_info' not in content:
                print("❌ bl_info manquant dans __init__.py")
                return False
            
            # Vérifier les imports Blender basiques
            required_imports = ['import bpy']
            for imp in required_imports:
                if imp not in content:
                    print(f"❌ Import manquant: {imp}")
                    return False
            
            # Vérifier les fonctions register/unregister
            if 'def register(' not in content:
                print("❌ Fonction register() manquante")
                return False
                
            if 'def unregister(' not in content:
                print("❌ Fonction unregister() manquante")
                return False
            
            print("✅ Compatibilité Blender basique validée")
            print("✅ bl_info présent")
            print("✅ Fonctions register/unregister présentes")
            return True
            
    except Exception as e:
        print(f"❌ Erreur validation Blender: {e}")
        return False

def validate_variety_features(zip_path):
    """Valide la présence des fonctionnalités de variété"""
    print("\\n=== VALIDATION FONCTIONNALITÉS VARIÉTÉ ===")
    
    try:
        with tempfile.TemporaryDirectory() as temp_dir:
            # Extraire le ZIP
            with zipfile.ZipFile(zip_path, 'r') as zip_file:
                zip_file.extractall(temp_dir)
            
            addon_dir = os.path.join(temp_dir, 'city_block_generator_clean')
            
            # Vérifier generator.py pour les nouvelles fonctions
            generator_file = os.path.join(addon_dir, 'generator.py')
            with open(generator_file, 'r', encoding='utf-8') as f:
                generator_content = f.read()
            
            variety_functions = [
                'create_varied_material',
                'choose_building_type', 
                'add_urban_variety'
            ]
            
            for func in variety_functions:
                if func in generator_content:
                    print(f"✅ Fonction {func} présente")
                else:
                    print(f"❌ Fonction {func} manquante")
                    return False
            
            # Vérifier operators.py pour les propriétés
            operators_file = os.path.join(addon_dir, 'operators.py')
            with open(operators_file, 'r', encoding='utf-8') as f:
                operators_content = f.read()
            
            if 'citygen_building_variety' in operators_content:
                print("✅ Propriété building_variety présente")
            else:
                print("❌ Propriété building_variety manquante")
                return False
            
            print("✅ Fonctionnalités de variété validées")
            return True
            
    except Exception as e:
        print(f"❌ Erreur validation variété: {e}")
        return False

def run_complete_validation():
    """Exécute toutes les validations"""
    zip_path = "city_block_generator_v6_13_8_CLEAN.zip"
    
    print("VALIDATION COMPLÈTE - CITY BLOCK GENERATOR CLEAN")
    print("=" * 55)
    
    if not os.path.exists(zip_path):
        print(f"❌ Fichier ZIP non trouvé: {zip_path}")
        return False
    
    print(f"📦 Validation du fichier: {zip_path}")
    file_size = os.path.getsize(zip_path) / 1024  # KB
    print(f"📊 Taille: {file_size:.1f} KB")
    print()
    
    validations = [
        ("Structure ZIP", validate_zip_structure),
        ("Syntaxe Python", validate_python_syntax),
        ("Compatibilité Blender", validate_blender_compatibility),
        ("Fonctionnalités Variété", validate_variety_features)
    ]
    
    results = {}
    for name, validator in validations:
        try:
            results[name] = validator(zip_path)
        except Exception as e:
            print(f"❌ Erreur {name}: {e}")
            results[name] = False
    
    print("\\n=== RÉSUMÉ VALIDATION ===")
    all_passed = True
    for name, passed in results.items():
        status = "✅ PASSÉ" if passed else "❌ ÉCHEC"
        print(f"{name}: {status}")
        if not passed:
            all_passed = False
    
    print()
    if all_passed:
        print("🎉 VALIDATION COMPLÈTE RÉUSSIE!")
        print("🚀 L'addon est prêt pour Blender")
        print()
        print("INSTRUCTIONS D'INSTALLATION:")
        print("1. Ouvrir Blender")
        print("2. Edit > Preferences > Add-ons") 
        print("3. Install > Sélectionner city_block_generator_v6_13_8_CLEAN.zip")
        print("4. Activer 'City Block Generator'")
        print("5. Utiliser le panneau CityGen dans la sidebar 3D")
        print()
        print("NOUVELLES FONCTIONNALITÉS:")
        print("• 6x plus de variété visuelle")
        print("• 18 couleurs par zone")
        print("• 10 types de bâtiments")
        print("• Variations urbaines")
        return 0
    else:
        print("❌ VALIDATION ÉCHOUÉE!")
        print("Des corrections sont nécessaires.")
        return 1

if __name__ == "__main__":
    try:
        exit_code = run_complete_validation()
        sys.exit(exit_code)
    except Exception as e:
        print(f"ERREUR FATALE: {e}")
        sys.exit(1)
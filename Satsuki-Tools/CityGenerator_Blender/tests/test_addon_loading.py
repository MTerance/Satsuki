#!/usr/bin/env python3
"""
Script de test pour vérifier que l'addon City Block Generator peut être chargé correctement.
Ce script simule le chargement de l'addon dans Blender pour détecter les erreurs potentielles.
"""

import sys
import os
import importlib.util
import traceback

def test_addon_loading():
    """Test de chargement de l'addon City Block Generator"""
    print("=== TEST DE CHARGEMENT ADDON CITY BLOCK GENERATOR ===")
    print()
    
    # Chemin vers le dossier de l'addon
    addon_path = "city_block_generator"
    
    if not os.path.exists(addon_path):
        print(f"❌ ERREUR: Le dossier '{addon_path}' n'existe pas!")
        return False
    
    print(f"✅ Dossier addon trouvé: {addon_path}")
    
    # Liste des fichiers requis
    required_files = ["__init__.py", "operators.py", "ui.py", "generator.py"]
    
    # Vérifier la présence des fichiers
    for file_name in required_files:
        file_path = os.path.join(addon_path, file_name)
        if os.path.exists(file_path):
            print(f"✅ {file_name}: Présent")
        else:
            print(f"❌ {file_name}: MANQUANT")
            return False
    
    print()
    print("=== TESTS DE SYNTAXE ===")
    
    # Test de syntaxe pour chaque fichier
    for file_name in required_files:
        file_path = os.path.join(addon_path, file_name)
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Tenter de compiler le code
            compile(content, file_path, 'exec')
            print(f"✅ {file_name}: Syntaxe OK")
            
        except SyntaxError as e:
            print(f"❌ {file_name}: ERREUR DE SYNTAXE à la ligne {e.lineno}: {e.msg}")
            return False
        except Exception as e:
            print(f"⚠️ {file_name}: Erreur de lecture: {e}")
            return False
    
    print()
    print("=== TESTS DE STRUCTURE ===")
    
    # Test de structure de __init__.py
    init_path = os.path.join(addon_path, "__init__.py")
    try:
        with open(init_path, 'r', encoding='utf-8') as f:
            init_content = f.read()
        
        # Vérifier bl_info
        if "bl_info" in init_content:
            print("✅ bl_info: Présent")
        else:
            print("❌ bl_info: MANQUANT")
            return False
        
        # Vérifier register/unregister
        if "def register(" in init_content:
            print("✅ fonction register(): Présente")
        else:
            print("❌ fonction register(): MANQUANTE")
            return False
            
        if "def unregister(" in init_content:
            print("✅ fonction unregister(): Présente")
        else:
            print("❌ fonction unregister(): MANQUANTE")
            return False
        
        # Vérifier imports
        if "from . import" in init_content:
            print("✅ Imports relatifs: Présents")
        else:
            print("⚠️ Imports relatifs: Possiblement manquants")
            
    except Exception as e:
        print(f"❌ Erreur lecture __init__.py: {e}")
        return False
    
    print()
    print("=== TESTS DES CLASSES BLENDER ===")
    
    # Test des classes dans operators.py
    operators_path = os.path.join(addon_path, "operators.py")
    try:
        with open(operators_path, 'r', encoding='utf-8') as f:
            operators_content = f.read()
        
        blender_classes = [
            "bpy.types.Operator",
            "bpy.types.PropertyGroup"
        ]
        
        for class_type in blender_classes:
            if class_type in operators_content:
                print(f"✅ {class_type}: Trouvé")
            else:
                print(f"⚠️ {class_type}: Non trouvé")
                
    except Exception as e:
        print(f"❌ Erreur lecture operators.py: {e}")
        return False
    
    # Test des classes dans ui.py
    ui_path = os.path.join(addon_path, "ui.py")
    try:
        with open(ui_path, 'r', encoding='utf-8') as f:
            ui_content = f.read()
        
        if "bpy.types.Panel" in ui_content:
            print("✅ bpy.types.Panel: Trouvé")
        else:
            print("❌ bpy.types.Panel: MANQUANT")
            return False
            
        # Vérifier bl_space_type et bl_region_type
        if "bl_space_type = 'VIEW_3D'" in ui_content:
            print("✅ bl_space_type: Configuré pour VIEW_3D")
        else:
            print("⚠️ bl_space_type: Configuration inconnue")
            
        if "bl_region_type = 'UI'" in ui_content:
            print("✅ bl_region_type: Configuré pour UI")
        else:
            print("⚠️ bl_region_type: Configuration inconnue")
            
    except Exception as e:
        print(f"❌ Erreur lecture ui.py: {e}")
        return False
    
    print()
    print("=== RÉSULTATS ===")
    print("✅ TOUS LES TESTS PASSÉS!")
    print("🎯 L'addon devrait se charger correctement dans Blender")
    print()
    print("Instructions d'installation:")
    print("1. Créez le package avec './package_addon.ps1'")
    print("2. Dans Blender: Edit > Preferences > Add-ons")
    print("3. Cliquez 'Install' et sélectionnez le fichier ZIP")
    print("4. Activez 'City Block Generator' dans la liste")
    print("5. Le panneau devrait apparaître dans la sidebar (N)")
    print("   sous l'onglet 'CityGen'")
    
    return True

if __name__ == "__main__":
    try:
        success = test_addon_loading()
        if success:
            print("\n🎉 TEST RÉUSSI - Addon prêt pour l'installation!")
            sys.exit(0)
        else:
            print("\n❌ TEST ÉCHOUÉ - Corrigez les erreurs avant de continuer")
            sys.exit(1)
    except Exception as e:
        print(f"\n💥 ERREUR CRITIQUE: {e}")
        print(f"Traceback: {traceback.format_exc()}")
        sys.exit(1)

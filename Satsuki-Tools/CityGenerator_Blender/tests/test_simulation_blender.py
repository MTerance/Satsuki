#!/usr/bin/env python3
"""
Script de test pour simuler le chargement de l'addon dans Blender
et identifier les erreurs qui empêchent la reconnaissance.
"""

import sys
import os
import importlib.util
import traceback

class MockBpy:
    """Mock de bpy pour tester l'addon sans Blender"""
    
    class types:
        class Operator:
            pass
        class Panel:
            pass
        class PropertyGroup:
            pass
        class Scene:
            pass
    
    class props:
        @staticmethod
        def IntProperty(**kwargs):
            return lambda: kwargs.get('default', 0)
        
        @staticmethod
        def FloatProperty(**kwargs):
            return lambda: kwargs.get('default', 0.0)
        
        @staticmethod
        def BoolProperty(**kwargs):
            return lambda: kwargs.get('default', False)
        
        @staticmethod
        def EnumProperty(**kwargs):
            items = kwargs.get('items', [])
            default = kwargs.get('default', '')
            if items and not default:
                default = items[0][0]
            return lambda: default
        
        @staticmethod
        def PointerProperty(**kwargs):
            return lambda: None
    
    class utils:
        @staticmethod
        def register_class(cls):
            print(f"Mock: register_class({cls.__name__})")
        
        @staticmethod
        def unregister_class(cls):
            print(f"Mock: unregister_class({cls.__name__})")
    
    class app:
        class handlers:
            load_post = []
            
            @staticmethod
            def persistent(func):
                """Mock du décorateur persistent"""
                print(f"Mock: persistent decorator applied to {func.__name__}")
                return func
        
        version_string = "4.0.0"
    
    class context:
        class scene:
            name = "Scene"

def test_addon_loading():
    """Test le chargement de l'addon avec un mock de bpy"""
    print("🧪 TEST DE CHARGEMENT ADDON AVEC SIMULATION BLENDER")
    print("=" * 60)
    
    # Ajouter le mock de bpy dans sys.modules
    sys.modules['bpy'] = MockBpy()
    
    addon_path = "city_block_generator"
    
    if not os.path.exists(addon_path):
        print(f"❌ Dossier addon introuvable: {addon_path}")
        return False
    
    # Ajouter le chemin de l'addon au sys.path pour les imports relatifs
    current_dir = os.getcwd()
    if current_dir not in sys.path:
        sys.path.insert(0, current_dir)
    
    print(f"✅ Dossier addon trouvé: {addon_path}")
    
    # Test 1: Import du module principal
    print("\n1️⃣ TEST IMPORT MODULE PRINCIPAL:")
    try:
        # Charger __init__.py
        init_path = os.path.join(addon_path, "__init__.py")
        spec = importlib.util.spec_from_file_location("city_block_generator", init_path)
        addon_module = importlib.util.module_from_spec(spec)
        
        # Ajouter le module à sys.modules avant l'exécution
        sys.modules["city_block_generator"] = addon_module
        
        print("   📦 Exécution du module principal...")
        spec.loader.exec_module(addon_module)
        print("   ✅ Module principal chargé avec succès")
        
        # Vérifier la présence de bl_info
        if hasattr(addon_module, 'bl_info'):
            bl_info = addon_module.bl_info
            print(f"   ✅ bl_info trouvé: {bl_info['name']} v{bl_info['version']}")
        else:
            print("   ❌ bl_info manquant!")
            return False
        
    except Exception as e:
        print(f"   ❌ ERREUR import module principal: {e}")
        print(f"   Traceback: {traceback.format_exc()}")
        return False
    
    # Test 2: Vérification des sous-modules
    print("\n2️⃣ TEST IMPORT SOUS-MODULES:")
    submodules = ["operators", "ui", "generator"]
    
    for submodule_name in submodules:
        try:
            submodule_path = os.path.join(addon_path, f"{submodule_name}.py")
            if not os.path.exists(submodule_path):
                print(f"   ❌ {submodule_name}.py: FICHIER MANQUANT")
                continue
            
            # Charger le sous-module
            spec = importlib.util.spec_from_file_location(
                f"city_block_generator.{submodule_name}", 
                submodule_path
            )
            submodule = importlib.util.module_from_spec(spec)
            
            # Ajouter à sys.modules
            sys.modules[f"city_block_generator.{submodule_name}"] = submodule
            
            print(f"   📦 Chargement {submodule_name}.py...")
            spec.loader.exec_module(submodule)
            print(f"   ✅ {submodule_name}: Chargé avec succès")
            
            # Vérifications spécifiques
            if submodule_name == "operators":
                if hasattr(submodule, 'classes'):
                    print(f"      • Classes trouvées: {len(submodule.classes)}")
                    for cls in submodule.classes:
                        print(f"        - {cls.__name__}")
                else:
                    print("      ⚠️ Variable 'classes' manquante")
                
                if hasattr(submodule, 'register'):
                    print("      ✅ Fonction register() présente")
                else:
                    print("      ❌ Fonction register() manquante")
            
            elif submodule_name == "ui":
                # Chercher les panneaux
                for attr_name in dir(submodule):
                    attr = getattr(submodule, attr_name)
                    if hasattr(attr, '__mro__') and any('Panel' in base.__name__ for base in attr.__mro__):
                        print(f"      ✅ Panneau trouvé: {attr_name}")
            
        except Exception as e:
            print(f"   ❌ ERREUR {submodule_name}: {e}")
            print(f"      Traceback: {traceback.format_exc()}")
            return False
    
    # Test 3: Test des fonctions register/unregister
    print("\n3️⃣ TEST FONCTIONS REGISTER/UNREGISTER:")
    try:
        if hasattr(addon_module, 'register'):
            print("   📝 Test de la fonction register()...")
            addon_module.register()
            print("   ✅ register() exécuté sans erreur")
        else:
            print("   ❌ Fonction register() manquante!")
            return False
        
        if hasattr(addon_module, 'unregister'):
            print("   📝 Test de la fonction unregister()...")
            addon_module.unregister()
            print("   ✅ unregister() exécuté sans erreur")
        else:
            print("   ❌ Fonction unregister() manquante!")
            return False
        
    except Exception as e:
        print(f"   ❌ ERREUR register/unregister: {e}")
        print(f"      Traceback: {traceback.format_exc()}")
        return False
    
    # Test 4: Vérification de la structure
    print("\n4️⃣ VÉRIFICATION STRUCTURE FINALE:")
    
    # Vérifier que tous les modules sont dans sys.modules
    expected_modules = [
        "city_block_generator",
        "city_block_generator.operators",
        "city_block_generator.ui", 
        "city_block_generator.generator"
    ]
    
    all_present = True
    for module_name in expected_modules:
        if module_name in sys.modules:
            print(f"   ✅ {module_name}: Module en mémoire")
        else:
            print(f"   ❌ {module_name}: Module manquant en mémoire")
            all_present = False
    
    if all_present:
        print("\n🎉 TOUS LES TESTS PASSÉS!")
        print("✅ L'addon devrait fonctionner dans Blender")
        return True
    else:
        print("\n❌ CERTAINS TESTS ONT ÉCHOUÉ")
        return False

def cleanup_modules():
    """Nettoie les modules chargés pour éviter les conflits"""
    modules_to_remove = [name for name in sys.modules.keys() if name.startswith('city_block_generator')]
    for module_name in modules_to_remove:
        del sys.modules[module_name]
    
    if 'bpy' in sys.modules:
        del sys.modules['bpy']

if __name__ == "__main__":
    try:
        success = test_addon_loading()
        cleanup_modules()
        
        print("\n" + "=" * 60)
        if success:
            print("🎯 RÉSULTAT: Addon prêt pour Blender!")
            print("\n💡 Si l'addon ne fonctionne toujours pas dans Blender:")
            print("   1. Problème de cache Blender")
            print("   2. Conflit avec un autre addon")
            print("   3. Installation incorrecte du ZIP")
            print("   4. Version Blender incompatible")
        else:
            print("🚨 RÉSULTAT: Addon a des problèmes!")
            print("   Corrigez les erreurs détectées avant de continuer")
            
    except Exception as e:
        cleanup_modules()
        print(f"\n💥 ERREUR CRITIQUE: {e}")
        print(f"Traceback: {traceback.format_exc()}")

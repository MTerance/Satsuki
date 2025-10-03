#!/usr/bin/env python3
"""
Script de diagnostic avancé pour identifier pourquoi l'addon City Block Generator
n'est pas pris en compte par Blender.
"""

import os
import sys
import importlib.util
import traceback
import ast

def check_blender_addon_structure():
    """Vérifie la structure et la validité de l'addon pour Blender"""
    print("🔍 DIAGNOSTIC AVANCÉ - ADDON CITY BLOCK GENERATOR")
    print("=" * 60)
    
    addon_path = "city_block_generator"
    
    if not os.path.exists(addon_path):
        print(f"❌ FATAL: Dossier '{addon_path}' introuvable!")
        return False
    
    print(f"✅ Dossier addon trouvé: {addon_path}")
    
    # 1. Vérification des fichiers requis
    print("\n1️⃣ VÉRIFICATION DES FICHIERS REQUIS:")
    required_files = {
        "__init__.py": "Module principal",
        "operators.py": "Opérateurs Blender", 
        "ui.py": "Interface utilisateur",
        "generator.py": "Générateur de ville"
    }
    
    missing_files = []
    for filename, description in required_files.items():
        filepath = os.path.join(addon_path, filename)
        if os.path.exists(filepath):
            size = os.path.getsize(filepath)
            print(f"   ✅ {filename} ({size} octets) - {description}")
            if size == 0:
                print(f"   ⚠️ ATTENTION: {filename} est vide!")
        else:
            print(f"   ❌ {filename} MANQUANT - {description}")
            missing_files.append(filename)
    
    if missing_files:
        print(f"\n❌ Fichiers manquants: {missing_files}")
        return False
    
    # 2. Analyse du bl_info
    print("\n2️⃣ ANALYSE DU bl_info:")
    init_path = os.path.join(addon_path, "__init__.py")
    try:
        with open(init_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Parser le fichier Python pour extraire bl_info
        tree = ast.parse(content)
        bl_info_found = False
        
        for node in ast.walk(tree):
            if isinstance(node, ast.Assign):
                for target in node.targets:
                    if isinstance(target, ast.Name) and target.id == 'bl_info':
                        bl_info_found = True
                        print("   ✅ bl_info trouvé dans __init__.py")
                        
                        # Extraire les valeurs de bl_info
                        try:
                            # Exécuter seulement la partie bl_info
                            bl_info_code = content.split('bl_info = ')[1].split('\n\n')[0]
                            bl_info_code = 'bl_info = ' + bl_info_code
                            exec_globals = {}
                            exec(bl_info_code, exec_globals)
                            bl_info = exec_globals['bl_info']
                            
                            # Vérifier les champs requis
                            required_fields = ["name", "author", "version", "blender", "category"]
                            for field in required_fields:
                                if field in bl_info:
                                    if field == "version":
                                        version = bl_info[field]
                                        print(f"   ✅ {field}: {version} (format: {type(version)})")
                                        if not isinstance(version, tuple) or len(version) != 3:
                                            print(f"   ⚠️ ATTENTION: Version doit être un tuple (x,y,z)")
                                    else:
                                        print(f"   ✅ {field}: {bl_info[field]}")
                                else:
                                    print(f"   ❌ {field}: MANQUANT")
                            
                            # Vérifier version Blender
                            if "blender" in bl_info:
                                blender_version = bl_info["blender"]
                                if isinstance(blender_version, tuple) and len(blender_version) >= 2:
                                    major, minor = blender_version[0], blender_version[1]
                                    print(f"   ✅ Version Blender requise: {major}.{minor}+")
                                    if major < 2 or (major == 2 and minor < 80):
                                        print(f"   ⚠️ Version Blender très ancienne!")
                                else:
                                    print(f"   ⚠️ Format version Blender incorrect: {blender_version}")
                            
                        except Exception as e:
                            print(f"   ⚠️ Erreur parsing bl_info: {e}")
                        break
        
        if not bl_info_found:
            print("   ❌ bl_info NOT FOUND dans __init__.py!")
            return False
            
    except Exception as e:
        print(f"   ❌ Erreur lecture __init__.py: {e}")
        return False
    
    # 3. Vérification des imports
    print("\n3️⃣ VÉRIFICATION DES IMPORTS:")
    try:
        # Vérifier les imports relatifs dans __init__.py
        if "from . import" in content:
            print("   ✅ Imports relatifs trouvés")
            import_lines = [line.strip() for line in content.split('\n') if 'from . import' in line]
            for line in import_lines:
                print(f"      • {line}")
        else:
            print("   ❌ Aucun import relatif trouvé!")
            return False
        
        # Vérifier les fonctions register/unregister
        if "def register(" in content:
            print("   ✅ Fonction register() trouvée")
        else:
            print("   ❌ Fonction register() MANQUANTE!")
            return False
            
        if "def unregister(" in content:
            print("   ✅ Fonction unregister() trouvée")
        else:
            print("   ❌ Fonction unregister() MANQUANTE!")
            return False
            
    except Exception as e:
        print(f"   ❌ Erreur vérification imports: {e}")
        return False
    
    # 4. Test de compilation Python
    print("\n4️⃣ TEST DE COMPILATION PYTHON:")
    for filename in required_files.keys():
        filepath = os.path.join(addon_path, filename)
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                file_content = f.read()
            
            # Test compilation
            compile(file_content, filepath, 'exec')
            print(f"   ✅ {filename}: Compilation OK")
            
            # Vérifier imports bpy
            if "import bpy" in file_content:
                print(f"      • Import bpy: ✅")
            else:
                print(f"      • Import bpy: ❌ (requis pour {filename})")
            
        except SyntaxError as e:
            print(f"   ❌ {filename}: ERREUR SYNTAXE ligne {e.lineno}: {e.msg}")
            print(f"      Code: {e.text}")
            return False
        except Exception as e:
            print(f"   ❌ {filename}: Erreur: {e}")
            return False
    
    # 5. Vérification des classes Blender
    print("\n5️⃣ VÉRIFICATION DES CLASSES BLENDER:")
    
    # Vérifier operators.py
    operators_path = os.path.join(addon_path, "operators.py")
    try:
        with open(operators_path, 'r', encoding='utf-8') as f:
            ops_content = f.read()
        
        blender_classes = [
            ("bpy.types.Operator", "Opérateurs"),
            ("bpy.types.PropertyGroup", "Groupes de propriétés"),
            ("bl_idname", "Identifiants Blender"),
            ("classes = [", "Liste des classes")
        ]
        
        for pattern, description in blender_classes:
            if pattern in ops_content:
                print(f"   ✅ {description}: Trouvé")
            else:
                print(f"   ❌ {description}: MANQUANT")
                
    except Exception as e:
        print(f"   ❌ Erreur vérification operators.py: {e}")
    
    # Vérifier ui.py
    ui_path = os.path.join(addon_path, "ui.py")
    try:
        with open(ui_path, 'r', encoding='utf-8') as f:
            ui_content = f.read()
        
        ui_elements = [
            ("bpy.types.Panel", "Panneau UI"),
            ("bl_space_type", "Type d'espace"),
            ("bl_region_type", "Type de région"),
            ("def draw(", "Fonction draw"),
        ]
        
        for pattern, description in ui_elements:
            if pattern in ui_content:
                print(f"   ✅ {description}: Trouvé")
            else:
                print(f"   ❌ {description}: MANQUANT")
                
    except Exception as e:
        print(f"   ❌ Erreur vérification ui.py: {e}")
    
    # 6. Détection de problèmes courants
    print("\n6️⃣ DÉTECTION DE PROBLÈMES COURANTS:")
    
    problems = []
    
    # Vérifier les imports cycliques
    all_files_content = {}
    for filename in required_files.keys():
        filepath = os.path.join(addon_path, filename)
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                all_files_content[filename] = f.read()
        except:
            continue
    
    # Rechercher imports cycliques
    for filename, content in all_files_content.items():
        if filename == "ui.py" and "from .operators import" in content:
            problems.append("Import cyclique détecté: ui.py importe depuis operators.py")
    
    # Vérifier noms de modules
    if "city_block_generator" not in content:
        problems.append("Nom de module incorrect dans le code")
    
    # Vérifier encodage
    for filename, content in all_files_content.items():
        try:
            content.encode('utf-8')
        except UnicodeEncodeError:
            problems.append(f"Problème d'encodage dans {filename}")
    
    if problems:
        print("   🚨 PROBLÈMES DÉTECTÉS:")
        for problem in problems:
            print(f"      • {problem}")
    else:
        print("   ✅ Aucun problème courant détecté")
    
    # 7. Recommandations
    print("\n7️⃣ RECOMMANDATIONS:")
    if problems:
        print("   🔧 Actions recommandées:")
        print("      1. Corrigez les problèmes listés ci-dessus")
        print("      2. Testez l'addon dans une nouvelle installation Blender")
        print("      3. Vérifiez la console Blender pour les erreurs")
    else:
        print("   🎯 Addon semble correct structurellement")
        print("   🔍 Problème probable:")
        print("      • Cache Blender corrompu")
        print("      • Conflit avec autre addon")
        print("      • Installation incorrecte")
        print("      • Version Blender incompatible")
    
    print("\n" + "=" * 60)
    return len(problems) == 0

if __name__ == "__main__":
    try:
        success = check_blender_addon_structure()
        if success:
            print("✅ DIAGNOSTIC TERMINÉ - Structure addon OK")
            print("\n🔧 Si l'addon ne fonctionne toujours pas:")
            print("   1. Redémarrez Blender complètement")
            print("   2. Réinstallez l'addon (Remove puis Install)")
            print("   3. Vérifiez Window > Toggle System Console")
            print("   4. Testez dans Blender vanilla (sans autres addons)")
        else:
            print("❌ DIAGNOSTIC TERMINÉ - Problèmes détectés")
            print("   Corrigez les erreurs avant de continuer")
    except Exception as e:
        print(f"💥 ERREUR CRITIQUE DIAGNOSTIC: {e}")
        print(f"Traceback: {traceback.format_exc()}")

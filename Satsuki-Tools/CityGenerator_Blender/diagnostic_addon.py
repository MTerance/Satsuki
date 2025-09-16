#!/usr/bin/env python3
"""
Script de diagnostic pour vérifier la validité syntaxique des fichiers de l'addon
City Block Generator avant packaging
"""
import ast
import os
import sys

def check_python_syntax(file_path):
    """Vérifie la syntaxe Python d'un fichier"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Tenter de parser le fichier
        ast.parse(content)
        return True, "OK"
    except SyntaxError as e:
        return False, f"Erreur de syntaxe ligne {e.lineno}: {e.msg}"
    except Exception as e:
        return False, f"Erreur: {str(e)}"

def main():
    """Fonction principale de diagnostic"""
    print("=== DIAGNOSTIC ADDON CITY BLOCK GENERATOR ===")
    print()
    
    addon_dir = "city_block_generator_6_12"
    
    if not os.path.exists(addon_dir):
        print(f"❌ ERREUR: Le dossier '{addon_dir}' n'existe pas!")
        return
    
    # Fichiers Python à vérifier
    python_files = [
        "__init__.py",
        "operators.py", 
        "ui.py",
        "generator.py"
    ]
    
    all_ok = True
    
    for filename in python_files:
        file_path = os.path.join(addon_dir, filename)
        
        if not os.path.exists(file_path):
            print(f"❌ {filename}: Fichier manquant")
            all_ok = False
            continue
        
        is_valid, message = check_python_syntax(file_path)
        
        if is_valid:
            print(f"✅ {filename}: {message}")
        else:
            print(f"❌ {filename}: {message}")
            all_ok = False
    
    print()
    
    if all_ok:
        print("✅ TOUS LES FICHIERS SONT VALIDES")
        print("🎯 L'addon devrait fonctionner correctement dans Blender")
    else:
        print("❌ ERREURS DÉTECTÉES")
        print("⚠️  Corrigez les erreurs avant d'installer l'addon")
    
    print()
    
    # Vérifications supplémentaires
    print("=== VÉRIFICATIONS SUPPLÉMENTAIRES ===")
    
    # Vérifier bl_info
    init_file = os.path.join(addon_dir, "__init__.py")
    if os.path.exists(init_file):
        with open(init_file, 'r', encoding='utf-8') as f:
            content = f.read()
            
        if 'bl_info' in content:
            print("✅ bl_info trouvé dans __init__.py")
        else:
            print("❌ bl_info manquant dans __init__.py")
            
        if '"name"' in content and '"version"' in content:
            print("✅ Informations de base de l'addon présentes")
        else:
            print("❌ Informations de base de l'addon manquantes")
    
    # Vérifier les imports
    for filename in python_files:
        file_path = os.path.join(addon_dir, filename)
        if os.path.exists(file_path):
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            if 'import bpy' in content:
                print(f"✅ {filename}: Import bpy présent")
            elif filename != "__init__.py":  # __init__.py peut ne pas importer bpy directement
                print(f"⚠️  {filename}: Import bpy manquant")
    
    print()
    print("=== RECOMMANDATIONS ===")
    
    if all_ok:
        print("1. ✅ L'addon est prêt pour le packaging")
        print("2. 🎯 Utilisez ./package_addon.ps1 pour créer le ZIP")
        print("3. 📦 Installez le ZIP dans Blender via Edit > Preferences > Add-ons")
    else:
        print("1. ❌ Corrigez les erreurs de syntaxe détectées")
        print("2. 🔄 Relancez ce diagnostic")
        print("3. 📝 Vérifiez les imports et la structure des fichiers")
    
    print()
    print("=== FIN DIAGNOSTIC ===")

if __name__ == "__main__":
    main()

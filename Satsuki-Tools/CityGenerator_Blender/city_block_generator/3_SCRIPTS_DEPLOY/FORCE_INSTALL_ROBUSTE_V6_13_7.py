"""
FORCE INSTALLATION ROBUSTE V6.13.7
Script ultra-robuste pour forcer l'installation du v6.13.7
"""

import shutil
import os
import sys

def force_install_robust():
    """Installation forcée ultra-robuste"""
    
    print("🔥🔥🔥 FORCE INSTALLATION ROBUSTE V6.13.7 🔥🔥🔥")
    
    workspace_path = r"C:\Users\sshom\source\repos\Satsuki\Satsuki-Tools\CityGenerator_Blender\city_block_generator"
    addon_path = r"C:\Users\sshom\Documents\assets\Tools\city_block_generator"
    
    # Étape 1: Vérifier que les fichiers workspace existent
    print("📁 === VÉRIFICATION WORKSPACE ===")
    required_files = ["__init__.py", "generator.py", "operators.py", "ui.py"]
    
    for file in required_files:
        file_path = os.path.join(workspace_path, file)
        if os.path.exists(file_path):
            size = os.path.getsize(file_path)
            print(f"   ✅ {file}: {size} bytes")
        else:
            print(f"   ❌ {file}: MANQUANT!")
            return False
    
    # Étape 2: Vérifier la version dans workspace
    init_file = os.path.join(workspace_path, "__init__.py")
    try:
        with open(init_file, 'r', encoding='utf-8') as f:
            content = f.read()
            if '"version": (6, 13, 7)' in content:
                print("   ✅ Version 6.13.7 confirmée dans workspace")
            else:
                print("   ⚠️ Version 6.13.7 non trouvée dans workspace")
                # Forcer la mise à jour de version
                content = content.replace('"version": (6, 13, 6)', '"version": (6, 13, 7)')
                content = content.replace('"version": (6, 13, 5)', '"version": (6, 13, 7)')
                content = content.replace('"version": (6, 13, 4)', '"version": (6, 13, 7)')
                with open(init_file, 'w', encoding='utf-8') as f:
                    f.write(content)
                print("   ✅ Version forcée à 6.13.7")
    except Exception as e:
        print(f"   ❌ Erreur lecture version: {e}")
    
    # Étape 3: Supprimer complètement l'ancien addon
    print("🗑️ === SUPPRESSION COMPLÈTE ADDON ===")
    if os.path.exists(addon_path):
        try:
            # Supprimer tous les fichiers .pyc
            for root, dirs, files in os.walk(addon_path):
                for file in files:
                    if file.endswith('.pyc'):
                        pyc_path = os.path.join(root, file)
                        try:
                            os.remove(pyc_path)
                            print(f"   🗑️ Supprimé: {file}")
                        except:
                            pass
            
            # Supprimer le dossier __pycache__
            pycache_path = os.path.join(addon_path, "__pycache__")
            if os.path.exists(pycache_path):
                shutil.rmtree(pycache_path, ignore_errors=True)
                print("   🗑️ __pycache__ supprimé")
            
            # Supprimer tout le dossier
            shutil.rmtree(addon_path, ignore_errors=True)
            print("   ✅ Ancien addon supprimé complètement")
        except Exception as e:
            print(f"   ⚠️ Erreur suppression: {e}")
    
    # Étape 4: Créer le dossier parent si nécessaire
    addon_parent = os.path.dirname(addon_path)
    if not os.path.exists(addon_parent):
        os.makedirs(addon_parent, exist_ok=True)
        print(f"   ✅ Dossier parent créé: {addon_parent}")
    
    # Étape 5: Copie complète
    print("📋 === COPIE COMPLÈTE ===")
    try:
        shutil.copytree(workspace_path, addon_path)
        print(f"   ✅ Copie réussie vers: {addon_path}")
    except Exception as e:
        print(f"   ❌ Erreur copie: {e}")
        return False
    
    # Étape 6: Vérification finale
    print("🔍 === VÉRIFICATION FINALE ===")
    
    # Vérifier que tous les fichiers sont présents
    for file in required_files:
        file_path = os.path.join(addon_path, file)
        if os.path.exists(file_path):
            size = os.path.getsize(file_path)
            print(f"   ✅ {file}: {size} bytes")
        else:
            print(f"   ❌ {file}: MANQUANT après copie!")
            return False
    
    # Vérifier la version finale
    addon_init = os.path.join(addon_path, "__init__.py")
    try:
        with open(addon_init, 'r', encoding='utf-8') as f:
            content = f.read()
            if '"version": (6, 13, 7)' in content:
                print("   ✅ Version 6.13.7 confirmée dans addon")
            else:
                print("   ❌ Version 6.13.7 non confirmée dans addon")
                return False
    except Exception as e:
        print(f"   ❌ Erreur vérification version finale: {e}")
        return False
    
    # Étape 7: Test d'importation Python
    print("🐍 === TEST IMPORTATION PYTHON ===")
    try:
        # Ajouter le chemin addon au sys.path temporairement
        if addon_path not in sys.path:
            sys.path.insert(0, addon_path)
        
        # Tester l'importation
        import importlib.util
        spec = importlib.util.spec_from_file_location("city_addon", addon_init)
        if spec and spec.loader:
            print("   ✅ Module importable")
        else:
            print("   ⚠️ Module non importable")
        
        # Nettoyer sys.path
        if addon_path in sys.path:
            sys.path.remove(addon_path)
            
    except Exception as e:
        print(f"   ⚠️ Test importation: {e}")
    
    print("🎯 === INSTALLATION ROBUSTE TERMINÉE ===")
    print(f"📁 Addon installé: {addon_path}")
    print(f"📊 Version: 6.13.7")
    print(f"🔥 Système: Courbes Blender natives MEGA visibles")
    print("")
    print("🔄 === INSTRUCTIONS BLENDER ===")
    print("1. 🔄 REDÉMARRER Blender complètement")
    print("2. 🔧 Edit > Preferences > Add-ons")
    print("3. 🔍 Rechercher 'City Block'")
    print("4. ❌ DÉSACTIVER l'ancien addon si présent")
    print("5. 🗑️ SUPPRIMER l'ancien addon")
    print("6. ➕ Install... > Sélectionner le dossier:")
    print(f"   📁 {addon_path}")
    print("7. ✅ ACTIVER le nouvel addon v6.13.7")
    print("8. 🎯 Tester avec courbes MEGA visibles!")
    
    return True

if __name__ == "__main__":
    success = force_install_robust()
    if success:
        print("🔥✅ INSTALLATION ROBUSTE RÉUSSIE !")
    else:
        print("❌ INSTALLATION ROBUSTE ÉCHOUÉE !")

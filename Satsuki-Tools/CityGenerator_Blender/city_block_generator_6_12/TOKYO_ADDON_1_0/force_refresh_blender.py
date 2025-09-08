# FORCE REFRESH ADDON DANS BLENDER
# Script à exécuter DANS Blender pour forcer le rafraîchissement

import bpy
import sys
import importlib

def force_refresh_tokyo_addon():
    """Force le rafraîchissement de l'addon Tokyo dans Blender"""
    
    print("🔄 FORCE REFRESH TOKYO CITY GENERATOR")
    print("=" * 45)
    
    addon_name = "tokyo_city_generator"
    
    # 1. Désactiver l'addon s'il est actif
    print("❌ Désactivation de l'addon...")
    try:
        if addon_name in bpy.context.preferences.addons:
            bpy.ops.preferences.addon_disable(module=addon_name)
            print("✅ Addon désactivé")
        else:
            print("⚠️ Addon pas activé")
    except Exception as e:
        print(f"❌ Erreur désactivation: {e}")
    
    # 2. Nettoyer le cache des modules
    print("🧹 Nettoyage du cache...")
    modules_to_remove = []
    for module_name in sys.modules:
        if module_name.startswith(addon_name):
            modules_to_remove.append(module_name)
    
    for module_name in modules_to_remove:
        try:
            del sys.modules[module_name]
            print(f"🗑️ Module {module_name} supprimé du cache")
        except:
            pass
    
    # 3. Forcer le refresh de la liste des addons
    print("🔄 Rafraîchissement de la liste...")
    try:
        bpy.ops.preferences.addon_refresh()
        print("✅ Liste rafraîchie")
    except Exception as e:
        print(f"❌ Erreur refresh: {e}")
    
    # 4. Réactiver l'addon
    print("✅ Réactivation de l'addon...")
    try:
        bpy.ops.preferences.addon_enable(module=addon_name)
        print("✅ Addon réactivé")
        
        # Vérifier la version affichée
        if addon_name in bpy.context.preferences.addons:
            addon = bpy.context.preferences.addons[addon_name]
            if hasattr(addon.module, 'bl_info'):
                info = addon.module.bl_info
                version = info.get('version', 'Inconnue')
                name = info.get('name', 'Inconnu')
                print(f"📋 Nom affiché: {name}")
                print(f"🔢 Version affichée: {version}")
                
                if version == (1, 3, 0):
                    print("🎉 SUCCESS! Version 1.3.0 maintenant affichée!")
                else:
                    print(f"⚠️ Version incorrecte affichée: {version}")
            else:
                print("❌ bl_info non trouvé")
        else:
            print("❌ Addon non trouvé après réactivation")
            
    except Exception as e:
        print(f"❌ Erreur réactivation: {e}")
    
    # 5. Vérifier les nouvelles propriétés
    print("🎛️ Vérification des nouvelles propriétés...")
    scene = bpy.context.scene
    
    new_properties = [
        'tokyo_use_advanced_textures',
        'tokyo_texture_base_path'
    ]
    
    for prop in new_properties:
        if hasattr(scene, prop):
            print(f"✅ Nouvelle propriété {prop} disponible")
        else:
            print(f"❌ Propriété {prop} manquante")
    
    print("\n✅ REFRESH TERMINÉ!")
    print("🔄 Allez dans Edit > Preferences > Add-ons")
    print("🔍 Cherchez 'Tokyo' - vous devriez voir v1.3.0")

def check_addon_status():
    """Vérifie le statut actuel de l'addon"""
    
    print("📊 STATUT ACTUEL DE L'ADDON")
    print("=" * 35)
    
    addon_name = "tokyo_city_generator"
    
    if addon_name in bpy.context.preferences.addons:
        addon = bpy.context.preferences.addons[addon_name]
        print(f"✅ Addon trouvé: {addon_name}")
        
        try:
            module = addon.module
            if hasattr(module, 'bl_info'):
                info = module.bl_info
                print(f"📋 Nom: {info.get('name', 'Non défini')}")
                print(f"🔢 Version: {info.get('version', 'Non définie')}")
                print(f"👤 Auteur: {info.get('author', 'Non défini')}")
                
                # Vérifier si c'est la bonne version
                version = info.get('version', None)
                if version == (1, 3, 0):
                    print("🎉 CORRECT: Version 1.3.0 détectée!")
                elif version == (1, 0, 8):
                    print("❌ PROBLÈME: Ancienne version 1.0.8 encore chargée!")
                    print("🔧 Solution: Exécutez force_refresh_tokyo_addon()")
                else:
                    print(f"⚠️ Version inattendue: {version}")
            else:
                print("❌ bl_info manquant")
        except Exception as e:
            print(f"❌ Erreur lecture addon: {e}")
    else:
        print(f"❌ Addon non activé: {addon_name}")
    
    # Vérifier les fichiers sur disque
    import os
    addon_path = bpy.utils.user_resource('SCRIPTS', 'addons')
    tokyo_path = os.path.join(addon_path, addon_name)
    
    print(f"\n📁 Fichiers sur disque:")
    print(f"📂 Chemin: {tokyo_path}")
    
    if os.path.exists(tokyo_path):
        init_file = os.path.join(tokyo_path, "__init__.py")
        if os.path.exists(init_file):
            try:
                with open(init_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                if '"version": (1, 3, 0)' in content:
                    print("✅ Fichier v1.3.0 présent sur disque")
                elif '"version": (1, 0, 8)' in content:
                    print("❌ Fichier v1.0.8 encore sur disque!")
                else:
                    print("⚠️ Version indéterminée sur disque")
                    
                if "TEXTURE SYSTEM" in content:
                    print("✅ Système de textures détecté dans le fichier")
                else:
                    print("❌ Système de textures non détecté")
                    
            except Exception as e:
                print(f"❌ Erreur lecture fichier: {e}")
        else:
            print("❌ Fichier __init__.py manquant")
    else:
        print("❌ Dossier addon non trouvé sur disque")

# Exécution automatique
if __name__ == "__main__":
    print("🔍 Vérification du statut actuel...")
    check_addon_status()
    
    print("\n" + "="*50)
    input("Appuyez sur Entrée pour forcer le refresh...")
    
    force_refresh_tokyo_addon()

# Instructions pour Blender
"""
DANS BLENDER:
1. Allez dans Scripting workspace
2. Créez un nouveau script
3. Copiez ce code
4. Exécutez avec "Run Script"

OU dans la console Python:
exec(open(r"c:\\path\\to\\this\\script.py").read())
"""

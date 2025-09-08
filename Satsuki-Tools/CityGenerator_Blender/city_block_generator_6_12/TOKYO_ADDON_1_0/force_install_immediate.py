# FORCE INSTALLATION IMMÉDIATE - TOKYO v1.4.0
# Installation directe après redémarrage Blender

import os
import shutil
import time

def force_install_tokyo_immediate():
    """Force l'installation immédiate de Tokyo v1.4.0 dans Blender"""
    
    print("🚨 FORCE INSTALLATION TOKYO v1.4.0 - IMMÉDIATE")
    print("=" * 55)
    print("🎯 ADDON TOKYO NON VISIBLE APRÈS REDÉMARRAGE")
    print("=" * 55)
    
    # Chemins critiques
    source_v1_4_0 = r"c:\Users\sshom\Documents\assets\Tools\tokyo_city_generator_1_4_0"
    blender_target = r"C:\Users\sshom\AppData\Roaming\Blender Foundation\Blender\4.0\scripts\addons\tokyo_city_generator"
    
    print(f"📁 Source v1.4.0: {source_v1_4_0}")
    print(f"🎯 Target Blender: {blender_target}")
    
    # Étape 1: Vérifier la source
    print(f"\n1️⃣ VÉRIFICATION SOURCE v1.4.0")
    
    if not os.path.exists(source_v1_4_0):
        print(f"❌ ERREUR: Source v1.4.0 non trouvée!")
        print(f"🔧 Relancez d'abord: python deploy_tokyo_v1_4_0.py")
        return False
    
    init_source = os.path.join(source_v1_4_0, "__init__.py")
    if not os.path.exists(init_source):
        print(f"❌ ERREUR: __init__.py manquant dans la source!")
        return False
    
    # Vérifier version dans la source
    with open(init_source, 'r', encoding='utf-8') as f:
        source_content = f.read()
    
    if '"version": (1, 4, 0)' in source_content:
        print(f"✅ Source v1.4.0 confirmée")
    else:
        print(f"❌ Source n'est pas v1.4.0!")
        return False
    
    source_size = os.path.getsize(init_source)
    print(f"📊 Taille source: {source_size:,} bytes")
    
    # Étape 2: Nettoyer complètement la destination
    print(f"\n2️⃣ NETTOYAGE COMPLET DESTINATION")
    
    if os.path.exists(blender_target):
        print(f"🗑️ Suppression complète ancien addon...")
        try:
            shutil.rmtree(blender_target, ignore_errors=True)
            time.sleep(2)  # Attendre un peu
            
            # Vérifier suppression
            if os.path.exists(blender_target):
                print(f"⚠️ Suppression incomplète, force manuelle...")
                # Essayer fichier par fichier
                for root, dirs, files in os.walk(blender_target, topdown=False):
                    for file in files:
                        try:
                            os.remove(os.path.join(root, file))
                        except:
                            pass
                    for dir in dirs:
                        try:
                            os.rmdir(os.path.join(root, dir))
                        except:
                            pass
                try:
                    os.rmdir(blender_target)
                except:
                    pass
            
            if not os.path.exists(blender_target):
                print(f"✅ Ancien addon supprimé")
            else:
                print(f"❌ Impossible de supprimer complètement")
                print(f"🔧 FERMEZ BLENDER et relancez ce script")
                return False
                
        except Exception as e:
            print(f"❌ Erreur suppression: {e}")
            return False
    else:
        print(f"✅ Aucun ancien addon trouvé")
    
    # Étape 3: Créer dossier parent si nécessaire
    print(f"\n3️⃣ PRÉPARATION DOSSIER BLENDER")
    
    blender_addons_dir = os.path.dirname(blender_target)
    if not os.path.exists(blender_addons_dir):
        os.makedirs(blender_addons_dir, exist_ok=True)
        print(f"📁 Dossier addons créé: {blender_addons_dir}")
    else:
        print(f"✅ Dossier addons existe: {blender_addons_dir}")
    
    # Étape 4: Copier v1.4.0
    print(f"\n4️⃣ INSTALLATION v1.4.0")
    
    try:
        shutil.copytree(source_v1_4_0, blender_target)
        print(f"✅ Copie terminée: {blender_target}")
    except Exception as e:
        print(f"❌ Erreur copie: {e}")
        return False
    
    # Étape 5: Vérification installation
    print(f"\n5️⃣ VÉRIFICATION INSTALLATION")
    
    if not os.path.exists(blender_target):
        print(f"❌ Dossier addon non créé!")
        return False
    
    init_target = os.path.join(blender_target, "__init__.py")
    if not os.path.exists(init_target):
        print(f"❌ __init__.py non copié!")
        return False
    
    # Vérifier contenu
    with open(init_target, 'r', encoding='utf-8') as f:
        target_content = f.read()
    
    if '"version": (1, 4, 0)' in target_content:
        print(f"✅ Version 1.4.0 installée")
    else:
        print(f"❌ Version incorrecte installée")
        return False
    
    if "tokyo_texture_base_path" in target_content:
        print(f"✅ Propriété Texture Base Path détectée")
    else:
        print(f"❌ Propriété Texture Base Path manquante")
        return False
    
    target_size = os.path.getsize(init_target)
    print(f"📊 Taille installée: {target_size:,} bytes")
    
    # Compter les fichiers installés
    files_count = 0
    for root, dirs, files in os.walk(blender_target):
        files_count += len(files)
    
    print(f"📊 {files_count} fichiers installés")
    
    # Étape 6: Instructions Blender
    print(f"\n6️⃣ INSTRUCTIONS BLENDER")
    print("=" * 30)
    print("🚀 MAINTENANT DANS BLENDER:")
    print("1. 🔄 FERMEZ cette fenêtre de préférences")
    print("2. 🔄 ROUVREZ Edit > Preferences > Add-ons")
    print("3. 🔍 Cherchez 'Tokyo' dans la barre de recherche")
    print("4. ✅ Vous devriez voir 'Tokyo City Generator 1.4.0'")
    print("5. ✅ ACTIVEZ l'addon (cochez la case)")
    print("6. 💾 Sauvegardez les préférences")
    print("7. 📐 Vue 3D > N > Onglet Tokyo")
    
    print(f"\n✅ INSTALLATION FORCÉE TERMINÉE!")
    print(f"🎯 L'addon v1.4.0 est maintenant installé dans Blender")
    print(f"🔄 Actualisez la liste des add-ons pour le voir")
    
    return True

def create_blender_refresh_script():
    """Crée un script pour rafraîchir dans Blender"""
    
    refresh_script = '''# SCRIPT À EXÉCUTER DANS BLENDER
# Copiez dans Scripting workspace et exécutez

import bpy

print("🔄 REFRESH ADDON TOKYO v1.4.0")

# Rafraîchir la liste des addons
bpy.ops.preferences.addon_refresh()
print("✅ Liste des addons rafraîchie")

# Chercher Tokyo
addon_name = "tokyo_city_generator"
if addon_name in bpy.context.preferences.addons:
    print("🎉 TOKYO ADDON TROUVÉ!")
    addon = bpy.context.preferences.addons[addon_name]
    if hasattr(addon.module, 'bl_info'):
        info = addon.module.bl_info
        print(f"📋 Nom: {info.get('name')}")
        print(f"🔢 Version: {info.get('version')}")
else:
    print("❌ Tokyo addon non trouvé")
    print("🔧 Essayez d'activer manuellement:")
    try:
        bpy.ops.preferences.addon_enable(module=addon_name)
        print("✅ Activation forcée réussie!")
    except Exception as e:
        print(f"❌ Échec activation: {e}")

print("📐 Allez dans Vue 3D > N > Tokyo pour utiliser l'addon")
'''
    
    script_path = r"c:\Users\sshom\source\repos\Satsuki\Satsuki-Tools\CityGenerator_Blender\city_block_generator_6_12\TOKYO_ADDON_1_0\refresh_addon_blender.py"
    
    with open(script_path, 'w', encoding='utf-8') as f:
        f.write(refresh_script)
    
    print(f"📝 Script Blender créé: {script_path}")
    return script_path

if __name__ == "__main__":
    try:
        # Force installation
        success = force_install_tokyo_immediate()
        
        # Créer script de refresh pour Blender
        refresh_script = create_blender_refresh_script()
        
        if success:
            print(f"\n🎉 INSTALLATION FORCÉE RÉUSSIE!")
            print(f"📋 PROCHAINES ÉTAPES:")
            print(f"1. 🔄 Dans Blender: Fermez/Rouvrez Edit > Preferences > Add-ons")
            print(f"2. 🔍 Cherchez 'Tokyo' dans la recherche")
            print(f"3. ✅ Activez 'Tokyo City Generator 1.4.0'")
            print(f"4. 📐 Vue 3D > N > Onglet Tokyo")
            print(f"\n📝 OU utilisez le script: {refresh_script}")
        else:
            print(f"\n❌ INSTALLATION ÉCHOUÉE")
            print(f"🔧 Vérifiez que Blender est fermé")
            print(f"🔧 Relancez avec droits administrateur si nécessaire")
            
    except Exception as e:
        print(f"❌ Erreur critique: {e}")
        import traceback
        traceback.print_exc()

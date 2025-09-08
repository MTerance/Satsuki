# FORCE RELOAD TOKYO v1.3.0
# Script pour forcer l'installation de la nouvelle version dans Blender

import os
import shutil
import time

def force_reload_tokyo_v1_3_0():
    """Force le rechargement de Tokyo City Generator v1.3.0"""
    
    print("🔄 FORCE RELOAD TOKYO CITY GENERATOR v1.3.0")
    print("=" * 55)
    
    # Chemins importants
    blender_addons = r"C:\Users\sshom\AppData\Roaming\Blender Foundation\Blender\4.0\scripts\addons"
    tokyo_folder = os.path.join(blender_addons, "tokyo_city_generator")
    source_folder = r"c:\Users\sshom\Documents\assets\Tools\tokyo_city_generator_1_3_0"
    
    print(f"📁 Dossier Blender: {blender_addons}")
    print(f"🎯 Addon Tokyo: {tokyo_folder}")
    print(f"📦 Source v1.3.0: {source_folder}")
    
    # Étape 1: Supprimer complètement l'ancienne version
    print(f"\n🗑️ Suppression complète de l'ancienne version...")
    
    if os.path.exists(tokyo_folder):
        try:
            # Forcer la suppression même si des fichiers sont verrouillés
            shutil.rmtree(tokyo_folder, ignore_errors=True)
            time.sleep(1)  # Attendre un peu
            
            # Vérifier si vraiment supprimé
            if os.path.exists(tokyo_folder):
                print("  ⚠️ Dossier encore présent, suppression forcée...")
                # Essayer de supprimer fichier par fichier
                for root, dirs, files in os.walk(tokyo_folder, topdown=False):
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
                    os.rmdir(tokyo_folder)
                except:
                    pass
            
            if not os.path.exists(tokyo_folder):
                print("  ✅ Ancienne version supprimée avec succès")
            else:
                print("  ❌ Impossible de supprimer complètement l'ancienne version")
                print("  🔧 Fermez Blender et relancez ce script")
                return False
                
        except Exception as e:
            print(f"  ❌ Erreur lors de la suppression: {e}")
            print("  🔧 Fermez Blender et relancez ce script")
            return False
    else:
        print("  ✅ Aucune ancienne version trouvée")
    
    # Étape 2: Vérifier que la source v1.3.0 existe
    print(f"\n📋 Vérification de la source v1.3.0...")
    
    if not os.path.exists(source_folder):
        print(f"  ❌ Dossier source non trouvé: {source_folder}")
        print("  🔧 Relancez le déploiement avec deploy_tokyo_v1_3_0.py")
        return False
    
    # Vérifier le fichier principal
    init_file = os.path.join(source_folder, "__init__.py")
    if os.path.exists(init_file):
        with open(init_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        if '"version": (1, 3, 0)' in content:
            print("  ✅ Source v1.3.0 confirmée")
        else:
            print("  ❌ Source n'est pas v1.3.0")
            return False
    else:
        print("  ❌ Fichier __init__.py manquant dans la source")
        return False
    
    # Étape 3: Copier la nouvelle version
    print(f"\n📦 Installation de la version 1.3.0...")
    
    try:
        shutil.copytree(source_folder, tokyo_folder)
        print("  ✅ Fichiers copiés avec succès")
    except Exception as e:
        print(f"  ❌ Erreur lors de la copie: {e}")
        return False
    
    # Étape 4: Vérifier l'installation
    print(f"\n🔍 Vérification de l'installation...")
    
    if os.path.exists(tokyo_folder):
        print("  ✅ Dossier addon créé")
        
        # Vérifier le fichier principal
        new_init = os.path.join(tokyo_folder, "__init__.py")
        if os.path.exists(new_init):
            with open(new_init, 'r', encoding='utf-8') as f:
                content = f.read()
            
            if '"version": (1, 3, 0)' in content:
                print("  ✅ Version 1.3.0 installée")
            else:
                print("  ❌ Version incorrecte installée")
                return False
            
            if "TEXTURE SYSTEM" in content:
                print("  ✅ Système de textures détecté")
            else:
                print("  ❌ Système de textures non détecté")
                return False
        else:
            print("  ❌ Fichier __init__.py manquant")
            return False
        
        # Compter les fichiers
        files = []
        for root, dirs, filenames in os.walk(tokyo_folder):
            for filename in filenames:
                files.append(filename)
        
        print(f"  📊 {len(files)} fichiers installés")
        
        if len(files) >= 8:  # Au minimum 8 fichiers essentiels
            print("  ✅ Installation complète")
        else:
            print("  ⚠️ Installation incomplète")
            return False
    else:
        print("  ❌ Dossier addon non créé")
        return False
    
    # Étape 5: Instructions pour Blender
    print(f"\n🎮 INSTRUCTIONS POUR BLENDER:")
    print("=" * 55)
    print("1. 🔄 FERMEZ Blender complètement")
    print("2. 🚀 REDÉMARREZ Blender")
    print("3. ⚙️ Edit > Preferences > Add-ons")
    print("4. 🔍 Cherchez 'Tokyo City Generator'")
    print("5. ❌ DÉSACTIVEZ l'ancien addon (si présent)")
    print("6. 🗑️ SUPPRIMEZ l'ancien addon (bouton Remove)")
    print("7. 🔄 ACTUALISEZ la liste (bouton Refresh)")
    print("8. ✅ ACTIVEZ le nouveau 'Tokyo City Generator 1.3.0 TEXTURE SYSTEM'")
    print("9. 🎯 Vérifiez dans l'onglet 'Tokyo' (sidebar N)")
    print("10. 🎨 L'option 'Advanced Textures' doit être disponible!")
    
    print(f"\n✅ FORCE RELOAD TERMINÉ!")
    print("🚀 La version 1.3.0 est maintenant installée")
    return True

def check_blender_process():
    """Vérifie si Blender est en cours d'exécution"""
    import subprocess
    try:
        # Vérifier les processus Windows
        result = subprocess.run(['tasklist'], capture_output=True, text=True)
        if 'blender.exe' in result.stdout.lower():
            print("⚠️ ATTENTION: Blender semble être en cours d'exécution")
            print("🔧 Fermez Blender avant de continuer pour éviter les conflits")
            return True
        else:
            print("✅ Blender n'est pas en cours d'exécution")
            return False
    except:
        print("⚠️ Impossible de vérifier les processus")
        return False

if __name__ == "__main__":
    try:
        # Vérifier si Blender est ouvert
        blender_running = check_blender_process()
        
        if blender_running:
            print("\n❌ Veuillez fermer Blender avant de continuer")
            input("Appuyez sur Entrée après avoir fermé Blender...")
        
        # Forcer le reload
        success = force_reload_tokyo_v1_3_0()
        
        if success:
            print("\n🎉 SUCCESS! Tokyo v1.3.0 installé avec force")
            print("🔄 Redémarrez Blender pour voir la nouvelle version")
        else:
            print("\n❌ ÉCHEC du force reload")
            print("🔧 Vérifiez les erreurs ci-dessus")
            
    except Exception as e:
        print(f"❌ Erreur inattendue: {e}")
        import traceback
        traceback.print_exc()

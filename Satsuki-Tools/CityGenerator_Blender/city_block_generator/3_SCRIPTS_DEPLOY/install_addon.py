import os
import shutil
import sys

def deploy_addon():
    """Déploie l'addon dans le dossier correct de Blender"""
    
    # Chemins source et destination
    source_dir = r"c:\Users\sshom\source\repos\Satsuki\Satsuki-Tools\CityGenerator_Blender\city_block_generator"
    
    # Dossier addons de Blender (version 4.0+)
    blender_addons_dir = os.path.expanduser(r"~\AppData\Roaming\Blender Foundation\Blender\4.0\scripts\addons")
    
    # Nom du dossier de destination
    addon_dest_dir = os.path.join(blender_addons_dir, "city_block_generator")
    
    print(f"🚀 Déploiement de l'addon City Block Generator")
    print(f"📁 Source: {source_dir}")
    print(f"📁 Destination: {addon_dest_dir}")
    
    try:
        # Créer le dossier addons s'il n'existe pas
        if not os.path.exists(blender_addons_dir):
            os.makedirs(blender_addons_dir)
            print(f"✅ Dossier addons créé: {blender_addons_dir}")
        
        # Supprimer l'ancien addon s'il existe
        if os.path.exists(addon_dest_dir):
            shutil.rmtree(addon_dest_dir)
            print(f"🗑️ Ancien addon supprimé")
        
        # Copier le nouveau addon
        shutil.copytree(source_dir, addon_dest_dir)
        print(f"✅ Addon copié avec succès!")
        
        # Lister les fichiers principaux copiés
        main_files = ["__init__.py", "operators.py", "ui.py", "generator.py"]
        for file in main_files:
            file_path = os.path.join(addon_dest_dir, file)
            if os.path.exists(file_path):
                print(f"   ✅ {file}")
            else:
                print(f"   ❌ {file} MANQUANT!")
        
        print(f"\n🎯 Maintenant dans Blender:")
        print(f"1. Fermez Blender complètement")
        print(f"2. Redémarrez Blender")
        print(f"3. Allez dans Edit > Preferences > Add-ons")
        print(f"4. Recherchez 'City Block Generator'")
        print(f"5. Activez l'addon")
        print(f"6. Appuyez sur N dans la vue 3D")
        print(f"7. Cherchez l'onglet 'CityGen'")
        
        return True
        
    except Exception as e:
        print(f"❌ Erreur lors du déploiement: {e}")
        return False

if __name__ == "__main__":
    deploy_addon()

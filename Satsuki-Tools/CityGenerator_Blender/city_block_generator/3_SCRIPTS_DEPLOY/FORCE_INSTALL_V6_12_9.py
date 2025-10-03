"""
INSTALLATION FORCÉE V6.12.9
Force la mise à jour de l'addon dans Blender
"""

import os
import shutil
import sys

def force_install_addon():
    """Force l'installation de l'addon mis à jour"""
    print("🔥 === INSTALLATION FORCÉE V6.12.9 ===")
    
    # Chemin source (notre code)
    source_path = r"c:\Users\sshom\source\repos\Satsuki\Satsuki-Tools\CityGenerator_Blender\city_block_generator"
    
    # Chemin destination (Blender addons)
    dest_path = r"C:\Users\sshom\AppData\Roaming\Blender Foundation\Blender\4.5\scripts\addons\city_block_generator"
    
    try:
        # 1. Supprimer l'ancien addon s'il existe
        if os.path.exists(dest_path):
            print(f"🗑️ Suppression ancien addon: {dest_path}")
            shutil.rmtree(dest_path)
            print("✅ Ancien addon supprimé")
        
        # 2. Copier le nouveau
        print(f"📂 Copie nouveau addon: {source_path} → {dest_path}")
        shutil.copytree(source_path, dest_path)
        print("✅ Nouveau addon copié")
        
        # 3. Vérifier les fichiers critiques
        critical_files = ["__init__.py", "generator.py", "operators.py", "ui.py"]
        for file in critical_files:
            file_path = os.path.join(dest_path, file)
            if os.path.exists(file_path):
                size = os.path.getsize(file_path)
                print(f"✅ {file}: {size} bytes")
            else:
                print(f"❌ MANQUANT: {file}")
        
        print("🎉 INSTALLATION FORCÉE TERMINÉE !")
        print("👉 REDÉMARREZ BLENDER pour prendre en compte les changements")
        print("👉 Ou désactivez/réactivez l'addon dans les préférences")
        
        return True
        
    except Exception as e:
        print(f"❌ Erreur installation: {e}")
        return False

if __name__ == "__main__":
    force_install_addon()

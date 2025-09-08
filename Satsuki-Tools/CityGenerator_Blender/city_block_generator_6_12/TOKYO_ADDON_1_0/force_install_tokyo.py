# FORCE INSTALLATION TOKYO ADDON v1.4.0

import os
import shutil
import time

def force_install_tokyo():
    """Force l'installation de Tokyo addon dans Blender"""
    
    print("🔧 FORCE INSTALLATION TOKYO v1.4.0")
    print("=" * 40)
    
    # Chemins
    source = r"c:\Users\sshom\Documents\assets\Tools\tokyo_city_generator_1_4_0"
    target = r"C:\Users\sshom\AppData\Roaming\Blender Foundation\Blender\4.0\scripts\addons\tokyo_city_generator"
    
    print(f"📁 Source: {source}")
    print(f"🎯 Target: {target}")
    
    # Vérifier source
    if not os.path.exists(source):
        print(f"❌ Source non trouvée: {source}")
        return False
    
    # Supprimer ancien
    if os.path.exists(target):
        print("🗑️ Suppression ancienne version...")
        shutil.rmtree(target, ignore_errors=True)
        time.sleep(1)
    
    # Créer dossier parent si nécessaire
    os.makedirs(os.path.dirname(target), exist_ok=True)
    
    # Copier
    print("📦 Copie nouvel addon...")
    shutil.copytree(source, target)
    
    # Vérifier
    init_file = os.path.join(target, "__init__.py")
    if os.path.exists(init_file):
        print("✅ Installation réussie!")
        print("🚀 Redémarrez Blender")
        return True
    else:
        print("❌ Installation échouée")
        return False

if __name__ == "__main__":
    force_install_tokyo()

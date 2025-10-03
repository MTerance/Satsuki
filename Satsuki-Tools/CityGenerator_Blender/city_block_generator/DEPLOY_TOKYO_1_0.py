"""
DÉPLOIEMENT TOKYO 1.0 
L'addon Tokyo simple et fonctionnel !
"""

import shutil
import os
import sys
from datetime import datetime

def deployer_tokyo_1_0():
    """Déploie TOKYO 1.0 - Simple et efficace"""
    
    print("🗾 === DÉPLOIEMENT TOKYO CITY GENERATOR 1.0 === 🗾")
    print(f"📅 {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("🎯 L'addon simple qui fait ce que vous voulez !")
    print("")
    
    # Chemins
    source_path = os.path.abspath("TOKYO_ADDON_1_0")
    target_path = r"C:\Users\sshom\Documents\assets\Tools\tokyo_city_generator_1_0"
    blender_path = r"C:\Users\sshom\AppData\Roaming\Blender Foundation\Blender\4.5\scripts\addons\tokyo_city_generator_1_0"
    
    print("🔍 === VÉRIFICATION TOKYO 1.0 ===")
    
    # Vérifier que le source existe
    if not os.path.exists(source_path):
        print(f"❌ Source introuvable: {source_path}")
        return False
    
    # Vérifier __init__.py
    init_file = os.path.join(source_path, "__init__.py")
    if os.path.exists(init_file):
        size = os.path.getsize(init_file)
        print(f"✅ Tokyo 1.0 addon: {size:,} bytes")
        
        # Vérifier contenu
        with open(init_file, 'r', encoding='utf-8') as f:
            content = f.read()
            if 'Tokyo City Generator 1.0' in content:
                print("✅ Version Tokyo 1.0 confirmée")
            if 'create_skyscraper' in content:
                print("✅ Gratte-ciels présents")
            if 'create_commercial_center' in content:
                print("✅ Centres commerciaux présents") 
            if 'create_residential_building' in content:
                print("✅ Bâtiments résidentiels présents")
            if 'create_organic_roads' in content:
                print("✅ Routes organiques présentes")
    else:
        print("❌ __init__.py manquant!")
        return False
    
    print("")
    print("🚀 === DÉPLOIEMENT DOUBLE ===")
    
    # === DÉPLOIEMENT 1: Assets ===
    print("📁 1. Déploiement vers Assets...")
    if os.path.exists(target_path):
        shutil.rmtree(target_path, ignore_errors=True)
        print("🗑️ Ancien dossier supprimé")
    
    os.makedirs(os.path.dirname(target_path), exist_ok=True)
    shutil.copytree(source_path, target_path)
    print(f"✅ Copié vers: {target_path}")
    
    # === DÉPLOIEMENT 2: Blender ===
    print("📁 2. Déploiement vers Blender...")
    if os.path.exists(blender_path):
        shutil.rmtree(blender_path, ignore_errors=True)
        print("🗑️ Ancien addon Blender supprimé")
    
    os.makedirs(os.path.dirname(blender_path), exist_ok=True)
    shutil.copytree(source_path, blender_path)
    print(f"✅ Copié vers: {blender_path}")
    
    # === VÉRIFICATION FINALE ===
    print("")
    print("🔍 === VÉRIFICATION FINALE ===")
    
    # Vérifier assets
    target_init = os.path.join(target_path, "__init__.py")
    if os.path.exists(target_init):
        size = os.path.getsize(target_init)
        print(f"✅ Assets OK: {size:,} bytes")
    else:
        print("❌ Assets ÉCHEC!")
        return False
    
    # Vérifier Blender
    blender_init = os.path.join(blender_path, "__init__.py")
    if os.path.exists(blender_init):
        size = os.path.getsize(blender_init)
        print(f"✅ Blender OK: {size:,} bytes")
    else:
        print("❌ Blender ÉCHEC!")
        return False
    
    print("")
    print("🎉 === TOKYO 1.0 DÉPLOYÉ AVEC SUCCÈS === 🎉")
    print("")
    print("📊 CARACTÉRISTIQUES:")
    print("   🏢 3 types de zones: Business/Commercial/Résidentiel")
    print("   🗼 Gratte-ciels 15-40 étages (centre)")
    print("   🏬 Centres commerciaux 3-8 étages (périphérie)")
    print("   🏠 Maisons 1-5 étages (extérieur)")
    print("   🛣️ Routes organiques courbes")
    print("   🎨 Matériaux différents par zone")
    print("")
    print("🔄 === INSTRUCTIONS BLENDER ===")
    print("OPTION A - Auto (recommandé):")
    print("   1. 🔄 REDÉMARRER Blender")
    print("   2. 🎯 L'addon Tokyo 1.0 sera disponible!")
    print("   3. 📍 Onglet 'Tokyo' dans la sidebar (N)")
    print("")
    print("OPTION B - Installation manuelle:")
    print("   1. 🔄 REDÉMARRER Blender")
    print("   2. 🔧 Edit > Preferences > Add-ons")
    print("   3. ➕ Install > Sélectionner:")
    print(f"      📁 {blender_path}")
    print("   4. ✅ Activer 'Tokyo City Generator 1.0'")
    print("")
    print("🧪 === UTILISATION ===")
    print("   1. 📍 Sidebar > Onglet 'Tokyo'")
    print("   2. 🎛️ District Size: 3 (pour commencer)")
    print("   3. 🌊 Organic Streets: 0.3 (courbes modérées)")
    print("   4. 🚀 Cliquer 'Generate Tokyo District'")
    print("")
    print("✨ ENFIN UN ADDON QUI FAIT CE QUE VOUS VOULEZ ! ✨")
    
    return True

def main():
    """Fonction principale"""
    try:
        success = deployer_tokyo_1_0()
        
        if success:
            print("")
            print("🔥✅ DÉPLOIEMENT TOKYO 1.0 RÉUSSI !")
            print("🗾 Addon simple, efficace et fonctionnel")
            print("🎯 Fini les 7000 lignes qui ne marchent pas !")
        else:
            print("")
            print("❌ DÉPLOIEMENT TOKYO 1.0 ÉCHOUÉ !")
            
        input("\nAppuyez sur Entrée pour fermer...")
        return success
        
    except Exception as e:
        print(f"💥 ERREUR: {e}")
        input("\nAppuyez sur Entrée pour fermer...")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)

import os
import shutil

def clean_all_blender_versions():
    print("NETTOYAGE COMPLET DE TOUTES LES VERSIONS BLENDER")
    print("=" * 50)
    
    base_path = os.path.expanduser("~\\AppData\\Roaming\\Blender Foundation\\Blender")
    versions = ["4.5", "4.0", "3.0", "2.93", "2.92", "2.90", "2.80"]
    
    total_cleaned = 0
    
    for version in versions:
        addon_path = os.path.join(base_path, version, "scripts", "addons")
        
        if os.path.exists(addon_path):
            print(f"\n📁 Nettoyage Blender {version}: {addon_path}")
            
            items = os.listdir(addon_path)
            tokyo_items = [item for item in items if any(keyword in item.lower() for keyword in ['tokyo', 'city', 'extended'])]
            
            if tokyo_items:
                print(f"   Trouvé {len(tokyo_items)} éléments:")
                for item in tokyo_items:
                    print(f"     - {item}")
                    
                    item_path = os.path.join(addon_path, item)
                    try:
                        if os.path.isdir(item_path):
                            shutil.rmtree(item_path)
                            print(f"     ✅ SUPPRIMÉ: {item}")
                            total_cleaned += 1
                        elif os.path.isfile(item_path):
                            os.remove(item_path)
                            print(f"     ✅ SUPPRIMÉ: {item}")
                            total_cleaned += 1
                    except Exception as e:
                        print(f"     ❌ Erreur: {e}")
            else:
                print("   ✅ Aucun addon Tokyo trouvé")
        else:
            print(f"   ⚠️ Blender {version} - Répertoire addons non trouvé")
    
    print(f"\n🎯 NETTOYAGE TERMINÉ!")
    print(f"Total d'éléments supprimés: {total_cleaned}")
    print("\n📋 PROCHAINES ÉTAPES:")
    print("1. Fermez Blender complètement")
    print("2. Rouvrez Blender")
    print("3. Edit > Preferences > Add-ons")
    print("4. Install > tokyo_v2_2_0_EXTENDED.zip")
    print("5. Activez 'Tokyo City Generator v2.2.0 Extended'")

if __name__ == "__main__":
    clean_all_blender_versions()
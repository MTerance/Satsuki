import os
import shutil
import glob

def main():
    print("NETTOYAGE MANUEL TOKYO ADDONS")
    print("=" * 40)
    
    # Répertoire principal des addons Blender
    addon_path = os.path.expanduser("~\\AppData\\Roaming\\Blender Foundation\\Blender\\4.0\\scripts\\addons")
    
    print(f"Répertoire: {addon_path}")
    
    if not os.path.exists(addon_path):
        print("❌ Répertoire non trouvé!")
        return
    
    # Lister tout ce qui contient "tokyo" ou "TOKYO"
    items = os.listdir(addon_path)
    tokyo_items = [item for item in items if 'tokyo' in item.lower() or 'TOKYO' in item]
    
    print(f"\nTrouvé {len(tokyo_items)} éléments Tokyo:")
    for item in tokyo_items:
        print(f"  - {item}")
    
    # Supprimer tous les éléments Tokyo
    for item in tokyo_items:
        item_path = os.path.join(addon_path, item)
        try:
            if os.path.isdir(item_path):
                shutil.rmtree(item_path)
                print(f"✅ SUPPRIMÉ: {item}")
            elif os.path.isfile(item_path):
                os.remove(item_path)
                print(f"✅ SUPPRIMÉ: {item}")
        except Exception as e:
            print(f"❌ Erreur suppression {item}: {e}")
    
    print("\n🎯 Nettoyage terminé!")
    print("Maintenant installez manuellement tokyo_v2_2_0_EXTENDED.zip")

if __name__ == "__main__":
    main()
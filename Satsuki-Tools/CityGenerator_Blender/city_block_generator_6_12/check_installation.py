import os

def check_addon_installation():
    """Vérifie que l'addon est correctement installé"""
    
    print("🔍 DIAGNOSTIC D'INSTALLATION - City Block Generator")
    print("=" * 60)
    
    # Dossier addons de Blender
    blender_addons_dir = os.path.expanduser(r"~\AppData\Roaming\Blender Foundation\Blender\4.0\scripts\addons")
    addon_dir = os.path.join(blender_addons_dir, "city_block_generator_6_12")
    
    print(f"📁 Dossier addons Blender: {blender_addons_dir}")
    print(f"📁 Dossier addon: {addon_dir}")
    print()
    
    # Vérifier l'existence du dossier
    if not os.path.exists(addon_dir):
        print("❌ PROBLÈME: Dossier addon introuvable!")
        print("   Lancez d'abord: python install_addon.py")
        return False
    
    print("✅ Dossier addon trouvé")
    
    # Vérifier les fichiers essentiels
    essential_files = {
        "__init__.py": "Fichier principal d'enregistrement",
        "operators.py": "Opérateurs (boutons d'action)",
        "ui.py": "Interface utilisateur", 
        "generator.py": "Générateur de ville"
    }
    
    print("\n📋 VÉRIFICATION DES FICHIERS:")
    all_files_ok = True
    
    for filename, description in essential_files.items():
        filepath = os.path.join(addon_dir, filename)
        if os.path.exists(filepath):
            size = os.path.getsize(filepath)
            print(f"   ✅ {filename:<15} ({size:,} bytes) - {description}")
        else:
            print(f"   ❌ {filename:<15} MANQUANT! - {description}")
            all_files_ok = False
    
    # Vérifier le contenu de __init__.py
    init_file = os.path.join(addon_dir, "__init__.py")
    if os.path.exists(init_file):
        with open(init_file, 'r', encoding='utf-8') as f:
            content = f.read()
            if 'bl_info' in content:
                print(f"   ✅ bl_info trouvé dans __init__.py")
            else:
                print(f"   ❌ bl_info manquant dans __init__.py")
                all_files_ok = False
            
            if '"name": "City Block Generator"' in content:
                print(f"   ✅ Nom d'addon correct")
            else:
                print(f"   ❌ Nom d'addon incorrect")
                all_files_ok = False
    
    print("\n🎯 INSTRUCTIONS POUR BLENDER:")
    if all_files_ok:
        print("✅ Installation OK! Maintenant dans Blender:")
        print("   1. Fermez Blender COMPLÈTEMENT")
        print("   2. Redémarrez Blender")
        print("   3. Edit > Preferences > Add-ons")
        print("   4. Recherchez 'City Block Generator'")
        print("   5. Cochez la case pour l'activer")
        print("   6. Vue 3D > Appuyez sur N > Onglet 'CityGen'")
        print("\n🛣️ TESTEZ LE SYSTÈME RÉVOLUTIONNAIRE 'ROUTES D'ABORD'!")
    else:
        print("❌ Problèmes détectés! Relancez: python install_addon.py")
    
    return all_files_ok

if __name__ == "__main__":
    check_addon_installation()

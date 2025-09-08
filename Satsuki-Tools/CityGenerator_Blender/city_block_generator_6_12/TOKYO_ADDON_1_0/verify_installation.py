# VÉRIFICATION INSTALLATION TOKYO v1.3.0
# Script pour vérifier que l'addon est correctement installé dans Blender

import os

def verify_tokyo_installation():
    """Vérifie l'installation de Tokyo City Generator v1.3.0"""
    
    print("🔍 VÉRIFICATION INSTALLATION TOKYO v1.3.0")
    print("=" * 50)
    
    # Chemin d'installation Blender
    blender_addon_path = r"C:\Users\sshom\AppData\Roaming\Blender Foundation\Blender\4.0\scripts\addons\tokyo_city_generator"
    
    # Vérifier le dossier principal
    if os.path.exists(blender_addon_path):
        print(f"✅ Dossier addon trouvé: {blender_addon_path}")
    else:
        print(f"❌ Dossier addon introuvable: {blender_addon_path}")
        return False
    
    # Fichiers essentiels à vérifier
    essential_files = {
        "__init__.py": "Fichier principal de l'addon",
        "texture_system.py": "Système de textures intelligent",
        "setup_textures.py": "Configuration des dossiers",
        "test_texture_system.py": "Tests du système",
        "TEXTURE_SYSTEM_GUIDE.md": "Guide d'utilisation",
        "VERSION.txt": "Informations de version",
        "INSTALLATION_RAPIDE.md": "Guide d'installation",
        "CHANGELOG.md": "Liste des changements"
    }
    
    print("\n📋 Vérification des fichiers:")
    missing_files = 0
    total_size = 0
    
    for filename, description in essential_files.items():
        file_path = os.path.join(blender_addon_path, filename)
        if os.path.exists(file_path):
            file_size = os.path.getsize(file_path)
            total_size += file_size
            print(f"  ✅ {filename} ({file_size:,} bytes) - {description}")
        else:
            print(f"  ❌ {filename} MANQUANT - {description}")
            missing_files += 1
    
    # Vérifier le contenu du fichier principal
    init_file = os.path.join(blender_addon_path, "__init__.py")
    if os.path.exists(init_file):
        print("\n🔍 Vérification du fichier principal:")
        with open(init_file, 'r', encoding='utf-8') as f:
            content = f.read()
            
        # Vérifier la version
        if '"version": (1, 3, 0)' in content:
            print("  ✅ Version 1.3.0 confirmée")
        else:
            print("  ❌ Version incorrecte dans __init__.py")
            missing_files += 1
            
        # Vérifier le nom
        if "Tokyo City Generator 1.3.0 TEXTURE SYSTEM" in content:
            print("  ✅ Nom d'addon correct")
        else:
            print("  ❌ Nom d'addon incorrect")
            missing_files += 1
            
        # Vérifier l'import du système de textures
        if "from .texture_system import tokyo_texture_system" in content:
            print("  ✅ Import du système de textures détecté")
        else:
            print("  ⚠️ Import du système de textures non trouvé")
            
        # Vérifier la nouvelle propriété
        if "tokyo_use_advanced_textures" in content:
            print("  ✅ Propriété 'Advanced Textures' détectée")
        else:
            print("  ❌ Propriété 'Advanced Textures' manquante")
            missing_files += 1
    
    # Vérifier la structure des dossiers de textures
    texture_base = "C:/Users/sshom/Documents/Assets/Textures/Tokyo_Buildings/"
    print(f"\n🗂️ Vérification structure textures: {texture_base}")
    
    if os.path.exists(texture_base):
        print("  ✅ Dossier de base des textures trouvé")
        
        # Compter les sous-dossiers
        categories = ["skyscrapers", "commercial", "midrise", "residential", "lowrise"]
        total_folders = 0
        
        for category in categories:
            category_path = os.path.join(texture_base, category)
            if os.path.exists(category_path):
                subfolders = [d for d in os.listdir(category_path) 
                            if os.path.isdir(os.path.join(category_path, d))]
                total_folders += len(subfolders)
                print(f"    ✅ {category}: {len(subfolders)} sous-dossiers")
            else:
                print(f"    ❌ {category}: dossier manquant")
        
        print(f"  📊 Total: {total_folders}/20 dossiers de textures")
        
        # Vérifier le guide principal
        guide_path = os.path.join(texture_base, "TOKYO_TEXTURE_GUIDE.md")
        if os.path.exists(guide_path):
            print("  ✅ Guide des textures présent")
        else:
            print("  ⚠️ Guide des textures manquant")
            
    else:
        print("  ⚠️ Dossier de textures non créé (exécuter setup_textures.py)")
    
    # Résumé final
    print("\n" + "=" * 50)
    print("📊 RÉSUMÉ DE LA VÉRIFICATION")
    print("=" * 50)
    
    if missing_files == 0:
        print("🎉 INSTALLATION PARFAITE!")
        print("✅ Tous les fichiers sont présents")
        print(f"💾 Taille totale: {total_size:,} bytes")
        print("🚀 L'addon est prêt à être utilisé dans Blender")
        
        print("\n🎮 PROCHAINES ÉTAPES:")
        print("1. Redémarrer Blender")
        print("2. Aller dans Edit > Preferences > Add-ons")
        print("3. Chercher 'Tokyo City Generator 1.3.0'")
        print("4. Activer l'addon")
        print("5. Aller dans l'onglet 'Tokyo' (sidebar N)")
        print("6. Cocher 'Advanced Textures'")
        print("7. Générer votre ville avec textures intelligentes!")
        
        return True
    else:
        print(f"⚠️ PROBLÈMES DÉTECTÉS: {missing_files}")
        print("🔧 Veuillez relancer le déploiement")
        return False

if __name__ == "__main__":
    try:
        success = verify_tokyo_installation()
        if success:
            print("\n✨ Vérification terminée avec succès!")
        else:
            print("\n❌ Vérification échouée - Problèmes détectés")
    except Exception as e:
        print(f"❌ Erreur lors de la vérification: {e}")
        import traceback
        traceback.print_exc()

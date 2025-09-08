# DIAGNOSTIC - ADDON TOKYO INVISIBLE DANS BLENDER

import os
import subprocess

def diagnostic_addon_invisible():
    """Diagnostic complet pour addon Tokyo invisible"""
    
    print("🔍 DIAGNOSTIC ADDON TOKYO INVISIBLE")
    print("=" * 50)
    
    # 1. Vérifier si Blender est ouvert
    print("1️⃣ VÉRIFICATION PROCESSUS BLENDER")
    print("-" * 30)
    
    try:
        result = subprocess.run(['tasklist'], capture_output=True, text=True, shell=True)
        if 'blender.exe' in result.stdout.lower():
            print("⚠️ BLENDER EST OUVERT")
            print("🔧 SOLUTION: Fermez Blender complètement et relancez")
            print("📝 Les addons ne se rechargent pas toujours avec Blender ouvert")
        else:
            print("✅ Blender fermé (bon pour installation)")
    except:
        print("⚠️ Impossible de vérifier les processus")
    
    # 2. Vérifier l'installation dans Blender
    print(f"\n2️⃣ VÉRIFICATION INSTALLATION BLENDER")
    print("-" * 30)
    
    blender_paths = [
        r"C:\Users\sshom\AppData\Roaming\Blender Foundation\Blender\4.0\scripts\addons\tokyo_city_generator",
        r"C:\Users\sshom\AppData\Roaming\Blender Foundation\Blender\4.1\scripts\addons\tokyo_city_generator",
        r"C:\Users\sshom\AppData\Roaming\Blender Foundation\Blender\4.2\scripts\addons\tokyo_city_generator"
    ]
    
    addon_found = False
    for path in blender_paths:
        if os.path.exists(path):
            print(f"✅ ADDON TROUVÉ: {path}")
            addon_found = True
            
            # Vérifier les fichiers
            init_file = os.path.join(path, "__init__.py")
            if os.path.exists(init_file):
                with open(init_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # Extraire version
                if '"version":' in content:
                    import re
                    version_match = re.search(r'"version":\s*\(([^)]+)\)', content)
                    if version_match:
                        version = version_match.group(1)
                        print(f"📋 Version détectée: ({version})")
                
                # Vérifier nom
                if '"name":' in content:
                    name_match = re.search(r'"name":\s*"([^"]+)"', content)
                    if name_match:
                        name = name_match.group(1)
                        print(f"🏷️ Nom: {name}")
                
                print(f"📊 Taille fichier: {os.path.getsize(init_file):,} bytes")
            else:
                print(f"❌ Fichier __init__.py manquant")
        else:
            print(f"❌ Pas trouvé: {path}")
    
    if not addon_found:
        print("❌ AUCUN ADDON TOKYO TROUVÉ DANS BLENDER!")
        print("🔧 SOLUTION: Réinstallation requise")
    
    # 3. Vérifier les versions disponibles
    print(f"\n3️⃣ VERSIONS DISPONIBLES")
    print("-" * 30)
    
    versions_paths = [
        r"c:\Users\sshom\Documents\assets\Tools\tokyo_city_generator_1_3_0",
        r"c:\Users\sshom\Documents\assets\Tools\tokyo_city_generator_1_4_0"
    ]
    
    for version_path in versions_paths:
        if os.path.exists(version_path):
            init_file = os.path.join(version_path, "__init__.py")
            if os.path.exists(init_file):
                size = os.path.getsize(init_file)
                print(f"✅ {os.path.basename(version_path)} - {size:,} bytes")
            else:
                print(f"⚠️ {os.path.basename(version_path)} - __init__.py manquant")
        else:
            print(f"❌ {os.path.basename(version_path)} - dossier manquant")
    
    # 4. Vérifier la version Blender
    print(f"\n4️⃣ VERSIONS BLENDER INSTALLÉES")
    print("-" * 30)
    
    blender_base = r"C:\Users\sshom\AppData\Roaming\Blender Foundation\Blender"
    if os.path.exists(blender_base):
        blender_versions = [d for d in os.listdir(blender_base) if os.path.isdir(os.path.join(blender_base, d))]
        for version in sorted(blender_versions):
            version_path = os.path.join(blender_base, version)
            addons_path = os.path.join(version_path, "scripts", "addons")
            if os.path.exists(addons_path):
                addons_count = len([d for d in os.listdir(addons_path) if os.path.isdir(os.path.join(addons_path, d))])
                print(f"📁 Blender {version} - {addons_count} addons installés")
            else:
                print(f"📁 Blender {version} - pas de dossier addons")
    else:
        print("❌ Dossier Blender Foundation non trouvé")
    
    print(f"\n🎯 SOLUTIONS RECOMMANDÉES:")
    print("=" * 50)
    
    if addon_found:
        print("✅ 1. REDÉMARRAGE BLENDER")
        print("   - Fermez Blender complètement")
        print("   - Redémarrez Blender")
        print("   - Edit > Preferences > Add-ons")
        print("   - Cherchez 'Tokyo'")
        print("   - Si trouvé mais pas visible: cochez la case")
        print()
        print("✅ 2. FORCE REFRESH")
        print("   - Dans Blender: Window > Toggle System Console")
        print("   - Copiez ce code dans la console Python:")
        print("   import bpy")
        print("   bpy.ops.preferences.addon_refresh()")
        print("   bpy.ops.preferences.addon_enable(module='tokyo_city_generator')")
    else:
        print("🔧 1. RÉINSTALLATION MANUELLE")
        print("   - Téléchargez le fichier ZIP de l'addon")
        print("   - Blender > Edit > Preferences > Add-ons")
        print("   - Install from Disk")
        print("   - Sélectionnez le ZIP ou le dossier")
        print()
        print("🔧 2. FORCE INSTALLATION")
        print("   - Utilisez le script force_install.py")
        print("   - Ou copiez manuellement le dossier")
    
    return addon_found

def create_force_install_script():
    """Crée un script de force installation"""
    
    script_content = '''# FORCE INSTALLATION TOKYO ADDON v1.4.0

import os
import shutil
import time

def force_install_tokyo():
    """Force l'installation de Tokyo addon dans Blender"""
    
    print("🔧 FORCE INSTALLATION TOKYO v1.4.0")
    print("=" * 40)
    
    # Chemins
    source = r"c:\\Users\\sshom\\Documents\\assets\\Tools\\tokyo_city_generator_1_4_0"
    target = r"C:\\Users\\sshom\\AppData\\Roaming\\Blender Foundation\\Blender\\4.0\\scripts\\addons\\tokyo_city_generator"
    
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
'''
    
    script_path = r"c:\Users\sshom\source\repos\Satsuki\Satsuki-Tools\CityGenerator_Blender\city_block_generator_6_12\TOKYO_ADDON_1_0\force_install_tokyo.py"
    
    with open(script_path, 'w', encoding='utf-8') as f:
        f.write(script_content)
    
    print(f"📝 Script de force installation créé: {script_path}")
    return script_path

if __name__ == "__main__":
    # Diagnostic
    addon_found = diagnostic_addon_invisible()
    
    # Créer script de secours
    force_script = create_force_install_script()
    
    print(f"\n📋 RÉSUMÉ:")
    if addon_found:
        print("✅ Addon détecté - Problème d'affichage")
        print("🔧 Solution: Redémarrage Blender + Force Refresh")
    else:
        print("❌ Addon non détecté - Problème d'installation")
        print("🔧 Solution: Force installation")
        print(f"▶️ Exécutez: python {force_script}")

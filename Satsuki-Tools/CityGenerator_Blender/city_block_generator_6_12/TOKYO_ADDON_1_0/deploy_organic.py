"""
🌊 TOKYO 1.1.0 ORGANIC - Script de déploiement
Déploie la version organique avec options Voronoï et routes courbes
"""

import os
import shutil
import sys
from datetime import datetime

def deploy_organic_tokyo():
    """Déploie la version organique Tokyo 1.1.0"""
    
    print("🌊" * 20)
    print("DÉPLOIEMENT TOKYO 1.1.0 ORGANIC")
    print("Options A (Voronoï) + B (Routes courbes)")
    print("🌊" * 20)
    
    # === CHEMINS ===
    current_dir = os.path.dirname(os.path.abspath(__file__))
    source_file = os.path.join(current_dir, "__init__organic.py")
    target_dir = r"c:\Users\sshom\Documents\assets\Tools\tokyo_organic_1_1_0"
    target_file = os.path.join(target_dir, "__init__.py")
    
    print(f"📂 Source: {source_file}")
    print(f"📁 Destination: {target_dir}")
    
    # === VÉRIFICATIONS ===
    if not os.path.exists(source_file):
        print(f"❌ ERREUR: Fichier source non trouvé: {source_file}")
        return False
    
    # Vérifier la taille du fichier
    file_size = os.path.getsize(source_file)
    file_size_kb = file_size / 1024
    
    print(f"📊 Taille du fichier: {file_size_kb:.1f} KB")
    
    if file_size < 1000:  # Moins de 1KB = probablement vide
        print("❌ ERREUR: Fichier trop petit, probablement corrompu")
        return False
    
    # === CRÉATION DU DOSSIER ===
    try:
        os.makedirs(target_dir, exist_ok=True)
        print(f"✅ Dossier créé: {target_dir}")
    except Exception as e:
        print(f"❌ ERREUR création dossier: {e}")
        return False
    
    # === SAUVEGARDE ANCIENNE VERSION ===
    if os.path.exists(target_file):
        backup_file = os.path.join(target_dir, f"__init___backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.py")
        try:
            shutil.copy2(target_file, backup_file)
            print(f"💾 Backup créé: {backup_file}")
        except Exception as e:
            print(f"⚠️ Erreur backup: {e}")
    
    # === COPIE NOUVELLE VERSION ===
    try:
        shutil.copy2(source_file, target_file)
        print(f"✅ Fichier copié: {target_file}")
    except Exception as e:
        print(f"❌ ERREUR copie: {e}")
        return False
    
    # === VÉRIFICATION POST-COPIE ===
    if os.path.exists(target_file):
        copied_size = os.path.getsize(target_file)
        if copied_size == file_size:
            print(f"✅ Copie vérifiée: {copied_size} bytes")
        else:
            print(f"❌ ERREUR: Tailles différentes {file_size} vs {copied_size}")
            return False
    else:
        print("❌ ERREUR: Fichier de destination non créé")
        return False
    
    # === COPIE DU SCRIPT DE TEST ===
    test_source = os.path.join(current_dir, "test_organic.py")
    test_target = os.path.join(target_dir, "test_organic.py")
    
    if os.path.exists(test_source):
        try:
            shutil.copy2(test_source, test_target)
            print(f"✅ Script de test copié: {test_target}")
        except Exception as e:
            print(f"⚠️ Erreur copie test: {e}")
    
    # === CRÉATION DU README ===
    readme_content = f"""# TOKYO 1.1.0 ORGANIC - City Generator

## 🌊 NOUVELLES FONCTIONNALITÉS ORGANIQUES

### Option A: Génération Voronoï
- Blocs irréguliers organiques
- Cellules Voronoï au lieu de grille
- Distribution naturelle des zones

### Option B: Routes courbes
- Rues organiques courbes
- Connexions naturelles entre cellules
- Intensité de courbure ajustable

## 🚀 INSTALLATION

1. **Dans Blender:**
   - Edit > Preferences > Add-ons
   - Install from File...
   - Sélectionner: `{target_file}`
   - Activer l'addon "Tokyo City Generator 1.1.0 ORGANIC"

2. **Utilisation:**
   - Panneau: View3D > Sidebar (N) > Tokyo Tab
   - Cocher "🌊 Utiliser Voronoï" pour mode organique
   - Cocher "🛤️ Routes courbes" pour rues organiques

## ⚙️ PARAMÈTRES ORGANIQUES

### Voronoï
- **Utiliser Voronoï**: Active la génération organique
- **Seed Voronoï**: Graine aléatoire (change la disposition)

### Routes courbes
- **Routes courbes**: Active les rues organiques
- **Intensité courbes**: Force de courbure (0.0 = droit, 1.0 = très courbe)

## 🔄 MODES DE GÉNÉRATION

### Mode Traditionnel (Voronoï OFF)
- Grille régulière classique
- Compatible avec toutes les options précédentes
- Variation organique ajustable

### Mode Organique (Voronoï ON)
- Cellules Voronoï irrégulières
- Routes droites OU courbes
- Distribution naturelle des zones

## 🧪 TESTS

Exécuter `test_organic.py` dans Blender pour vérifier:
- Installation correcte
- Fonctionnement des deux modes
- Génération Voronoï
- Routes courbes
- Performance benchmark

## 📊 VERSIONS

- **1.0.8**: Version stable traditionnelle
- **1.1.0**: Ajout options organiques Voronoï + routes courbes

## ⚡ PERFORMANCE

- Mode traditionnel: ~0.5-2s selon taille
- Mode organique: ~1-4s selon complexité
- Optimisé pour districts jusqu'à 10x10

## 🎯 OBJECTIFS ATTEINTS

✅ Option A: Génération Voronoï avec blocs irréguliers
✅ Option B: Routes courbes organiques  
✅ Interface utilisateur intuitive
✅ Compatibilité avec mode traditionnel
✅ Tests automatiques inclus

---
Généré le: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
Version: 1.1.0 ORGANIC
Taille: {file_size_kb:.1f} KB
"""
    
    readme_file = os.path.join(target_dir, "README.md")
    try:
        with open(readme_file, 'w', encoding='utf-8') as f:
            f.write(readme_content)
        print(f"✅ README créé: {readme_file}")
    except Exception as e:
        print(f"⚠️ Erreur README: {e}")
    
    # === INSTRUCTIONS D'INSTALLATION ===
    print("\n" + "="*50)
    print("🎉 DÉPLOIEMENT RÉUSSI!")
    print("="*50)
    print(f"📁 Dossier: {target_dir}")
    print(f"📄 Addon: {target_file}")
    print(f"📊 Taille: {file_size_kb:.1f} KB")
    
    print("\n🚀 INSTRUCTIONS D'INSTALLATION:")
    print("1. Ouvrez Blender")
    print("2. Edit > Preferences > Add-ons")
    print("3. Install from File...")
    print(f"4. Sélectionnez: {target_file}")
    print("5. Activez 'Tokyo City Generator 1.1.0 ORGANIC'")
    
    print("\n🌊 NOUVELLES FONCTIONNALITÉS:")
    print("✅ Option A: Blocs Voronoï organiques")
    print("✅ Option B: Routes courbes naturelles")
    print("✅ Interface: Cochez 'Utiliser Voronoï' + 'Routes courbes'")
    
    print("\n🧪 TEST:")
    print(f"Exécutez dans Blender: {test_target}")
    
    return True

def compare_versions():
    """Compare la nouvelle version avec l'ancienne"""
    
    print("\n📊 COMPARAISON DES VERSIONS:")
    
    current_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Ancienne version
    old_file = os.path.join(current_dir, "__init__.py")
    if os.path.exists(old_file):
        old_size = os.path.getsize(old_file) / 1024
        print(f"📄 Version 1.0.8 (traditionnelle): {old_size:.1f} KB")
    else:
        print("📄 Version 1.0.8: Non trouvée")
    
    # Nouvelle version
    new_file = os.path.join(current_dir, "__init__organic.py")
    if os.path.exists(new_file):
        new_size = os.path.getsize(new_file) / 1024
        print(f"🌊 Version 1.1.0 (organique): {new_size:.1f} KB")
        
        if os.path.exists(old_file):
            diff = new_size - old_size
            print(f"📈 Différence: +{diff:.1f} KB ({((new_size/old_size-1)*100):.1f}% d'augmentation)")
    else:
        print("🌊 Version 1.1.0: Non trouvée")
    
    print("\n🆕 NOUVELLES FONCTIONNALITÉS AJOUTÉES:")
    print("• generate_voronoi_cells() - Génération cellules Voronoï")
    print("• create_organic_blocks() - Blocs irréguliers")  
    print("• create_curved_street_network() - Routes courbes")
    print("• create_curved_path() - Chemins Bézier organiques")
    print("• Interface utilisateur étendue avec options organiques")
    print("• Propriétés: voronoi_seed, curve_intensity, use_voronoi, use_curved_streets")

if __name__ == "__main__":
    print("🌊 TOKYO 1.1.0 ORGANIC - DÉPLOIEMENT")
    
    # Comparaison des versions
    compare_versions()
    
    # Déploiement
    success = deploy_organic_tokyo()
    
    if success:
        print("\n🎊 DÉPLOIEMENT ORGANIQUE RÉUSSI!")
        print("🌊 Voronoï + 🛤️ Routes courbes disponibles!")
    else:
        print("\n❌ ÉCHEC DU DÉPLOIEMENT")
        sys.exit(1)

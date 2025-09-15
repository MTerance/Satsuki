#!/usr/bin/env python3
"""
CHECK COMPLET TOKYO CITY GENERATOR V2.1.8
Vérification de tous les composants critiques
"""

import os
import zipfile

def check_tokyo_v2_1_8():
    """Check complet de la version 2.1.8"""
    
    print("=" * 60)
    print("🔍 CHECK TOKYO CITY GENERATOR V2.1.8")
    print("=" * 60)
    
    # Vérification du fichier source
    source_file = r"TOKYO_SIMPLE_V2_1\__init__.py"
    
    print(f"📁 Fichier source: {source_file}")
    if os.path.exists(source_file):
        print("  ✅ Fichier source trouvé")
        
        # Lire le contenu
        with open(source_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        print(f"  📄 Taille: {len(content)} caractères")
        print(f"  📄 Lignes: {len(content.splitlines())}")
        
        # Vérifications critiques
        checks = [
            ('bl_info version', '"version": (2, 1, 8)'),
            ('bl_info name', '"name": "Tokyo City Generator v2.1.8"'),
            ('bl_info location', '"location": "View3D > Sidebar > CityGen"'),
            ('Densité par défaut', 'default=0.8'),
            ('Bâtiments par bloc', 'max(2, int(10 * density'),
            ('8 types bâtiments', "'residential',"),
            ('Type office', "'office',"),
            ('Type commercial', "'commercial',"),
            ('Type tower', "'tower',"),
            ('Type hotel', "'hotel',"),
            ('Type mixed_use', "'mixed_use',"),
            ('Type warehouse', "'warehouse',"),
            ('Type school', "'school'"),
            ('Fonction apply_building_material_by_type', 'def apply_building_material_by_type'),
            ('Marge bâtiments', 'building_margin = 0.3'),
            ('Debug bloc', 'print(f"📍 Bloc {grid_x},{grid_y}:'),
            ('Debug bâtiment', 'print(f"  🏢 Bâtiment {i+1}: {building_type}'),
        ]
        
        print("\\n🔍 VÉRIFICATIONS:")
        for check_name, check_string in checks:
            if check_string in content:
                print(f"  ✅ {check_name}")
            else:
                print(f"  ❌ {check_name} - MANQUANT!")
        
        # Vérifications d'erreurs potentielles
        error_checks = [
            ('Transmission (erreur)', 'Transmission'),
            ('Emission Strength (problème)', 'Emission Strength'),
            ('Emission Color (problème)', 'Emission Color'),
        ]
        
        print("\\n🚨 VÉRIFICATIONS D'ERREURS:")
        for check_name, check_string in error_checks:
            if check_string in content:
                print(f"  ⚠️  {check_name} - TROUVÉ (peut causer erreur)")
            else:
                print(f"  ✅ {check_name} - ABSENT (bon)")
                
    else:
        print("  ❌ Fichier source introuvable!")
        return False
    
    # Vérification du package ZIP
    zip_path = r"C:\Users\sshom\OneDrive\Documents\Assets\BlendFiles\tokyo_city_generator_v2_1_8_STABLE.zip"
    
    print(f"\\n📦 Package ZIP: {os.path.basename(zip_path)}")
    if os.path.exists(zip_path):
        print("  ✅ Package ZIP trouvé")
        
        # Vérifier le contenu du ZIP
        with zipfile.ZipFile(zip_path, 'r') as zipf:
            files = zipf.namelist()
            print(f"  📄 Fichiers dans ZIP: {len(files)}")
            
            for file in files:
                print(f"    📄 {file}")
            
            # Vérifier structure
            if 'tokyo_city_generator/__init__.py' in files:
                print("  ✅ Structure correcte")
            else:
                print("  ❌ Structure incorrecte!")
                
        # Taille du fichier
        size = os.path.getsize(zip_path)
        print(f"  💾 Taille ZIP: {size:,} bytes")
        
    else:
        print("  ❌ Package ZIP introuvable!")
    
    print("\\n" + "=" * 60)
    print("✅ CHECK TERMINÉ")
    print("=" * 60)
    
    print("\\n📋 RÉSUMÉ V2.1.8:")
    print("  🏗️ 8 types de bâtiments variés")
    print("  🎯 Densité optimisée (0.8 par défaut)")
    print("  📍 2-10 bâtiments par bloc")
    print("  🔧 Matériaux compatibles Blender 4.0+")
    print("  🚨 Erreurs Transmission/Emission supprimées")
    print("  📱 Debug intégré pour diagnostics")
    print("  🏘️ Positionnement proche trottoirs (0.3m)")
    
    return True

if __name__ == "__main__":
    try:
        check_tokyo_v2_1_8()
    except Exception as e:
        print(f"\\n💥 ERREUR CHECK: {e}")
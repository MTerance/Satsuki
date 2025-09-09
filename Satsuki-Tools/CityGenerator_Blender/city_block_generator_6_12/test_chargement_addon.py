# TEST CHARGEMENT ADDON - À copier-coller dans la console Blender
# Ce script teste si l'addon Tokyo peut se charger correctement

import bpy
import sys
import os

def test_chargement_addon():
    print("🔧 TEST CHARGEMENT ADDON TOKYO")
    print("=" * 50)
    
    # 1. Vérifier les addons installés
    print("\n1. ADDONS INSTALLÉS:")
    addons_installed = [addon.module for addon in bpy.context.preferences.addons]
    tokyo_addons = [addon for addon in addons_installed if 'tokyo' in addon.lower()]
    
    if tokyo_addons:
        for addon in tokyo_addons:
            print(f"   ✅ Trouvé: {addon}")
    else:
        print("   ❌ Aucun addon Tokyo trouvé")
        return
    
    # 2. Vérifier les modules Python
    print("\n2. MODULES PYTHON:")
    tokyo_modules = [name for name in sys.modules.keys() if 'tokyo' in name.lower()]
    
    if tokyo_modules:
        for module in tokyo_modules:
            print(f"   📦 Module: {module}")
    else:
        print("   ❌ Aucun module Tokyo chargé")
    
    # 3. Test d'import direct
    print("\n3. TEST IMPORT:")
    try:
        import tokyo_city_generator
        print("   ✅ Import tokyo_city_generator: OK")
        
        # Vérifier les attributs
        if hasattr(tokyo_city_generator, 'TEXTURE_SYSTEM_AVAILABLE'):
            print(f"   ✅ TEXTURE_SYSTEM_AVAILABLE: {tokyo_city_generator.TEXTURE_SYSTEM_AVAILABLE}")
        else:
            print("   ❌ TEXTURE_SYSTEM_AVAILABLE manquant")
            
        if hasattr(tokyo_city_generator, 'tokyo_texture_system'):
            print(f"   ✅ tokyo_texture_system: {tokyo_city_generator.tokyo_texture_system}")
        else:
            print("   ❌ tokyo_texture_system manquant")
            
    except ImportError as e:
        print(f"   ❌ Erreur import: {e}")
    except Exception as e:
        print(f"   ❌ Erreur générale: {e}")
    
    # 4. Vérifier les opérateurs
    print("\n4. OPÉRATEURS TOKYO:")
    operators = []
    for op_name in dir(bpy.ops):
        if 'tokyo' in op_name.lower():
            operators.append(op_name)
    
    if operators:
        for op in operators:
            print(f"   🎮 Opérateur: bpy.ops.{op}")
    else:
        print("   ❌ Aucun opérateur Tokyo trouvé")
    
    # 5. Vérifier les panneaux
    print("\n5. PANNEAUX UI:")
    panels = []
    for panel_name in dir(bpy.types):
        if 'TOKYO' in panel_name:
            panels.append(panel_name)
    
    if panels:
        for panel in panels:
            print(f"   🎨 Panneau: {panel}")
    else:
        print("   ❌ Aucun panneau Tokyo trouvé")
    
    # 6. Test de création de district
    print("\n6. TEST FONCTIONNEL:")
    try:
        if hasattr(bpy.ops, 'tokyo') and hasattr(bpy.ops.tokyo, 'generate_district'):
            print("   ✅ Opérateur generate_district disponible")
            print("   💡 Vous pouvez tester: bpy.ops.tokyo.generate_district()")
        else:
            print("   ❌ Opérateur generate_district manquant")
    except Exception as e:
        print(f"   ❌ Erreur test: {e}")
    
    print("\n" + "=" * 50)
    print("🎯 FIN TEST CHARGEMENT")

# Exécuter le test
test_chargement_addon()

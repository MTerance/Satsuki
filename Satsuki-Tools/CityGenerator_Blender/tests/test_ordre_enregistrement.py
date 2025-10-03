# Test d'ordre d'enregistrement des classes
# À exécuter dans la console Blender pour diagnostiquer les problèmes d'ordre

import bpy

print("🧪 TEST D'ORDRE D'ENREGISTREMENT")
print("="*50)

# Liste des classes dans l'ordre attendu
expected_order = [
    'CityGenProperties',        # Doit être enregistré en PREMIER
    'CITYGEN_OT_Generate',
    'CITYGEN_OT_RegenRoads', 
    'CITYGEN_OT_ReloadAddon',
    'CITYGEN_OT_QuickReload',
    'CITYGEN_OT_UpdateColors',
    'CITYGEN_OT_ResetProperties',
    'CITYGEN_OT_Diagnostic'
]

print("📋 Vérification de l'ordre d'enregistrement:")
missing_classes = []

for i, cls_name in enumerate(expected_order, 1):
    if hasattr(bpy.types, cls_name):
        print(f"   {i}. ✅ {cls_name}")
    else:
        print(f"   {i}. ❌ {cls_name} - MANQUANT")
        missing_classes.append(cls_name)

# Test spécial pour CityGenProperties
print("\n🔍 Test spécial CityGenProperties:")
if hasattr(bpy.types, 'CityGenProperties'):
    props_class = bpy.types.CityGenProperties
    print("   ✅ Classe trouvée")
    
    # Vérifier les propriétés de la classe
    expected_props = ['width', 'length', 'max_floors', 'shape_mode', 'block_variety', 
                     'base_block_size', 'district_mode', 'commercial_ratio', 
                     'residential_ratio', 'industrial_ratio', 'road_width', 'sidewalk_width']
    
    print("   📋 Propriétés définies dans la classe:")
    for prop_name in expected_props:
        # Vérifier si la propriété est définie dans la classe
        if hasattr(props_class, prop_name):
            print(f"      ✅ {prop_name}")
        else:
            print(f"      ❌ {prop_name} - MANQUANT")
else:
    print("   ❌ Classe CityGenProperties non trouvée")

# Test d'enregistrement des propriétés sur Scene
print("\n🔗 Test d'enregistrement Scene.citygen_props:")
if hasattr(bpy.types.Scene, 'citygen_props'):
    print("   ✅ citygen_props enregistré sur Scene")
    
    # Test d'accès dans une scène
    if hasattr(bpy.context.scene, 'citygen_props'):
        print("   ✅ Accessible dans la scène courante")
        
        # Test d'accès aux propriétés individuelles
        props = bpy.context.scene.citygen_props
        test_props = ['width', 'length', 'max_floors']
        
        print("   📋 Test d'accès aux propriétés:")
        for prop_name in test_props:
            try:
                value = getattr(props, prop_name)
                print(f"      ✅ {prop_name}: {value}")
            except Exception as e:
                print(f"      ❌ {prop_name}: ERREUR - {e}")
    else:
        print("   ❌ Non accessible dans la scène courante")
else:
    print("   ❌ citygen_props NON enregistré sur Scene")

# Recommandations
print("\n💡 RECOMMANDATIONS:")
if missing_classes:
    print("🚨 Classes manquantes détectées:")
    for cls in missing_classes:
        print(f"   • {cls}")
    print("\n🔧 Solutions:")
    print("   1. Redémarrer Blender")
    print("   2. Désactiver puis réactiver l'addon")
    print("   3. Vérifier l'ordre dans le fichier operators.py")
else:
    if not hasattr(bpy.types.Scene, 'citygen_props'):
        print("🔧 Propriétés non liées à Scene:")
        print("   1. Utiliser le bouton 'Réinitialiser Paramètres'")
        print("   2. Ou exécuter: bpy.types.Scene.citygen_props = bpy.props.PointerProperty(type=bpy.types.CityGenProperties)")
    elif not hasattr(bpy.context.scene, 'citygen_props'):
        print("🔧 Propriétés non accessibles:")
        print("   1. Changer de scène puis revenir")
        print("   2. Redémarrer Blender")
    else:
        print("✅ TOUT SEMBLE CORRECT!")
        print("   L'addon devrait fonctionner normalement")

print("\n" + "="*50)
print("🏁 TEST TERMINÉ")

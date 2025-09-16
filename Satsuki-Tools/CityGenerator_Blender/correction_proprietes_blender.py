# Script de correction des propriétés manquantes
# À copier dans la console Python de Blender

import bpy

print("🔧 CORRECTION DES PROPRIÉTÉS MANQUANTES")
print("="*50)

# Étape 1: Vérifier si CityGenProperties existe
if hasattr(bpy.types, 'CityGenProperties'):
    print("✅ Classe CityGenProperties trouvée")
else:
    print("❌ Classe CityGenProperties manquante")
    print("Solution: Redémarrer Blender et réactiver l'addon")

# Étape 2: Forcer la suppression et recréation des propriétés
print("\n🔄 Suppression des anciennes propriétés...")
try:
    if hasattr(bpy.types.Scene, 'citygen_props'):
        del bpy.types.Scene.citygen_props
        print("✅ Anciennes propriétés supprimées")
    else:
        print("ℹ️ Aucune propriété à supprimer")
except Exception as e:
    print(f"⚠️ Erreur suppression: {e}")

# Étape 3: Recréer les propriétés si possible
print("\n🔄 Recréation des propriétés...")
try:
    if hasattr(bpy.types, 'CityGenProperties'):
        bpy.types.Scene.citygen_props = bpy.props.PointerProperty(type=bpy.types.CityGenProperties)
        print("✅ Propriétés recréées avec succès")
        
        # Test d'accès
        if hasattr(bpy.context.scene, 'citygen_props'):
            props = bpy.context.scene.citygen_props
            print("✅ Propriétés accessibles dans la scène")
            
            # Initialiser les valeurs
            try:
                props.width = 5
                props.length = 5
                props.max_floors = 8
                props.shape_mode = 'AUTO'
                props.block_variety = 'MEDIUM'
                props.base_block_size = 10.0
                props.district_mode = False
                props.commercial_ratio = 0.2
                props.residential_ratio = 0.6
                props.industrial_ratio = 0.2
                props.road_width = 4.0
                props.sidewalk_width = 1.0
                print("✅ Valeurs par défaut initialisées")
            except Exception as e:
                print(f"❌ Erreur initialisation valeurs: {e}")
        else:
            print("❌ Propriétés non accessibles dans la scène")
    else:
        print("❌ Impossible de recréer - Classe CityGenProperties manquante")
        print("💡 Solution: Utiliser le bouton 'Réinitialiser Paramètres' dans le panneau")
        
except Exception as e:
    print(f"❌ Erreur recréation: {e}")

# Étape 4: Diagnostic final
print("\n📋 DIAGNOSTIC FINAL")
print("-" * 30)

# Vérifier les classes essentielles
essential_classes = ['CityGenProperties', 'CITYGEN_PT_Panel', 'CITYGEN_OT_Generate', 'CITYGEN_OT_ResetProperties']
missing_classes = []

for cls_name in essential_classes:
    if hasattr(bpy.types, cls_name):
        print(f"✅ {cls_name}")
    else:
        print(f"❌ {cls_name}")
        missing_classes.append(cls_name)

# Vérifier les propriétés
if hasattr(bpy.context.scene, 'citygen_props'):
    print("✅ citygen_props accessible")
    try:
        props = bpy.context.scene.citygen_props
        print(f"   • width: {props.width}")
        print(f"   • length: {props.length}")
        print(f"   • max_floors: {props.max_floors}")
        print("✅ Propriétés fonctionnelles")
    except Exception as e:
        print(f"❌ Erreur accès propriétés: {e}")
else:
    print("❌ citygen_props non accessible")

# Instructions finales
print("\n💡 INSTRUCTIONS FINALES")
print("-" * 30)

if missing_classes:
    print("🚨 Classes manquantes détectées:")
    for cls in missing_classes:
        print(f"   • {cls}")
    print("\n🔧 SOLUTIONS:")
    print("   1. Redémarrer Blender complètement")
    print("   2. Réinstaller l'addon (nouvelle version)")
    print("   3. Vérifier que l'addon est bien activé")
else:
    if hasattr(bpy.context.scene, 'citygen_props'):
        print("✅ TOUT FONCTIONNE:")
        print("   1. Ouvrir la sidebar (touche N)")
        print("   2. Chercher l'onglet 'CityGen'")
        print("   3. Utiliser 'Générer Ville'")
    else:
        print("🔧 UTILISER LE BOUTON:")
        print("   1. Chercher 'Réinitialiser Paramètres' dans le panneau")
        print("   2. Cliquer sur ce bouton")
        print("   3. Vérifier que les propriétés apparaissent")

print("\n" + "="*50)
print("🏁 DIAGNOSTIC TERMINÉ")

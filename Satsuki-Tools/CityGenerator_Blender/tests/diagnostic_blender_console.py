#!/usr/bin/env python3
"""
Script pour copier dans la console Python de Blender pour diagnostiquer
pourquoi l'addon n'apparaît pas activé.
"""

# Diagnostic City Block Generator dans Blender
import bpy
import sys
import traceback

print("=== DIAGNOSTIC ADDON CITY BLOCK GENERATOR DANS BLENDER ===")

# 1. Vérifier si l'addon est présent dans les modules
addon_name = "city_block_generator"
print(f"\n1️⃣ VÉRIFICATION PRÉSENCE MODULE:")
if addon_name in sys.modules:
    print(f"✅ Module {addon_name}: CHARGÉ en mémoire")
    addon_module = sys.modules[addon_name]
    
    if hasattr(addon_module, 'bl_info'):
        bl_info = addon_module.bl_info
        print(f"✅ bl_info: {bl_info['name']} v{bl_info['version']}")
    else:
        print("❌ bl_info: MANQUANT")
else:
    print(f"❌ Module {addon_name}: NON CHARGÉ")
    print("   ℹ️ L'addon n'est pas en mémoire - c'est normal s'il n'est pas activé")

# 2. Vérifier l'état d'activation
print(f"\n2️⃣ VÉRIFICATION ÉTAT ACTIVATION:")
addon_prefs = bpy.context.preferences.addons
if addon_name in addon_prefs:
    print(f"✅ Addon {addon_name}: ACTIVÉ")
    addon_pref = addon_prefs[addon_name]
    print(f"   Module: {addon_pref.module}")
else:
    print(f"❌ Addon {addon_name}: NON ACTIVÉ")

# 3. Lister tous les addons disponibles avec "city" dans le nom
print(f"\n3️⃣ ADDONS AVEC 'CITY' DANS LE NOM:")
import addon_utils
for mod in addon_utils.modules():
    if hasattr(mod, 'bl_info') and mod.bl_info:
        name = mod.bl_info.get('name', 'Sans nom')
        if 'city' in name.lower() or 'block' in name.lower():
            module_name = mod.__name__
            is_enabled = addon_utils.check(module_name)[0]
            print(f"   {'✅' if is_enabled else '❌'} {name} ({module_name})")

# 4. Essayer d'activer l'addon
print(f"\n4️⃣ TENTATIVE D'ACTIVATION:")
try:
    was_enabled = bpy.ops.preferences.addon_enable(module=addon_name)
    if was_enabled == {'FINISHED'}:
        print(f"✅ Addon {addon_name}: ACTIVATION RÉUSSIE")
        
        # Vérifier si les propriétés sont créées
        if hasattr(bpy.context.scene, 'citygen_props'):
            print("✅ Propriétés citygen_props: CRÉÉES")
            props = bpy.context.scene.citygen_props
            print(f"   • Largeur: {props.width}")
            print(f"   • Longueur: {props.length}")
        else:
            print("❌ Propriétés citygen_props: NON CRÉÉES")
            
        # Vérifier si le panneau est enregistré
        if hasattr(bpy.types, 'CITYGEN_PT_Panel'):
            print("✅ Panneau UI: ENREGISTRÉ")
        else:
            print("❌ Panneau UI: NON ENREGISTRÉ")
            
    else:
        print(f"❌ Échec activation: {was_enabled}")
        
except Exception as e:
    print(f"❌ ERREUR lors de l'activation: {e}")
    print(f"   Traceback: {traceback.format_exc()}")

# 5. Informations système
print(f"\n5️⃣ INFORMATIONS SYSTÈME:")
print(f"   • Version Blender: {bpy.app.version_string}")
print(f"   • Version Python: {sys.version}")
print(f"   • Nombre d'addons chargés: {len(bpy.context.preferences.addons)}")

# 6. Instructions finales
print(f"\n6️⃣ INSTRUCTIONS:")
print("   Si l'addon n'est pas activé:")
print("   1. Edit > Preferences > Add-ons")
print("   2. Recherchez 'City Block Generator'")
print("   3. Cochez la case à côté du nom")
print("   4. Si erreur d'activation: Window > Toggle System Console pour voir les détails")

print("\n=== FIN DIAGNOSTIC ===")

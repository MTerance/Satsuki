# SCRIPT À EXÉCUTER DANS BLENDER
# Copiez dans Scripting workspace et exécutez

import bpy

print("🔄 REFRESH ADDON TOKYO v1.4.0")

# Rafraîchir la liste des addons
bpy.ops.preferences.addon_refresh()
print("✅ Liste des addons rafraîchie")

# Chercher Tokyo
addon_name = "tokyo_city_generator"
if addon_name in bpy.context.preferences.addons:
    print("🎉 TOKYO ADDON TROUVÉ!")
    addon = bpy.context.preferences.addons[addon_name]
    if hasattr(addon.module, 'bl_info'):
        info = addon.module.bl_info
        print(f"📋 Nom: {info.get('name')}")
        print(f"🔢 Version: {info.get('version')}")
else:
    print("❌ Tokyo addon non trouvé")
    print("🔧 Essayez d'activer manuellement:")
    try:
        bpy.ops.preferences.addon_enable(module=addon_name)
        print("✅ Activation forcée réussie!")
    except Exception as e:
        print(f"❌ Échec activation: {e}")

print("📐 Allez dans Vue 3D > N > Tokyo pour utiliser l'addon")

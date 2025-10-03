# Script rapide pour activer et tester City Block Generator
# À copier dans la console Python de Blender

import bpy
import addon_utils

# Nom de l'addon
addon_name = "city_block_generator"

print(f"🔧 Test d'activation pour {addon_name}")

# Trouver le module
module_found = None
for mod in addon_utils.modules():
    if addon_name in mod.__name__:
        module_found = mod
        break

if module_found:
    print(f"✅ Module trouvé: {module_found.__name__}")
    
    # Vérifier l'état
    is_enabled = addon_utils.check(module_found.__name__)[1]
    print(f"État actuel: {'Activé' if is_enabled else 'Désactivé'}")
    
    if not is_enabled:
        print("🔄 Tentative d'activation...")
        try:
            addon_utils.enable(module_found.__name__, default_set=True, persistent=True)
            print("✅ Activation tentée")
            
            # Vérifier le résultat
            is_enabled_after = addon_utils.check(module_found.__name__)[1]
            if is_enabled_after:
                print("✅ SUCCÈS: Addon activé!")
                
                # Vérifier les classes
                if hasattr(bpy.types, 'CITYGEN_PT_Panel'):
                    print("✅ Panneau UI disponible")
                    print("💡 Appuyez sur N dans la vue 3D et cherchez l'onglet 'CityGen'")
                else:
                    print("❌ Panneau UI non trouvé")
                    
            else:
                print("❌ ÉCHEC: Addon non activé après tentative")
                
        except Exception as e:
            print(f"❌ ERREUR: {e}")
            import traceback
            traceback.print_exc()
    else:
        print("✅ Addon déjà activé")
        
        # Vérifier les classes essentielles
        essential_classes = ['CITYGEN_PT_Panel', 'CITYGEN_OT_Generate', 'CityGenProperties']
        for cls_name in essential_classes:
            if hasattr(bpy.types, cls_name):
                print(f"   ✅ {cls_name}")
            else:
                print(f"   ❌ {cls_name} manquant")
                
        # Vérifier les propriétés
        if hasattr(bpy.context.scene, 'citygen_props'):
            print("   ✅ Propriétés citygen_props disponibles")
        else:
            print("   ❌ Propriétés citygen_props manquantes")
            
else:
    print(f"❌ Module {addon_name} non trouvé")
    print("💡 Vérifiez que l'addon est bien installé")

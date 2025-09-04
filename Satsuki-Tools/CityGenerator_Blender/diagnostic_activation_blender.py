"""
Script de diagnostic pour résoudre les problèmes d'activation de l'addon City Block Generator
À copier-coller dans la console Python de Blender (Scripting workspace)
"""

import bpy
import sys
import traceback
import addon_utils

def diagnostic_activation_addon():
    """Diagnostic complet pour les problèmes d'activation d'addon"""
    
    print("\n" + "="*80)
    print("🔧 DIAGNOSTIC ACTIVATION CITY BLOCK GENERATOR")
    print("="*80)
    
    addon_name = "city_block_generator_6_12"
    
    # 1. Vérifier la présence de l'addon
    print("\n📦 1. VÉRIFICATION PRÉSENCE ADDON")
    print("-" * 40)
    
    # Lister tous les addons disponibles
    addons_available = []
    for mod in addon_utils.modules():
        if addon_name in mod.__name__:
            addons_available.append(mod)
            print(f"✅ Module trouvé: {mod.__name__}")
            print(f"   📁 Chemin: {mod.__file__}")
    
    if not addons_available:
        print(f"❌ Aucun module contenant '{addon_name}' trouvé")
        print("\n💡 SOLUTIONS:")
        print("   1. Vérifiez que le ZIP a été installé correctement")
        print("   2. Redémarrez Blender")
        print("   3. Réinstallez l'addon")
        return False
    
    # 2. Vérifier l'état d'activation
    print("\n🔄 2. VÉRIFICATION ÉTAT ACTIVATION")
    print("-" * 40)
    
    for mod in addons_available:
        is_enabled = addon_utils.check(mod.__name__)[1]
        print(f"📋 Module: {mod.__name__}")
        print(f"   État: {'✅ ACTIVÉ' if is_enabled else '❌ DÉSACTIVÉ'}")
        
        if not is_enabled:
            print(f"\n🧪 Test d'activation pour {mod.__name__}...")
            try:
                # Tenter l'activation
                addon_utils.enable(mod.__name__, default_set=True, persistent=True)
                
                # Vérifier si l'activation a réussi
                is_enabled_after = addon_utils.check(mod.__name__)[1]
                if is_enabled_after:
                    print("✅ Activation réussie!")
                else:
                    print("❌ Activation échouée")
            
            except Exception as e:
                print(f"❌ ERREUR ACTIVATION: {str(e)}")
                print(f"📋 Traceback complet:")
                traceback.print_exc()
    
    # 3. Vérifier les imports
    print("\n📥 3. VÉRIFICATION IMPORTS")
    print("-" * 40)
    
    try:
        # Test d'import du module principal
        if addon_name in sys.modules:
            mod = sys.modules[addon_name]
            print(f"✅ Module {addon_name} importé avec succès")
            
            # Vérifier les attributs essentiels
            required_attrs = ['bl_info', 'register', 'unregister']
            for attr in required_attrs:
                if hasattr(mod, attr):
                    print(f"   ✅ {attr}: PRÉSENT")
                else:
                    print(f"   ❌ {attr}: MANQUANT")
            
            # Vérifier bl_info
            if hasattr(mod, 'bl_info'):
                bl_info = mod.bl_info
                print(f"\n📋 Informations addon (bl_info):")
                for key, value in bl_info.items():
                    print(f"   • {key}: {value}")
        else:
            print(f"❌ Module {addon_name} non trouvé dans sys.modules")
            
    except Exception as e:
        print(f"❌ ERREUR IMPORT: {str(e)}")
        traceback.print_exc()
    
    # 4. Vérifier les classes enregistrées
    print("\n🏗️ 4. VÉRIFICATION CLASSES ENREGISTRÉES")
    print("-" * 40)
    
    required_classes = [
        'CITYGEN_OT_Generate',
        'CITYGEN_PT_Panel', 
        'CityGenProperties',
        'CITYGEN_OT_ResetProperties',
        'CITYGEN_OT_Diagnostic'
    ]
    
    for class_name in required_classes:
        if hasattr(bpy.types, class_name):
            print(f"   ✅ {class_name}: ENREGISTRÉ")
        else:
            print(f"   ❌ {class_name}: MANQUANT")
    
    # 5. Vérifier les propriétés de scène
    print("\n🎛️ 5. VÉRIFICATION PROPRIÉTÉS SCÈNE")
    print("-" * 40)
    
    if hasattr(bpy.types.Scene, 'citygen_props'):
        print("   ✅ citygen_props: ENREGISTRÉ au niveau Scene")
        
        if hasattr(bpy.context.scene, 'citygen_props'):
            print("   ✅ citygen_props: ACCESSIBLE dans la scène courante")
            try:
                props = bpy.context.scene.citygen_props
                print(f"   📋 Valeurs actuelles:")
                print(f"      • width: {props.width}")
                print(f"      • length: {props.length}")
                print(f"      • max_floors: {props.max_floors}")
            except Exception as e:
                print(f"   ❌ Erreur accès propriétés: {e}")
        else:
            print("   ❌ citygen_props: NON ACCESSIBLE dans la scène courante")
    else:
        print("   ❌ citygen_props: NON ENREGISTRÉ au niveau Scene")
    
    # 6. Vérifier les erreurs dans la console système
    print("\n📋 6. VÉRIFICATIONS FINALES")
    print("-" * 40)
    
    print("💡 ACTIONS RECOMMANDÉES:")
    print("   1. Si l'addon n'est pas activé, essayez de le cocher dans la liste")
    print("   2. Si l'activation échoue, regardez les erreurs ci-dessus")
    print("   3. Si des classes sont manquantes, redémarrez Blender")
    print("   4. Si les propriétés sont manquantes, utilisez 'Réinitialiser Paramètres'")
    
    # 7. Test d'accès au panneau UI
    print("\n🖥️ 7. VÉRIFICATION INTERFACE")
    print("-" * 40)
    
    if hasattr(bpy.types, 'CITYGEN_PT_Panel'):
        print("   ✅ Panneau UI enregistré")
        print("   💡 Pour voir le panneau:")
        print("      1. Allez dans la vue 3D")
        print("      2. Appuyez sur 'N' pour ouvrir la sidebar")
        print("      3. Cherchez l'onglet 'CityGen'")
    else:
        print("   ❌ Panneau UI non enregistré")
    
    print("\n" + "="*80)
    print("🏁 DIAGNOSTIC TERMINÉ")
    print("="*80)
    
    return True

# Exécuter le diagnostic
if __name__ == "__main__" or True:  # Force l'exécution même en import
    diagnostic_activation_addon()

"""
VÉRIFICATION ADDON V6.13.7 DANS BLENDER
Script à exécuter DANS Blender pour vérifier l'installation
"""

import bpy
import addon_utils

def verifier_addon():
    """Vérifie que l'addon v6.13.7 est correctement installé"""
    
    print("🔍🔍🔍 === VÉRIFICATION ADDON V6.13.7 === 🔍🔍🔍")
    
    # Chercher l'addon City Block Generator
    addon_found = False
    addon_version = None
    addon_enabled = False
    
    for addon in addon_utils.modules():
        if hasattr(addon, 'bl_info'):
            bl_info = addon.bl_info
            if 'City Block Generator' in bl_info.get('name', ''):
                addon_found = True
                addon_version = bl_info.get('version', 'Unknown')
                addon_enabled = addon_utils.check(addon.__name__)[1]
                
                print(f"✅ === ADDON TROUVÉ ===")
                print(f"   📛 Nom: {bl_info.get('name', 'N/A')}")
                print(f"   📊 Version: {addon_version}")
                print(f"   🔌 Activé: {'OUI' if addon_enabled else 'NON'}")
                print(f"   📁 Module: {addon.__name__}")
                print(f"   📝 Description: {bl_info.get('description', 'N/A')[:100]}...")
                break
    
    if not addon_found:
        print("❌ === ADDON NON TROUVÉ ===")
        print("🔄 L'addon City Block Generator n'est pas installé")
        print("📁 Vérifiez l'installation dans Preferences > Add-ons")
        return False
    
    # Vérifier la version
    if addon_version == (6, 13, 7):
        print(f"✅ === VERSION CORRECTE ===")
        print(f"   🎯 Version {addon_version} = v6.13.7 !")
    else:
        print(f"⚠️ === VERSION INCORRECTE ===")
        print(f"   📊 Trouvée: {addon_version}")
        print(f"   🎯 Attendue: (6, 13, 7)")
    
    # Vérifier l'activation
    if not addon_enabled:
        print("⚠️ === ADDON DÉSACTIVÉ ===")
        print("🔌 L'addon doit être ACTIVÉ pour fonctionner")
        return False
    
    # Vérifier les propriétés de la scène
    scene = bpy.context.scene
    proprietes_requises = [
        'citygen_width',
        'citygen_length', 
        'citygen_organic_mode',
        'citygen_road_first_method',
        'citygen_road_curve_intensity'
    ]
    
    proprietes_ok = True
    print("🔧 === VÉRIFICATION PROPRIÉTÉS ===")
    for prop in proprietes_requises:
        if hasattr(scene, prop):
            valeur = getattr(scene, prop)
            print(f"   ✅ {prop}: {valeur}")
        else:
            print(f"   ❌ {prop}: MANQUANT")
            proprietes_ok = False
    
    # Vérifier l'opérateur
    try:
        if hasattr(bpy.ops, 'citygen') and hasattr(bpy.ops.citygen, 'generate_city'):
            print("✅ === OPÉRATEUR DISPONIBLE ===")
            print("   🎯 bpy.ops.citygen.generate_city trouvé")
        else:
            print("❌ === OPÉRATEUR MANQUANT ===")
            print("   🎯 bpy.ops.citygen.generate_city non trouvé")
            proprietes_ok = False
    except Exception as e:
        print(f"❌ === ERREUR OPÉRATEUR ===")
        print(f"   🎯 Erreur: {e}")
        proprietes_ok = False
    
    # Résultat final
    if addon_found and addon_enabled and addon_version == (6, 13, 7) and proprietes_ok:
        print("🔥✅🎯 === SUCCÈS COMPLET === 🎯✅🔥")
        print("🌊 Addon v6.13.7 correctement installé et activé")
        print("🔥 Courbes MEGA visibles prêtes à être testées")
        print("🎯 Utilisez le script TEST_COURBES_MEGA_VISIBLES_V6_13_7.py")
        return True
    else:
        print("⚠️❌ === PROBLÈME DÉTECTÉ ===")
        print("🔄 Suivez les instructions d'installation robuste")
        return False

# Exécuter la vérification
verifier_addon()

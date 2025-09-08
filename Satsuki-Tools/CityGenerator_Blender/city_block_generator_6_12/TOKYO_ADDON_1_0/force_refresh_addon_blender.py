# FORCE REFRESH ADDON TOKYO DANS BLENDER
# À exécuter DANS Blender pour forcer l'affichage de l'addon

import bpy
import sys

def force_refresh_tokyo_addon():
    """Force le rafraîchissement de l'addon Tokyo dans Blender"""
    
    print("🔄 FORCE REFRESH TOKYO ADDON v1.4.0")
    print("=" * 45)
    
    addon_name = "tokyo_city_generator"
    
    # 1. Vérifier l'état actuel
    print("🔍 1. VÉRIFICATION ÉTAT ACTUEL")
    
    if addon_name in bpy.context.preferences.addons:
        addon = bpy.context.preferences.addons[addon_name]
        print(f"✅ Addon trouvé et activé: {addon_name}")
        
        if hasattr(addon.module, 'bl_info'):
            info = addon.module.bl_info
            version = info.get('version', 'Inconnue')
            name = info.get('name', 'Inconnu')
            print(f"📋 Nom: {name}")
            print(f"🔢 Version: {version}")
        else:
            print("⚠️ bl_info non disponible")
    else:
        print(f"❌ Addon non activé: {addon_name}")
    
    # 2. Nettoyer le cache des modules
    print(f"\n🧹 2. NETTOYAGE CACHE MODULES")
    
    modules_to_remove = []
    for module_name in list(sys.modules.keys()):
        if module_name.startswith(addon_name) or 'tokyo' in module_name.lower():
            modules_to_remove.append(module_name)
    
    for module_name in modules_to_remove:
        try:
            del sys.modules[module_name]
            print(f"🗑️ Module supprimé du cache: {module_name}")
        except:
            pass
    
    # 3. Désactiver puis réactiver l'addon
    print(f"\n🔄 3. DÉSACTIVATION/RÉACTIVATION")
    
    try:
        # Désactiver
        if addon_name in bpy.context.preferences.addons:
            bpy.ops.preferences.addon_disable(module=addon_name)
            print("❌ Addon désactivé")
        
        # Rafraîchir la liste
        bpy.ops.preferences.addon_refresh()
        print("🔄 Liste des addons rafraîchie")
        
        # Réactiver
        bpy.ops.preferences.addon_enable(module=addon_name)
        print("✅ Addon réactivé")
        
    except Exception as e:
        print(f"❌ Erreur lors du refresh: {e}")
        return False
    
    # 4. Vérifier le résultat
    print(f"\n✅ 4. VÉRIFICATION FINALE")
    
    if addon_name in bpy.context.preferences.addons:
        addon = bpy.context.preferences.addons[addon_name]
        print(f"🎉 SUCCESS! Addon trouvé: {addon_name}")
        
        if hasattr(addon.module, 'bl_info'):
            info = addon.module.bl_info
            version = info.get('version', 'Inconnue')
            name = info.get('name', 'Inconnu')
            print(f"📋 Nom affiché: {name}")
            print(f"🔢 Version affichée: {version}")
            
            if version == (1, 4, 0):
                print("🎯 PARFAIT! Version 1.4.0 confirmée")
            else:
                print(f"⚠️ Version inattendue: {version}")
        
        # 5. Vérifier les propriétés
        print(f"\n🎛️ 5. VÉRIFICATION PROPRIÉTÉS")
        
        scene = bpy.context.scene
        properties = [
            'tokyo_use_advanced_textures',
            'tokyo_texture_base_path'
        ]
        
        for prop in properties:
            if hasattr(scene, prop):
                value = getattr(scene, prop)
                print(f"✅ {prop}: {value}")
            else:
                print(f"❌ Propriété manquante: {prop}")
        
        # 6. Vérifier l'interface
        print(f"\n🖥️ 6. VÉRIFICATION INTERFACE")
        
        # Chercher les panneaux
        panels_found = []
        for cls_name in dir(bpy.types):
            cls = getattr(bpy.types, cls_name)
            if hasattr(cls, 'bl_category') and getattr(cls, 'bl_category', '') == 'Tokyo':
                panels_found.append(cls_name)
                print(f"✅ Panneau trouvé: {cls_name}")
        
        if panels_found:
            print(f"🎯 {len(panels_found)} panneau(s) Tokyo trouvé(s)")
            print("📍 Emplacement: Vue 3D > Sidebar (N) > Onglet 'Tokyo'")
        else:
            print("❌ Aucun panneau Tokyo trouvé")
        
        return True
    else:
        print("❌ ÉCHEC: Addon non trouvé après refresh")
        return False

def quick_test_interface():
    """Test rapide de l'interface"""
    
    print(f"\n🧪 TEST RAPIDE INTERFACE")
    print("-" * 25)
    
    try:
        # Test des opérateurs
        if hasattr(bpy.ops, 'tokyo'):
            tokyo_ops = dir(bpy.ops.tokyo)
            print(f"✅ Opérateurs Tokyo: {len(tokyo_ops)}")
            for op in tokyo_ops:
                if not op.startswith('_'):
                    print(f"  🔧 {op}")
        else:
            print("❌ Aucun opérateur Tokyo trouvé")
        
        # Test génération rapide (optionnel)
        print(f"\n💡 Pour tester la génération:")
        print("1. Vue 3D > Sidebar (N) > Tokyo")
        print("2. ✅ Advanced Textures")
        print("3. 🚀 Generate Tokyo District")
        
    except Exception as e:
        print(f"❌ Erreur test interface: {e}")

# Fonction principale
def main():
    """Fonction principale de refresh"""
    
    try:
        success = force_refresh_tokyo_addon()
        
        if success:
            quick_test_interface()
            
            print(f"\n🎉 REFRESH TERMINÉ AVEC SUCCÈS!")
            print("=" * 45)
            print("🎯 ÉTAPES SUIVANTES:")
            print("1. 📐 Ouvrez la Vue 3D")
            print("2. 📋 Appuyez sur N pour la sidebar")
            print("3. 🔍 Cherchez l'onglet 'Tokyo'")
            print("4. ✅ Cochez 'Advanced Textures'")
            print("5. 📁 Configurez 'Texture Path' si nécessaire")
            print("6. 🚀 Generate Tokyo District!")
            
        else:
            print(f"\n❌ REFRESH ÉCHOUÉ")
            print("🔧 Solutions alternatives:")
            print("1. Redémarrer Blender complètement")
            print("2. Réinstaller l'addon manuellement")
            print("3. Vérifier les erreurs dans la console")
            
    except Exception as e:
        print(f"❌ ERREUR CRITIQUE: {e}")
        import traceback
        traceback.print_exc()

# Exécution
if __name__ == "__main__":
    main()

# Instructions d'utilisation
print(f"\n" + "="*60)
print("📋 INSTRUCTIONS POUR UTILISER CE SCRIPT:")
print("="*60)
print("1. 🖥️ Ouvrez Blender")
print("2. 📝 Allez dans 'Scripting' workspace")
print("3. 📄 Créez un nouveau script")
print("4. 📋 Copiez-collez ce code")
print("5. ▶️ Cliquez 'Run Script'")
print("6. 👀 Regardez la console pour les résultats")
print("7. 📐 Allez dans Vue 3D > N > Tokyo")
print("="*60)

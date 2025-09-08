# DIAGNOSTIC TEXTURES TOKYO - Pourquoi les textures ne s'appliquent pas ?

import bpy
import os

def diagnostic_textures_tokyo():
    """Diagnostic complet du système de textures Tokyo"""
    
    print("🔍 DIAGNOSTIC SYSTÈME TEXTURES TOKYO")
    print("=" * 50)
    
    # Test 1: Vérifier l'addon est activé
    print("\n1️⃣ ADDON TOKYO:")
    addon_modules = [mod for mod in bpy.context.preferences.addons.keys() if 'tokyo' in mod.lower()]
    if addon_modules:
        for mod in addon_modules:
            print(f"  ✅ Addon trouvé: {mod}")
    else:
        print("  ❌ Aucun addon Tokyo trouvé!")
        return
    
    # Test 2: Vérifier les propriétés de scène
    print("\n2️⃣ PROPRIÉTÉS DE SCÈNE:")
    scene = bpy.context.scene
    
    # Vérifier tokyo_use_advanced_textures
    if hasattr(scene, 'tokyo_use_advanced_textures'):
        use_advanced = scene.tokyo_use_advanced_textures
        print(f"  ✅ tokyo_use_advanced_textures: {use_advanced}")
    else:
        print("  ❌ Propriété tokyo_use_advanced_textures manquante!")
        use_advanced = False
    
    # Vérifier tokyo_texture_base_path
    if hasattr(scene, 'tokyo_texture_base_path'):
        texture_path = scene.tokyo_texture_base_path
        print(f"  ✅ tokyo_texture_base_path: {texture_path}")
    else:
        print("  ❌ Propriété tokyo_texture_base_path manquante!")
        texture_path = None
    
    # Test 3: Vérifier le module texture_system
    print("\n3️⃣ MODULE TEXTURE_SYSTEM:")
    try:
        # Essayer d'importer le module
        import sys
        for mod_name in sys.modules:
            if 'texture_system' in mod_name:
                print(f"  ✅ Module trouvé: {mod_name}")
        
        # Tester l'import direct
        exec("from . import texture_system")
        print("  ✅ Import texture_system réussi")
    except Exception as e:
        print(f"  ❌ Erreur import texture_system: {e}")
    
    # Test 4: Vérifier les dossiers de textures
    print("\n4️⃣ DOSSIERS TEXTURES:")
    if texture_path and os.path.exists(texture_path):
        print(f"  ✅ Dossier base existe: {texture_path}")
        
        # Lister les sous-dossiers
        try:
            subdirs = [d for d in os.listdir(texture_path) if os.path.isdir(os.path.join(texture_path, d))]
            if subdirs:
                print(f"  📁 Sous-dossiers trouvés: {len(subdirs)}")
                for subdir in subdirs[:5]:  # Limiter à 5
                    print(f"    - {subdir}")
                if len(subdirs) > 5:
                    print(f"    ... et {len(subdirs) - 5} autres")
            else:
                print("  ⚠️ Aucun sous-dossier trouvé")
        except Exception as e:
            print(f"  ❌ Erreur lecture dossier: {e}")
    else:
        print(f"  ❌ Dossier base inexistant: {texture_path}")
    
    # Test 5: Vérifier les matériaux existants
    print("\n5️⃣ MATÉRIAUX SCÈNE:")
    materials = [mat for mat in bpy.data.materials if 'tokyo' in mat.name.lower()]
    if materials:
        print(f"  ✅ Matériaux Tokyo trouvés: {len(materials)}")
        for mat in materials[:5]:
            print(f"    - {mat.name}")
            # Vérifier si le matériau a des textures
            if mat.node_tree:
                img_nodes = [node for node in mat.node_tree.nodes if node.type == 'TEX_IMAGE']
                if img_nodes:
                    print(f"      📷 Textures: {len(img_nodes)}")
                else:
                    print("      ⚠️ Pas de texture image")
            else:
                print("      ⚠️ Pas de node tree")
    else:
        print("  ⚠️ Aucun matériau Tokyo trouvé")
    
    # Test 6: Vérifier les objets avec matériaux
    print("\n6️⃣ OBJETS AVEC MATÉRIAUX:")
    objects_with_materials = [obj for obj in bpy.context.scene.objects if obj.data and hasattr(obj.data, 'materials') and obj.data.materials]
    if objects_with_materials:
        print(f"  ✅ Objets avec matériaux: {len(objects_with_materials)}")
        for obj in objects_with_materials[:5]:
            mat_count = len([mat for mat in obj.data.materials if mat])
            print(f"    - {obj.name}: {mat_count} matériaux")
    else:
        print("  ⚠️ Aucun objet avec matériau trouvé")
    
    # Test 7: Tester l'interface
    print("\n7️⃣ INTERFACE TOKYO:")
    try:
        # Vérifier les panneaux
        panels = [cls for cls in bpy.types.Panel.__subclasses__() if 'TOKYO' in cls.__name__]
        if panels:
            print(f"  ✅ Panneaux Tokyo: {len(panels)}")
            for panel in panels:
                print(f"    - {panel.__name__}")
        else:
            print("  ❌ Aucun panneau Tokyo trouvé")
    except Exception as e:
        print(f"  ❌ Erreur vérification interface: {e}")
    
    # DIAGNOSTIC FINAL
    print("\n" + "=" * 50)
    print("🎯 RÉSUMÉ DIAGNOSTIC:")
    
    if not use_advanced:
        print("❌ PROBLÈME PRINCIPAL: Advanced Textures désactivé!")
        print("   → Solution: Cocher 'Advanced Textures' dans l'interface Tokyo")
    elif not texture_path or not os.path.exists(texture_path):
        print("❌ PROBLÈME PRINCIPAL: Dossier textures inexistant!")
        print("   → Solution: Configurer le chemin textures ou créer les dossiers")
    elif not materials:
        print("❌ PROBLÈME PRINCIPAL: Aucun matériau Tokyo créé!")
        print("   → Solution: Générer un district pour créer les matériaux")
    else:
        print("✅ Système semble correctement configuré")
        print("   → Vérifiez le mode d'affichage Blender (Material Preview/Rendered)")
    
    print("\n🔧 ACTIONS RECOMMANDÉES:")
    print("1. Activer 'Advanced Textures' dans l'onglet Tokyo")
    print("2. Vérifier le chemin des textures")
    print("3. Générer un nouveau district")
    print("4. Passer en mode Material Preview (Blender)")
    
    return {
        'advanced_textures': use_advanced,
        'texture_path_exists': texture_path and os.path.exists(texture_path) if texture_path else False,
        'materials_count': len(materials),
        'objects_count': len(objects_with_materials)
    }

# Exécuter le diagnostic
if __name__ == "__main__":
    try:
        result = diagnostic_textures_tokyo()
        print(f"\n📊 Résultat: {result}")
    except Exception as e:
        print(f"❌ Erreur diagnostic: {e}")
        import traceback
        traceback.print_exc()

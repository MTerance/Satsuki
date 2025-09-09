# DIAGNOSTIC APPROFONDI - À copier-coller dans la console Blender
# Ce script va identifier pourquoi les textures ne s'appliquent pas

import bpy
import os

def diagnostic_complet():
    print("=" * 80)
    print("🔍 DIAGNOSTIC COMPLET TEXTURES TOKYO")
    print("=" * 80)
    
    # 1. Vérifier l'addon
    print("\n1. VÉRIFICATION ADDON:")
    addon_found = False
    for addon in bpy.context.preferences.addons:
        if 'tokyo' in addon.module.lower():
            print(f"   ✅ Addon: {addon.module}")
            addon_found = True
    
    if not addon_found:
        print("   ❌ Addon Tokyo non trouvé")
        return
    
    # 2. Vérifier les variables globales
    print("\n2. VARIABLES SYSTÈME:")
    
    # Tenter d'accéder aux variables du système
    try:
        # Importer le module
        import sys
        modules = [name for name in sys.modules.keys() if 'tokyo' in name.lower()]
        print(f"   📦 Modules Tokyo chargés: {modules}")
        
        # Vérifier TEXTURE_SYSTEM_AVAILABLE
        if 'tokyo_city_generator' in sys.modules:
            module = sys.modules['tokyo_city_generator']
            if hasattr(module, 'TEXTURE_SYSTEM_AVAILABLE'):
                available = module.TEXTURE_SYSTEM_AVAILABLE
                print(f"   🔧 TEXTURE_SYSTEM_AVAILABLE: {available}")
                
                if hasattr(module, 'tokyo_texture_system'):
                    system = module.tokyo_texture_system
                    print(f"   🎨 tokyo_texture_system: {system}")
                else:
                    print("   ❌ tokyo_texture_system non trouvé")
            else:
                print("   ❌ TEXTURE_SYSTEM_AVAILABLE non trouvé")
    except Exception as e:
        print(f"   ❌ Erreur accès module: {e}")
    
    # 3. Vérifier les propriétés de scène
    print("\n3. PROPRIÉTÉS SCÈNE:")
    scene = bpy.context.scene
    
    props_to_check = [
        'tokyo_use_advanced_textures',
        'tokyo_texture_base_path'
    ]
    
    for prop in props_to_check:
        if hasattr(scene, prop):
            value = getattr(scene, prop)
            print(f"   ✅ {prop}: {value}")
            
            if prop == 'tokyo_texture_base_path' and value:
                # Vérifier si le chemin existe
                if os.path.exists(value):
                    print(f"       ✅ Chemin existe")
                    # Lister le contenu
                    try:
                        content = os.listdir(value)
                        print(f"       📁 Contenu: {content}")
                    except:
                        print(f"       ❌ Impossible de lister le contenu")
                else:
                    print(f"       ❌ Chemin n'existe pas")
        else:
            print(f"   ❌ {prop}: manquant")
    
    # 4. Vérifier les objets Tokyo
    print("\n4. OBJETS TOKYO:")
    tokyo_objects = [obj for obj in bpy.data.objects if 'tokyo' in obj.name.lower()]
    
    if tokyo_objects:
        print(f"   ✅ {len(tokyo_objects)} objets Tokyo trouvés")
        
        # Analyser les premiers objets
        buildings = [obj for obj in tokyo_objects if 'building' in obj.name.lower()]
        print(f"   🏢 {len(buildings)} bâtiments")
        
        if buildings:
            # Analyser le premier bâtiment en détail
            first_building = buildings[0]
            print(f"\n   🔍 ANALYSE: {first_building.name}")
            print(f"       📏 Dimensions: {first_building.dimensions}")
            print(f"       📦 Matériaux: {len(first_building.data.materials)}")
            
            if first_building.data.materials:
                mat = first_building.data.materials[0]
                print(f"       🎨 Premier matériau: {mat.name}")
                print(f"       🔗 Use nodes: {mat.use_nodes}")
                
                if mat.use_nodes and mat.node_tree:
                    nodes = mat.node_tree.nodes
                    print(f"       📋 Nodes: {len(nodes)}")
                    
                    # Analyser les types de nodes
                    node_types = {}
                    for node in nodes:
                        node_type = node.type
                        if node_type in node_types:
                            node_types[node_type] += 1
                        else:
                            node_types[node_type] = 1
                    
                    print(f"       📊 Types de nodes: {node_types}")
                    
                    # Chercher des textures
                    tex_nodes = [n for n in nodes if n.type == 'TEX_IMAGE']
                    if tex_nodes:
                        print(f"       🖼️ Textures trouvées:")
                        for tex in tex_nodes:
                            if tex.image:
                                print(f"           - {tex.image.name}: {tex.image.filepath}")
                            else:
                                print(f"           - Node texture sans image")
                    else:
                        print(f"       ❌ Aucune texture image trouvée")
            else:
                print(f"       ❌ Aucun matériau assigné")
    else:
        print("   ❌ Aucun objet Tokyo trouvé")
    
    # 5. Test de création de matériau
    print("\n5. TEST CRÉATION MATÉRIAU:")
    try:
        # Essayer de créer un matériau test
        if 'tokyo_city_generator' in sys.modules:
            module = sys.modules['tokyo_city_generator']
            if hasattr(module, 'tokyo_texture_system') and module.tokyo_texture_system:
                system = module.tokyo_texture_system
                test_mat = system.create_advanced_building_material(
                    "residential", 10.0, 5.0, 5.0, "DiagnosticTest", ""
                )
                if test_mat:
                    print("   ✅ Création matériau test réussie")
                    print(f"       🎨 Matériau: {test_mat.name}")
                    print(f"       🔗 Nodes: {test_mat.use_nodes}")
                    # Nettoyer
                    bpy.data.materials.remove(test_mat)
                else:
                    print("   ❌ Création matériau test échouée (None)")
            else:
                print("   ❌ tokyo_texture_system non disponible")
        else:
            print("   ❌ Module tokyo_city_generator non trouvé")
    except Exception as e:
        print(f"   ❌ Erreur test création: {e}")
    
    # 6. Mode d'affichage
    print("\n6. MODE D'AFFICHAGE:")
    for area in bpy.context.screen.areas:
        if area.type == 'VIEW_3D':
            for space in area.spaces:
                if space.type == 'VIEW_3D':
                    mode = space.shading.type
                    print(f"   🎨 Mode: {mode}")
                    if mode in ['MATERIAL', 'RENDERED']:
                        print("   ✅ Mode compatible textures")
                    else:
                        print("   ⚠️ Mode pourrait masquer les textures")
    
    print("\n" + "=" * 80)
    print("🎯 FIN DU DIAGNOSTIC")
    print("=" * 80)

# Exécuter le diagnostic
diagnostic_complet()

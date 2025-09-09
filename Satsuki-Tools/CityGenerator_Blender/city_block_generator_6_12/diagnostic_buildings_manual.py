# Script de diagnostic rapide pour vérifier pourquoi les textures n'apparaissent pas
# À exécuter dans Blender pour identifier le problème

import bpy
import os

def diagnostic_textures_buildings():
    """Diagnostic complet pour textures de bâtiments"""
    
    print("=" * 60)
    print("🔍 DIAGNOSTIC TEXTURES BÂTIMENTS TOKYO")
    print("=" * 60)
    
    # Test 1: Vérifier l'addon
    print("\n1. VÉRIFICATION ADDON:")
    addon_enabled = False
    for addon in bpy.context.preferences.addons:
        if 'tokyo' in addon.module.lower():
            print(f"   ✅ Addon trouvé: {addon.module}")
            addon_enabled = True
            break
    
    if not addon_enabled:
        print("   ❌ Addon Tokyo non trouvé ou non activé")
        return
    
    # Test 2: Vérifier les propriétés de scène
    print("\n2. PROPRIÉTÉS DE SCÈNE:")
    scene = bpy.context.scene
    
    if hasattr(scene, 'tokyo_use_advanced_textures'):
        print(f"   ✅ tokyo_use_advanced_textures: {scene.tokyo_use_advanced_textures}")
    else:
        print("   ❌ tokyo_use_advanced_textures manquante")
    
    if hasattr(scene, 'tokyo_texture_base_path'):
        path = scene.tokyo_texture_base_path
        print(f"   📁 tokyo_texture_base_path: {path}")
        if path and os.path.exists(path):
            print("   ✅ Chemin existe")
        else:
            print("   ❌ Chemin invalide ou vide")
    else:
        print("   ❌ tokyo_texture_base_path manquante")
    
    # Test 3: Vérifier les objets Tokyo
    print("\n3. OBJETS TOKYO DANS LA SCÈNE:")
    tokyo_objects = [obj for obj in bpy.data.objects if 'tokyo' in obj.name.lower()]
    
    if tokyo_objects:
        print(f"   ✅ {len(tokyo_objects)} objets Tokyo trouvés:")
        for obj in tokyo_objects[:5]:  # Limiter à 5 pour l'affichage
            print(f"      - {obj.name}")
    else:
        print("   ❌ Aucun objet Tokyo trouvé")
        print("   💡 Générez d'abord un district Tokyo")
        return
    
    # Test 4: Vérifier les matériaux
    print("\n4. MATÉRIAUX TOKYO:")
    tokyo_materials = [mat for mat in bpy.data.materials if 'tokyo' in mat.name.lower()]
    
    if tokyo_materials:
        print(f"   ✅ {len(tokyo_materials)} matériaux Tokyo trouvés:")
        for mat in tokyo_materials[:3]:
            print(f"      - {mat.name}")
            if mat.use_nodes:
                print("        ✅ Nodes activés")
                nodes = mat.node_tree.nodes
                texture_nodes = [n for n in nodes if n.type == 'TEX_IMAGE']
                print(f"        📄 {len(texture_nodes)} texture nodes")
            else:
                print("        ❌ Nodes désactivés")
    else:
        print("   ❌ Aucun matériau Tokyo trouvé")
    
    # Test 5: Vérifier le mode d'affichage
    print("\n5. MODE D'AFFICHAGE:")
    for area in bpy.context.screen.areas:
        if area.type == 'VIEW_3D':
            for space in area.spaces:
                if space.type == 'VIEW_3D':
                    mode = space.shading.type
                    print(f"   🎨 Mode actuel: {mode}")
                    if mode in ['MATERIAL', 'RENDERED']:
                        print("   ✅ Mode compatible avec textures")
                    else:
                        print("   ❌ Mode incompatible - passez en Material Preview ou Rendered")
                    break
    
    # Test 6: Diagnostic spécifique au premier objet
    if tokyo_objects:
        print(f"\n6. DIAGNOSTIC DÉTAILLÉ - {tokyo_objects[0].name}:")
        obj = tokyo_objects[0]
        
        if obj.data.materials:
            mat = obj.data.materials[0]
            print(f"   📦 Matériau: {mat.name}")
            
            if mat.use_nodes and mat.node_tree:
                nodes = mat.node_tree.nodes
                print(f"   🔗 Nodes: {len(nodes)} trouvés")
                
                # Vérifier les types de nodes
                node_types = [n.type for n in nodes]
                print(f"   📋 Types: {set(node_types)}")
                
                # Vérifier les textures
                tex_nodes = [n for n in nodes if n.type == 'TEX_IMAGE']
                if tex_nodes:
                    print(f"   🖼️ {len(tex_nodes)} texture(s):")
                    for tex_node in tex_nodes:
                        if tex_node.image:
                            print(f"      - {tex_node.image.name} ({tex_node.image.filepath})")
                        else:
                            print(f"      - Node texture sans image")
                else:
                    print("   ❌ Aucune texture trouvée")
            else:
                print("   ❌ Pas de node tree")
        else:
            print("   ❌ Aucun matériau assigné")
    
    print("\n" + "=" * 60)
    print("🎯 RÉSUMÉ DU DIAGNOSTIC")
    print("=" * 60)

# Exécuter le diagnostic
if __name__ == "__main__":
    diagnostic_textures_buildings()

# TEST SIMPLE TEXTURES - Créer des textures de démo et tester l'application

import bpy
import os
import bmesh
from mathutils import Vector

def test_textures_simple():
    """Test simple pour vérifier l'application des textures"""
    
    print("🧪 TEST SIMPLE TEXTURES TOKYO")
    print("=" * 40)
    
    # Nettoyer la scène
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete(use_global=False)
    
    # Créer un cube test
    bpy.ops.mesh.primitive_cube_add(location=(0, 0, 1))
    cube = bpy.context.object
    cube.name = "TestCube_Tokyo"
    
    print("✅ Cube de test créé")
    
    # Test 1: Matériau simple avec couleur
    print("\n1️⃣ Test matériau coloré...")
    mat_colored = bpy.data.materials.new(name="Tokyo_Test_Colored")
    mat_colored.use_nodes = True
    nodes = mat_colored.node_tree.nodes
    nodes.clear()
    
    # Nœuds de base
    output = nodes.new(type='ShaderNodeOutputMaterial')
    bsdf = nodes.new(type='ShaderNodeBsdfPrincipled')
    
    # Couleur bleue pour test
    bsdf.inputs['Base Color'].default_value = (0.2, 0.5, 1.0, 1.0)  # Bleu
    bsdf.inputs['Metallic'].default_value = 0.0
    bsdf.inputs['Roughness'].default_value = 0.5
    
    # Connexion
    mat_colored.node_tree.links.new(bsdf.outputs['BSDF'], output.inputs['Surface'])
    
    # Appliquer au cube
    cube.data.materials.append(mat_colored)
    print("  ✅ Matériau coloré appliqué")
    
    # Test 2: Créer une texture procédurale simple
    print("\n2️⃣ Test texture procédurale...")
    
    # Créer un second cube
    bpy.ops.mesh.primitive_cube_add(location=(3, 0, 1))
    cube2 = bpy.context.object
    cube2.name = "TestCube_Procedural"
    
    mat_proc = bpy.data.materials.new(name="Tokyo_Test_Procedural")
    mat_proc.use_nodes = True
    nodes = mat_proc.node_tree.nodes
    nodes.clear()
    
    # Nœuds
    output = nodes.new(type='ShaderNodeOutputMaterial')
    bsdf = nodes.new(type='ShaderNodeBsdfPrincipled')
    
    # Texture de bruit
    noise = nodes.new(type='ShaderNodeTexNoise')
    noise.inputs['Scale'].default_value = 5.0
    noise.inputs['Detail'].default_value = 2.0
    noise.inputs['Roughness'].default_value = 0.5
    
    # ColorRamp pour créer des bandes
    colorramp = nodes.new(type='ShaderNodeValToRGB')
    colorramp.color_ramp.elements[0].color = (0.8, 0.4, 0.2, 1.0)  # Orange
    colorramp.color_ramp.elements[1].color = (0.2, 0.2, 0.2, 1.0)  # Gris foncé
    
    # Connexions
    mat_proc.node_tree.links.new(noise.outputs['Fac'], colorramp.inputs['Fac'])
    mat_proc.node_tree.links.new(colorramp.outputs['Color'], bsdf.inputs['Base Color'])
    mat_proc.node_tree.links.new(bsdf.outputs['BSDF'], output.inputs['Surface'])
    
    cube2.data.materials.append(mat_proc)
    print("  ✅ Texture procédurale appliquée")
    
    # Test 3: Tester avec le système Tokyo si disponible
    print("\n3️⃣ Test système Tokyo...")
    
    try:
        # Vérifier si le système Tokyo est disponible
        scene = bpy.context.scene
        
        # Activer les textures avancées si la propriété existe
        if hasattr(scene, 'tokyo_use_advanced_textures'):
            scene.tokyo_use_advanced_textures = True
            print("  ✅ Advanced Textures activé")
        else:
            print("  ⚠️ Propriété Advanced Textures non trouvée")
        
        # Créer un bâtiment avec le système Tokyo
        bpy.ops.mesh.primitive_cube_add(location=(6, 0, 1))
        cube3 = bpy.context.object
        cube3.name = "TestBuilding_Tokyo"
        cube3.scale = (2, 2, 4)  # Faire un bâtiment
        
        # Essayer d'appliquer le matériau Tokyo
        try:
            # Simuler les paramètres d'un bâtiment
            zone_type = "business"
            height = 8.0
            width_x = 4.0
            width_y = 4.0
            
            # Test du système de textures
            exec("""
# Essayer d'importer et utiliser le système
try:
    from . import texture_system
    tokyo_system = texture_system.TokyoTextureSystem()
    material = tokyo_system.create_advanced_building_material(
        zone_type, height, width_x, width_y, "TestBuilding", 
        r"C:\\Users\\sshom\\Documents\\assets\\Tools\\tokyo_textures"
    )
    cube3.data.materials.append(material)
    print("  ✅ Matériau Tokyo appliqué")
except Exception as e:
    print(f"  ❌ Erreur système Tokyo: {e}")
    # Fallback vers matériau simple
    mat_fallback = bpy.data.materials.new(name="Tokyo_Fallback")
    mat_fallback.use_nodes = True
    nodes = mat_fallback.node_tree.nodes
    nodes.clear()
    
    output = nodes.new(type='ShaderNodeOutputMaterial')
    bsdf = nodes.new(type='ShaderNodeBsdfPrincipled')
    bsdf.inputs['Base Color'].default_value = (0.7, 0.7, 0.7, 1.0)
    bsdf.inputs['Metallic'].default_value = 0.3
    bsdf.inputs['Roughness'].default_value = 0.4
    
    mat_fallback.node_tree.links.new(bsdf.outputs['BSDF'], output.inputs['Surface'])
    cube3.data.materials.append(mat_fallback)
    print("  ✅ Matériau fallback appliqué")
""")
            
        except Exception as e:
            print(f"  ❌ Erreur test Tokyo: {e}")
            
    except Exception as e:
        print(f"  ❌ Erreur générale: {e}")
    
    # Configurer la vue pour voir les matériaux
    print("\n4️⃣ Configuration vue...")
    
    # Changer le mode d'affichage en Material Preview
    for area in bpy.context.screen.areas:
        if area.type == 'VIEW_3D':
            for space in area.spaces:
                if space.type == 'VIEW_3D':
                    space.shading.type = 'MATERIAL'
                    print("  ✅ Mode Material Preview activé")
                    break
    
    # Positionner la caméra pour voir les cubes
    if bpy.context.scene.camera:
        cam = bpy.context.scene.camera
        cam.location = (10, -10, 8)
        cam.rotation_euler = (1.1, 0, 0.785)
    
    print("\n✅ TEST TERMINÉ!")
    print("🎯 RÉSULTATS:")
    print("  - 3 cubes créés avec différents matériaux")
    print("  - Mode Material Preview activé")
    print("  - Vérifiez visuellement dans Blender")
    
    print("\n💡 SI LES TEXTURES NE SONT PAS VISIBLES:")
    print("  1. Vérifiez le mode d'affichage (Material Preview/Rendered)")
    print("  2. Vérifiez que les objets ont bien des matériaux")
    print("  3. Activez 'Advanced Textures' dans l'onglet Tokyo")
    print("  4. Configurez le chemin des textures")

# Exécuter le test
if __name__ == "__main__":
    test_textures_simple()

# TEST SIMPLE TEXTURE - Version ultra simplifiée
# À copier-coller dans la console Blender

import bpy
import os

def test_texture_simple():
    print("🧪 TEST TEXTURE SIMPLE")
    print("=" * 40)
    
    # 1. Prendre le premier bâtiment
    buildings = [obj for obj in bpy.data.objects if 'building' in obj.name.lower()]
    if not buildings:
        print("❌ Aucun bâtiment trouvé")
        return
    
    building = buildings[0]
    print(f"🏢 Test sur: {building.name}")
    
    # 2. Trouver une texture
    scene = bpy.context.scene
    base_path = scene.tokyo_texture_base_path
    
    # Chercher dans tous les dossiers
    texture_found = None
    for subdir in ['commercial', 'residential', 'skyscrapers', 'lowrise', 'midrise']:
        texture_folder = os.path.join(base_path, subdir)
        if os.path.exists(texture_folder):
            files = os.listdir(texture_folder)
            images = [f for f in files if f.lower().endswith(('.png', '.jpg', '.jpeg'))]
            if images:
                texture_found = os.path.join(texture_folder, images[0])
                print(f"✅ Texture trouvée: {texture_found}")
                break
    
    if not texture_found:
        print("❌ Aucune texture trouvée")
        return
    
    # 3. Créer un matériau TRÈS simple
    mat_name = "TestTextureSimple"
    
    # Supprimer l'ancien matériau s'il existe
    if mat_name in bpy.data.materials:
        bpy.data.materials.remove(bpy.data.materials[mat_name])
    
    # Créer nouveau matériau
    material = bpy.data.materials.new(name=mat_name)
    material.use_nodes = True
    
    # Nettoyer tous les nodes
    material.node_tree.nodes.clear()
    
    # Créer seulement les nodes essentiels
    output = material.node_tree.nodes.new(type='ShaderNodeOutputMaterial')
    principled = material.node_tree.nodes.new(type='ShaderNodeBsdfPrincipled')
    tex_image = material.node_tree.nodes.new(type='ShaderNodeTexImage')
    
    # Charger l'image
    try:
        image = bpy.data.images.load(texture_found)
        tex_image.image = image
        print(f"✅ Image chargée: {image.name}")
    except Exception as e:
        print(f"❌ Erreur chargement: {e}")
        return
    
    # Connecter simplement
    material.node_tree.links.new(tex_image.outputs['Color'], principled.inputs['Base Color'])
    material.node_tree.links.new(principled.outputs['BSDF'], output.inputs['Surface'])
    
    # Appliquer au bâtiment
    building.data.materials.clear()
    building.data.materials.append(material)
    
    print(f"✅ Matériau appliqué à {building.name}")
    print("💡 Changez en mode MATERIAL pour voir la texture")
    
    # Test - changer le mode d'affichage
    for area in bpy.context.screen.areas:
        if area.type == 'VIEW_3D':
            for space in area.spaces:
                if space.type == 'VIEW_3D':
                    space.shading.type = 'MATERIAL'
                    print("✅ Mode changé vers MATERIAL")
    
    print("🎯 Test terminé!")

# Exécuter
test_texture_simple()

# DIAGNOSTIC ULTRA-PRÉCIS CHARGEMENT TEXTURES
# À copier-coller dans la console Blender pour identifier pourquoi les images ne se chargent pas

import bpy
import os
import sys

def diagnostic_ultra_precis():
    print("🔬 DIAGNOSTIC ULTRA-PRÉCIS CHARGEMENT TEXTURES")
    print("=" * 70)
    
    # 1. Accéder au système de textures
    try:
        module = sys.modules['tokyo_city_generator']
        texture_system = module.tokyo_texture_system
        print("✅ Système de textures accessible")
    except Exception as e:
        print(f"❌ Erreur accès système: {e}")
        return
    
    # 2. Vérifier les chemins de textures
    scene = bpy.context.scene
    base_path = scene.tokyo_texture_base_path
    print(f"📁 Chemin de base: {base_path}")
    
    # 3. Test avec skyscrapers spécifiquement
    skyscraper_path = os.path.join(base_path, "skyscrapers")
    print(f"🏗️ Chemin skyscrapers: {skyscraper_path}")
    
    if os.path.exists(skyscraper_path):
        files = os.listdir(skyscraper_path)
        image_files = [f for f in files if f.lower().endswith(('.png', '.jpg', '.jpeg', '.tiff', '.bmp'))]
        print(f"🖼️ Images trouvées: {len(image_files)}")
        
        if image_files:
            print("📋 Liste des images:")
            for img in image_files[:10]:  # Première 10 images
                full_path = os.path.join(skyscraper_path, img)
                size = os.path.getsize(full_path)
                print(f"   - {img} ({size} bytes)")
        else:
            print("❌ Aucune image trouvée dans skyscrapers")
            return
    else:
        print("❌ Dossier skyscrapers n'existe pas")
        return
    
    # 4. TEST MANUEL DE CHARGEMENT D'IMAGE
    print("\n🧪 TEST MANUEL CHARGEMENT IMAGE:")
    
    if image_files:
        test_image_path = os.path.join(skyscraper_path, image_files[0])
        print(f"🎯 Test avec: {test_image_path}")
        
        try:
            # Essayer de charger l'image dans Blender
            test_image = bpy.data.images.load(test_image_path)
            print(f"✅ Image chargée: {test_image.name}")
            print(f"   Taille: {test_image.size[0]}x{test_image.size[1]}")
            print(f"   Chemin: {test_image.filepath}")
            
            # Créer un matériau test avec cette image
            test_mat = bpy.data.materials.new(name="TestImageMaterial")
            test_mat.use_nodes = True
            nodes = test_mat.node_tree.nodes
            
            # Nettoyer les nodes existants
            nodes.clear()
            
            # Créer les nodes
            output = nodes.new(type='ShaderNodeOutputMaterial')
            principled = nodes.new(type='ShaderNodeBsdfPrincipled')
            tex_image = nodes.new(type='ShaderNodeTexImage')
            
            # Assigner l'image
            tex_image.image = test_image
            
            # Connecter les nodes
            test_mat.node_tree.links.new(tex_image.outputs[0], principled.inputs[0])
            test_mat.node_tree.links.new(principled.outputs[0], output.inputs[0])
            
            print("✅ Matériau test créé avec image")
            print(f"   Nodes: {len(nodes)}")
            print(f"   Image assignée: {tex_image.image.name if tex_image.image else 'None'}")
            
            # Nettoyer
            bpy.data.materials.remove(test_mat)
            bpy.data.images.remove(test_image)
            
        except Exception as e:
            print(f"❌ Erreur chargement image: {e}")
    
    # 5. INSPECTER LA MÉTHODE CREATE_ADVANCED_BUILDING_MATERIAL
    print("\n🔍 INSPECTION MÉTHODE CRÉATION:")
    
    try:
        # Accéder au code de la méthode
        method = texture_system.create_advanced_building_material
        print(f"✅ Méthode accessible: {method}")
        
        # Test avec des paramètres spécifiques
        print("🧪 Test création matériau skyscraper...")
        test_material = texture_system.create_advanced_building_material(
            "skyscrapers", 20.0, 50.0, 20.0, "DiagnosticSkyscraper", ""
        )
        
        if test_material:
            print(f"✅ Matériau créé: {test_material.name}")
            print(f"   Use nodes: {test_material.use_nodes}")
            
            if test_material.use_nodes:
                nodes = test_material.node_tree.nodes
                print(f"   Nodes: {len(nodes)}")
                
                # Analyser chaque node
                for node in nodes:
                    print(f"   - {node.type}: {node.name}")
                    if node.type == 'TEX_IMAGE':
                        print(f"     Image: {node.image.name if node.image else 'None'}")
                        if node.image:
                            print(f"     Chemin: {node.image.filepath}")
                            print(f"     Taille: {node.image.size[0]}x{node.image.size[1]}")
                
                # Vérifier les connexions
                links = test_material.node_tree.links
                print(f"   Connexions: {len(links)}")
                for link in links:
                    from_node = link.from_node.type
                    to_node = link.to_node.type
                    print(f"   - {from_node} → {to_node}")
            
            # Nettoyer
            bpy.data.materials.remove(test_material)
        else:
            print("❌ Échec création matériau")
            
    except Exception as e:
        print(f"❌ Erreur inspection: {e}")
        import traceback
        traceback.print_exc()
    
    # 6. VÉRIFIER LES PRÉFÉRENCES BLENDER
    print("\n⚙️ PRÉFÉRENCES BLENDER:")
    prefs = bpy.context.preferences
    
    # Vérifier les chemins d'assets
    if hasattr(prefs, 'filepaths'):
        print(f"📁 Asset Libraries: {len(prefs.filepaths.asset_libraries)}")
        for lib in prefs.filepaths.asset_libraries:
            print(f"   - {lib.name}: {lib.path}")
    
    print("\n" + "=" * 70)
    print("🎯 FIN DIAGNOSTIC ULTRA-PRÉCIS")

# Exécuter
diagnostic_ultra_precis()

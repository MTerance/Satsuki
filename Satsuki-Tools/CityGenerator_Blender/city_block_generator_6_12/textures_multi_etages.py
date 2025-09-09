# SYSTÈME TEXTURES MULTI-ÉTAGES - À copier-coller dans la console Blender
# Ce script applique correctement les textures avec 4 étages par fichier

import bpy
import bmesh
import os
import sys
from mathutils import Vector

def appliquer_textures_multi_etages():
    print("🏢 SYSTÈME TEXTURES MULTI-ÉTAGES")
    print("=" * 60)
    
    # 1. Accéder au système
    try:
        module = sys.modules['tokyo_city_generator']
        texture_system = module.tokyo_texture_system
        scene = bpy.context.scene
        base_path = scene.tokyo_texture_base_path
        print(f"✅ Système accessible, chemin: {base_path}")
    except Exception as e:
        print(f"❌ Erreur: {e}")
        return
    
    # 2. Fonction pour créer un matériau multi-étages
    def creer_materiau_multi_etages(building_type, hauteur_building, nom_building):
        """Crée un matériau avec texture multi-étages correctement mappée"""
        
        # Chemin vers les textures
        texture_folder = os.path.join(base_path, building_type)
        if not os.path.exists(texture_folder):
            print(f"❌ Dossier manquant: {texture_folder}")
            return None
        
        # Trouver une texture
        texture_files = [f for f in os.listdir(texture_folder) 
                        if f.lower().endswith(('.png', '.jpg', '.jpeg'))]
        
        if not texture_files:
            print(f"❌ Aucune texture dans: {texture_folder}")
            return None
        
        texture_file = texture_files[0]  # Prendre la première
        texture_path = os.path.join(texture_folder, texture_file)
        
        print(f"🎨 Texture sélectionnée: {texture_file}")
        
        # Créer le matériau
        mat_name = f"MultiFloor_{building_type}_{nom_building}"
        material = bpy.data.materials.new(name=mat_name)
        material.use_nodes = True
        
        # Nettoyer les nodes existants
        nodes = material.node_tree.nodes
        nodes.clear()
        
        # Créer les nodes nécessaires
        output = nodes.new(type='ShaderNodeOutputMaterial')
        principled = nodes.new(type='ShaderNodeBsdfPrincipled')
        tex_image = nodes.new(type='ShaderNodeTexImage')
        mapping = nodes.new(type='ShaderNodeMapping')
        tex_coord = nodes.new(type='ShaderNodeTexCoord')
        
        # Charger l'image
        try:
            image = bpy.data.images.load(texture_path)
            tex_image.image = image
            print(f"✅ Image chargée: {image.name}")
        except Exception as e:
            print(f"❌ Erreur chargement image: {e}")
            return None
        
        # Calculer le nombre d'étages
        # Chaque texture contient 4 étages
        etages_par_texture = 4
        hauteur_etage = 3.0  # Hauteur standard d'un étage en mètres
        nb_etages_building = max(1, int(hauteur_building / hauteur_etage))
        
        # Calculer la répétition verticale nécessaire
        repetitions_verticales = nb_etages_building / etages_par_texture
        
        print(f"📏 Hauteur bâtiment: {hauteur_building:.1f}m")
        print(f"🏗️ Étages estimés: {nb_etages_building}")
        print(f"🔄 Répétitions texture: {repetitions_verticales:.2f}")
        
        # Configurer le mapping pour répéter la texture
        mapping.inputs['Scale'].default_value = (1.0, repetitions_verticales, 1.0)
        
        # Connecter les nodes
        links = material.node_tree.links
        links.new(tex_coord.outputs['UV'], mapping.inputs['Vector'])
        links.new(mapping.outputs['Vector'], tex_image.inputs['Vector'])
        links.new(tex_image.outputs['Color'], principled.inputs['Base Color'])
        links.new(principled.outputs['BSDF'], output.inputs['Surface'])
        
        # Positionner les nodes pour clarté
        tex_coord.location = (-800, 0)
        mapping.location = (-600, 0)
        tex_image.location = (-400, 0)
        principled.location = (-200, 0)
        output.location = (0, 0)
        
        return material
    
    # 3. Fonction pour appliquer UV mapping correct
    def appliquer_uv_mapping_etages(obj):
        """Applique un UV mapping correct pour les étages"""
        
        if obj.type != 'MESH':
            return
        
        # Passer en mode édition
        bpy.context.view_layer.objects.active = obj
        bpy.ops.object.mode_set(mode='EDIT')
        
        # Créer bmesh depuis mesh
        bm = bmesh.from_mesh(obj.data)
        
        # S'assurer qu'on a une couche UV
        if not bm.loops.layers.uv:
            bm.loops.layers.uv.new()
        
        uv_layer = bm.loops.layers.uv.active
        
        # Pour chaque face, calculer les UV en fonction de la position
        for face in bm.faces:
            if len(face.loops) == 4:  # Face rectangulaire
                # Calculer les coordonnées UV basées sur la position mondiale
                for loop in face.loops:
                    vert = loop.vert
                    world_pos = obj.matrix_world @ vert.co
                    
                    # UV X basé sur la position X (0-1 sur la largeur de la façade)
                    # UV Y basé sur la position Z (hauteur, répété selon les étages)
                    u = (world_pos.x % 10.0) / 10.0  # Normaliser sur 10m de largeur
                    v = world_pos.z / 3.0  # 3m par étage
                    
                    loop[uv_layer].uv = (u, v)
        
        # Mettre à jour le mesh
        bmesh.update_edit_mesh(obj.data)
        bpy.ops.object.mode_set(mode='OBJECT')
        
        print(f"✅ UV mapping appliqué: {obj.name}")
    
    # 4. Traiter tous les bâtiments
    buildings = [obj for obj in bpy.data.objects 
                if 'tokyo' in obj.name.lower() and 'building' in obj.name.lower()]
    
    if not buildings:
        print("❌ Aucun bâtiment trouvé")
        return
    
    print(f"🏢 Traitement de {len(buildings)} bâtiments...")
    
    buildings_avec_textures = 0
    
    for building in buildings:
        try:
            # Déterminer le type de bâtiment
            building_type = "residential"
            if "commercial" in building.name.lower():
                building_type = "commercial"
            elif "skyscraper" in building.name.lower():
                building_type = "skyscrapers"
            elif "lowrise" in building.name.lower():
                building_type = "lowrise"
            elif "midrise" in building.name.lower():
                building_type = "midrise"
            
            # Hauteur du bâtiment
            hauteur = building.dimensions.z
            
            # Créer le matériau multi-étages
            nouveau_materiau = creer_materiau_multi_etages(
                building_type, hauteur, building.name
            )
            
            if nouveau_materiau:
                # Appliquer UV mapping
                appliquer_uv_mapping_etages(building)
                
                # Nettoyer les anciens matériaux et appliquer le nouveau
                building.data.materials.clear()
                building.data.materials.append(nouveau_materiau)
                
                buildings_avec_textures += 1
                print(f"✅ {building.name}: texture multi-étages appliquée")
            else:
                print(f"❌ {building.name}: échec matériau")
                
        except Exception as e:
            print(f"❌ {building.name}: erreur {e}")
    
    print(f"\n🎯 RÉSULTAT: {buildings_avec_textures}/{len(buildings)} bâtiments avec textures multi-étages")
    
    if buildings_avec_textures > 0:
        print("✅ SUCCÈS! Les bâtiments ont maintenant des textures correctement répétées par étage!")
        print("💡 Passez en mode MATERIAL ou RENDERED pour voir le résultat")
        print("🏗️ Chaque fichier texture contient 4 étages et se répète selon la hauteur")
    
    print("\n" + "=" * 60)

# Exécuter
appliquer_textures_multi_etages()

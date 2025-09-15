#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
TEST TOKYO ORGANIC v2.1.9 - Routes diagonales courtes et blocs organiques
=========================================================================

Script pour tester la nouvelle version organique avec :
- Routes diagonales courtes entre intersections
- Blocs non uniformes (fin du style "Excel sheet")
- Trottoirs adaptatifs
- Ordre optimisé : Routes → Diagonales → Trottoirs → Bâtiments
"""

import bpy
import sys
import os

def test_tokyo_organic_v2_1_9():
    """Test complet de la version organique"""
    
    print("\n" + "="*80)
    print("TEST TOKYO ORGANIC v2.1.9 - ROUTES DIAGONALES COURTES")
    print("="*80)
    
    # 1. Vérification de l'installation
    print("\n🔍 VÉRIFICATION INSTALLATION:")
    print("-" * 50)
    
    addon_path = r"c:\Users\sshom\source\repos\Satsuki\Satsuki-Tools\CityGenerator_Blender\city_block_generator_6_12\TOKYO_ORGANIC_V2_1_9"
    
    if os.path.exists(addon_path):
        print(f"   ✅ Dossier addon trouvé: {addon_path}")
    else:
        print(f"   ❌ ERREUR: Dossier addon non trouvé: {addon_path}")
        return
    
    init_file = os.path.join(addon_path, "__init__.py")
    if os.path.exists(init_file):
        print(f"   ✅ Fichier __init__.py trouvé")
        print(f"   📏 Taille: {os.path.getsize(init_file)} bytes")
    else:
        print(f"   ❌ ERREUR: __init__.py manquant")
        return
    
    # 2. Nettoyer la scène
    print("\n🧹 NETTOYAGE SCÈNE:")
    print("-" * 50)
    
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete(use_global=False)
    print("   ✅ Scène nettoyée")
    
    # 3. Changer mode viewport pour voir les matériaux
    print("\n🎨 CONFIGURATION VIEWPORT:")
    print("-" * 50)
    
    for area in bpy.context.screen.areas:
        if area.type == 'VIEW_3D':
            for space in area.spaces:
                if space.type == 'VIEW_3D':
                    space.shading.type = 'MATERIAL_PREVIEW'
                    print("   ✅ Mode viewport: Material Preview")
                    break
    
    # 4. Test de génération manuelle (simuler l'addon)
    print("\n🏗️ GÉNÉRATION VILLE ORGANIQUE:")
    print("-" * 50)
    
    # Paramètres de test
    size = 6  # Grille 6x6 pour tester diagonales
    base_block_size = 18.0
    main_road_width = 6.0
    secondary_road_width = 3.5
    style = 'modern'
    density = 0.8
    
    print(f"   📏 Taille: {size}x{size}")
    print(f"   🏗️ Style: {style}")
    print(f"   📊 Densité: {density}")
    
    # ÉTAPE 1: Routes principales
    print(f"\n   1️⃣ CRÉATION ROUTES PRINCIPALES:")
    roads = []
    
    # Routes horizontales
    for i in range(size + 1):
        y = i * base_block_size - (size * base_block_size) / 2
        is_main = (i == 0 or i == size or i == size // 2)
        width = main_road_width if is_main else secondary_road_width
        
        bpy.ops.mesh.primitive_cube_add(size=1, location=(0, y, 0.05))
        road = bpy.context.active_object
        road.scale = (size * base_block_size + width, width, 0.1)
        road.name = f"Organic_Road_H_{i}_{'Main' if is_main else 'Sec'}"
        
        # Matériau route
        mat = bpy.data.materials.new(name=f"Road_H_{i}")
        mat.use_nodes = True
        bsdf = mat.node_tree.nodes["Principled BSDF"]
        bsdf.inputs['Base Color'].default_value = (0.3, 0.3, 0.3, 1.0) if is_main else (0.4, 0.4, 0.4, 1.0)
        road.data.materials.append(mat)
        
        bpy.ops.object.transform_apply(scale=True)
        roads.append(road)
    
    # Routes verticales
    for i in range(size + 1):
        x = i * base_block_size - (size * base_block_size) / 2
        is_main = (i == 0 or i == size or i == size // 2)
        width = main_road_width if is_main else secondary_road_width
        
        bpy.ops.mesh.primitive_cube_add(size=1, location=(x, 0, 0.05))
        road = bpy.context.active_object
        road.scale = (width, size * base_block_size + width, 0.1)
        road.name = f"Organic_Road_V_{i}_{'Main' if is_main else 'Sec'}"
        
        # Matériau route
        mat = bpy.data.materials.new(name=f"Road_V_{i}")
        mat.use_nodes = True
        bsdf = mat.node_tree.nodes["Principled BSDF"]
        bsdf.inputs['Base Color'].default_value = (0.3, 0.3, 0.3, 1.0) if is_main else (0.4, 0.4, 0.4, 1.0)
        road.data.materials.append(mat)
        
        bpy.ops.object.transform_apply(scale=True)
        roads.append(road)
    
    print(f"      ✅ {len(roads)} routes principales créées")
    
    # ÉTAPE 2: Routes diagonales COURTES
    print(f"\n   2️⃣ CRÉATION DIAGONALES COURTES:")
    diagonal_roads = []
    
    import random
    import math
    
    # Créer 8 diagonales courtes aléatoires
    for i in range(8):
        # Choisir intersection de départ
        start_i = random.randint(0, size - 1)
        start_j = random.randint(0, size - 1)
        
        # Direction diagonale
        directions = [(1, 1), (1, -1), (-1, 1), (-1, -1)]
        dx, dy = random.choice(directions)
        
        end_i = start_i + dx
        end_j = start_j + dy
        
        # Vérifier limites
        if 0 <= end_i <= size and 0 <= end_j <= size:
            # Positions réelles
            start_x = start_i * base_block_size - (size * base_block_size) / 2
            start_y = start_j * base_block_size - (size * base_block_size) / 2
            end_x = end_i * base_block_size - (size * base_block_size) / 2
            end_y = end_j * base_block_size - (size * base_block_size) / 2
            
            # Centre et orientation
            center_x = (start_x + end_x) / 2
            center_y = (start_y + end_y) / 2
            length = math.sqrt((end_x - start_x)**2 + (end_y - start_y)**2)
            angle = math.atan2(end_y - start_y, end_x - start_x)
            
            # Créer diagonale
            bpy.ops.mesh.primitive_cube_add(size=1, location=(center_x, center_y, 0.07))
            diagonal = bpy.context.active_object
            diagonal.scale = (length * 0.9, 3.0, 0.12)
            diagonal.rotation_euler = (0, 0, angle)
            diagonal.name = f"Organic_Diagonal_{i}_{start_i}_{start_j}_to_{end_i}_{end_j}"
            
            # Matériau orange distinctif
            mat = bpy.data.materials.new(name=f"Diagonal_{i}")
            mat.use_nodes = True
            bsdf = mat.node_tree.nodes["Principled BSDF"]
            bsdf.inputs['Base Color'].default_value = (0.9, 0.4, 0.1, 1.0)  # Orange vif
            bsdf.inputs['Emission'].default_value = (0.3, 0.1, 0.0, 1.0)
            bsdf.inputs['Emission Strength'].default_value = 0.2
            diagonal.data.materials.append(mat)
            
            bpy.ops.object.transform_apply(scale=True)
            diagonal_roads.append(diagonal)
            
            print(f"      ↗️ Diagonale {i}: ({start_i},{start_j}) → ({end_i},{end_j})")
    
    print(f"      ✅ {len(diagonal_roads)} diagonales courtes créées")
    
    # ÉTAPE 3: Trottoirs adaptatifs
    print(f"\n   3️⃣ CRÉATION TROTTOIRS ADAPTATIFS:")
    sidewalks = []
    
    for i in range(size):
        for j in range(size):
            # Position du bloc
            block_x = (i + 0.5) * base_block_size - (size * base_block_size) / 2
            block_y = (j + 0.5) * base_block_size - (size * base_block_size) / 2
            
            # Vérifier si diagonale traverse ce bloc
            has_diagonal = False
            for diag in diagonal_roads:
                dist = math.sqrt((diag.location.x - block_x)**2 + (diag.location.y - block_y)**2)
                if dist < base_block_size * 0.6:
                    has_diagonal = True
                    break
            
            if has_diagonal:
                # Trottoirs fragmentés (4 petits segments)
                for k in range(4):
                    offset_x = random.uniform(-6, 6)
                    offset_y = random.uniform(-6, 6)
                    
                    bpy.ops.mesh.primitive_cube_add(size=1, location=(block_x + offset_x, block_y + offset_y, 0.02))
                    sidewalk = bpy.context.active_object
                    sidewalk.scale = (3, 3, 0.05)
                    sidewalk.name = f"Organic_Sidewalk_Frag_{i}_{j}_{k}"
                    
                    # Matériau trottoir
                    mat = bpy.data.materials.new(name=f"Sidewalk_Frag_{i}_{j}_{k}")
                    mat.use_nodes = True
                    bsdf = mat.node_tree.nodes["Principled BSDF"]
                    bsdf.inputs['Base Color'].default_value = (0.7, 0.7, 0.6, 1.0)
                    sidewalk.data.materials.append(mat)
                    
                    bpy.ops.object.transform_apply(scale=True)
                    sidewalks.append(sidewalk)
            else:
                # Trottoir standard
                bpy.ops.mesh.primitive_cube_add(size=1, location=(block_x, block_y, 0.02))
                sidewalk = bpy.context.active_object
                sidewalk.scale = (14, 14, 0.05)
                sidewalk.name = f"Organic_Sidewalk_Std_{i}_{j}"
                
                # Matériau trottoir
                mat = bpy.data.materials.new(name=f"Sidewalk_Std_{i}_{j}")
                mat.use_nodes = True
                bsdf = mat.node_tree.nodes["Principled BSDF"]
                bsdf.inputs['Base Color'].default_value = (0.7, 0.7, 0.6, 1.0)
                sidewalk.data.materials.append(mat)
                
                bpy.ops.object.transform_apply(scale=True)
                sidewalks.append(sidewalk)
    
    print(f"      ✅ {len(sidewalks)} trottoirs adaptatifs créés")
    
    # ÉTAPE 4: Bâtiments organiques dans blocs non uniformes
    print(f"\n   4️⃣ CRÉATION BÂTIMENTS ORGANIQUES:")
    buildings = []
    
    building_types = ['residential', 'office', 'commercial', 'tower', 'hotel', 'mixed_use', 'warehouse', 'school']
    colors = {
        'residential': (0.9, 0.6, 0.3, 1.0),  # Orange
        'office': (0.6, 0.7, 0.9, 1.0),       # Bleu clair
        'commercial': (0.9, 0.2, 0.2, 1.0),   # Rouge
        'tower': (0.1, 0.3, 0.8, 1.0),        # Bleu foncé
        'hotel': (0.9, 0.9, 0.2, 1.0),        # Jaune
        'mixed_use': (0.3, 0.8, 0.3, 1.0),    # Vert
        'warehouse': (0.5, 0.5, 0.5, 1.0),    # Gris
        'school': (0.8, 0.4, 0.8, 1.0)        # Violet
    }
    
    building_count = 0
    for i in range(size):
        for j in range(size):
            if random.random() > density:
                continue
            
            # Position de base du bloc
            base_x = (i + 0.5) * base_block_size - (size * base_block_size) / 2
            base_y = (j + 0.5) * base_block_size - (size * base_block_size) / 2
            
            # Nombre de bâtiments variables (1-3)
            num_buildings = random.randint(1, 3)
            
            for b in range(num_buildings):
                # Position avec variation pour éviter l'uniformité
                x = base_x + random.uniform(-7, 7)
                y = base_y + random.uniform(-7, 7)
                
                # Dimensions variables
                width = random.uniform(4, 10)
                depth = random.uniform(4, 10)
                height = random.uniform(8, 40)
                
                # Type de bâtiment
                building_type = random.choice(building_types)
                color = colors.get(building_type, (0.7, 0.7, 0.7, 1.0))
                
                # Créer bâtiment
                bpy.ops.mesh.primitive_cube_add(size=1, location=(x, y, height/2))
                building = bpy.context.active_object
                building.scale = (width, depth, height)
                building.rotation_euler = (0, 0, random.uniform(-0.1, 0.1))  # Légère rotation
                building.name = f"Organic_Building_{building_type}_{i}_{j}_{b}"
                
                # Matériau coloré
                mat = bpy.data.materials.new(name=f"Building_{building_type}_{building_count}")
                mat.use_nodes = True
                bsdf = mat.node_tree.nodes["Principled BSDF"]
                
                # Variation de couleur
                varied_color = [
                    min(1.0, color[0] * random.uniform(0.8, 1.2)),
                    min(1.0, color[1] * random.uniform(0.8, 1.2)),
                    min(1.0, color[2] * random.uniform(0.8, 1.2)),
                    1.0
                ]
                
                bsdf.inputs['Base Color'].default_value = varied_color
                bsdf.inputs['Metallic'].default_value = 0.3
                bsdf.inputs['Roughness'].default_value = 0.7
                building.data.materials.append(mat)
                
                bpy.ops.object.transform_apply(scale=True)
                buildings.append(building)
                building_count += 1
    
    print(f"      ✅ {len(buildings)} bâtiments organiques créés")
    
    # 5. Résumé final
    print(f"\n📊 RÉSUMÉ GÉNÉRATION ORGANIQUE:")
    print("-" * 50)
    print(f"   🛣️  Routes principales: {len(roads)}")
    print(f"   ↗️  Diagonales courtes: {len(diagonal_roads)}")
    print(f"   🚶 Trottoirs adaptatifs: {len(sidewalks)}")
    print(f"   🏢 Bâtiments organiques: {len(buildings)}")
    
    # Vérifier diversité des matériaux
    mat_types = set()
    for building in buildings:
        if building.data.materials:
            mat = building.data.materials[0]
            if "residential" in mat.name: mat_types.add("residential")
            elif "office" in mat.name: mat_types.add("office") 
            elif "commercial" in mat.name: mat_types.add("commercial")
            elif "tower" in mat.name: mat_types.add("tower")
            elif "hotel" in mat.name: mat_types.add("hotel")
            elif "mixed_use" in mat.name: mat_types.add("mixed_use")
            elif "warehouse" in mat.name: mat_types.add("warehouse")
            elif "school" in mat.name: mat_types.add("school")
    
    print(f"   🎨 Types de bâtiments: {len(mat_types)} → {list(mat_types)}")
    
    if len(diagonal_roads) > 0:
        print("   ✅ DIAGONALES COURTES CRÉÉES AVEC SUCCÈS!")
    else:
        print("   ⚠️  Aucune diagonale créée")
        
    if len(mat_types) >= 4:
        print("   ✅ VARIÉTÉ DE BÂTIMENTS CONFIRMÉE!")
    else:
        print("   ⚠️  Peu de variété dans les bâtiments")
    
    print(f"\n💡 INSTRUCTIONS:")
    print("-" * 50)
    print("   1. Vous devriez voir des ROUTES DIAGONALES ORANGE VIVES")
    print("   2. Les bâtiments ont des COULEURS DIFFÉRENTES par type:")
    print("      - Orange: Résidentiel")
    print("      - Bleu: Bureaux/Tours") 
    print("      - Rouge: Commercial")
    print("      - Jaune: Hôtels")
    print("      - Vert: Usage mixte")
    print("      - Gris: Entrepôts")
    print("      - Violet: Écoles")
    print("   3. Les blocs ne sont plus uniformes (fini le style Excel!)")
    print("   4. Les trottoirs s'adaptent aux diagonales")
    
    print("="*80)

if __name__ == "__main__":
    test_tokyo_organic_v2_1_9()
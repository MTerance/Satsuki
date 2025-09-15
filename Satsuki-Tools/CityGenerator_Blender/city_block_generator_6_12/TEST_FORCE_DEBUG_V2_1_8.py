#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
TEST FORCE AVEC DEBUG - Tokyo City Generator v2.1.8
====================================================

Script pour forcer la génération avec des prints de debug
pour tracer exactement ce qui se passe.
"""

import bpy
import random
import math

def test_force_avec_debug():
    """Test avec debug prints pour tracer les problèmes"""
    
    print("\n" + "="*70)
    print("TEST FORCE AVEC DEBUG - Tokyo v2.1.8")
    print("="*70)
    
    # Nettoyer la scène
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete(use_global=False)
    
    # Paramètres de test
    size = 7  # Grille 7x7 pour forcer les diagonales
    block_size = 20.0
    main_road_width = 6.0
    secondary_road_width = 3.2
    style = 'modern'
    density = 0.8
    use_materials = True
    
    print(f"\n🏗️  GÉNÉRATION VILLE {size}x{size}")
    print(f"   Block size: {block_size}")
    print(f"   Style: {style}")
    print(f"   Matériaux: {use_materials}")
    
    # Test de la condition diagonale
    print(f"\n🔍 TEST CONDITION DIAGONALE:")
    print(f"   size = {size}")
    print(f"   size >= 6 ? {size >= 6}")
    
    if size >= 6:
        print("   ✅ CONDITION DIAGONALE REMPLIE - Diagonale devrait être créée")
    else:
        print("   ❌ CONDITION DIAGONALE NON REMPLIE")
    
    # Simuler la création de routes avec diagonale
    print(f"\n🛣️  CRÉATION ROUTES:")
    roads = []
    
    # Routes principales horizontales
    for i in range(size + 1):
        y = -size * block_size / 2 + i * block_size
        x_start = -size * block_size / 2
        x_end = size * block_size / 2
        
        bpy.ops.mesh.primitive_cube_add(size=1, location=((x_start + x_end) / 2, y, 0.05))
        road = bpy.context.active_object
        road.scale = (size * block_size, main_road_width, 0.1)
        road.name = f"Tokyo_Road_Main_H_{i}"
        roads.append(road)
    
    # Routes principales verticales
    for i in range(size + 1):
        x = -size * block_size / 2 + i * block_size
        y_start = -size * block_size / 2
        y_end = size * block_size / 2
        
        bpy.ops.mesh.primitive_cube_add(size=1, location=(x, (y_start + y_end) / 2, 0.05))
        road = bpy.context.active_object
        road.scale = (main_road_width, size * block_size, 0.1)
        road.name = f"Tokyo_Road_Main_V_{i}"
        roads.append(road)
    
    print(f"   ✅ Routes principales créées: {len(roads)}")
    
    # CRÉATION DIAGONALE FORCÉE
    print(f"\n↗️  CRÉATION DIAGONALE FORCÉE:")
    if size >= 6:
        print("   🔨 Création diagonale...")
        
        start_x = -size * block_size / 2
        start_y = -size * block_size / 2
        end_x = size * block_size / 2
        end_y = size * block_size / 2
        
        center_x = (start_x + end_x) / 2
        center_y = (start_y + end_y) / 2
        length = math.sqrt((end_x - start_x)**2 + (end_y - start_y)**2)
        angle = math.atan2(end_y - start_y, end_x - start_x)
        
        print(f"   📍 Position: ({center_x:.2f}, {center_y:.2f})")
        print(f"   📏 Longueur: {length:.2f}")
        print(f"   🔄 Angle: {angle * 180 / math.pi:.1f}°")
        
        bpy.ops.mesh.primitive_cube_add(size=1, location=(center_x, center_y, 0.05))
        diagonal_road = bpy.context.active_object
        diagonal_road.scale = (length, 4.0, 0.1)  # Largeur visible
        diagonal_road.rotation_euler = (0, 0, angle)
        diagonal_road.name = "Tokyo_Road_Diagonal_FORCE"
        bpy.ops.object.transform_apply(scale=True)
        
        # Matériau rouge pour être visible
        mat = bpy.data.materials.new(name="Diagonal_Rouge")
        mat.use_nodes = True
        bsdf = mat.node_tree.nodes["Principled BSDF"]
        bsdf.inputs['Base Color'].default_value = (1.0, 0.0, 0.0, 1.0)  # Rouge vif
        diagonal_road.data.materials.append(mat)
        
        roads.append(diagonal_road)
        print("   ✅ DIAGONALE CRÉÉE EN ROUGE VIF")
    
    # CRÉATION BÂTIMENTS AVEC DEBUG
    print(f"\n🏢 CRÉATION BÂTIMENTS AVEC DEBUG:")
    buildings = []
    types_de_batiments = ['tower', 'office', 'residential', 'commercial', 'hotel', 'mixed_use', 'warehouse', 'school']
    
    # Créer quelques bâtiments de test avec types différents
    for i, building_type in enumerate(types_de_batiments[:6]):  # 6 premiers types
        
        # Position de test
        x = -40 + i * 16
        y = 0
        z = 0
        
        # Hauteur selon le type
        height_map = {
            'tower': 50,
            'office': 30,
            'residential': 15,
            'commercial': 8,
            'hotel': 25,
            'mixed_use': 20,
            'warehouse': 6,
            'school': 10
        }
        
        height = height_map.get(building_type, 15)
        
        print(f"\n   🏗️  Bâtiment {i+1}: {building_type}")
        print(f"      Position: ({x}, {y}, {z})")
        print(f"      Hauteur: {height}m")
        
        # Créer le bâtiment
        bpy.ops.mesh.primitive_cube_add(size=1, location=(x, y, z + height/2))
        building = bpy.context.active_object
        building.scale = (8, 8, height)
        building.name = f"Tokyo_Building_{building_type}_{i}"
        bpy.ops.object.transform_apply(scale=True)
        
        # DEBUG MATÉRIAU
        print(f"      🎨 Application matériau type: {building_type}")
        
        # Couleurs distinctes par type pour debug
        couleurs_debug = {
            'tower': (0.2, 0.4, 0.8, 1.0),      # Bleu foncé
            'office': (0.5, 0.6, 0.8, 1.0),     # Bleu clair
            'residential': (0.8, 0.7, 0.6, 1.0), # Beige
            'commercial': (0.9, 0.3, 0.2, 1.0),  # Rouge
            'hotel': (0.9, 0.9, 0.8, 1.0),      # Crème
            'mixed_use': (0.6, 0.6, 0.7, 1.0),  # Gris
            'warehouse': (0.4, 0.4, 0.4, 1.0),  # Gris foncé
            'school': (0.9, 0.8, 0.6, 1.0)      # Beige institutionnel
        }
        
        couleur = couleurs_debug.get(building_type, (0.7, 0.7, 0.7, 1.0))
        
        # Créer matériau debug distinctif
        mat = bpy.data.materials.new(name=f"DEBUG_{building_type}_{height}m")
        mat.use_nodes = True
        bsdf = mat.node_tree.nodes["Principled BSDF"]
        bsdf.inputs['Base Color'].default_value = couleur
        bsdf.inputs['Roughness'].default_value = 0.7
        
        building.data.materials.append(mat)
        buildings.append(building)
        
        print(f"      ✅ Matériau appliqué: RGB({couleur[0]:.2f}, {couleur[1]:.2f}, {couleur[2]:.2f})")
    
    print(f"\n📊 RÉSUMÉ GÉNÉRATION:")
    print(f"   🏢 Bâtiments créés: {len(buildings)}")
    print(f"   🛣️  Routes créées: {len(roads)}")
    print(f"   ↗️  Diagonales: {len([r for r in roads if 'Diagonal' in r.name])}")
    
    print(f"\n🎨 CHANGEZ LE MODE DE VUE EN 'Material Preview' pour voir les couleurs!")
    print("="*70)

if __name__ == "__main__":
    test_force_avec_debug()
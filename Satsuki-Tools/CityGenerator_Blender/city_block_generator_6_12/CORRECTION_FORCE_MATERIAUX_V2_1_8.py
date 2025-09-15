#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
CORRECTION FORCE MATÉRIAUX - Tokyo City Generator v2.1.8
=========================================================

Script pour forcer l'application correcte des matériaux
et corriger les problèmes de visibilité.
"""

import bpy
import random

def corriger_materiaux_force():
    """Corriger les matériaux de tous les bâtiments existants"""
    
    print("\n" + "="*70)
    print("CORRECTION FORCE MATÉRIAUX - Tokyo v2.1.8")
    print("="*70)
    
    # 1. Changer le mode de vue pour voir les matériaux
    print("\n🎨 CHANGEMENT MODE VIEWPORT:")
    print("-" * 40)
    
    for area in bpy.context.screen.areas:
        if area.type == 'VIEW_3D':
            for space in area.spaces:
                if space.type == 'VIEW_3D':
                    space.shading.type = 'MATERIAL_PREVIEW'
                    print("   ✅ Mode viewport changé en Material Preview")
                    break
    
    # 2. Trouver tous les bâtiments
    buildings = [obj for obj in bpy.data.objects if "Tokyo_Building" in obj.name or "Building" in obj.name]
    
    print(f"\n🏢 BÂTIMENTS TROUVÉS: {len(buildings)}")
    print("-" * 40)
    
    if not buildings:
        print("   ❌ AUCUN BÂTIMENT TROUVÉ!")
        return
    
    # 3. Types de bâtiments et couleurs distinctives
    types_de_batiments = ['tower', 'office', 'residential', 'commercial', 'hotel', 'mixed_use', 'warehouse', 'school']
    
    couleurs_distinctives = {
        'tower': (0.2, 0.4, 0.9, 1.0),       # Bleu électrique
        'office': (0.5, 0.6, 0.8, 1.0),      # Bleu bureau
        'residential': (0.9, 0.7, 0.5, 1.0), # Orange résidentiel
        'commercial': (1.0, 0.2, 0.2, 1.0),  # Rouge commercial
        'hotel': (0.9, 0.9, 0.2, 1.0),       # Jaune luxe
        'mixed_use': (0.6, 0.8, 0.6, 1.0),   # Vert mixte
        'warehouse': (0.4, 0.4, 0.4, 1.0),   # Gris industriel
        'school': (0.8, 0.5, 0.9, 1.0)       # Violet institutionnel
    }
    
    # 4. Appliquer des matériaux distinctifs
    print("\n🎨 APPLICATION MATÉRIAUX DISTINCTIFS:")
    print("-" * 40)
    
    for i, building in enumerate(buildings):
        # Assigner un type cyclique
        building_type = types_de_batiments[i % len(types_de_batiments)]
        couleur = couleurs_distinctives[building_type]
        
        # Supprimer les anciens matériaux
        building.data.materials.clear()
        
        # Créer nouveau matériau distinctif
        mat_name = f"FORCE_{building_type}_{i}"
        mat = bpy.data.materials.new(name=mat_name)
        mat.use_nodes = True
        
        # Node setup
        bsdf = mat.node_tree.nodes["Principled BSDF"]
        bsdf.inputs['Base Color'].default_value = couleur
        bsdf.inputs['Metallic'].default_value = 0.3
        bsdf.inputs['Roughness'].default_value = 0.6
        
        # Ajouter émission pour rendre plus visible
        bsdf.inputs['Emission'].default_value = (couleur[0] * 0.1, couleur[1] * 0.1, couleur[2] * 0.1, 1.0)
        bsdf.inputs['Emission Strength'].default_value = 0.2
        
        # Appliquer le matériau
        building.data.materials.append(mat)
        
        print(f"   🏗️  {building.name}: {building_type} → RGB({couleur[0]:.1f}, {couleur[1]:.1f}, {couleur[2]:.1f})")
    
    # 5. Créer une diagonale visible si manquante
    print("\n↗️  VÉRIFICATION DIAGONALES:")
    print("-" * 40)
    
    diagonals = [obj for obj in bpy.data.objects if "Diagonal" in obj.name]
    
    if not diagonals:
        print("   🔨 Création diagonale de force...")
        
        # Calculer la taille de la grille
        roads_h = [obj for obj in bpy.data.objects if "Road_Main_H" in obj.name or "Road_H" in obj.name]
        size = len(roads_h) - 1 if roads_h else 7
        block_size = 20.0
        
        # Créer diagonale visible
        start_x = -size * block_size / 2
        start_y = -size * block_size / 2
        end_x = size * block_size / 2
        end_y = size * block_size / 2
        
        center_x = (start_x + end_x) / 2
        center_y = (start_y + end_y) / 2
        length = ((end_x - start_x)**2 + (end_y - start_y)**2)**0.5
        angle = 0.785398  # 45 degrés en radians
        
        bpy.ops.mesh.primitive_cube_add(size=1, location=(center_x, center_y, 0.1))
        diagonal = bpy.context.active_object
        diagonal.scale = (length, 5.0, 0.2)  # Large et visible
        diagonal.rotation_euler = (0, 0, angle)
        diagonal.name = "Tokyo_Diagonal_FORCE"
        
        # Matériau rouge vif pour la diagonale
        mat_diag = bpy.data.materials.new(name="Diagonal_ROUGE_FORCE")
        mat_diag.use_nodes = True
        bsdf_diag = mat_diag.node_tree.nodes["Principled BSDF"]
        bsdf_diag.inputs['Base Color'].default_value = (1.0, 0.0, 0.0, 1.0)  # Rouge pur
        bsdf_diag.inputs['Emission'].default_value = (1.0, 0.0, 0.0, 1.0)
        bsdf_diag.inputs['Emission Strength'].default_value = 0.5
        diagonal.data.materials.append(mat_diag)
        
        bpy.ops.object.transform_apply(scale=True)
        print("   ✅ Diagonale rouge créée de force!")
    else:
        print(f"   ✅ {len(diagonals)} diagonale(s) existante(s)")
        
        # Rendre les diagonales plus visibles
        for diag in diagonals:
            diag.data.materials.clear()
            mat_diag = bpy.data.materials.new(name="Diagonal_VISIBLE")
            mat_diag.use_nodes = True
            bsdf_diag = mat_diag.node_tree.nodes["Principled BSDF"]
            bsdf_diag.inputs['Base Color'].default_value = (1.0, 0.0, 0.0, 1.0)
            bsdf_diag.inputs['Emission'].default_value = (0.5, 0.0, 0.0, 1.0)
            bsdf_diag.inputs['Emission Strength'].default_value = 0.3
            diag.data.materials.append(mat_diag)
    
    # 6. Vérification finale
    print("\n📊 VÉRIFICATION FINALE:")
    print("-" * 40)
    
    materiaux_uniques = set()
    for building in buildings:
        if building.data.materials:
            mat = building.data.materials[0]
            if mat.use_nodes:
                bsdf = mat.node_tree.nodes.get("Principled BSDF")
                if bsdf:
                    color = bsdf.inputs['Base Color'].default_value
                    color_str = f"{color[0]:.1f}-{color[1]:.1f}-{color[2]:.1f}"
                    materiaux_uniques.add(color_str)
    
    print(f"   🎨 Couleurs uniques: {len(materiaux_uniques)}")
    print(f"   🏢 Bâtiments traités: {len(buildings)}")
    
    if len(materiaux_uniques) >= 3:
        print("   ✅ VARIÉTÉ DE COULEURS CONFIRMÉE")
    else:
        print("   ⚠️  Peu de variété - Vérifiez le mode Material Preview")
    
    print("\n💡 INSTRUCTIONS:")
    print("-" * 40)
    print("   1. Le mode viewport est maintenant en 'Material Preview'")
    print("   2. Vous devriez voir des bâtiments en couleurs distinctes:")
    print("      - Bleu: Tours/Bureaux")
    print("      - Orange: Résidentiel") 
    print("      - Rouge: Commercial")
    print("      - Jaune: Hôtels")
    print("      - Vert: Usage mixte")
    print("      - Gris: Entrepôts")
    print("      - Violet: Écoles")
    print("   3. La diagonale (si présente) est maintenant ROUGE VIF")
    
    print("="*70)

if __name__ == "__main__":
    corriger_materiaux_force()
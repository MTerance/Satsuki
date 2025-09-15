#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
DIAGNOSTIC MATERIAUX ET DIAGONALES - Tokyo City Generator v2.1.8
================================================================

Script pour diagnostiquer pourquoi les matériaux ne sont pas visibles 
et les diagonales ne se génèrent pas correctement.
"""

import bpy
import bmesh
import os
import sys

def diagnostic_materiaux_diagonales():
    """Diagnostic complet des matériaux et diagonales"""
    
    print("\n" + "="*70)
    print("DIAGNOSTIC MATERIAUX ET DIAGONALES - Tokyo v2.1.8")
    print("="*70)
    
    # 1. Vérifier les objets dans la scène
    print("\n1. OBJETS DANS LA SCENE:")
    print("-" * 40)
    
    buildings = [obj for obj in bpy.data.objects if "Tokyo_Building" in obj.name]
    roads = [obj for obj in bpy.data.objects if "Tokyo_Road" in obj.name]
    diagonals = [obj for obj in bpy.data.objects if "Diagonal" in obj.name]
    
    print(f"   🏢 Bâtiments trouvés: {len(buildings)}")
    print(f"   🛣️  Routes trouvées: {len(roads)}")
    print(f"   ↗️  Diagonales trouvées: {len(diagonals)}")
    
    # 2. Analyser les matériaux des bâtiments
    print("\n2. MATERIAUX DES BATIMENTS:")
    print("-" * 40)
    
    if not buildings:
        print("   ❌ AUCUN BATIMENT TROUVÉ - Génération échouée!")
        return
    
    building_materials = {}
    for building in buildings:
        if building.data.materials:
            mat_name = building.data.materials[0].name
            if mat_name not in building_materials:
                building_materials[mat_name] = []
            building_materials[mat_name].append(building.name)
    
    print(f"   📊 Types de matériaux différents: {len(building_materials)}")
    
    for mat_name, building_list in building_materials.items():
        print(f"   🎨 {mat_name}: {len(building_list)} bâtiments")
        
        # Analyser les couleurs
        mat = bpy.data.materials.get(mat_name)
        if mat and mat.use_nodes:
            bsdf = mat.node_tree.nodes.get("Principled BSDF")
            if bsdf:
                color = bsdf.inputs['Base Color'].default_value
                metallic = bsdf.inputs['Metallic'].default_value
                roughness = bsdf.inputs['Roughness'].default_value
                print(f"      RGB: ({color[0]:.2f}, {color[1]:.2f}, {color[2]:.2f})")
                print(f"      Metallic: {metallic:.2f}, Roughness: {roughness:.2f}")
    
    # 3. Vérifier les types de bâtiments attendus
    print("\n3. TYPES DE BATIMENTS ATTENDUS:")
    print("-" * 40)
    
    types_attendus = ['tower', 'office', 'residential', 'commercial', 'hotel', 'mixed_use', 'warehouse', 'school']
    types_trouvés = set()
    
    for mat_name in building_materials.keys():
        for type_attendu in types_attendus:
            if type_attendu.title() in mat_name or type_attendu.lower() in mat_name.lower():
                types_trouvés.add(type_attendu)
    
    print(f"   ✅ Types trouvés: {list(types_trouvés)}")
    print(f"   ❌ Types manquants: {[t for t in types_attendus if t not in types_trouvés]}")
    
    # 4. Analyser les diagonales
    print("\n4. ROUTES DIAGONALES:")
    print("-" * 40)
    
    if diagonals:
        for diag in diagonals:
            print(f"   ↗️  {diag.name}")
            print(f"      Position: ({diag.location.x:.2f}, {diag.location.y:.2f}, {diag.location.z:.2f})")
            print(f"      Échelle: ({diag.scale.x:.2f}, {diag.scale.y:.2f}, {diag.scale.z:.2f})")
            print(f"      Rotation: {diag.rotation_euler.z * 180 / 3.14159:.1f}°")
    else:
        print("   ❌ AUCUNE DIAGONALE TROUVÉE")
        
        # Vérifier la grille
        grid_size = len([obj for obj in bpy.data.objects if "Tokyo_Road_Main_H" in obj.name])
        print(f"   📏 Taille de grille détectée: {grid_size}x{grid_size}")
        if grid_size >= 6:
            print("   ⚠️  Grille assez grande pour diagonales - Vérifier le code!")
        else:
            print("   ℹ️  Grille trop petite pour diagonales (minimum 6x6)")
    
    # 5. Mode de rendu actuel
    print("\n5. MODE DE RENDU:")
    print("-" * 40)
    
    viewport_shading = bpy.context.space_data.shading.type if hasattr(bpy.context, 'space_data') else "UNKNOWN"
    print(f"   🎨 Mode viewport: {viewport_shading}")
    print("   💡 Pour voir les matériaux, utilisez:")
    print("      - Material Preview (icône sphère)")
    print("      - Rendered (icône sphère blanche)")
    
    # 6. Vérifier les couleurs par défaut
    print("\n6. VERIFICATION COULEURS:")
    print("-" * 40)
    
    if building_materials:
        couleurs_identiques = True
        première_couleur = None
        
        for mat_name in building_materials.keys():
            mat = bpy.data.materials.get(mat_name)
            if mat and mat.use_nodes:
                bsdf = mat.node_tree.nodes.get("Principled BSDF")
                if bsdf:
                    color = bsdf.inputs['Base Color'].default_value[:3]
                    if première_couleur is None:
                        première_couleur = color
                    elif abs(color[0] - première_couleur[0]) > 0.1 or \
                         abs(color[1] - première_couleur[1]) > 0.1 or \
                         abs(color[2] - première_couleur[2]) > 0.1:
                        couleurs_identiques = False
                        break
        
        if couleurs_identiques:
            print("   ❌ PROBLÈME: Toutes les couleurs sont similaires!")
            print("   🔧 Solution: Vérifier la fonction apply_building_material_by_type")
        else:
            print("   ✅ Couleurs variées détectées")
    
    # 7. Instructions de correction
    print("\n7. ACTIONS RECOMMANDÉES:")
    print("-" * 40)
    
    if len(building_materials) < 3:
        print("   🔧 Peu de variété de matériaux - Vérifier:")
        print("      - Les types de bâtiments assignés")
        print("      - La fonction apply_building_material_by_type")
    
    if not diagonals and grid_size >= 6:
        print("   🔧 Diagonales manquantes - Vérifier:")
        print("      - La condition 'if size >= 6' dans generate_city")
        print("      - La fonction add_single_diagonal")
    
    print("\n   📋 Changez le mode de vue en 'Material Preview' pour voir les couleurs!")
    print("="*70)

if __name__ == "__main__":
    diagnostic_materiaux_diagonales()
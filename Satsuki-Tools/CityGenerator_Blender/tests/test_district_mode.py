#!/usr/bin/env python3
"""
Script de test pour valider le mode district du City Block Generator.
Ce script doit être exécuté dans Blender avec l'addon installé.
"""

import bpy
import sys
import os

# Ajouter le dossier de l'addon au chemin Python si nécessaire
addon_dir = r"C:\Users\sshom\Documents\assets\Tools\city_block_generator"
if addon_dir not in sys.path:
    sys.path.append(addon_dir)

def test_district_mode():
    """Test du mode district avec différentes configurations."""
    
    print("=" * 60)
    print("DÉBUT DU TEST DU MODE DISTRICT")
    print("=" * 60)
    
    # Vérifier que l'addon est activé
    if 'city_block_generator' not in bpy.context.preferences.addons:
        print("ERREUR: L'addon City Block Generator n'est pas activé !")
        return False
    
    # Nettoyer la scène
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete(use_global=False)
    
    # Configurer les propriétés pour le test
    scene = bpy.context.scene
    
    # S'assurer que les propriétés existent
    if not hasattr(scene, 'citygen_props'):
        print("ERREUR: Les propriétés citygen_props n'existent pas !")
        return False
    
    props = scene.citygen_props
    
    # Configuration 1: Mode district avec grille moyenne
    print("\n--- TEST 1: Mode district activé, grille 6x6 ---")
    props.width = 6
    props.length = 6
    props.max_floors = 12
    props.shape_mode = 'AUTO'
    props.block_variety = 'HIGH'
    props.base_block_size = 15.0
    props.district_mode = True
    props.commercial_ratio = 0.3
    props.residential_ratio = 0.5
    props.industrial_ratio = 0.2
    
    print(f"Configuration:")
    print(f"  - Grille: {props.width}x{props.length}")
    print(f"  - Mode district: {props.district_mode}")
    print(f"  - Variété: {props.block_variety}")
    print(f"  - Taille de base: {props.base_block_size}")
    print(f"  - Ratios: C={props.commercial_ratio}, R={props.residential_ratio}, I={props.industrial_ratio}")
    
    # Générer le quartier
    try:
        result = bpy.ops.citygen.generate_city()
        if result == {'FINISHED'}:
            print("✓ Génération réussie !")
            
            # Analyser les objets créés
            analyze_generated_objects()
        else:
            print("✗ Échec de la génération")
            return False
    except Exception as e:
        print(f"✗ Erreur lors de la génération: {e}")
        return False
    
    # Pause pour permettre l'observation
    print("\n--- Appuyez sur Entrée pour continuer vers le test 2 ---")
    input()
    
    # Nettoyer pour le test suivant
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete(use_global=False)
    
    # Configuration 2: Mode district avec grille plus grande
    print("\n--- TEST 2: Mode district, grille 8x8, ratios différents ---")
    props.width = 8
    props.length = 8
    props.max_floors = 20
    props.block_variety = 'EXTREME'
    props.base_block_size = 12.0
    props.district_mode = True
    props.commercial_ratio = 0.4
    props.residential_ratio = 0.4
    props.industrial_ratio = 0.2
    
    print(f"Configuration:")
    print(f"  - Grille: {props.width}x{props.length}")
    print(f"  - Variété: {props.block_variety}")
    print(f"  - Taille de base: {props.base_block_size}")
    print(f"  - Ratios: C={props.commercial_ratio}, R={props.residential_ratio}, I={props.industrial_ratio}")
    
    try:
        result = bpy.ops.citygen.generate_city()
        if result == {'FINISHED'}:
            print("✓ Génération réussie !")
            analyze_generated_objects()
        else:
            print("✗ Échec de la génération")
            return False
    except Exception as e:
        print(f"✗ Erreur lors de la génération: {e}")
        return False
    
    print("\n--- Appuyez sur Entrée pour continuer vers le test 3 ---")
    input()
    
    # Nettoyer pour le test suivant
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete(use_global=False)
    
    # Configuration 3: Comparaison avec mode district désactivé
    print("\n--- TEST 3: Mode district DÉSACTIVÉ pour comparaison ---")
    props.width = 6
    props.length = 6
    props.max_floors = 12
    props.block_variety = 'HIGH'
    props.base_block_size = 15.0
    props.district_mode = False
    
    print(f"Configuration:")
    print(f"  - Grille: {props.width}x{props.length}")
    print(f"  - Mode district: {props.district_mode}")
    print(f"  - Variété: {props.block_variety}")
    print(f"  - Taille de base: {props.base_block_size}")
    
    try:
        result = bpy.ops.citygen.generate_city()
        if result == {'FINISHED'}:
            print("✓ Génération réussie !")
            analyze_generated_objects()
        else:
            print("✗ Échec de la génération")
            return False
    except Exception as e:
        print(f"✗ Erreur lors de la génération: {e}")
        return False
    
    print("\n" + "=" * 60)
    print("TESTS TERMINÉS AVEC SUCCÈS !")
    print("=" * 60)
    return True

def analyze_generated_objects():
    """Analyse les objets générés pour comprendre la structure."""
    
    print("\nAnalyse des objets générés:")
    
    buildings = [obj for obj in bpy.context.scene.objects if 'building' in obj.name.lower()]
    roads = [obj for obj in bpy.context.scene.objects if 'road' in obj.name.lower()]
    sidewalks = [obj for obj in bpy.context.scene.objects if 'sidewalk' in obj.name.lower()]
    
    print(f"  - Bâtiments: {len(buildings)}")
    print(f"  - Routes: {len(roads)}")
    print(f"  - Trottoirs: {len(sidewalks)}")
    
    if buildings:
        # Analyser la variété des tailles
        sizes = []
        heights = []
        for building in buildings:
            if building.dimensions:
                size = max(building.dimensions.x, building.dimensions.y)
                height = building.dimensions.z
                sizes.append(size)
                heights.append(height)
        
        if sizes:
            print(f"  - Tailles des bâtiments: min={min(sizes):.1f}, max={max(sizes):.1f}, moy={sum(sizes)/len(sizes):.1f}")
        if heights:
            print(f"  - Hauteurs des bâtiments: min={min(heights):.1f}, max={max(heights):.1f}, moy={sum(heights)/len(heights):.1f}")
    
    # Vérifier les matériaux (indicateur de type de zone)
    materials = set()
    for obj in bpy.context.scene.objects:
        if obj.data and hasattr(obj.data, 'materials'):
            for mat in obj.data.materials:
                if mat:
                    materials.add(mat.name)
    
    if materials:
        print(f"  - Matériaux détectés: {', '.join(sorted(materials))}")

if __name__ == "__main__":
    # Ce script doit être exécuté dans Blender
    if bpy.app.version < (2, 80, 0):
        print("ATTENTION: Ce script nécessite Blender 2.80 ou plus récent")
    
    success = test_district_mode()
    
    if success:
        print("\nTous les tests ont réussi ! Le mode district fonctionne correctement.")
    else:
        print("\nDes erreurs ont été détectées. Vérifiez l'installation de l'addon.")

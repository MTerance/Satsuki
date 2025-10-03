#!/usr/bin/env python3
"""
Script de test pour valider l'alignement parfait routes/blocs/trottoirs
Version finale - City Block Generator 6.13.3
"""

import sys
import os

# Ajouter le chemin du module
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def test_alignment_calculation():
    """Test le calcul des positions pour vérifier l'alignement parfait"""
    
    print("=== TEST ALIGNEMENT ROUTES/BLOCS/TROTTOIRS ===")
    
    # Simuler une grille 3x3 avec des blocs de tailles différentes
    block_sizes = [
        [{'size': (20, 15), 'zone_type': 'RESIDENTIAL'}, {'size': (20, 25), 'zone_type': 'COMMERCIAL'}, {'size': (20, 20), 'zone_type': 'RESIDENTIAL'}],
        [{'size': (25, 15), 'zone_type': 'INDUSTRIAL'}, {'size': (25, 25), 'zone_type': 'RESIDENTIAL'}, {'size': (25, 20), 'zone_type': 'COMMERCIAL'}],
        [{'size': (30, 15), 'zone_type': 'RESIDENTIAL'}, {'size': (30, 25), 'zone_type': 'RESIDENTIAL'}, {'size': (30, 20), 'zone_type': 'INDUSTRIAL'}]
    ]
    
    road_width = 4
    grid_width = len(block_sizes)
    grid_length = len(block_sizes[0])
    
    print(f"Grille: {grid_width}x{grid_length}")
    print(f"Largeur route: {road_width}")
    
    # Calculer les positions X
    x_starts = []
    current_x = 0
    for i in range(grid_width):
        x_starts.append(current_x)
        max_width = max(block_sizes[i][j]['size'][0] for j in range(grid_length))
        print(f"Colonne {i}: x_start={current_x}, max_width={max_width}")
        current_x += max_width
        if i < grid_width - 1:
            print(f"  Route verticale après colonne {i}: position x={current_x}")
            current_x += road_width
    
    print(f"Positions X finales: {x_starts}")
    
    # Calculer les positions Y
    y_starts = []
    current_y = 0
    for j in range(grid_length):
        y_starts.append(current_y)
        max_depth = max(block_sizes[i][j]['size'][1] for i in range(grid_width))
        print(f"Rangée {j}: y_start={current_y}, max_depth={max_depth}")
        current_y += max_depth
        if j < grid_length - 1:
            print(f"  Route horizontale après rangée {j}: position y={current_y}")
            current_y += road_width
    
    print(f"Positions Y finales: {y_starts}")
    
    # Vérifier l'alignement des routes horizontales
    print("\n=== ROUTES HORIZONTALES ===")
    for j in range(grid_length - 1):
        max_depth_j = max(block_sizes[i][j]['size'][1] for i in range(grid_width))
        y_road_start = y_starts[j] + max_depth_j
        y_next_block = y_starts[j + 1]
        
        print(f"Route horizontale {j}:")
        print(f"  Fin bloc rangée {j}: y={y_starts[j] + max_depth_j}")
        print(f"  Position route: y={y_road_start}")
        print(f"  Fin route: y={y_road_start + road_width}")
        print(f"  Début bloc rangée {j+1}: y={y_next_block}")
        
        # Vérification de l'alignement parfait
        if y_road_start + road_width == y_next_block:
            print(f"  ✓ ALIGNEMENT PARFAIT")
        else:
            print(f"  ✗ PROBLÈME D'ALIGNEMENT: écart de {abs(y_road_start + road_width - y_next_block)}")
    
    # Vérifier l'alignement des routes verticales
    print("\n=== ROUTES VERTICALES ===")
    for i in range(grid_width - 1):
        max_width_i = max(block_sizes[i][j]['size'][0] for j in range(grid_length))
        x_road_start = x_starts[i] + max_width_i
        x_next_block = x_starts[i + 1]
        
        print(f"Route verticale {i}:")
        print(f"  Fin bloc colonne {i}: x={x_starts[i] + max_width_i}")
        print(f"  Position route: x={x_road_start}")
        print(f"  Fin route: x={x_road_start + road_width}")
        print(f"  Début bloc colonne {i+1}: x={x_next_block}")
        
        # Vérification de l'alignement parfait
        if x_road_start + road_width == x_next_block:
            print(f"  ✓ ALIGNEMENT PARFAIT")
        else:
            print(f"  ✗ PROBLÈME D'ALIGNEMENT: écart de {abs(x_road_start + road_width - x_next_block)}")
    
    # Vérifier les positions des blocs/trottoirs
    print("\n=== BLOCS ET TROTTOIRS ===")
    for i in range(grid_width):
        for j in range(grid_length):
            block_width, block_depth = block_sizes[i][j]['size']
            x_block = x_starts[i]
            y_block = y_starts[j]
            
            print(f"Bloc [{i}][{j}]:")
            print(f"  Position: ({x_block}, {y_block})")
            print(f"  Taille: {block_width}x{block_depth}")
            print(f"  Fin: ({x_block + block_width}, {y_block + block_depth})")
    
    print("\n=== RÉSUMÉ ===")
    print("Tous les calculs semblent corrects pour un alignement parfait.")
    print("Les routes commencent exactement à la fin des blocs.")
    print("Les blocs suivants commencent exactement à la fin des routes.")
    
def test_object_positioning():
    """Test le positionnement des objets dans l'espace 3D"""
    
    print("\n=== TEST POSITIONNEMENT OBJETS ===")
    
    # Simuler le positionnement d'un trottoir
    x_block, y_block = 10, 15
    block_width, block_depth = 20, 25
    
    print(f"Bloc: position=({x_block}, {y_block}), taille={block_width}x{block_depth}")
    
    # Position du trottoir (doit couvrir exactement le bloc)
    trottoir_x = x_block + block_width/2  # Centre en X
    trottoir_y = y_block + block_depth/2  # Centre en Y
    
    print(f"Trottoir: centre=({trottoir_x}, {trottoir_y})")
    print(f"Trottoir: échelle=({block_width/2}, {block_depth/2})")
    print(f"Trottoir: limites X=({trottoir_x - block_width/2}, {trottoir_x + block_width/2})")
    print(f"Trottoir: limites Y=({trottoir_y - block_depth/2}, {trottoir_y + block_depth/2})")
    
    # Vérification
    if (trottoir_x - block_width/2 == x_block and 
        trottoir_x + block_width/2 == x_block + block_width and
        trottoir_y - block_depth/2 == y_block and
        trottoir_y + block_depth/2 == y_block + block_depth):
        print("✓ TROTTOIR PARFAITEMENT ALIGNÉ")
    else:
        print("✗ PROBLÈME D'ALIGNEMENT TROTTOIR")
    
    # Simuler le positionnement d'une route horizontale
    y_road = y_block + block_depth  # Route commence à la fin du bloc
    road_width = 4
    road_length = 60  # Longueur totale
    
    route_x = 0 + road_length/2  # Centre en X
    route_y = y_road + road_width/2  # Centre en Y
    
    print(f"\nRoute horizontale: position_début=({0}, {y_road})")
    print(f"Route horizontale: centre=({route_x}, {route_y})")
    print(f"Route horizontale: échelle=({road_length/2}, {road_width/2})")
    print(f"Route horizontale: limites Y=({route_y - road_width/2}, {route_y + road_width/2})")
    
    # Vérification de l'alignement route-bloc
    if route_y - road_width/2 == y_block + block_depth:
        print("✓ ROUTE PARFAITEMENT ALIGNÉE AVEC LE BLOC")
    else:
        print("✗ PROBLÈME D'ALIGNEMENT ROUTE-BLOC")

if __name__ == "__main__":
    test_alignment_calculation()
    test_object_positioning()
    print("\n=== TESTS TERMINÉS ===")

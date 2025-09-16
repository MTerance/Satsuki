# =============================================
# NOUVEAU GÉNÉRATEUR : ROUTES D'ABORD
# =============================================
# Approche inverse : créer les routes d'abord, puis les blocs dans les espaces

import bpy
import random
import math
from .generator import create_material, safe_int, generate_building, generate_oriented_building

def generate_road_network_first(context):
    """Nouvelle approche : générer d'abord le réseau de routes, puis remplir les espaces"""
    try:
        scene = context.scene
        
        # Récupérer les paramètres
        width = safe_int(getattr(scene, 'citygen_width', 5), 5)
        length = safe_int(getattr(scene, 'citygen_length', 5), 5)
        road_width = getattr(scene, 'citygen_road_width', 4.0)
        
        # Paramètres organiques
        organic_mode = getattr(scene, 'citygen_organic_mode', False)
        road_curve_intensity = getattr(scene, 'citygen_road_curve_intensity', 0.5)
        
        print(f"🛣️ NOUVEAU SYSTÈME: Génération routes d'abord ({width}x{length})")
        
        # Créer les matériaux
        road_mat = create_material("RoadMat_First", (0.3, 0.3, 0.3))  # Gris foncé pour routes
        block_mat = create_material("BlockMat_First", (0.7, 0.7, 0.7))  # Gris clair pour blocs
        build_mat = create_material("BuildingMat_First", (0.8, 0.6, 0.4))  # Beige pour bâtiments
        
        # ÉTAPE 1: Créer le réseau de routes
        road_network = create_primary_road_network(width, length, road_width, road_mat, organic_mode, road_curve_intensity)
        
        # ÉTAPE 2: Identifier les zones entre les routes
        block_zones = identify_block_zones_from_roads(road_network, width, length, road_width)
        
        # ÉTAPE 3: Créer les blocs dans ces zones
        blocks_created = create_blocks_in_zones(block_zones, block_mat)
        
        # ÉTAPE 4: Ajouter les bâtiments dans les blocs
        buildings_created = add_buildings_to_blocks(block_zones, build_mat, scene)
        
        print(f"✅ Système routes-first complété:")
        print(f"   🛣️ {len(road_network)} segments de routes")
        print(f"   📐 {len(block_zones)} zones de blocs identifiées") 
        print(f"   🏗️ {blocks_created} blocs créés")
        print(f"   🏢 {buildings_created} bâtiments générés")
        
        return True
        
    except Exception as e:
        print(f"❌ Erreur génération routes-first: {e}")
        import traceback
        print(f"Traceback: {traceback.format_exc()}")
        return False

def create_primary_road_network(width, length, road_width, road_mat, organic_mode, curve_intensity):
    """Crée le réseau principal de routes"""
    road_network = []
    block_size = 12.0  # Taille d'un bloc avec sa route
    
    try:
        print(f"🛣️ Création réseau de routes principal...")
        
        if organic_mode and curve_intensity > 0.3:
            # Réseau organique avec courbes
            road_network = create_organic_road_grid(width, length, block_size, road_width, road_mat, curve_intensity)
        else:
            # Réseau standard rectangulaire
            road_network = create_rectangular_road_grid(width, length, block_size, road_width, road_mat)
        
        print(f"✅ {len(road_network)} segments de routes créés")
        return road_network
        
    except Exception as e:
        print(f"Erreur création réseau routes: {e}")
        return []

def create_rectangular_road_grid(width, length, block_size, road_width, road_mat):
    """Crée une grille rectangulaire de routes"""
    road_network = []
    
    try:
        # Routes verticales
        for i in range(width + 1):
            road_x = (i - width/2) * block_size
            road_y = 0
            road_length = length * block_size
            
            # Créer route verticale
            bpy.ops.mesh.primitive_cube_add(
                size=2.0,
                location=(road_x, road_y, 0.05)
            )
            road = bpy.context.object
            if road:
                road.scale = (road_width/2, road_length/2, 0.05)
                bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
                road.name = f"Road_Vertical_{i}_{road_x:.1f}"
                
                # Matériau
                if road_mat and road.data:
                    road.data.materials.clear()
                    road.data.materials.append(road_mat)
                
                road_network.append({
                    'object': road,
                    'type': 'vertical',
                    'x': road_x,
                    'y': road_y,
                    'width': road_width,
                    'length': road_length
                })
        
        # Routes horizontales
        for j in range(length + 1):
            road_y = (j - length/2) * block_size
            road_x = 0
            road_length = width * block_size
            
            # Créer route horizontale
            bpy.ops.mesh.primitive_cube_add(
                size=2.0,
                location=(road_x, road_y, 0.05)
            )
            road = bpy.context.object
            if road:
                road.scale = (road_length/2, road_width/2, 0.05)
                bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
                road.name = f"Road_Horizontal_{j}_{road_y:.1f}"
                
                # Matériau
                if road_mat and road.data:
                    road.data.materials.clear()
                    road.data.materials.append(road_mat)
                
                road_network.append({
                    'object': road,
                    'type': 'horizontal',
                    'x': road_x,
                    'y': road_y,
                    'width': road_length,
                    'length': road_width
                })
        
        return road_network
        
    except Exception as e:
        print(f"Erreur grille rectangulaire: {e}")
        return []

def create_organic_road_grid(width, length, block_size, road_width, road_mat, curve_intensity):
    """Crée une grille organique de routes avec courbes"""
    road_network = []
    
    try:
        # Pour l'instant, version simplifiée - routes droites avec légères variations
        for i in range(width + 1):
            # Routes verticales avec légères courbes
            base_x = (i - width/2) * block_size
            deviation = random.uniform(-1, 1) * curve_intensity * 2
            road_x = base_x + deviation
            
            road_y = 0
            road_length = length * block_size
            
            bpy.ops.mesh.primitive_cube_add(
                size=2.0,
                location=(road_x, road_y, 0.05)
            )
            road = bpy.context.object
            if road:
                road.scale = (road_width/2, road_length/2, 0.05)
                bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
                road.name = f"OrganicRoad_V_{i}_{road_x:.1f}"
                
                if road_mat and road.data:
                    road.data.materials.clear()
                    road.data.materials.append(road_mat)
                
                road_network.append({
                    'object': road,
                    'type': 'vertical',
                    'x': road_x,
                    'y': road_y,
                    'width': road_width,
                    'length': road_length
                })
        
        # Routes horizontales avec légères courbes
        for j in range(length + 1):
            base_y = (j - length/2) * block_size
            deviation = random.uniform(-1, 1) * curve_intensity * 2
            road_y = base_y + deviation
            
            road_x = 0
            road_length = width * block_size
            
            bpy.ops.mesh.primitive_cube_add(
                size=2.0,
                location=(road_x, road_y, 0.05)
            )
            road = bpy.context.object
            if road:
                road.scale = (road_length/2, road_width/2, 0.05)
                bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
                road.name = f"OrganicRoad_H_{j}_{road_y:.1f}"
                
                if road_mat and road.data:
                    road.data.materials.clear()
                    road.data.materials.append(road_mat)
                
                road_network.append({
                    'object': road,
                    'type': 'horizontal',
                    'x': road_x,
                    'y': road_y,
                    'width': road_length,
                    'length': road_width
                })
        
        return road_network
        
    except Exception as e:
        print(f"Erreur grille organique: {e}")
        return []

def identify_block_zones_from_roads(road_network, width, length, road_width):
    """Identifie les zones de blocs entre les routes"""
    block_zones = []
    block_size = 12.0
    
    try:
        # Séparer les routes verticales et horizontales
        vertical_roads = [r for r in road_network if r['type'] == 'vertical']
        horizontal_roads = [r for r in road_network if r['type'] == 'horizontal']
        
        # Trier par position
        vertical_roads.sort(key=lambda r: r['x'])
        horizontal_roads.sort(key=lambda r: r['y'])
        
        # Créer les zones entre les routes
        for i in range(len(vertical_roads) - 1):
            for j in range(len(horizontal_roads) - 1):
                # Coordonnées de la zone
                left_road = vertical_roads[i]
                right_road = vertical_roads[i + 1]
                bottom_road = horizontal_roads[j]
                top_road = horizontal_roads[j + 1]
                
                # Centre de la zone
                zone_x = (left_road['x'] + right_road['x']) / 2
                zone_y = (bottom_road['y'] + top_road['y']) / 2
                
                # Dimensions de la zone (moins la largeur des routes)
                zone_width = abs(right_road['x'] - left_road['x']) - road_width
                zone_height = abs(top_road['y'] - bottom_road['y']) - road_width
                
                # Vérifier que la zone est valide
                if zone_width > 2 and zone_height > 2:
                    block_zones.append({
                        'x': zone_x,
                        'y': zone_y,
                        'width': zone_width,
                        'height': zone_height,
                        'left_bound': left_road['x'] + road_width/2,
                        'right_bound': right_road['x'] - road_width/2,
                        'bottom_bound': bottom_road['y'] + road_width/2,
                        'top_bound': top_road['y'] - road_width/2
                    })
        
        print(f"📐 {len(block_zones)} zones de blocs identifiées")
        return block_zones
        
    except Exception as e:
        print(f"Erreur identification zones: {e}")
        return []

def create_blocks_in_zones(block_zones, block_mat):
    """Crée les blocs dans les zones identifiées"""
    blocks_created = 0
    
    try:
        for i, zone in enumerate(block_zones):
            # Créer un bloc qui remplit exactement la zone
            bpy.ops.mesh.primitive_cube_add(
                size=2.0,
                location=(zone['x'], zone['y'], 0.1)
            )
            
            block = bpy.context.object
            if block:
                # Ajuster les dimensions pour remplir la zone
                block.scale = (zone['width']/2, zone['height']/2, 0.1)
                bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
                block.name = f"Block_Zone_{i}_{zone['x']:.1f}_{zone['y']:.1f}"
                
                # Matériau
                if block_mat and block.data:
                    block.data.materials.clear()
                    block.data.materials.append(block_mat)
                
                blocks_created += 1
                
                # Stocker les informations dans la zone
                zone['block_object'] = block
        
        return blocks_created
        
    except Exception as e:
        print(f"Erreur création blocs: {e}")
        return 0

def add_buildings_to_blocks(block_zones, build_mat, scene):
    """Ajoute des bâtiments dans chaque bloc"""
    buildings_created = 0
    
    try:
        # Paramètres des bâtiments
        buildings_per_block = safe_int(getattr(scene, 'citygen_buildings_per_block', 2), 2)
        max_floors = safe_int(getattr(scene, 'citygen_max_floors', 8), 8)
        variety = getattr(scene, 'citygen_building_variety', 'MEDIUM')
        
        for zone in block_zones:
            # Calculer le nombre de bâtiments selon la taille du bloc
            zone_area = zone['width'] * zone['height']
            if zone_area < 20:
                buildings_count = 1
            elif zone_area < 50:
                buildings_count = buildings_per_block
            else:
                buildings_count = buildings_per_block + 1
            
            for b in range(buildings_count):
                # Position dans la zone avec marge
                margin = 2.0  # Marge depuis les bords du bloc
                available_width = max(2, zone['width'] - 2*margin)
                available_height = max(2, zone['height'] - 2*margin)
                
                building_x = zone['x'] + random.uniform(-available_width/2, available_width/2)
                building_y = zone['y'] + random.uniform(-available_height/2, available_height/2)
                
                # Dimensions du bâtiment adaptées à la zone
                max_building_size = min(available_width, available_height) * 0.4
                building_width = random.uniform(max_building_size*0.6, max_building_size)
                building_depth = random.uniform(max_building_size*0.6, max_building_size)
                building_height = random.randint(1, max_floors) * 3.0
                
                # Créer le bâtiment
                building = generate_building(
                    building_x, building_y, building_width, building_depth, 
                    building_height, build_mat, building_variety=variety
                )
                
                if building:
                    building.name = f"Building_Block_{zone['x']:.1f}_{zone['y']:.1f}_{b}"
                    buildings_created += 1
        
        return buildings_created
        
    except Exception as e:
        print(f"Erreur ajout bâtiments: {e}")
        return 0

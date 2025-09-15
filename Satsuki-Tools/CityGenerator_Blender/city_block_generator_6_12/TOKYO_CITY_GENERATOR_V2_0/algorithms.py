"""
Algorithmes unifiés pour Tokyo City Generator v2.0
Contient les 3 algorithmes principaux : Tokyo, Organic, Grid
"""

import bpy
import bmesh
import mathutils
import random
import math
from typing import Dict, List, Tuple, Any
from .core_unified import unified_core, district_manager

class BaseAlgorithm:
    """Classe de base pour tous les algorithmes de génération"""
    
    def __init__(self, name: str):
        self.name = name
        self.version = "2.0.0"
    
    def generate(self, context: bpy.types.Context, params: Dict[str, Any], 
                texture_system=None) -> Dict[str, Any]:
        """Méthode principale de génération (à implémenter dans les sous-classes)"""
        raise NotImplementedError("Must implement generate method")
    
    def validate_params(self, params: Dict[str, Any]) -> bool:
        """Valide les paramètres de génération"""
        required_params = ['size', 'density', 'variety']
        return all(param in params for param in required_params)

class TokyoAlgorithm(BaseAlgorithm):
    """Algorithme de génération de districts Tokyo réalistes"""
    
    def __init__(self):
        super().__init__("Tokyo Districts")
        self.clear_prefixes = ["TokyoBuilding_", "TokyoSidewalk_", "TokyoStreet_", "TokyoCrossing_"]
    
    def generate(self, context: bpy.types.Context, params: Dict[str, Any], 
                texture_system=None) -> Dict[str, Any]:
        """Génère un district Tokyo avec zones mixtes"""
        if not self.validate_params(params):
            raise ValueError("Invalid parameters for Tokyo generation")
        
        # Nettoyer la scène
        unified_core.clear_scene(self.clear_prefixes)
        
        # Récupérer les paramètres
        size = params['size']
        density = params['density']
        variety = params['variety']
        district_type = params.get('district_type', 'MIXED')
        use_textures = params.get('use_advanced_textures', False)
        include_roads = params.get('include_roads', True)
        
        # Configuration du district
        district_config = district_manager.get_district_config(district_type)
        
        print(f"🗾 Génération district Tokyo {size}x{size} - Type: {district_type}")
        
        # 1. CRÉER LES ZONES
        zones = self.create_tokyo_zones(size, district_config, variety)
        
        # 2. CRÉER LES BÂTIMENTS
        buildings = self.create_tokyo_buildings(zones, district_config, texture_system, use_textures)
        
        # 3. CRÉER L'INFRASTRUCTURE (routes, trottoirs)
        infrastructure = []
        if include_roads:
            infrastructure = self.create_tokyo_infrastructure(size, zones, district_config)
        
        # 4. STATISTIQUES
        building_stats = unified_core.generate_building_stats(buildings)
        
        result = {
            'buildings': buildings,
            'infrastructure': infrastructure,
            'zones': zones,
            'stats': {
                'buildings': len(buildings),
                'blocks': len(zones),
                'infrastructure': len(infrastructure),
                'district_type': district_type,
                'building_stats': building_stats
            }
        }
        
        print(f"✅ District Tokyo créé: {len(buildings)} bâtiments, {len(infrastructure)} éléments d'infrastructure")
        return result
    
    def create_tokyo_zones(self, size: int, district_config: Dict, variety: float) -> List[Dict]:
        """Crée les zones du district Tokyo"""
        zones = []
        block_size = 20.0  # Taille des blocs en mètres
        
        for x in range(size):
            for y in range(size):
                # Position du bloc
                pos_x = x * block_size - (size * block_size) / 2
                pos_y = y * block_size - (size * block_size) / 2
                
                # Déterminer le sous-type de zone selon la position
                center_distance = math.sqrt((x - size/2)**2 + (y - size/2)**2)
                max_distance = math.sqrt((size/2)**2 + (size/2)**2)
                center_factor = 1.0 - (center_distance / max_distance)
                
                # Ajuster la densité selon la distance du centre
                zone_density = district_config['building_density'] * (0.5 + 0.5 * center_factor)
                
                zone = {
                    'position': (pos_x, pos_y, 0),
                    'size': (block_size * 0.8, block_size * 0.8),  # Laisser place pour les routes
                    'density': zone_density,
                    'center_factor': center_factor,
                    'variety': variety
                }
                zones.append(zone)
        
        return zones
    
    def create_tokyo_buildings(self, zones: List[Dict], district_config: Dict, 
                             texture_system=None, use_textures: bool = False) -> List[bpy.types.Object]:
        """Crée les bâtiments dans les zones Tokyo"""
        buildings = []
        
        for i, zone in enumerate(zones):
            # Nombre de bâtiments dans cette zone
            max_buildings = int(6 * zone['density'])  # Max 6 bâtiments par zone
            num_buildings = random.randint(max(1, max_buildings//2), max_buildings)
            
            zone_x, zone_y, _ = zone['position']
            zone_w, zone_h = zone['size']
            
            for j in range(num_buildings):
                # Position aléatoire dans la zone
                offset_x = random.uniform(-zone_w/2, zone_w/2)
                offset_y = random.uniform(-zone_h/2, zone_h/2)
                
                building_x = zone_x + offset_x
                building_y = zone_y + offset_y
                
                # Dimensions du bâtiment
                width = random.uniform(4, 12) * (1 + zone['variety'] * 0.5)
                depth = random.uniform(4, 12) * (1 + zone['variety'] * 0.5)
                height = district_manager.get_building_height(
                    'MIXED',  # Type par défaut
                    zone['variety']
                ) * (1 + zone['center_factor'] * 2)  # Plus haut au centre
                
                # Créer le bâtiment
                building = unified_core.create_building_mesh(
                    width, depth, height,
                    (building_x, building_y, height/2)
                )
                
                building.name = f"TokyoBuilding_{i:02d}_{j:02d}"
                
                # Appliquer matériau/texture
                if use_textures and texture_system:
                    building_params = {
                        'category': unified_core.get_building_category(height, width),
                        'zone_type': 'mixed',
                        'height': height,
                        'width': width
                    }
                    unified_core.apply_material(building, "tokyo_building", texture_system, building_params)
                else:
                    unified_core.apply_material(building, "TokyoBuilding", None, None)
                
                buildings.append(building)
        
        return buildings
    
    def create_tokyo_infrastructure(self, size: int, zones: List[Dict], 
                                  district_config: Dict) -> List[bpy.types.Object]:
        """Crée l'infrastructure urbaine (routes, trottoirs)"""
        infrastructure = []
        block_size = 20.0
        road_width = district_config['road_width']
        
        # Routes horizontales
        for y in range(size + 1):
            start_x = -size * block_size / 2
            end_x = size * block_size / 2
            road_y = y * block_size - (size * block_size) / 2 - block_size / 2
            
            if y < size:  # Éviter la route en trop
                road = unified_core.create_road_mesh(
                    (start_x, road_y), (end_x, road_y), road_width
                )
                road.name = f"TokyoStreet_H_{y:02d}"
                unified_core.apply_material(road, "TokyoRoad", None, None)
                infrastructure.append(road)
        
        # Routes verticales
        for x in range(size + 1):
            start_y = -size * block_size / 2
            end_y = size * block_size / 2
            road_x = x * block_size - (size * block_size) / 2 - block_size / 2
            
            if x < size:  # Éviter la route en trop
                road = unified_core.create_road_mesh(
                    (road_x, start_y), (road_x, end_y), road_width
                )
                road.name = f"TokyoStreet_V_{x:02d}"
                unified_core.apply_material(road, "TokyoRoad", None, None)
                infrastructure.append(road)
        
        return infrastructure

class OrganicAlgorithm(BaseAlgorithm):
    """Algorithme de génération de villes organiques non-rectangulaires"""
    
    def __init__(self):
        super().__init__("Organic Cities")
        self.clear_prefixes = ["OrganicBuilding_", "OrganicRoad_", "OrganicBlock_"]
    
    def generate(self, context: bpy.types.Context, params: Dict[str, Any], 
                texture_system=None) -> Dict[str, Any]:
        """Génère une ville organique avec courbes naturelles"""
        if not self.validate_params(params):
            raise ValueError("Invalid parameters for Organic generation")
        
        # Nettoyer la scène
        unified_core.clear_scene(self.clear_prefixes)
        
        # Récupérer les paramètres
        size = params['size']
        density = params['density']
        variety = params['variety']
        organic_factor = params.get('organic_factor', 0.5)
        use_textures = params.get('use_advanced_textures', False)
        
        print(f"🌿 Génération ville organique {size}x{size} - Facteur: {organic_factor:.1f}")
        
        # 1. CRÉER LA STRUCTURE ORGANIQUE
        centers = self.create_organic_centers(size, organic_factor)
        
        # 2. CRÉER LES BÂTIMENTS AUTOUR DES CENTRES
        buildings = self.create_organic_buildings(centers, density, variety, texture_system, use_textures)
        
        # 3. CRÉER LES ROUTES ORGANIQUES
        roads = self.create_organic_roads(centers, organic_factor)
        
        # 4. STATISTIQUES
        building_stats = unified_core.generate_building_stats(buildings)
        
        result = {
            'buildings': buildings,
            'infrastructure': roads,
            'centers': centers,
            'stats': {
                'buildings': len(buildings),
                'blocks': len(centers),
                'infrastructure': len(roads),
                'organic_factor': organic_factor,
                'building_stats': building_stats
            }
        }
        
        print(f"✅ Ville organique créée: {len(buildings)} bâtiments, {len(roads)} routes organiques")
        return result
    
    def create_organic_centers(self, size: int, organic_factor: float) -> List[Dict]:
        """Crée des centres organiques pour la distribution des bâtiments"""
        centers = []
        base_distance = 15.0  # Distance de base entre centres
        
        # Nombre de centres selon la taille
        num_centers = max(3, size * 2)
        
        for i in range(num_centers):
            # Position de base en grille déformée
            grid_x = (i % size) * base_distance - (size * base_distance) / 2
            grid_y = (i // size) * base_distance - (size * base_distance) / 2
            
            # Déformation organique
            deform_range = base_distance * organic_factor * 0.8
            offset_x = random.uniform(-deform_range, deform_range)
            offset_y = random.uniform(-deform_range, deform_range)
            
            center = {
                'position': (grid_x + offset_x, grid_y + offset_y, 0),
                'influence_radius': random.uniform(8, 15) * (1 + organic_factor),
                'building_count': random.randint(3, 8),
                'center_id': i
            }
            centers.append(center)
        
        return centers
    
    def create_organic_buildings(self, centers: List[Dict], density: float, variety: float,
                               texture_system=None, use_textures: bool = False) -> List[bpy.types.Object]:
        """Crée des bâtiments organiquement distribués autour des centres"""
        buildings = []
        
        for center in centers:
            center_x, center_y, _ = center['position']
            radius = center['influence_radius']
            num_buildings = int(center['building_count'] * density)
            
            for j in range(num_buildings):
                # Distribution radiale avec variation
                angle = random.uniform(0, 2 * math.pi)
                distance = random.uniform(2, radius * 0.8)
                
                building_x = center_x + distance * math.cos(angle)
                building_y = center_y + distance * math.sin(angle)
                
                # Dimensions avec plus de variété
                width = random.uniform(3, 10) * (1 + variety)
                depth = random.uniform(3, 10) * (1 + variety)
                height = random.uniform(5, 30) * (1 + variety * 0.5)
                
                # Créer le bâtiment
                building = unified_core.create_building_mesh(
                    width, depth, height,
                    (building_x, building_y, height/2)
                )
                
                building.name = f"OrganicBuilding_{center['center_id']:02d}_{j:02d}"
                
                # Appliquer matériau/texture
                if use_textures and texture_system:
                    building_params = {
                        'category': unified_core.get_building_category(height, width),
                        'zone_type': 'organic',
                        'height': height,
                        'width': width
                    }
                    unified_core.apply_material(building, "organic_building", texture_system, building_params)
                else:
                    unified_core.apply_material(building, "OrganicBuilding", None, None)
                
                buildings.append(building)
        
        return buildings
    
    def create_organic_roads(self, centers: List[Dict], organic_factor: float) -> List[bpy.types.Object]:
        """Crée des routes organiques courbes entre les centres"""
        roads = []
        
        # Connecter les centres proches
        for i, center1 in enumerate(centers):
            for j, center2 in enumerate(centers):
                if i >= j:  # Éviter les doublons
                    continue
                
                pos1 = center1['position']
                pos2 = center2['position']
                
                # Distance entre centres
                distance = math.sqrt((pos2[0] - pos1[0])**2 + (pos2[1] - pos1[1])**2)
                
                # Connecter seulement les centres proches
                if distance < 25.0:
                    # Créer route avec courbure organique
                    road = self.create_curved_road(pos1, pos2, organic_factor)
                    road.name = f"OrganicRoad_{i:02d}_{j:02d}"
                    unified_core.apply_material(road, "OrganicRoad", None, None)
                    roads.append(road)
        
        return roads
    
    def create_curved_road(self, start: Tuple[float, float, float], 
                          end: Tuple[float, float, float], curvature: float) -> bpy.types.Object:
        """Crée une route courbe entre deux points"""
        # Pour simplifier, créer une route droite (courbes complexes nécessiteraient des courbes Bézier)
        road = unified_core.create_road_mesh(
            (start[0], start[1]), (end[0], end[1]), 
            width=4.0 * (1 + curvature * 0.3)
        )
        return road

class GridAlgorithm(BaseAlgorithm):
    """Algorithme de génération de villes en grille rectangulaire classique"""
    
    def __init__(self):
        super().__init__("Grid Cities")
        self.clear_prefixes = ["GridBuilding_", "GridStreet_", "GridBlock_"]
    
    def generate(self, context: bpy.types.Context, params: Dict[str, Any], 
                texture_system=None) -> Dict[str, Any]:
        """Génère une ville en grille rectangulaire régulière"""
        if not self.validate_params(params):
            raise ValueError("Invalid parameters for Grid generation")
        
        # Nettoyer la scène
        unified_core.clear_scene(self.clear_prefixes)
        
        # Récupérer les paramètres
        size = params['size']
        density = params['density']
        variety = params['variety']
        use_textures = params.get('use_advanced_textures', False)
        include_roads = params.get('include_roads', True)
        
        print(f"📐 Génération ville grille {size}x{size}")
        
        # 1. CRÉER LA GRILLE
        grid_blocks = self.create_grid_blocks(size)
        
        # 2. CRÉER LES BÂTIMENTS
        buildings = self.create_grid_buildings(grid_blocks, density, variety, texture_system, use_textures)
        
        # 3. CRÉER LES ROUTES
        roads = []
        if include_roads:
            roads = self.create_grid_roads(size)
        
        # 4. STATISTIQUES
        building_stats = unified_core.generate_building_stats(buildings)
        
        result = {
            'buildings': buildings,
            'infrastructure': roads,
            'blocks': grid_blocks,
            'stats': {
                'buildings': len(buildings),
                'blocks': len(grid_blocks),
                'infrastructure': len(roads),
                'building_stats': building_stats
            }
        }
        
        print(f"✅ Ville grille créée: {len(buildings)} bâtiments, {len(roads)} routes")
        return result
    
    def create_grid_blocks(self, size: int) -> List[Dict]:
        """Crée les blocs de la grille"""
        blocks = []
        block_size = 18.0
        
        for x in range(size):
            for y in range(size):
                pos_x = x * block_size - (size * block_size) / 2 + block_size / 2
                pos_y = y * block_size - (size * block_size) / 2 + block_size / 2
                
                block = {
                    'position': (pos_x, pos_y, 0),
                    'size': (block_size * 0.7, block_size * 0.7),  # Place pour routes
                    'grid_x': x,
                    'grid_y': y
                }
                blocks.append(block)
        
        return blocks
    
    def create_grid_buildings(self, blocks: List[Dict], density: float, variety: float,
                            texture_system=None, use_textures: bool = False) -> List[bpy.types.Object]:
        """Crée des bâtiments dans la grille"""
        buildings = []
        
        for i, block in enumerate(blocks):
            block_x, block_y, _ = block['position']
            block_w, block_h = block['size']
            
            # Nombre de bâtiments par bloc
            num_buildings = random.randint(1, max(1, int(4 * density)))
            
            for j in range(num_buildings):
                # Position dans le bloc
                offset_x = random.uniform(-block_w/3, block_w/3)
                offset_y = random.uniform(-block_h/3, block_h/3)
                
                building_x = block_x + offset_x
                building_y = block_y + offset_y
                
                # Dimensions régulières avec un peu de variété
                base_width = 8.0
                base_depth = 8.0
                base_height = 15.0
                
                width = base_width * random.uniform(0.7, 1.3) * (1 + variety * 0.3)
                depth = base_depth * random.uniform(0.7, 1.3) * (1 + variety * 0.3)
                height = base_height * random.uniform(0.5, 2.0) * (1 + variety * 0.5)
                
                # Créer le bâtiment
                building = unified_core.create_building_mesh(
                    width, depth, height,
                    (building_x, building_y, height/2)
                )
                
                building.name = f"GridBuilding_{i:03d}_{j:02d}"
                
                # Appliquer matériau/texture
                if use_textures and texture_system:
                    building_params = {
                        'category': unified_core.get_building_category(height, width),
                        'zone_type': 'grid',
                        'height': height,
                        'width': width
                    }
                    unified_core.apply_material(building, "grid_building", texture_system, building_params)
                else:
                    unified_core.apply_material(building, "GridBuilding", None, None)
                
                buildings.append(building)
        
        return buildings
    
    def create_grid_roads(self, size: int) -> List[bpy.types.Object]:
        """Crée les routes de la grille"""
        roads = []
        block_size = 18.0
        road_width = 6.0
        
        # Routes horizontales
        for y in range(size - 1):
            for x in range(size):
                start_x = x * block_size - (size * block_size) / 2
                end_x = (x + 1) * block_size - (size * block_size) / 2
                road_y = (y + 0.5) * block_size - (size * block_size) / 2 + block_size / 2
                
                road = unified_core.create_road_mesh(
                    (start_x, road_y), (end_x, road_y), road_width
                )
                road.name = f"GridStreet_H_{x:02d}_{y:02d}"
                unified_core.apply_material(road, "GridRoad", None, None)
                roads.append(road)
        
        # Routes verticales
        for x in range(size - 1):
            for y in range(size):
                start_y = y * block_size - (size * block_size) / 2
                end_y = (y + 1) * block_size - (size * block_size) / 2
                road_x = (x + 0.5) * block_size - (size * block_size) / 2 + block_size / 2
                
                road = unified_core.create_road_mesh(
                    (road_x, start_y), (road_x, end_y), road_width
                )
                road.name = f"GridStreet_V_{x:02d}_{y:02d}"
                unified_core.apply_material(road, "GridRoad", None, None)
                roads.append(road)
        
        return roads
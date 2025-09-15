"""
Core unifié pour Tokyo City Generator v2.0
Centralise les fonctionnalités communes des 3 générateurs
"""

import bpy
import bmesh
import mathutils
import random
import os
from typing import Dict, List, Tuple, Any

class CityGeneratorCore:
    """Classe de base pour tous les générateurs de ville"""
    
    def __init__(self):
        self.name = "Base Generator"
        self.version = "2.0.0"
    
    def clear_scene(self, prefixes: List[str]):
        """Nettoie la scène des objets avec les préfixes spécifiés"""
        for obj in list(bpy.data.objects):
            if any(obj.name.startswith(prefix) for prefix in prefixes):
                bpy.data.objects.remove(obj, do_unlink=True)
    
    def create_building_mesh(self, width: float, depth: float, height: float, 
                           position: Tuple[float, float, float]) -> bpy.types.Object:
        """Crée un maillage de bâtiment basique"""
        bpy.ops.mesh.primitive_cube_add(size=1, location=position)
        building = bpy.context.active_object
        
        # Redimensionner
        building.scale = (width, depth, height)
        
        # Appliquer la transformation
        bpy.context.view_layer.objects.active = building
        bpy.ops.object.transform_apply(scale=True)
        
        return building
    
    def create_road_mesh(self, start: Tuple[float, float], end: Tuple[float, float], 
                        width: float = 4.0, height: float = 0.1) -> bpy.types.Object:
        """Crée un maillage de route entre deux points"""
        # Calculer la position et rotation
        center_x = (start[0] + end[0]) / 2
        center_y = (start[1] + end[1]) / 2
        
        length = ((end[0] - start[0])**2 + (end[1] - start[1])**2)**0.5
        
        # Créer le cube de base
        bpy.ops.mesh.primitive_cube_add(
            size=1, 
            location=(center_x, center_y, height/2)
        )
        road = bpy.context.active_object
        
        # Redimensionner
        road.scale = (length, width, height)
        
        # Rotation si nécessaire
        if start[0] != end[0] or start[1] != end[1]:
            import math
            angle = math.atan2(end[1] - start[1], end[0] - start[0])
            road.rotation_euler[2] = angle
        
        # Appliquer transformations
        bpy.ops.object.transform_apply(scale=True, rotation=True)
        
        return road
    
    def apply_material(self, obj: bpy.types.Object, material_name: str, 
                      texture_system=None, building_params=None):
        """Applique un matériau à un objet"""
        try:
            if texture_system and building_params:
                # Utiliser le système de textures avancé
                material = texture_system.create_building_material(
                    building_params.get('category', 'residential'),
                    building_params.get('zone_type', 'mixed'),
                    building_params.get('height', 10.0),
                    building_params.get('width', 8.0)
                )
            else:
                # Matériau procédural basique
                material = self.create_basic_material(material_name)
            
            # Assigner le matériau
            if obj.data.materials:
                obj.data.materials[0] = material
            else:
                obj.data.materials.append(material)
                
        except Exception as e:
            print(f"⚠️ Erreur application matériau {material_name}: {e}")
            # Fallback vers matériau de base
            basic_mat = self.create_basic_material("Fallback_" + material_name)
            if obj.data.materials:
                obj.data.materials[0] = basic_mat
            else:
                obj.data.materials.append(basic_mat)
    
    def create_basic_material(self, name: str) -> bpy.types.Material:
        """Crée un matériau procédural basique"""
        mat = bpy.data.materials.new(name=name)
        mat.use_nodes = True
        nodes = mat.node_tree.nodes
        links = mat.node_tree.links
        
        # Nettoyer les nodes existants
        nodes.clear()
        
        # Créer les nodes de base
        output = nodes.new(type='ShaderNodeOutputMaterial')
        bsdf = nodes.new(type='ShaderNodeBsdfPrincipled')
        
        # Configuration selon le type
        if "building" in name.lower():
            # Couleur aléatoire pour les bâtiments
            color = [random.uniform(0.3, 0.8) for _ in range(3)] + [1.0]
            bsdf.inputs['Base Color'].default_value = color
            bsdf.inputs['Roughness'].default_value = 0.7
        elif "road" in name.lower():
            # Gris foncé pour les routes
            bsdf.inputs['Base Color'].default_value = (0.2, 0.2, 0.2, 1.0)
            bsdf.inputs['Roughness'].default_value = 0.9
        elif "sidewalk" in name.lower():
            # Gris clair pour les trottoirs
            bsdf.inputs['Base Color'].default_value = (0.6, 0.6, 0.6, 1.0)
            bsdf.inputs['Roughness'].default_value = 0.8
        else:
            # Matériau par défaut
            bsdf.inputs['Base Color'].default_value = (0.5, 0.5, 0.5, 1.0)
            bsdf.inputs['Roughness'].default_value = 0.7
        
        # Connecter les nodes
        links.new(bsdf.outputs['BSDF'], output.inputs['Surface'])
        
        # Positionner les nodes
        output.location = (200, 0)
        bsdf.location = (0, 0)
        
        return mat
    
    def get_building_category(self, height: float, width: float, zone_type: str = 'mixed') -> str:
        """Détermine la catégorie d'un bâtiment selon ses dimensions"""
        if height > 50:
            return 'skyscraper'
        elif height > 20 and width < 15:
            return 'midrise'
        elif height > 10 and width > 15:
            return 'commercial'
        elif height < 10:
            return 'lowrise'
        else:
            return 'residential'
    
    def generate_building_stats(self, buildings: List[bpy.types.Object]) -> Dict[str, Any]:
        """Génère des statistiques sur les bâtiments créés"""
        stats = {
            'total_buildings': len(buildings),
            'categories': {},
            'height_range': {'min': float('inf'), 'max': 0},
            'total_volume': 0
        }
        
        for building in buildings:
            # Calculer la hauteur (dimension Z)
            height = building.dimensions.z
            width = max(building.dimensions.x, building.dimensions.y)
            
            # Catégorie
            category = self.get_building_category(height, width)
            stats['categories'][category] = stats['categories'].get(category, 0) + 1
            
            # Hauteur min/max
            stats['height_range']['min'] = min(stats['height_range']['min'], height)
            stats['height_range']['max'] = max(stats['height_range']['max'], height)
            
            # Volume approximatif
            volume = building.dimensions.x * building.dimensions.y * building.dimensions.z
            stats['total_volume'] += volume
        
        # Correction si aucun bâtiment
        if not buildings:
            stats['height_range'] = {'min': 0, 'max': 0}
        
        return stats

class DistrictManager:
    """Gestionnaire des districts urbains"""
    
    DISTRICT_TYPES = {
        'RESIDENTIAL': {
            'building_height_range': (3, 25),
            'building_density': 0.6,
            'building_variety': 0.8,
            'road_width': 6.0,
            'main_color': (0.8, 0.7, 0.6, 1.0)
        },
        'COMMERCIAL': {
            'building_height_range': (8, 40),
            'building_density': 0.8,
            'building_variety': 0.9,
            'road_width': 8.0,
            'main_color': (0.6, 0.7, 0.9, 1.0)
        },
        'BUSINESS': {
            'building_height_range': (20, 100),
            'building_density': 0.9,
            'building_variety': 0.7,
            'road_width': 10.0,
            'main_color': (0.5, 0.5, 0.7, 1.0)
        },
        'INDUSTRIAL': {
            'building_height_range': (5, 20),
            'building_density': 0.5,
            'building_variety': 0.4,
            'road_width': 12.0,
            'main_color': (0.6, 0.6, 0.5, 1.0)
        },
        'MIXED': {
            'building_height_range': (3, 60),
            'building_density': 0.7,
            'building_variety': 1.0,
            'road_width': 8.0,
            'main_color': (0.7, 0.7, 0.7, 1.0)
        }
    }
    
    @classmethod
    def get_district_config(cls, district_type: str) -> Dict[str, Any]:
        """Retourne la configuration d'un type de district"""
        return cls.DISTRICT_TYPES.get(district_type.upper(), cls.DISTRICT_TYPES['MIXED'])
    
    @classmethod
    def get_building_height(cls, district_type: str, variety_factor: float = 0.5) -> float:
        """Génère une hauteur de bâtiment selon le type de district"""
        config = cls.get_district_config(district_type)
        min_h, max_h = config['building_height_range']
        
        # Ajouter de la variété
        base_height = random.uniform(min_h, max_h)
        variety_adjustment = random.uniform(-variety_factor, variety_factor) * (max_h - min_h) * 0.3
        
        return max(min_h, min(max_h, base_height + variety_adjustment))

def register():
    """Enregistrement du module core unifié"""
    print("🏗️ Core unifié v2.0 enregistré")

def unregister():
    """Désenregistrement du module core unifié"""
    print("🔄 Core unifié v2.0 désenregistré")

# Instance globale du core
unified_core = CityGeneratorCore()
district_manager = DistrictManager()
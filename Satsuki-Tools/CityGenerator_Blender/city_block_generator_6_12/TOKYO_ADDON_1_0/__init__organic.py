bl_info = {
    "name": "Tokyo City Generator 1.1.0 ORGANIC",
    "author": "Tokyo Urban Designer", 
    "version": (1, 1, 0),
    "blender": (4, 0, 0),
    "location": "View3D > Sidebar > Tokyo Tab",
    "description": "Generate realistic Tokyo-style districts with ORGANIC Voronoï cells and curved streets",
    "category": "Add Mesh",
    "doc_url": "",
    "tracker_url": ""
}

import bpy
from bpy.props import IntProperty, FloatProperty, EnumProperty, BoolProperty
from bpy.types import Operator, Panel
import bmesh
import mathutils
from mathutils import Vector
import random
import math

# TOKYO 1.1.0 ORGANIC - RÉVOLUTION ORGANIQUE
# Nouvelles fonctionnalités:
# - Option A: Génération Voronoï pour blocs irréguliers
# - Option B: Routes courbes organiques
# - Système hybride: grille traditionnelle OU organique

class TOKYO_OT_generate_district(Operator):
    """Generate Tokyo-style district with organic options"""
    bl_idname = "tokyo.generate_district"
    bl_label = "Generate Tokyo District"
    bl_options = {'REGISTER', 'UNDO'}
    
    def execute(self, context):
        # Récupérer les paramètres depuis la scène
        size = context.scene.tokyo_size
        density = context.scene.tokyo_density
        variety = context.scene.tokyo_variety
        organic = context.scene.tokyo_organic
        
        # NOUVEAUX PARAMÈTRES ORGANIQUES
        use_voronoi = context.scene.tokyo_use_voronoi
        use_curved_streets = context.scene.tokyo_use_curved_streets
        voronoi_seed = context.scene.tokyo_voronoi_seed
        curve_intensity = context.scene.tokyo_curve_intensity
        
        # Nettoyer la scène
        self.clear_scene()
        
        # Créer le district Tokyo (grille ou organique)
        if use_voronoi:
            self.create_organic_tokyo_district(size, organic, density, variety, use_curved_streets, voronoi_seed, curve_intensity)
        else:
            self.create_tokyo_district(size, organic, density, variety)
        
        generation_type = "ORGANIC Voronoï" if use_voronoi else "Classic Grid"
        streets_type = "with CURVED streets" if use_curved_streets else "with straight streets"
        blocks_count = int(size * size * density)
        self.report({'INFO'}, f"Tokyo district {generation_type} {size}x{size} {streets_type} - {blocks_count} zones generated!")
        return {'FINISHED'}
    
    def clear_scene(self):
        """Supprime tous les objets Tokyo existants"""
        for obj in bpy.data.objects:
            if obj.name.startswith(("TokyoSidewalk_", "TokyoStreet_", "TokyoBuilding_", "TokyoCrossing_", "TokyoBaseGround", "TokyoVoronoi_", "TokyoCurved_")):
                bpy.data.objects.remove(obj, do_unlink=True)
    
    def create_organic_tokyo_district(self, size, organic_factor, block_density, building_variety, use_curved_streets, voronoi_seed, curve_intensity):
        """🌊 NOUVELLE FONCTION: Crée un district Tokyo ORGANIQUE avec cellules Voronoï"""
        print(f"🌊 Création district Tokyo ORGANIQUE {size}x{size} avec Voronoï")
        
        # 1. GÉNÉRATION VORONOÏ - Créer des points de germe aléatoires
        voronoi_cells = self.generate_voronoi_cells(size, block_density, voronoi_seed)
        
        # 2. DÉFINIR LES ZONES ORGANIQUES
        organic_zones = self.define_organic_zones(voronoi_cells, building_variety)
        
        # 3. CRÉER LES BLOCS ORGANIQUES
        organic_blocks = self.create_organic_blocks(voronoi_cells, organic_zones)
        
        # 4. CRÉER LES BÂTIMENTS ORGANIQUES
        organic_buildings = self.create_organic_buildings(voronoi_cells, organic_zones)
        
        # 5. CRÉER LE RÉSEAU ORGANIQUE (courbe ou droit)
        if use_curved_streets:
            organic_network = self.create_curved_street_network(voronoi_cells, organic_zones, curve_intensity)
        else:
            organic_network = self.create_organic_straight_network(voronoi_cells, organic_zones)
        
        print(f"✅ District ORGANIQUE créé: {len(organic_blocks)} blocs Voronoï, {len(organic_buildings)} bâtiments, {len(organic_network)} éléments réseau")
        return {"blocks": organic_blocks, "buildings": organic_buildings, "network": organic_network}
    
    def generate_voronoi_cells(self, size, density, seed):
        """🌊 Génère des cellules Voronoï organiques"""
        random.seed(seed)
        
        # Calculer le nombre de cellules basé sur la densité
        area = size * size * 400  # 400 = 20*20 (block_size au carré)
        num_cells = int(area * density / 400)  # Approximativement density cellules par bloc
        
        # Créer des points de germe répartis organiquement
        boundary = size * 10  # Demi-taille du district en unités Blender
        cells = []
        
        # Méthode: distribution avec clustering naturel
        for i in range(num_cells):
            # Centre avec clustering gaussien pour plus de réalisme
            if random.random() < 0.3:  # 30% dans le centre
                center_bias = 0.3
            else:  # 70% distribution normale
                center_bias = 1.0
            
            # Position avec distribution gaussienne centrée
            x = random.gauss(0, boundary * center_bias)
            y = random.gauss(0, boundary * center_bias)
            
            # Contraindre dans les limites
            x = max(-boundary, min(boundary, x))
            y = max(-boundary, min(boundary, y))
            
            # Calculer la zone d'influence (distance aux autres cellules)
            zone_radius = random.uniform(8.0, 25.0)  # Taille variable
            zone_type = self.determine_zone_from_position(x, y, boundary)
            
            cell = {
                'id': i,
                'center': Vector((x, y, 0)),
                'radius': zone_radius,
                'zone_type': zone_type,
                'neighbors': [],
                'vertices': []
            }
            cells.append(cell)
        
        # Calculer les polygones Voronoï (version simplifiée)
        self.calculate_voronoi_polygons(cells, boundary)
        
        print(f"🌊 Voronoï: {len(cells)} cellules générées avec seed {seed}")
        return cells
    
    def determine_zone_from_position(self, x, y, boundary):
        """Détermine le type de zone selon la distance du centre"""
        distance_from_center = math.sqrt(x*x + y*y)
        relative_distance = distance_from_center / boundary
        
        if relative_distance < 0.2:
            return 'business'
        elif relative_distance < 0.5:
            return 'commercial'
        else:
            return 'residential'
    
    def calculate_voronoi_polygons(self, cells, boundary):
        """Calcule les polygones Voronoï simplifiés pour chaque cellule"""
        # Version simplifiée: utiliser des approximations circulaires ou octogonales
        for cell in cells:
            vertices = []
            center = cell['center']
            radius = cell['radius']
            
            # Créer un octogone approximatif (8 vertices)
            for angle in range(0, 360, 45):
                rad = math.radians(angle)
                
                # Variation organique du rayon
                organic_radius = radius * random.uniform(0.7, 1.3)
                
                x = center.x + organic_radius * math.cos(rad)
                y = center.y + organic_radius * math.sin(rad)
                
                # Contraindre dans les limites
                x = max(-boundary, min(boundary, x))
                y = max(-boundary, min(boundary, y))
                
                vertices.append(Vector((x, y, 0)))
            
            cell['vertices'] = vertices
    
    def define_organic_zones(self, voronoi_cells, building_variety):
        """Définit les zones organiques selon le type de variété demandé"""
        organic_zones = {}
        
        for cell in voronoi_cells:
            cell_id = cell['id']
            
            if building_variety == 'RESIDENTIAL_ONLY':
                organic_zones[cell_id] = 'residential'
            elif building_variety == 'BUSINESS_ONLY':
                organic_zones[cell_id] = 'business'
            elif building_variety == 'NO_BUSINESS':
                # Pas de business, que commercial et résidentiel
                if cell['zone_type'] == 'business':
                    organic_zones[cell_id] = 'commercial'
                else:
                    organic_zones[cell_id] = cell['zone_type']
            else:  # ALL
                organic_zones[cell_id] = cell['zone_type']
        
        return organic_zones
    
    def create_organic_blocks(self, voronoi_cells, organic_zones):
        """🌊 Crée les blocs organiques basés sur les cellules Voronoï"""
        organic_blocks = {}
        
        for cell in voronoi_cells:
            cell_id = cell['id']
            zone_type = organic_zones[cell_id]
            vertices = cell['vertices']
            center = cell['center']
            
            # Créer le bloc organique avec mesh personnalisé
            mesh = bpy.data.meshes.new(f"VoronoiBlock_{zone_type}_{cell_id}")
            obj = bpy.data.objects.new(f"TokyoVoronoi_Sidewalk_{zone_type}_{cell_id}", mesh)
            bpy.context.collection.objects.link(obj)
            
            # Construire le mesh à partir des vertices Voronoï
            bm = bmesh.new()
            
            # Hauteur selon la zone
            if zone_type == 'business':
                height = 0.15
            elif zone_type == 'commercial':
                height = 0.12
            else:  # residential
                height = 0.08
            
            # Créer les vertices de base (niveau sol)
            base_verts = []
            for vertex in vertices:
                base_verts.append(bm.verts.new((vertex.x, vertex.y, 0)))
            
            # Créer les vertices du dessus
            top_verts = []
            for vertex in vertices:
                top_verts.append(bm.verts.new((vertex.x, vertex.y, height)))
            
            # Créer les faces
            if len(base_verts) >= 3:
                # Face du bas
                bm.faces.new(base_verts)
                # Face du dessus
                bm.faces.new(list(reversed(top_verts)))
                
                # Faces latérales
                for i in range(len(base_verts)):
                    next_i = (i + 1) % len(base_verts)
                    bm.faces.new([
                        base_verts[i], base_verts[next_i],
                        top_verts[next_i], top_verts[i]
                    ])
            
            # Finaliser le mesh
            bm.normal_update()
            bm.to_mesh(mesh)
            bm.free()
            
            # Positionner l'objet
            obj.location = (0, 0, 0)
            
            # Matériau
            material = self.create_sidewalk_material(self.determine_sidewalk_type(zone_type))
            obj.data.materials.append(material)
            
            organic_blocks[cell_id] = obj
        
        return organic_blocks
    
    def create_organic_buildings(self, voronoi_cells, organic_zones):
        """🌊 Crée les bâtiments organiques sur les cellules Voronoï"""
        organic_buildings = {}
        
        for cell in voronoi_cells:
            cell_id = cell['id']
            zone_type = organic_zones[cell_id]
            center = cell['center']
            radius = cell['radius']
            
            # Position avec variation organique
            pos_x = center.x + random.uniform(-radius*0.2, radius*0.2)
            pos_y = center.y + random.uniform(-radius*0.2, radius*0.2)
            
            # Hauteur et taille selon le type de zone
            if zone_type == 'business':
                height = random.uniform(60, 160)
                width_factor = random.uniform(0.4, 0.7)
                building_name = f"TokyoVoronoi_Skyscraper_{cell_id}"
            elif zone_type == 'commercial':
                height = random.uniform(12, 32)
                width_factor = random.uniform(0.5, 0.8)
                building_name = f"TokyoVoronoi_Commercial_{cell_id}"
            else:  # residential
                height = random.uniform(4, 20)
                width_factor = random.uniform(0.3, 0.6)
                building_name = f"TokyoVoronoi_House_{cell_id}"
            
            # Taille basée sur le rayon de la cellule
            width_x = radius * width_factor
            width_y = radius * width_factor * random.uniform(0.8, 1.2)
            
            # Créer le bâtiment
            bpy.ops.mesh.primitive_cube_add(size=2.0, location=(pos_x, pos_y, height/2))
            building_obj = bpy.context.object
            building_obj.scale = (width_x/2, width_y/2, height/2)
            building_obj.name = building_name
            
            # Matériau
            material = self.create_building_material(zone_type)
            building_obj.data.materials.append(material)
            
            organic_buildings[cell_id] = building_obj
        
        return organic_buildings
    
    def create_curved_street_network(self, voronoi_cells, organic_zones, curve_intensity):
        """🛤️ OPTION B: Crée un réseau de routes COURBES organiques"""
        curved_network = {}
        
        print(f"🛤️ Génération réseau courbe avec intensité {curve_intensity}")
        
        # Créer des connexions entre cellules voisines avec routes courbes
        for i, cell_a in enumerate(voronoi_cells):
            for j, cell_b in enumerate(voronoi_cells[i+1:], i+1):
                distance = (cell_a['center'] - cell_b['center']).length
                
                # Connecter seulement les cellules proches
                if distance < 40.0:  # Distance maximale de connexion
                    # Créer une route courbe entre les centres
                    curved_path = self.create_curved_path(
                        cell_a['center'], 
                        cell_b['center'],
                        curve_intensity,
                        self.determine_street_type_organic(cell_a, cell_b, organic_zones)
                    )
                    
                    if curved_path:
                        path_name = f"curved_path_{i}_{j}"
                        curved_network[path_name] = curved_path
        
        # Ajouter sol de base simple
        background = self.create_organic_ground(voronoi_cells)
        if background:
            curved_network['organic_ground'] = background
        
        return curved_network
    
    def create_curved_path(self, start_pos, end_pos, curve_intensity, street_type):
        """Crée un chemin courbe entre deux points"""
        
        # Paramètres selon le type de rue
        if street_type == "main_avenue":
            width = 8.0
            height = 0.02
            material_type = "asphalt_main"
        elif street_type == "secondary_road":
            width = 6.0
            height = 0.015
            material_type = "asphalt_secondary"
        elif street_type == "shopping_street":
            width = 5.0
            height = 0.01
            material_type = "paved_commercial"
        elif street_type == "local_street":
            width = 4.0
            height = 0.01
            material_type = "asphalt_local"
        else:  # pedestrian_path
            width = 2.5
            height = 0.005
            material_type = "pedestrian_stones"
        
        # Créer la courbe Bézier
        curve_data = bpy.data.curves.new(f"CurvedStreet_{street_type}", type='CURVE')
        curve_data.dimensions = '3D'
        curve_data.bevel_depth = width / 2
        curve_data.bevel_resolution = 4
        
        # Créer le spline
        spline = curve_data.splines.new(type='BEZIER')
        spline.bezier_points.add(1)  # Ajouter un point (on en a déjà 1 par défaut)
        
        # Point de départ
        spline.bezier_points[0].co = start_pos
        spline.bezier_points[0].handle_left_type = 'AUTO'
        spline.bezier_points[0].handle_right_type = 'AUTO'
        
        # Point d'arrivée
        spline.bezier_points[1].co = end_pos
        spline.bezier_points[1].handle_left_type = 'AUTO'
        spline.bezier_points[1].handle_right_type = 'AUTO'
        
        # Ajouter des points de contrôle pour la courbure
        if curve_intensity > 0.1:
            # Point milieu avec déviation
            mid_point = (start_pos + end_pos) / 2
            
            # Calculer la direction perpendiculaire
            direction = end_pos - start_pos
            perpendicular = Vector((-direction.y, direction.x, 0)).normalized()
            
            # Déviation selon l'intensité
            deviation = perpendicular * curve_intensity * direction.length * random.uniform(-0.3, 0.3)
            curved_mid = mid_point + deviation
            
            # Ajouter le point de contrôle
            spline.bezier_points.add(1)
            spline.bezier_points[1].co = curved_mid
            spline.bezier_points[1].handle_left_type = 'AUTO'
            spline.bezier_points[1].handle_right_type = 'AUTO'
            
            # Réorganiser les points
            spline.bezier_points[2].co = end_pos
            spline.bezier_points[2].handle_left_type = 'AUTO'
            spline.bezier_points[2].handle_right_type = 'AUTO'
        
        # Créer l'objet
        curve_obj = bpy.data.objects.new(f"TokyoCurved_{street_type}", curve_data)
        bpy.context.collection.objects.link(curve_obj)
        
        # Positionner au niveau correct
        curve_obj.location.z = height
        
        # Matériau
        material = self.create_street_material(material_type)
        curve_obj.data.materials.append(material)
        
        return curve_obj
    
    def determine_street_type_organic(self, cell_a, cell_b, organic_zones):
        """Détermine le type de rue organique selon les cellules connectées"""
        zone_a = organic_zones[cell_a['id']]
        zone_b = organic_zones[cell_b['id']]
        
        # Si une des cellules est business
        if zone_a == 'business' or zone_b == 'business':
            return "main_avenue"
        # Si une des cellules est commercial
        elif zone_a == 'commercial' or zone_b == 'commercial':
            return "shopping_street"
        # Si toutes sont residential
        else:
            # Distance pour déterminer le type
            distance = (cell_a['center'] - cell_b['center']).length
            if distance > 30:
                return "secondary_road"
            elif distance > 20:
                return "local_street"
            else:
                return "pedestrian_path"
    
    def create_organic_straight_network(self, voronoi_cells, organic_zones):
        """Réseau droit mais organique (connexions entre cellules)"""
        network = {}
        
        # Créer des connexions droites entre cellules voisines
        for i, cell_a in enumerate(voronoi_cells):
            for j, cell_b in enumerate(voronoi_cells[i+1:], i+1):
                distance = (cell_a['center'] - cell_b['center']).length
                
                if distance < 35.0:  # Distance de connexion
                    street_element = self.create_straight_connection(
                        cell_a['center'],
                        cell_b['center'],
                        self.determine_street_type_organic(cell_a, cell_b, organic_zones)
                    )
                    
                    if street_element:
                        network[f"straight_connection_{i}_{j}"] = street_element
        
        # Sol de base
        background = self.create_organic_ground(voronoi_cells)
        if background:
            network['organic_ground'] = background
        
        return network
    
    def create_straight_connection(self, start_pos, end_pos, street_type):
        """Crée une connexion droite entre deux points"""
        
        # Paramètres selon le type
        if street_type == "main_avenue":
            width = 8.0
            height = 0.02
        elif street_type == "secondary_road":
            width = 6.0
            height = 0.015
        elif street_type == "shopping_street":
            width = 5.0
            height = 0.01
        elif street_type == "local_street":
            width = 4.0
            height = 0.01
        else:  # pedestrian_path
            width = 2.5
            height = 0.005
        
        # Calculer position et rotation
        direction = end_pos - start_pos
        distance = direction.length
        center = (start_pos + end_pos) / 2
        
        # Créer l'objet route
        bpy.ops.mesh.primitive_cube_add(size=2.0, location=center)
        street_obj = bpy.context.object
        
        # Échelle
        street_obj.scale = (distance/2, width/2, height/2)
        
        # Rotation pour aligner avec la direction
        if distance > 0.001:
            angle = math.atan2(direction.y, direction.x)
            street_obj.rotation_euler = (0, 0, angle)
        
        street_obj.name = f"TokyoVoronoi_Street_{street_type}"
        
        # Matériau
        material = self.create_street_material("asphalt_main")
        street_obj.data.materials.append(material)
        
        return street_obj
    
    def create_organic_ground(self, voronoi_cells):
        """Crée un sol de base organique"""
        # Calculer les limites
        min_x = min_y = float('inf')
        max_x = max_y = float('-inf')
        
        for cell in voronoi_cells:
            center = cell['center']
            radius = cell['radius']
            min_x = min(min_x, center.x - radius)
            max_x = max(max_x, center.x + radius)
            min_y = min(min_y, center.y - radius)
            max_y = max(max_y, center.y + radius)
        
        # Créer le sol
        size_x = max_x - min_x + 20
        size_y = max_y - min_y + 20
        center_x = (min_x + max_x) / 2
        center_y = (min_y + max_y) / 2
        
        bpy.ops.mesh.primitive_cube_add(size=2.0, location=(center_x, center_y, -0.1))
        ground_obj = bpy.context.object
        ground_obj.scale = (size_x/2, size_y/2, 0.05)
        ground_obj.name = "TokyoVoronoi_OrganicGround"
        
        # Matériau
        material = self.create_ground_material()
        ground_obj.data.materials.append(material)
        
        return ground_obj
    
    # === FONCTIONS TRADITIONNELLES (pour compatibilité) ===
    
    def create_tokyo_district(self, size, organic_factor, block_density, building_variety):
        """Fonction traditionnelle pour génération grille (inchangée)"""
        print(f"🗾 Création district Tokyo TRADITIONNEL {size}x{size}")
        
        # Code identique à la version 1.0.8 (traditionnel)
        zones = self.define_tokyo_zones(size, block_density, building_variety)
        blocks = self.create_district_blocks(size, zones)
        buildings = self.create_tokyo_buildings(size, zones)
        urban_network = self.create_urban_network(size, zones, organic_factor)
        
        print(f"✅ District traditionnel créé: {len(blocks)} blocs-trottoirs, {len(buildings)} bâtiments")
        return {"blocks": blocks, "buildings": buildings, "urban_network": urban_network}
    
    def define_tokyo_zones(self, size, block_density, building_variety):
        """Zones traditionnelles (grille)"""
        zones = {}
        center = size // 2
        total_blocks = size * size
        blocks_to_generate = int(total_blocks * block_density)
        
        all_positions = [(x, y) for x in range(size) for y in range(size)]
        
        def priority_score(pos):
            x, y = pos
            dist_from_center = abs(x - center) + abs(y - center)
            return dist_from_center
        
        all_positions.sort(key=priority_score)
        selected_positions = all_positions[:blocks_to_generate]
        
        for x, y in selected_positions:
            dist_from_center = abs(x - center) + abs(y - center)
            
            if building_variety == 'RESIDENTIAL_ONLY':
                zones[(x, y)] = 'residential'
            elif building_variety == 'BUSINESS_ONLY':
                zones[(x, y)] = 'business'
            elif building_variety == 'NO_BUSINESS':
                if dist_from_center <= 1:
                    zones[(x, y)] = 'commercial'
                else:
                    zones[(x, y)] = 'residential'
            else:  # ALL
                if dist_from_center == 0:
                    zones[(x, y)] = 'business'
                elif dist_from_center == 1:
                    zones[(x, y)] = 'commercial'
                else:
                    zones[(x, y)] = 'residential'
        
        return zones
    
    def create_district_blocks(self, size, zones):
        """Blocs traditionnels (grille)"""
        blocks = {}
        block_size = 20.0
        
        for (x, y), zone_type in zones.items():
            base_x = (x - size/2 + 0.5) * block_size
            base_y = (y - size/2 + 0.5) * block_size
            
            pos_x = base_x + random.uniform(-1.5, 1.5)
            pos_y = base_y + random.uniform(-1.5, 1.5)
            
            if zone_type == 'business':
                size_variation = random.uniform(0.85, 1.0)
                height = 0.15
            elif zone_type == 'commercial':
                size_variation = random.uniform(0.75, 0.95)
                height = 0.12
            else:  # residential
                size_variation = random.uniform(0.6, 0.9)
                height = 0.08
            
            actual_size = block_size * size_variation
            
            bpy.ops.mesh.primitive_cube_add(size=2.0, location=(pos_x, pos_y, height/2))
            block_obj = bpy.context.object
            block_obj.scale = (actual_size*0.9/2, actual_size*0.9/2, height/2)
            block_obj.name = f"TokyoSidewalk_{zone_type}_{x}_{y}"
            
            material = self.create_sidewalk_material(self.determine_sidewalk_type(zone_type))
            block_obj.data.materials.append(material)
            blocks[(x, y)] = block_obj
        
        return blocks
    
    def create_tokyo_buildings(self, size, zones):
        """Bâtiments traditionnels (grille)"""
        buildings = {}
        block_size = 20.0
        
        for (x, y), zone_type in zones.items():
            pos_x = (x - size/2 + 0.5) * block_size + random.uniform(-1.0, 1.0)
            pos_y = (y - size/2 + 0.5) * block_size + random.uniform(-1.0, 1.0)
            
            if zone_type == 'business':
                height = random.uniform(60, 160)
                width_x = random.uniform(0.5, 0.8) * block_size
                width_y = random.uniform(0.5, 0.8) * block_size
                building_name = f"TokyoBuilding_Skyscraper_{x}_{y}"
            elif zone_type == 'commercial':
                height = random.uniform(12, 32)
                width_x = random.uniform(0.6, 0.85) * block_size
                width_y = random.uniform(0.6, 0.85) * block_size
                building_name = f"TokyoBuilding_Commercial_{x}_{y}"
            else:  # residential
                height = random.uniform(4, 20)
                width_x = random.uniform(0.4, 0.7) * block_size
                width_y = random.uniform(0.4, 0.7) * block_size
                building_name = f"TokyoBuilding_House_{x}_{y}"
            
            bpy.ops.mesh.primitive_cube_add(size=2.0, location=(pos_x, pos_y, height/2))
            building_obj = bpy.context.object
            building_obj.scale = (width_x/2, width_y/2, height/2)
            building_obj.name = building_name
            
            material = self.create_building_material(zone_type)
            building_obj.data.materials.append(material)
            buildings[(x, y)] = building_obj
        
        return buildings
    
    def create_urban_network(self, size, zones, organic_factor):
        """Réseau urbain traditionnel (grille)"""
        network = {}
        block_size = 20.0
        
        # Routes horizontales
        for y in range(size + 1):
            for x in range(size):
                road_type = self.determine_street_type(x, y, size, "horizontal", zones)
                element = self.create_street_element(x, y, size, road_type, "horizontal", block_size, organic_factor)
                if element:
                    network[f"street_h_{x}_{y}"] = element
        
        # Routes verticales
        for x in range(size + 1):
            for y in range(size):
                road_type = self.determine_street_type(x, y, size, "vertical", zones)
                element = self.create_street_element(x, y, size, road_type, "vertical", block_size, organic_factor)
                if element:
                    network[f"street_v_{x}_{y}"] = element
        
        # Croisements
        for x in range(size + 1):
            for y in range(size + 1):
                crossing = self.create_crossing(x, y, size, block_size, zones, organic_factor)
                if crossing:
                    network[f"crossing_{x}_{y}"] = crossing
        
        # Sol de base
        background_zones = self.create_simple_ground(size, zones, block_size)
        for key, element in background_zones.items():
            network[key] = element
        
        return network
    
    def determine_street_type(self, x, y, size, direction, zones):
        """Type de rue traditionnel"""
        center = size // 2
        distance_from_center = max(abs(x - center), abs(y - center))
        
        adjacent_zones = []
        if direction == "horizontal":
            if (x, y) in zones: adjacent_zones.append(zones[(x, y)])
            if (x, y-1) in zones: adjacent_zones.append(zones[(x, y-1)])
        else:  # vertical
            if (x, y) in zones: adjacent_zones.append(zones[(x, y)])
            if (x-1, y) in zones: adjacent_zones.append(zones[(x-1, y)])
        
        if distance_from_center <= 1:
            if 'business' in adjacent_zones:
                return "main_avenue"
            else:
                return "secondary_road"
        elif distance_from_center <= 2:
            if 'commercial' in adjacent_zones:
                return "shopping_street"
            else:
                return "local_street"
        else:
            return "pedestrian_path"
    
    def create_street_element(self, x, y, size, street_type, direction, block_size, organic_factor):
        """Élément de rue traditionnel"""
        
        if street_type == "main_avenue":
            width = 8.0
            height = 0.02
            material_type = "asphalt_main"
        elif street_type == "secondary_road":
            width = 6.0
            height = 0.015
            material_type = "asphalt_secondary"
        elif street_type == "shopping_street":
            width = 5.0
            height = 0.01
            material_type = "paved_commercial"
        elif street_type == "local_street":
            width = 4.0
            height = 0.01
            material_type = "asphalt_local"
        else:  # pedestrian_path
            width = 2.5
            height = 0.005
            material_type = "pedestrian_stones"
        
        if direction == "horizontal":
            pos_x = (x - size/2 + 0.5) * block_size
            pos_y = (y - size/2) * block_size
            scale_x = block_size * 0.95 / 2
            scale_y = width / 2
            name = f"TokyoStreet_{street_type}_H_{x}_{y}"
        else:  # vertical
            pos_x = (x - size/2) * block_size
            pos_y = (y - size/2 + 0.5) * block_size
            scale_x = width / 2
            scale_y = block_size * 0.95 / 2
            name = f"TokyoStreet_{street_type}_V_{x}_{y}"
        
        # Variation organique
        pos_x += random.uniform(-organic_factor, organic_factor)
        pos_y += random.uniform(-organic_factor, organic_factor)
        
        bpy.ops.mesh.primitive_cube_add(size=2.0, location=(pos_x, pos_y, height/2))
        street_obj = bpy.context.object
        street_obj.scale = (scale_x, scale_y, height/2)
        street_obj.name = name
        
        material = self.create_street_material(material_type)
        street_obj.data.materials.append(material)
        
        return street_obj
    
    def create_crossing(self, x, y, size, block_size, zones, organic_factor):
        """Croisement traditionnel"""
        pos_x = (x - size/2) * block_size
        pos_y = (y - size/2) * block_size
        
        pos_x += random.uniform(-organic_factor*0.5, organic_factor*0.5)
        pos_y += random.uniform(-organic_factor*0.5, organic_factor*0.5)
        
        crossing_size = 4.0
        height = 0.01
        
        bpy.ops.mesh.primitive_cube_add(size=2.0, location=(pos_x, pos_y, height/2))
        crossing_obj = bpy.context.object
        crossing_obj.scale = (crossing_size/2, crossing_size/2, height/2)
        crossing_obj.name = f"TokyoCrossing_{x}_{y}"
        
        material = self.create_street_material("crossing")
        crossing_obj.data.materials.append(material)
        
        return crossing_obj
    
    def create_simple_ground(self, size, zones, block_size):
        """Sol simple traditionnel"""
        ground_elements = {}
        
        # Créer un sol de base général
        total_size = size * block_size + 10
        
        bpy.ops.mesh.primitive_cube_add(size=2.0, location=(0, 0, -0.05))
        ground_obj = bpy.context.object
        ground_obj.scale = (total_size/2, total_size/2, 0.025)
        ground_obj.name = "TokyoBaseGround"
        
        material = self.create_ground_material()
        ground_obj.data.materials.append(material)
        
        ground_elements['base_ground'] = ground_obj
        return ground_elements
    
    # === FONCTIONS DE MATÉRIAUX ===
    
    def determine_sidewalk_type(self, zone_type):
        """Détermine le type de trottoir selon la zone"""
        if zone_type == 'business':
            return "marble"
        elif zone_type == 'commercial':
            return "tiles"
        else:
            return "concrete"
    
    def create_sidewalk_material(self, sidewalk_type):
        """Crée un matériau de trottoir"""
        material = bpy.data.materials.new(name=f"Sidewalk_{sidewalk_type}")
        material.use_nodes = True
        nodes = material.node_tree.nodes
        nodes.clear()
        
        # Shader principal
        bsdf = nodes.new(type='ShaderNodeBsdfPrincipled')
        output = nodes.new(type='ShaderNodeOutputMaterial')
        material.node_tree.links.new(bsdf.outputs[0], output.inputs[0])
        
        if sidewalk_type == "marble":
            bsdf.inputs[0].default_value = (0.9, 0.9, 0.95, 1.0)  # Blanc cassé
            bsdf.inputs[9].default_value = 0.8  # Rugosité faible
        elif sidewalk_type == "tiles":
            bsdf.inputs[0].default_value = (0.7, 0.6, 0.5, 1.0)  # Beige
            bsdf.inputs[9].default_value = 0.4  # Rugosité moyenne
        else:  # concrete
            bsdf.inputs[0].default_value = (0.5, 0.5, 0.5, 1.0)  # Gris
            bsdf.inputs[9].default_value = 0.9  # Rugosité élevée
        
        return material
    
    def create_building_material(self, zone_type):
        """Crée un matériau de bâtiment"""
        material = bpy.data.materials.new(name=f"Building_{zone_type}")
        material.use_nodes = True
        nodes = material.node_tree.nodes
        nodes.clear()
        
        bsdf = nodes.new(type='ShaderNodeBsdfPrincipled')
        output = nodes.new(type='ShaderNodeOutputMaterial')
        material.node_tree.links.new(bsdf.outputs[0], output.inputs[0])
        
        if zone_type == 'business':
            bsdf.inputs[0].default_value = (0.2, 0.3, 0.4, 1.0)  # Bleu-gris (gratte-ciel)
            bsdf.inputs[6].default_value = 0.8  # Métallique
        elif zone_type == 'commercial':
            bsdf.inputs[0].default_value = (0.8, 0.6, 0.4, 1.0)  # Orange (centre commercial)
        else:  # residential
            bsdf.inputs[0].default_value = (0.7, 0.5, 0.4, 1.0)  # Brun (maison)
        
        return material
    
    def create_street_material(self, street_type):
        """Crée un matériau de rue"""
        material = bpy.data.materials.new(name=f"Street_{street_type}")
        material.use_nodes = True
        nodes = material.node_tree.nodes
        nodes.clear()
        
        bsdf = nodes.new(type='ShaderNodeBsdfPrincipled')
        output = nodes.new(type='ShaderNodeOutputMaterial')
        material.node_tree.links.new(bsdf.outputs[0], output.inputs[0])
        
        if street_type == "asphalt_main":
            bsdf.inputs[0].default_value = (0.1, 0.1, 0.1, 1.0)  # Noir
        elif street_type == "asphalt_secondary":
            bsdf.inputs[0].default_value = (0.15, 0.15, 0.15, 1.0)  # Gris foncé
        elif street_type == "paved_commercial":
            bsdf.inputs[0].default_value = (0.6, 0.5, 0.4, 1.0)  # Pavé brun
        elif street_type == "asphalt_local":
            bsdf.inputs[0].default_value = (0.2, 0.2, 0.2, 1.0)  # Gris
        elif street_type == "pedestrian_stones":
            bsdf.inputs[0].default_value = (0.8, 0.8, 0.7, 1.0)  # Pierre claire
        else:  # crossing
            bsdf.inputs[0].default_value = (0.9, 0.9, 0.9, 1.0)  # Blanc (passage piéton)
        
        bsdf.inputs[9].default_value = 0.8  # Rugosité
        return material
    
    def create_ground_material(self):
        """Crée un matériau de sol"""
        material = bpy.data.materials.new(name="Ground_Base")
        material.use_nodes = True
        nodes = material.node_tree.nodes
        nodes.clear()
        
        bsdf = nodes.new(type='ShaderNodeBsdfPrincipled')
        output = nodes.new(type='ShaderNodeOutputMaterial')
        material.node_tree.links.new(bsdf.outputs[0], output.inputs[0])
        
        bsdf.inputs[0].default_value = (0.3, 0.5, 0.3, 1.0)  # Vert (herbe/terre)
        bsdf.inputs[9].default_value = 1.0  # Rugosité maximale
        
        return material

# === INTERFACE UTILISATEUR ORGANIQUE ===

class TOKYO_PT_organic_panel(Panel):
    """Panneau Tokyo Organic"""
    bl_label = "Tokyo City Generator 1.1.0 ORGANIC"
    bl_idname = "TOKYO_PT_organic_panel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Tokyo'
    
    def draw(self, context):
        layout = self.layout
        scene = context.scene
        
        # === PARAMÈTRES DE BASE ===
        box = layout.box()
        box.label(text="🗾 Paramètres de base", icon='WORLD')
        
        col = box.column(align=True)
        col.prop(scene, "tokyo_size", text="Taille")
        col.prop(scene, "tokyo_density", text="Densité")
        col.prop(scene, "tokyo_variety", text="Types de bâtiments")
        col.prop(scene, "tokyo_organic", text="Variation organique")
        
        # === NOUVELLES OPTIONS ORGANIQUES ===
        box = layout.box()
        box.label(text="🌊 Options Organiques", icon='FORCE_TURBULENCE')
        
        col = box.column(align=True)
        col.prop(scene, "tokyo_use_voronoi", text="🌊 Utiliser Voronoï")
        
        if scene.tokyo_use_voronoi:
            subcol = col.column(align=True)
            subcol.prop(scene, "tokyo_voronoi_seed", text="Seed Voronoï")
            subcol.prop(scene, "tokyo_use_curved_streets", text="🛤️ Routes courbes")
            
            if scene.tokyo_use_curved_streets:
                subcol.prop(scene, "tokyo_curve_intensity", text="Intensité courbes")
        
        # === BOUTON DE GÉNÉRATION ===
        layout.separator()
        
        generation_text = "🌊 Générer Ville ORGANIQUE" if scene.tokyo_use_voronoi else "🗾 Générer Ville Traditionnelle"
        layout.operator("tokyo.generate_district", text=generation_text, icon='MESH_CUBE')
        
        # === INFORMATIONS ===
        box = layout.box()
        box.label(text="ℹ️ Informations", icon='INFO')
        
        info_text = ""
        if scene.tokyo_use_voronoi:
            info_text = "Mode ORGANIQUE:\n• Blocs irréguliers Voronoï\n"
            if scene.tokyo_use_curved_streets:
                info_text += "• Routes courbes naturelles"
            else:
                info_text += "• Connexions droites organiques"
        else:
            info_text = "Mode TRADITIONNEL:\n• Grille régulière\n• Variation organique"
        
        for line in info_text.split('\n'):
            if line.strip():
                box.label(text=line)

# === PROPRIÉTÉS DE SCÈNE ===

def register():
    bpy.utils.register_class(TOKYO_OT_generate_district)
    bpy.utils.register_class(TOKYO_PT_organic_panel)
    
    # Propriétés existantes
    bpy.types.Scene.tokyo_size = IntProperty(
        name="Taille du district",
        description="Nombre de blocs par côté",
        default=5,
        min=2,
        max=20
    )
    
    bpy.types.Scene.tokyo_density = FloatProperty(
        name="Densité de blocs",
        description="Proportion de l'espace occupée par des blocs",
        default=0.6,
        min=0.1,
        max=1.0
    )
    
    bpy.types.Scene.tokyo_variety = EnumProperty(
        name="Variété des bâtiments",
        description="Types de bâtiments à générer",
        items=[
            ('ALL', 'Tous types', 'Business + Commercial + Résidentiel'),
            ('NO_BUSINESS', 'Pas de business', 'Commercial + Résidentiel seulement'),
            ('RESIDENTIAL_ONLY', 'Résidentiel seulement', 'Maisons uniquement'),
            ('BUSINESS_ONLY', 'Business seulement', 'Gratte-ciels uniquement')
        ],
        default='ALL'
    )
    
    bpy.types.Scene.tokyo_organic = FloatProperty(
        name="Facteur organique",
        description="Variation de position pour aspect plus naturel",
        default=2.0,
        min=0.0,
        max=5.0
    )
    
    # === NOUVELLES PROPRIÉTÉS ORGANIQUES ===
    
    bpy.types.Scene.tokyo_use_voronoi = BoolProperty(
        name="Utiliser Voronoï",
        description="Génération organique avec cellules Voronoï au lieu de grille",
        default=False
    )
    
    bpy.types.Scene.tokyo_use_curved_streets = BoolProperty(
        name="Routes courbes",
        description="Utiliser des routes courbes organiques (requiert Voronoï)",
        default=False
    )
    
    bpy.types.Scene.tokyo_voronoi_seed = IntProperty(
        name="Seed Voronoï",
        description="Graine aléatoire pour la génération Voronoï",
        default=42,
        min=1,
        max=9999
    )
    
    bpy.types.Scene.tokyo_curve_intensity = FloatProperty(
        name="Intensité des courbes",
        description="Force de courbure des routes organiques",
        default=0.3,
        min=0.0,
        max=1.0
    )

def unregister():
    bpy.utils.unregister_class(TOKYO_OT_generate_district)
    bpy.utils.unregister_class(TOKYO_PT_organic_panel)
    
    # Supprimer les propriétés
    del bpy.types.Scene.tokyo_size
    del bpy.types.Scene.tokyo_density
    del bpy.types.Scene.tokyo_variety
    del bpy.types.Scene.tokyo_organic
    del bpy.types.Scene.tokyo_use_voronoi
    del bpy.types.Scene.tokyo_use_curved_streets
    del bpy.types.Scene.tokyo_voronoi_seed
    del bpy.types.Scene.tokyo_curve_intensity

if __name__ == "__main__":
    register()

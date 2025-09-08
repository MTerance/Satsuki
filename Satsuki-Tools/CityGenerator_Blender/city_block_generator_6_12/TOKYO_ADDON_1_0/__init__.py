bl_info = {
    "name": "Tokyo City Generator 1.5.1 TEXTURE SYSTEM + ROUTES + DIAGNOSTIC FIXED",
    "author": "Tokyo Urban Designer",
    "version": (1, 5, 1),
    "blender": (4, 0, 0),
    "location": "View3D > Sidebar > Tokyo Tab",
    "description": "Generate realistic Tokyo-style districts with INTELLIGENT TEXTURE SYSTEM for buildings AND ROADS + enhanced diagnostic tools",
    "category": "Add Mesh",
    "doc_url": "",
    "tracker_url": ""
}

import bpy
from bpy.props import IntProperty, FloatProperty, EnumProperty, BoolProperty
from bpy.types import Operator, Panel
import bmesh
import mathutils
import random
import os

# Import du système de textures avancé
try:
    from . import texture_system
    from .texture_system import TokyoTextureSystem, TokyoRoadTextureSystem
    
    # Créer l'instance globale si elle n'existe pas
    if not hasattr(texture_system, 'tokyo_texture_system'):
        texture_system.tokyo_texture_system = TokyoTextureSystem()
    
    tokyo_texture_system = texture_system.tokyo_texture_system
    TEXTURE_SYSTEM_AVAILABLE = True
    print("🎨 Système de textures Tokyo chargé avec succès")
    print("🛣️ Système de routes Tokyo chargé avec succès")
except ImportError as e:
    TEXTURE_SYSTEM_AVAILABLE = False
    tokyo_texture_system = None
    print(f"⚠️ Système de textures non disponible: {e}")
    print("🎨 Utilisation des matériaux procéduraux de base")
except Exception as e:
    TEXTURE_SYSTEM_AVAILABLE = False
    tokyo_texture_system = None
    print(f"⚠️ Erreur chargement système de textures: {e}")

# TOKYO 1.0.3 - FICHIER CORRIGÉ
# Bug résolu: Fichier vide → Contenu complet restauré

class TOKYO_OT_generate_district(Operator):
    """Generate Tokyo-style district"""
    bl_idname = "tokyo.generate_district"
    bl_label = "Generate Tokyo District"
    bl_options = {'REGISTER', 'UNDO'}
    
    def execute(self, context):
        # Récupérer les paramètres depuis la scène
        size = context.scene.tokyo_size
        density = context.scene.tokyo_density
        variety = context.scene.tokyo_variety
        organic = context.scene.tokyo_organic
        use_advanced_textures = context.scene.tokyo_use_advanced_textures
        
        # Nettoyer la scène
        self.clear_scene()
        
        # Vérifier disponibilité du système de textures
        if use_advanced_textures and not TEXTURE_SYSTEM_AVAILABLE:
            self.report({'WARNING'}, "Advanced texture system not available. Using basic materials.")
        
        # Créer le district Tokyo
        self.create_tokyo_district(size, organic, density, variety)
        
        blocks_count = int(size * size * density)
        texture_info = "with advanced textures" if (use_advanced_textures and TEXTURE_SYSTEM_AVAILABLE) else "with basic materials"
        self.report({'INFO'}, f"Tokyo district {size}x{size} with {blocks_count} blocks generated {texture_info}!")
        return {'FINISHED'}
    
    def clear_scene(self):
        """Supprime tous les objets Tokyo existants"""
        for obj in bpy.data.objects:
            if obj.name.startswith(("TokyoSidewalk_", "TokyoStreet_", "TokyoBuilding_", "TokyoCrossing_", "TokyoBaseGround")):
                bpy.data.objects.remove(obj, do_unlink=True)
    
    def create_tokyo_district(self, size, organic_factor, block_density, building_variety):
        """Crée un district Tokyo complet"""
        print(f"🗾 Création district Tokyo {size}x{size}")
        
        # 1. DÉFINIR LES ZONES
        zones = self.define_tokyo_zones(size, block_density, building_variety)
        
        # 2. CRÉER LES BLOCS
        blocks = self.create_district_blocks(size, zones)
        
        # 3. CRÉER LES BÂTIMENTS
        buildings = self.create_tokyo_buildings(size, zones)
        
        # 4. CRÉER LE RÉSEAU URBAIN (routes, rues piétonnes, croisements)
        urban_network = self.create_urban_network(size, zones, organic_factor)
        
        print(f"✅ District créé: {len(blocks)} blocs-trottoirs, {len(buildings)} bâtiments, {len(urban_network)} éléments urbains")
        return {"blocks": blocks, "buildings": buildings, "urban_network": urban_network}
    
    def define_tokyo_zones(self, size, block_density, building_variety):
        """Définit les zones du district Tokyo avec contrôle de densité"""
        zones = {}
        center = size // 2
        total_blocks = size * size
        blocks_to_generate = int(total_blocks * block_density)
        
        # Créer liste de toutes les positions
        all_positions = [(x, y) for x in range(size) for y in range(size)]
        
        # Trier par priorité (centre d'abord, puis proche centre, puis périphérie)
        def priority_score(pos):
            x, y = pos
            dist_from_center = abs(x - center) + abs(y - center)
            return dist_from_center
        
        all_positions.sort(key=priority_score)
        
        # Sélectionner les blocs à générer selon la densité
        selected_positions = all_positions[:blocks_to_generate]
        
        # Assigner les zones selon le type de bâtiments voulu
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
        """Crée les blocs-trottoirs du district selon les zones définies"""
        blocks = {}
        block_size = 20.0
        
        for (x, y), zone_type in zones.items():
            # Position du bloc avec variation aléatoire
            base_x = (x - size/2 + 0.5) * block_size
            base_y = (y - size/2 + 0.5) * block_size
            
            # Ajouter variation de position et taille pour plus de réalisme
            pos_x = base_x + random.uniform(-1.5, 1.5)
            pos_y = base_y + random.uniform(-1.5, 1.5)
            
            # Variation de taille selon la zone
            if zone_type == 'business':
                size_variation = random.uniform(0.85, 1.0)  # Blocs business plus réguliers
                height = 0.15  # Trottoirs surélevés
            elif zone_type == 'commercial':
                size_variation = random.uniform(0.75, 0.95)  # Variation moyenne
                height = 0.12  # Trottoirs moyens
            else:  # residential
                size_variation = random.uniform(0.6, 0.9)   # Plus de variation
                height = 0.08  # Trottoirs plus bas
            
            actual_size = block_size * size_variation
            
            # Créer le bloc-trottoir
            bpy.ops.mesh.primitive_cube_add(size=2.0, location=(pos_x, pos_y, height/2))
            block_obj = bpy.context.object
            # Appliquer la taille correcte avec variation
            block_obj.scale = (actual_size*0.9/2, actual_size*0.9/2, height/2)
            block_obj.name = f"TokyoSidewalk_{zone_type}_{x}_{y}"
            
            # Matériau de trottoir selon la zone
            material = self.create_sidewalk_material(self.determine_sidewalk_type(zone_type))
            block_obj.data.materials.append(material)
            blocks[(x, y)] = block_obj
        
        return blocks
    
    def create_tokyo_buildings(self, size, zones):
        """Crée les bâtiments sur chaque bloc selon la zone"""
        buildings = {}
        block_size = 20.0
        
        for (x, y), zone_type in zones.items():
            # Position avec variation organique
            pos_x = (x - size/2 + 0.5) * block_size + random.uniform(-1.0, 1.0)
            pos_y = (y - size/2 + 0.5) * block_size + random.uniform(-1.0, 1.0)
            
            # Hauteur et taille selon le type de zone avec plus de variation
            if zone_type == 'business':
                height = random.uniform(60, 160)
                # Gratte-ciels avec formes variées
                width_x = random.uniform(0.5, 0.8) * block_size
                width_y = random.uniform(0.5, 0.8) * block_size
                building_name = f"Skyscraper_{x}_{y}"
            elif zone_type == 'commercial':
                height = random.uniform(12, 32)
                # Centres commerciaux plus carrés
                width_x = random.uniform(0.6, 0.85) * block_size
                width_y = random.uniform(0.6, 0.85) * block_size
                building_name = f"Commercial_{x}_{y}"
            else:  # residential
                height = random.uniform(4, 20)
                # Maisons avec formes plus variées
                width_x = random.uniform(0.4, 0.7) * block_size
                width_y = random.uniform(0.4, 0.7) * block_size
                building_name = f"House_{x}_{y}"
            
            # Créer le bâtiment
            bpy.ops.mesh.primitive_cube_add(size=2.0, location=(pos_x, pos_y, height/2))
            building_obj = bpy.context.object
            # Appliquer la taille avec variation
            building_obj.scale = (width_x/2, width_y/2, height/2)
            building_obj.name = f"TokyoBuilding_{building_name}"
            
            # NOUVEAU: Utiliser le système de textures avancé si activé
            use_advanced = bpy.context.scene.tokyo_use_advanced_textures if hasattr(bpy.context.scene, 'tokyo_use_advanced_textures') else True
            
            if TEXTURE_SYSTEM_AVAILABLE and use_advanced and tokyo_texture_system is not None:
                try:
                    # Récupérer le chemin configuré
                    texture_path = getattr(bpy.context.scene, 'tokyo_texture_base_path', r"C:\Users\sshom\Documents\assets\Tools\tokyo_textures")
                    material = tokyo_texture_system.create_advanced_building_material(
                        zone_type, height, width_x, width_y, building_name, texture_path
                    )
                except Exception as e:
                    print(f"⚠️ Erreur création matériau avancé: {e}")
                    material = self.create_building_material(zone_type)
            else:
                # Fallback vers ancien système
                material = self.create_building_material(zone_type)
            
            building_obj.data.materials.append(material)
            buildings[(x, y)] = building_obj
        
        return buildings
    
    def create_urban_network(self, size, zones, organic_factor):
        """Crée le réseau urbain : routes, rues piétonnes et croisements avec couverture complète"""
        network = {}
        block_size = 20.0
        
        # === ÉTAPE 1: CRÉER TOUTES LES ROUTES HORIZONTALES ===
        for y in range(size + 1):
            for x in range(size):
                road_type = self.determine_street_type(x, y, size, "horizontal", zones)
                element = self.create_street_element(x, y, size, road_type, "horizontal", block_size, organic_factor)
                if element:
                    network[f"street_h_{x}_{y}"] = element
        
        # === ÉTAPE 2: CRÉER TOUTES LES ROUTES VERTICALES ===
        for x in range(size + 1):
            for y in range(size):
                road_type = self.determine_street_type(x, y, size, "vertical", zones)
                element = self.create_street_element(x, y, size, road_type, "vertical", block_size, organic_factor)
                if element:
                    network[f"street_v_{x}_{y}"] = element
        
        # === ÉTAPE 3: CRÉER TOUS LES CROISEMENTS ===
        for x in range(size + 1):
            for y in range(size + 1):
                crossing = self.create_crossing(x, y, size, block_size, zones, organic_factor)
                if crossing:
                    network[f"crossing_{x}_{y}"] = crossing
        
        # === ÉTAPE 4: SOL DE BASE SIMPLE (seulement là où nécessaire) ===
        background_zones = self.create_simple_ground(size, zones, block_size)
        for key, element in background_zones.items():
            network[key] = element
        
        return network
    
    def determine_street_type(self, x, y, size, direction, zones):
        """Détermine le type de rue selon la position et les zones adjacentes"""
        center = size // 2
        distance_from_center = max(abs(x - center), abs(y - center))
        
        # Analyser les zones adjacentes pour déterminer le type de rue
        adjacent_zones = []
        if direction == "horizontal":
            if (x, y) in zones: adjacent_zones.append(zones[(x, y)])
            if (x, y-1) in zones: adjacent_zones.append(zones[(x, y-1)])
        else:  # vertical
            if (x, y) in zones: adjacent_zones.append(zones[(x, y)])
            if (x-1, y) in zones: adjacent_zones.append(zones[(x-1, y)])
        
        # Règles de détermination
        if distance_from_center <= 1:
            if 'business' in adjacent_zones:
                return "main_avenue"      # Avenue principale (business)
            else:
                return "secondary_road"   # Route secondaire
        elif distance_from_center <= 2:
            if 'commercial' in adjacent_zones:
                return "shopping_street"  # Rue commerçante
            else:
                return "local_street"     # Rue locale
        else:
            return "pedestrian_path"      # Chemin piéton
    
    def create_street_element(self, x, y, size, street_type, direction, block_size, organic_factor):
        """Crée un élément de rue selon le type"""
        
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
        
        # Position selon la direction avec couverture raisonnée
        if direction == "horizontal":
            pos_x = (x - size/2 + 0.5) * block_size
            pos_y = (y - size/2) * block_size
            scale_x = block_size * 0.95 / 2  # Réajusté pour éviter trop de chevauchement
            scale_y = width / 2
            name = f"TokyoStreet_{street_type}_H_{x}_{y}"
        else:  # vertical
            pos_x = (x - size/2) * block_size
            pos_y = (y - size/2 + 0.5) * block_size
            scale_x = width / 2
            scale_y = block_size * 0.95 / 2  # Réajusté pour éviter trop de chevauchement
            name = f"TokyoStreet_{street_type}_V_{x}_{y}"
        
        # Variation organique
        if organic_factor > 0:
            curve_strength = organic_factor * 3.0
            pos_x += random.uniform(-curve_strength, curve_strength)
            pos_y += random.uniform(-curve_strength, curve_strength)
        
        # Créer l'élément
        bpy.ops.mesh.primitive_cube_add(size=2.0, location=(pos_x, pos_y, height/2))
        street_obj = bpy.context.object
        street_obj.scale = (scale_x, scale_y, height/2)
        street_obj.name = name
        
        # Matériau
        material = self.create_street_material(material_type)
        street_obj.data.materials.append(material)
        
        return street_obj
    
    def create_crossing(self, x, y, size, block_size, zones, organic_factor):
        """Crée un croisement à l'intersection"""
        pos_x = (x - size/2) * block_size
        pos_y = (y - size/2) * block_size
        
        # Variation organique
        if organic_factor > 0:
            pos_x += random.uniform(-1.0, 1.0)
            pos_y += random.uniform(-1.0, 1.0)
        
        # Taille du croisement (réduite pour plus de réalisme)
        crossing_size = 4.0  # Réduit pour éviter la domination visuelle
        height = 0.01        # Plus fin
        
        # Créer le croisement
        bpy.ops.mesh.primitive_cube_add(size=2.0, location=(pos_x, pos_y, height/2))
        crossing_obj = bpy.context.object
        crossing_obj.scale = (crossing_size/2, crossing_size/2, height/2)
        crossing_obj.name = f"TokyoCrossing_{x}_{y}"
        
        # Matériau de croisement
        material = self.create_street_material("crossing_asphalt")
        crossing_obj.data.materials.append(material)
        
        return crossing_obj
    
    def create_simple_ground(self, size, zones, block_size):
        """Crée un sol de base simple seulement où nécessaire"""
        ground = {}
        
        # Sol de base simple sous tout le district
        ground_size = size * block_size + 10  # Légèrement plus grand que le district
        height = 0.001  # Très fin
        
        # Un seul grand plan de sol
        pos_x = 0
        pos_y = 0
        
        bpy.ops.mesh.primitive_cube_add(size=2.0, location=(pos_x, pos_y, -height/2))
        ground_obj = bpy.context.object
        ground_obj.scale = (ground_size/2, ground_size/2, height/2)
        ground_obj.name = "TokyoBaseGround"
        
        # Matériau de sol simple
        material = self.create_simple_ground_material()
        ground_obj.data.materials.append(material)
        
        ground["base_ground"] = ground_obj
        return ground
    
    def create_simple_ground_material(self):
        """Crée un matériau simple pour le sol de base"""
        mat_name = "Tokyo_BaseGround"
        mat = bpy.data.materials.new(name=mat_name)
        mat.use_nodes = True
        
        # Couleur discrète
        color = (0.4, 0.4, 0.4, 1.0)  # Gris neutre
        roughness = 0.95
        
        mat.node_tree.nodes["Principled BSDF"].inputs[0].default_value = color
        mat.node_tree.nodes["Principled BSDF"].inputs[7].default_value = roughness
        return mat
    
    def create_street_material(self, material_type):
        """Crée un matériau pour les éléments de rue"""
        mat_name = f"Tokyo_Street_{material_type}"
        mat = bpy.data.materials.new(name=mat_name)
        mat.use_nodes = True
        
        if material_type == "asphalt_main":
            color = (0.1, 0.1, 0.1, 1.0)    # Asphalte principal - noir
            roughness = 0.9
        elif material_type == "asphalt_secondary":
            color = (0.15, 0.15, 0.15, 1.0)  # Asphalte secondaire - gris foncé
            roughness = 0.8
        elif material_type == "paved_commercial":
            color = (0.6, 0.55, 0.5, 1.0)   # Pavés commerciaux - beige
            roughness = 0.95
        elif material_type == "asphalt_local":
            color = (0.2, 0.2, 0.2, 1.0)    # Asphalte local - gris
            roughness = 0.7
        elif material_type == "pedestrian_stones":
            color = (0.7, 0.65, 0.6, 1.0)   # Pierres piétonnes - beige clair
            roughness = 0.85
        else:  # crossing_asphalt
            color = (0.12, 0.12, 0.12, 1.0) # Croisement - asphalte avec marquage
            roughness = 0.8
        
        mat.node_tree.nodes["Principled BSDF"].inputs[0].default_value = color
        mat.node_tree.nodes["Principled BSDF"].inputs[7].default_value = roughness
        return mat
    
    def determine_sidewalk_type(self, zone_type):
        """Détermine le type de trottoir selon la zone"""
        if zone_type == "business":
            return "modern_concrete"  # Trottoir béton moderne
        elif zone_type == "commercial":
            return "paved_stones"     # Trottoir pavé
        else:  # residential
            return "simple_concrete"  # Trottoir béton simple
    
    def create_building_material(self, zone_type):
        """Crée un matériau pour les bâtiments"""
        mat_name = f"Tokyo_{zone_type}_Building"
        mat = bpy.data.materials.new(name=mat_name)
        mat.use_nodes = True
        
        if zone_type == 'business':
            color = (0.8, 0.8, 0.9, 1.0)  # Gris métallique
            mat.node_tree.nodes["Principled BSDF"].inputs[6].default_value = 0.8  # Metallic
        elif zone_type == 'commercial':
            color = (0.9, 0.6, 0.3, 1.0)  # Orange
        else:  # residential
            color = (0.7, 0.9, 0.6, 1.0)  # Vert clair
        
        mat.node_tree.nodes["Principled BSDF"].inputs[0].default_value = color
        return mat
    
    def create_sidewalk_material(self, sidewalk_type):
        """Crée un matériau pour les trottoirs"""
        mat_name = f"Tokyo_Sidewalk_{sidewalk_type}"
        mat = bpy.data.materials.new(name=mat_name)
        mat.use_nodes = True
        
        if sidewalk_type == "modern_concrete":
            color = (0.85, 0.85, 0.85, 1.0)  # Béton moderne clair
            roughness = 0.4
        elif sidewalk_type == "paved_stones":
            color = (0.6, 0.55, 0.5, 1.0)    # Pavés beiges
            roughness = 0.9
        else:  # simple_concrete
            color = (0.7, 0.7, 0.7, 1.0)     # Béton simple
            roughness = 0.6
        
        mat.node_tree.nodes["Principled BSDF"].inputs[0].default_value = color
        mat.node_tree.nodes["Principled BSDF"].inputs[7].default_value = roughness
        return mat


# INTERFACE UTILISATEUR COMPATIBLE BLENDER 4.x
class TOKYO_PT_main_panel(Panel):
    """Panneau principal Tokyo"""
    bl_label = "Tokyo City Generator 1.4.0"
    bl_idname = "TOKYO_PT_main_panel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Tokyo'
    
    def draw(self, context):
        layout = self.layout
        
        # Titre avec icône
        row = layout.row()
        row.label(text="🗾 Tokyo District Generator", icon='WORLD')
        layout.separator()
        
        # Boîte pour les paramètres
        box = layout.box()
        box.label(text="⚙️ Configuration", icon='PREFERENCES')
        
        # District Size
        row = box.row()
        row.label(text="District Size:")
        row.prop(context.scene, "tokyo_size", text="")
        
        # Block Density  
        row = box.row()
        row.label(text="Block Density:")
        row.prop(context.scene, "tokyo_density", text="", slider=True)
        
        # Building Variety
        row = box.row()
        row.label(text="Building Variety:")
        row.prop(context.scene, "tokyo_variety", text="")
        
        # Organic Factor
        row = box.row()
        row.label(text="Organic Streets:")
        row.prop(context.scene, "tokyo_organic", text="", slider=True)
        
        # NOUVEAU: Système de textures avancé
        row = box.row()
        row.label(text="Advanced Textures:")
        row.prop(context.scene, "tokyo_use_advanced_textures", text="")
        
        # Chemin des textures (seulement si textures avancées activées)
        if context.scene.tokyo_use_advanced_textures:
            row = box.row()
            row.label(text="Texture Path:")
            row.prop(context.scene, "tokyo_texture_base_path", text="")
        
        layout.separator()
        
        # Bouton de génération
        layout.operator("tokyo.generate_district", text="🚀 Generate Tokyo District", icon='MESH_CUBE')
        
        layout.separator()
        
        # NOUVEAUX BOUTONS: Diagnostic et Test
        if context.scene.tokyo_use_advanced_textures:
            box_debug = layout.box()
            box_debug.label(text="🔧 Texture Troubleshooting:", icon='TOOL_SETTINGS')
            
            col = box_debug.column(align=True)
            col.operator("tokyo.diagnostic_textures", text="🔍 Diagnostic Textures", icon='INFO')
            col.operator("tokyo.test_textures", text="🧪 Test Bâtiments", icon='CUBE')
            col.operator("tokyo.test_road_textures", text="🛣️ Test Routes", icon='MESH_PLANE')
        
        layout.separator()
        
        # Informations
        box2 = layout.box()
        box2.label(text="📊 Building Types", icon='INFO')
        box2.label(text="• Business: Skyscrapers 15-40 floors")
        box2.label(text="• Commercial: Centers 3-8 floors") 
        box2.label(text="• Residential: Houses 1-5 floors")


# NOUVEL OPÉRATEUR: DIAGNOSTIC TEXTURES
class TOKYO_OT_diagnostic_textures(Operator):
    """Diagnostic automatique du système de textures Tokyo"""
    bl_idname = "tokyo.diagnostic_textures"
    bl_label = "🔍 Diagnostic Textures"
    bl_description = "Diagnostiquer pourquoi les textures ne s'appliquent pas"

    def execute(self, context):
        self.report({'INFO'}, "🔍 Diagnostic des textures en cours...")
        
        # Résultats du diagnostic
        issues = []
        solutions = []
        
        # Test 1: Vérifier Advanced Textures
        if hasattr(context.scene, 'tokyo_use_advanced_textures'):
            use_advanced = context.scene.tokyo_use_advanced_textures
            if not use_advanced:
                issues.append("❌ Advanced Textures désactivé")
                solutions.append("→ Cocher 'Advanced Textures' dans le panneau Tokyo")
            else:
                self.report({'INFO'}, "✅ Advanced Textures activé")
        else:
            issues.append("❌ Propriété Advanced Textures manquante")
            solutions.append("→ Réinstaller l'addon Tokyo v1.4.0")
        
        # Test 2: Vérifier chemin textures
        if hasattr(context.scene, 'tokyo_texture_base_path'):
            texture_path = context.scene.tokyo_texture_base_path
            if texture_path and os.path.exists(texture_path):
                self.report({'INFO'}, f"✅ Dossier textures trouvé: {texture_path}")
            else:
                issues.append("❌ Dossier textures inexistant")
                solutions.append("→ Configurer le chemin textures ou créer les dossiers")
        else:
            issues.append("❌ Propriété chemin textures manquante")
            solutions.append("→ Réinstaller l'addon Tokyo v1.4.0")
        
        # Test 3: Vérifier module texture_system
        try:
            if TEXTURE_SYSTEM_AVAILABLE:
                self.report({'INFO'}, "✅ Module texture_system chargé")
            else:
                issues.append("❌ Module texture_system non disponible")
                solutions.append("→ Vérifier l'installation de l'addon")
        except:
            issues.append("❌ Erreur module texture_system")
            solutions.append("→ Réinstaller l'addon complet")
        
        # Test 4: Vérifier mode d'affichage
        for area in context.screen.areas:
            if area.type == 'VIEW_3D':
                for space in area.spaces:
                    if space.type == 'VIEW_3D':
                        if space.shading.type not in ['MATERIAL', 'RENDERED']:
                            issues.append("❌ Mode d'affichage incorrect")
                            solutions.append("→ Passer en Material Preview ou Rendered")
                        else:
                            self.report({'INFO'}, f"✅ Mode d'affichage: {space.shading.type}")
        
        # Test 5: Vérifier matériaux Tokyo existants
        tokyo_materials = [mat for mat in bpy.data.materials if 'tokyo' in mat.name.lower()]
        if tokyo_materials:
            self.report({'INFO'}, f"✅ {len(tokyo_materials)} matériaux Tokyo trouvés")
        else:
            issues.append("❌ Aucun matériau Tokyo trouvé")
            solutions.append("→ Générer un nouveau district pour créer les matériaux")
        
        # Test 6: Diagnostic approfondi du système de textures
        self.report({'INFO'}, "🔍 Diagnostic système de textures...")
        
        if TEXTURE_SYSTEM_AVAILABLE:
            self.report({'INFO'}, "✅ TEXTURE_SYSTEM_AVAILABLE = True")
            
            if tokyo_texture_system is not None:
                self.report({'INFO'}, "✅ tokyo_texture_system instance OK")
                try:
                    # Test basique de création de matériau
                    test_material = tokyo_texture_system.create_advanced_building_material(
                        "residential", 10.0, 5.0, 5.0, "DiagnosticTest", ""
                    )
                    if test_material:
                        self.report({'INFO'}, "✅ Création matériau test réussie")
                        # Nettoyer le test
                        bpy.data.materials.remove(test_material)
                    else:
                        issues.append("❌ Création matériau test échouée")
                        solutions.append("→ Vérifier les paramètres du système")
                except Exception as e:
                    issues.append(f"❌ Erreur test matériau: {str(e)}")
                    solutions.append("→ Réinstaller l'addon")
            else:
                issues.append("❌ tokyo_texture_system = None")
                solutions.append("→ Erreur d'initialisation - redémarrer Blender")
        else:
            issues.append("❌ TEXTURE_SYSTEM_AVAILABLE = False")
            solutions.append("→ Erreur d'import - vérifier les fichiers addon")
        
        # Test 7: Vérifier module texture_system
        try:
            import sys
            addon_modules = [name for name in sys.modules.keys() if 'texture_system' in name]
            if addon_modules:
                self.report({'INFO'}, f"✅ Modules texture trouvés: {addon_modules}")
            else:
                issues.append("❌ Module texture_system absent")
                solutions.append("→ Fichier texture_system.py manquant")
        except:
            pass
        
        # Afficher les résultats
        if issues:
            self.report({'WARNING'}, f"🔍 DIAGNOSTIC: {len(issues)} problème(s) détecté(s)")
            for i, issue in enumerate(issues):
                self.report({'ERROR'}, f"{i+1}. {issue}")
                if i < len(solutions):
                    self.report({'INFO'}, f"   {solutions[i]}")
        else:
            self.report({'INFO'}, "✅ Aucun problème détecté - Système de textures OK")
            self.report({'INFO'}, "💡 Si textures toujours invisibles: vérifier le mode d'affichage")
        
        return {'FINISHED'}


# NOUVEL OPÉRATEUR: TEST TEXTURES SIMPLE
class TOKYO_OT_test_textures(Operator):
    """Test visuel simple des textures avec cubes de démonstration"""
    bl_idname = "tokyo.test_textures"
    bl_label = "🧪 Test Textures"
    bl_description = "Créer des cubes test pour vérifier l'affichage des textures"

    def execute(self, context):
        self.report({'INFO'}, "🧪 Création des cubes test...")
        
        # Sauvegarder la sélection actuelle
        selected_objects = context.selected_objects.copy()
        
        try:
            # Créer cube test 1: Matériau coloré
            bpy.ops.mesh.primitive_cube_add(location=(0, 0, 1))
            cube1 = context.object
            cube1.name = "Tokyo_Test_Colored"
            
            # Matériau coloré
            mat1 = bpy.data.materials.new(name="Tokyo_Test_Blue")
            mat1.use_nodes = True
            nodes = mat1.node_tree.nodes
            nodes.clear()
            
            output = nodes.new(type='ShaderNodeOutputMaterial')
            bsdf = nodes.new(type='ShaderNodeBsdfPrincipled')
            bsdf.inputs['Base Color'].default_value = (0.2, 0.5, 1.0, 1.0)  # Bleu
            mat1.node_tree.links.new(bsdf.outputs['BSDF'], output.inputs['Surface'])
            
            cube1.data.materials.append(mat1)
            
            # Créer cube test 2: Texture procédurale
            bpy.ops.mesh.primitive_cube_add(location=(3, 0, 1))
            cube2 = context.object
            cube2.name = "Tokyo_Test_Procedural"
            
            mat2 = bpy.data.materials.new(name="Tokyo_Test_Noise")
            mat2.use_nodes = True
            nodes = mat2.node_tree.nodes
            nodes.clear()
            
            output = nodes.new(type='ShaderNodeOutputMaterial')
            bsdf = nodes.new(type='ShaderNodeBsdfPrincipled')
            noise = nodes.new(type='ShaderNodeTexNoise')
            noise.inputs['Scale'].default_value = 5.0
            
            colorramp = nodes.new(type='ShaderNodeValToRGB')
            colorramp.color_ramp.elements[0].color = (0.8, 0.4, 0.2, 1.0)
            colorramp.color_ramp.elements[1].color = (0.2, 0.2, 0.2, 1.0)
            
            mat2.node_tree.links.new(noise.outputs['Fac'], colorramp.inputs['Fac'])
            mat2.node_tree.links.new(colorramp.outputs['Color'], bsdf.inputs['Base Color'])
            mat2.node_tree.links.new(bsdf.outputs['BSDF'], output.inputs['Surface'])
            
            cube2.data.materials.append(mat2)
            
            # Créer cube test 3: Test système Tokyo
            bpy.ops.mesh.primitive_cube_add(location=(6, 0, 1))
            cube3 = context.object
            cube3.name = "Tokyo_Test_System"
            cube3.scale = (2, 2, 4)  # Forme de bâtiment
            
            # Essayer d'utiliser le système Tokyo
            if TEXTURE_SYSTEM_AVAILABLE and tokyo_texture_system is not None and hasattr(context.scene, 'tokyo_use_advanced_textures'):
                try:
                    texture_path = getattr(context.scene, 'tokyo_texture_base_path', "")
                    material = tokyo_texture_system.create_advanced_building_material(
                        "business", 8.0, 4.0, 4.0, "TestBuilding", texture_path
                    )
                    cube3.data.materials.append(material)
                    self.report({'INFO'}, "✅ Matériau Tokyo système appliqué")
                except Exception as e:
                    # Fallback
                    mat3 = bpy.data.materials.new(name="Tokyo_Test_Fallback")
                    mat3.use_nodes = True
                    nodes = mat3.node_tree.nodes
                    nodes.clear()
                    
                    output = nodes.new(type='ShaderNodeOutputMaterial')
                    bsdf = nodes.new(type='ShaderNodeBsdfPrincipled')
                    bsdf.inputs['Base Color'].default_value = (0.7, 0.7, 0.7, 1.0)
                    bsdf.inputs['Metallic'].default_value = 0.3
                    mat3.node_tree.links.new(bsdf.outputs['BSDF'], output.inputs['Surface'])
                    
                    cube3.data.materials.append(mat3)
                    self.report({'WARNING'}, f"⚠️ Fallback appliqué: {str(e)}")
            else:
                self.report({'WARNING'}, "⚠️ Système Tokyo non disponible")
            
            # Configurer la vue en Material Preview
            for area in context.screen.areas:
                if area.type == 'VIEW_3D':
                    for space in area.spaces:
                        if space.type == 'VIEW_3D':
                            space.shading.type = 'MATERIAL'
                            break
            
            self.report({'INFO'}, "✅ 3 cubes test créés! Mode Material Preview activé.")
            self.report({'INFO'}, "💡 Vérifiez visuellement les textures dans la vue 3D")
            
        except Exception as e:
            self.report({'ERROR'}, f"❌ Erreur création test: {str(e)}")
        
        return {'FINISHED'}


class TOKYO_OT_test_road_textures(Operator):
    """Test visuel des textures de routes avec sections de démonstration"""
    bl_idname = "tokyo.test_road_textures"
    bl_label = "🛣️ Test Textures Routes"
    bl_description = "Créer des sections de routes test pour vérifier les textures quadrants"

    def execute(self, context):
        self.report({'INFO'}, "🛣️ Création des sections test routes...")
        
        try:
            # Vérifier que le système de routes est disponible
            if not TEXTURE_SYSTEM_AVAILABLE:
                self.report({'ERROR'}, "❌ Système de textures non disponible")
                return {'CANCELLED'}
            
            # Récupérer le chemin de base
            texture_path = getattr(context.scene, 'tokyo_texture_base_path', "")
            if not texture_path:
                texture_path = "C:\\Users\\sshom\\Documents\\assets\\Tools\\textures"
            
            road_system = TokyoRoadTextureSystem(texture_path)
            
            # Créer un setup de route de test avec 4 sections
            sections = [
                {'name': 'Centre_Route', 'location': (0, 0, 0), 'type': 'road_center'},
                {'name': 'Bord_Route', 'location': (4, 0, 0), 'type': 'road_border'},
                {'name': 'Trottoir_Beton', 'location': (8, 0, 0), 'type': 'sidewalk_concrete'},
                {'name': 'Trottoir_Carrelage', 'location': (12, 0, 0), 'type': 'sidewalk_tiles'}
            ]
            
            for section in sections:
                # Créer un plane pour chaque section
                bpy.ops.mesh.primitive_plane_add(
                    size=3,
                    location=section['location']
                )
                plane = context.object
                plane.name = f"Tokyo_Road_Test_{section['name']}"
                
                # Créer le matériau correspondant
                material = road_system.create_road_material(
                    road_type=section['type'],
                    material_name=f"Tokyo_Test_{section['name']}"
                )
                
                # Appliquer le matériau
                plane.data.materials.append(material)
                
                # Ajouter un texte 3D pour identifier la section
                bpy.ops.object.text_add(location=(section['location'][0], section['location'][1] - 2, 0.1))
                text_obj = context.object
                text_obj.name = f"Label_{section['name']}"
                text_obj.data.body = section['type'].replace('_', ' ').title()
                text_obj.data.size = 0.5
                text_obj.rotation_euler = (1.5708, 0, 0)  # Rotation X de 90 degrés
            
            # Créer une scène de route complète
            bpy.ops.mesh.primitive_plane_add(size=20, location=(20, 0, 0))
            full_road = context.object
            full_road.name = "Tokyo_Full_Road_Demo"
            
            # Matériau combiné pour la route complète (on utilisera le centre)
            full_material = road_system.create_road_material(
                road_type='road_center',
                material_name="Tokyo_Full_Road"
            )
            full_road.data.materials.append(full_material)
            
            # Ajouter des cubes pour simuler des bâtiments autour
            for i in range(4):
                for j in range(4):
                    if i != 1 and j != 1:  # Laisser de l'espace pour la route
                        bpy.ops.mesh.primitive_cube_add(
                            location=(15 + i*5, -5 + j*5, 2),
                            scale=(2, 2, 4)
                        )
                        building = context.object
                        building.name = f"Demo_Building_{i}_{j}"
            
            # Configurer la vue
            for area in context.screen.areas:
                if area.type == 'VIEW_3D':
                    for space in area.spaces:
                        if space.type == 'VIEW_3D':
                            space.shading.type = 'MATERIAL'
                            # Centrer la vue sur les tests
                            space.region_3d.view_location = (10, 0, 0)
                            break
            
            self.report({'INFO'}, "✅ Tests routes créés!")
            self.report({'INFO'}, f"📁 Chemin textures: {texture_path}")
            self.report({'INFO'}, "🔍 4 sections test + 1 route complète + bâtiments démo")
            self.report({'INFO'}, "🎨 Vérifiez les mappings de texture dans Material Preview")
            
        except Exception as e:
            self.report({'ERROR'}, f"❌ Erreur création test routes: {str(e)}")
        
        return {'FINISHED'}


# ENREGISTREMENT BLENDER
classes = [
    TOKYO_OT_generate_district,
    TOKYO_OT_diagnostic_textures,  # NOUVEAU
    TOKYO_OT_test_textures,        # NOUVEAU
    TOKYO_OT_test_road_textures,   # NOUVEAU - ROUTES
    TOKYO_PT_main_panel,
]

# PROPRIÉTÉS DE SCÈNE pour l'interface
def init_scene_properties():
    """Initialise les propriétés de scène pour l'interface"""
    bpy.types.Scene.tokyo_size = IntProperty(
        name="District Size",
        description="Size of the district (3=3x3, 5=5x5)",
        default=3,
        min=3,
        max=7
    )
    
    bpy.types.Scene.tokyo_density = FloatProperty(
        name="Block Density",
        description="Percentage of blocks that will have buildings",
        default=1.0,
        min=0.3,
        max=1.0,
        subtype='PERCENTAGE'
    )
    
    bpy.types.Scene.tokyo_variety = EnumProperty(
        name="Building Variety",
        description="Types of buildings to generate",
        items=[
            ('ALL', 'All Types', 'Business + Commercial + Residential'),
            ('BUSINESS_ONLY', 'Business Only', 'Only skyscrapers'),
            ('NO_BUSINESS', 'No Business', 'Commercial + Residential only'),
            ('RESIDENTIAL_ONLY', 'Residential Only', 'Only houses')
        ],
        default='ALL'
    )
    
    bpy.types.Scene.tokyo_organic = FloatProperty(
        name="Organic Streets",
        description="How organic/curved the streets are",
        default=0.3,
        min=0.0,
        max=1.0,
        subtype='FACTOR'
    )
    
    # NOUVEAU: Propriété pour système de textures avancé
    bpy.types.Scene.tokyo_use_advanced_textures = BoolProperty(
        name="Use Advanced Textures",
        description="Use texture system based on building dimensions",
        default=True
    )
    
    # Chemin vers les textures
    bpy.types.Scene.tokyo_texture_base_path = bpy.props.StringProperty(
        name="Texture Base Path",
        description="Path to the texture folders (skyscrapers, commercial, etc.)",
        default=r"C:\Users\sshom\Documents\assets\Tools\tokyo_textures",
        subtype='DIR_PATH'
    )

def clear_scene_properties():
    """Supprime les propriétés de scène"""
    del bpy.types.Scene.tokyo_size
    del bpy.types.Scene.tokyo_density  
    del bpy.types.Scene.tokyo_variety
    del bpy.types.Scene.tokyo_organic
    del bpy.types.Scene.tokyo_use_advanced_textures
    del bpy.types.Scene.tokyo_texture_base_path

def register():
    for cls in classes:
        bpy.utils.register_class(cls)
    init_scene_properties()
    print("🗾 Tokyo City Generator 1.0.8 registered!")

def unregister():
    clear_scene_properties()
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)
    print("🗾 Tokyo City Generator 1.0.8 unregistered!")

if __name__ == "__main__":
    register()
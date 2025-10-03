import bpy
import random
import traceback

# Compteur global pour les bâtiments
building_counter = 0

# Validation des paramètres
def validate_parameters(width, length, max_floors):
    """Valide les paramètres d'entrée pour la génération de ville"""
    errors = []
    
    if width < 1 or width > 50:
        errors.append(f"Largeur invalide: {width}. Doit être entre 1 et 50.")
    
    if length < 1 or length > 50:
        errors.append(f"Longueur invalide: {length}. Doit être entre 1 et 50.")
        
    if max_floors < 1 or max_floors > 100:
        errors.append(f"Nombre d'étages invalide: {max_floors}. Doit être entre 1 et 100.")
    
    # Vérifier si nous avons trop de blocs (limite de performance)
    total_blocks = width * length
    if total_blocks > 100:
        errors.append(f"Trop de blocs: {total_blocks}. Maximum recommandé: 100 (10x10).")
    
    return errors

def check_blender_state():
    """Vérifie que Blender est dans un état approprié pour la génération"""
    try:
        # Vérifier que nous avons accès au contexte
        if not bpy.context:
            return ["Contexte Blender non disponible."]
        
        # Vérifier que nous avons une scène active
        if not bpy.context.scene:
            return ["Aucune scène active dans Blender."]
            
        # Vérifier que nous sommes en mode Object
        if bpy.context.mode != 'OBJECT':
            return ["Blender doit être en mode Object pour la génération."]
            
        return []
    except Exception as e:
        return [f"Erreur lors de la vérification de l'état Blender: {str(e)}"]

# Fonction utilitaire pour convertir en toute sécurité les propriétés Blender en nombres
def safe_float(value, default=0.0):
    """Convertit une valeur en float de façon sécurisée"""
    try:
        # Essayer d'accéder directement comme valeur numérique
        return float(value)
    except (TypeError, ValueError):
        try:
            # Si c'est une PropertyDeferred, essayer d'obtenir sa valeur
            return float(value.real)
        except (AttributeError, TypeError, ValueError):
            try:
                # Comme dernier recours, essayer de le convertir en string puis en float
                return float(str(value))
            except (TypeError, ValueError):
                # En cas d'échec complet, retourner la valeur par défaut
                print(f"Conversion en float échouée, utilisation de la valeur par défaut: {default}")
                return default

def safe_int(value, default=0):
    try:
        # Essayer d'accéder directement comme valeur numérique
        return int(value)
    except (TypeError, ValueError):
        try:
            # Si c'est une PropertyDeferred, essayer d'obtenir sa valeur
            return int(value.real)
        except (AttributeError, TypeError, ValueError):
            try:
                # Comme dernier recours, essayer de le convertir en string puis en int
                return int(str(value))
            except (TypeError, ValueError):
                # En cas d'échec complet, retourner la valeur par défaut
                print(f"Conversion en entier échouée, utilisation de la valeur par défaut: {default}")
                return default

def create_material(name, color):
    """Crée un matériau avec gestion d'erreurs et support des Shader Nodes"""
    try:
        mat = bpy.data.materials.get(name)
        if not mat:
            mat = bpy.data.materials.new(name)
            # Activer les nodes pour Blender moderne
            mat.use_nodes = True
            
            # Obtenir le node Principled BSDF
            if mat.node_tree:
                principled = mat.node_tree.nodes.get("Principled BSDF")
                if principled:
                    # Définir la couleur de base (Base Color)
                    principled.inputs[0].default_value = (*color, 1.0)
                    print(f"Matériau '{name}' créé avec couleur {color}")
                else:
                    print(f"Node Principled BSDF introuvable pour {name}")
            
            # Fallback pour compatibilité
            mat.diffuse_color = (*color, 1.0)
        else:
            print(f"Matériau '{name}' existe déjà, mise à jour de la couleur")
            # Mettre à jour la couleur même si le matériau existe
            if mat.use_nodes and mat.node_tree:
                principled = mat.node_tree.nodes.get("Principled BSDF")
                if principled:
                    principled.inputs[0].default_value = (*color, 1.0)
            mat.diffuse_color = (*color, 1.0)
            
        return mat
    except Exception as e:
        print(f"Erreur lors de la création du matériau '{name}': {str(e)}")
        # Retourner un matériau par défaut ou None
        try:
            # Essayer de créer un matériau de base
            default_mat = bpy.data.materials.new(f"default_{name}")
            default_mat.use_nodes = True
            if default_mat.node_tree:
                principled = default_mat.node_tree.nodes.get("Principled BSDF")
                if principled:
                    principled.inputs[0].default_value = (0.5, 0.5, 0.5, 1.0)
            default_mat.diffuse_color = (0.5, 0.5, 0.5, 1.0)
            return default_mat
        except:
            return None

def create_varied_material(building_index, zone_type='RESIDENTIAL', building_type='rectangular'):
    """Crée un matériau varié selon le type de bâtiment et la zone"""
    import random
    
    # Palettes de couleurs par zone
    color_palettes = {
        'RESIDENTIAL': [
            (0.9, 0.85, 0.8),   # Beige clair
            (0.8, 0.7, 0.6),    # Terre cuite
            (0.7, 0.8, 0.9),    # Bleu pastel
            (0.9, 0.9, 0.8),    # Crème
            (0.8, 0.85, 0.7),   # Vert olive clair
            (0.9, 0.8, 0.7),    # Saumon
            (0.85, 0.8, 0.9),   # Lavande
        ],
        'COMMERCIAL': [
            (0.2, 0.3, 0.8),    # Bleu corporate
            (0.8, 0.8, 0.8),    # Gris métallique
            (0.9, 0.9, 0.9),    # Blanc moderne
            (0.1, 0.1, 0.1),    # Noir élégant
            (0.3, 0.6, 0.8),    # Bleu ciel
            (0.7, 0.2, 0.2),    # Rouge brique
        ],
        'INDUSTRIAL': [
            (0.4, 0.4, 0.4),    # Gris foncé
            (0.6, 0.5, 0.3),    # Brun industriel
            (0.5, 0.6, 0.5),    # Vert militaire
            (0.8, 0.6, 0.2),    # Orange rouille
            (0.3, 0.3, 0.5),    # Bleu navy
        ]
    }
    
    # Variations selon le type de bâtiment
    type_variations = {
        'tower': 0.1,        # Tours plus uniformes
        'residential': 0.3,   # Résidentiel plus varié
        'l_shaped': 0.2,     # Formes complexes modérément variées
        'u_shaped': 0.2,
        't_shaped': 0.2,
    }
    
    # Choisir une couleur de base
    base_colors = color_palettes.get(zone_type, color_palettes['RESIDENTIAL'])
    base_color = random.choice(base_colors)
    
    # Ajouter des variations selon le type
    variation = type_variations.get(building_type, 0.2)
    varied_color = tuple(
        max(0.1, min(0.9, base_color[i] + random.uniform(-variation, variation)))
        for i in range(3)
    )
    
    # Créer un nom unique pour le matériau
    material_name = f"Building_{zone_type}_{building_type}_{building_index}"
    
    return create_material(material_name, varied_color)

def safe_object_creation(creation_func, *args, **kwargs):
    """Wrapper sécurisé pour la création d'objets Blender"""
    try:
        return creation_func(*args, **kwargs)
    except Exception as e:
        print(f"Erreur lors de la création d'objet: {str(e)}")
        print(f"Traceback: {traceback.format_exc()}")
        return None

def safe_mesh_operation(operation_func, obj, *args, **kwargs):
    """Wrapper sécurisé pour les opérations sur les mesh"""
    try:
        if not obj or not obj.data:
            print("Objet ou mesh invalide pour l'opération")
            return False
            
        # S'assurer que l'objet est sélectionné et actif
        bpy.context.view_layer.objects.active = obj
        obj.select_set(True)
        
        return operation_func(*args, **kwargs)
    except Exception as e:
        print(f"Erreur lors de l'opération mesh: {str(e)}")
        return False

def calculate_building_subdivisions(block_width, block_depth, buildings_per_block):
    """Calcule les subdivisions d'un bloc pour placer plusieurs bâtiments"""
    import math
    
    if buildings_per_block <= 1:
        return [(0, 0, block_width, block_depth)]
    
    # Calculer une grille optimale pour le nombre de bâtiments
    if buildings_per_block == 2:
        # 2 bâtiments : côte à côte ou l'un au-dessus de l'autre selon les proportions
        if block_width >= block_depth:
            # Diviser horizontalement
            sub_width = block_width / 2
            return [
                (0, 0, sub_width, block_depth),
                (sub_width, 0, sub_width, block_depth)
            ]
        else:
            # Diviser verticalement
            sub_depth = block_depth / 2
            return [
                (0, 0, block_width, sub_depth),
                (0, sub_depth, block_width, sub_depth)
            ]
    
    elif buildings_per_block == 3:
        # 3 bâtiments : disposition 3x1 ou 1x3
        if block_width >= block_depth:
            sub_width = block_width / 3
            return [
                (0, 0, sub_width, block_depth),
                (sub_width, 0, sub_width, block_depth),
                (sub_width * 2, 0, sub_width, block_depth)
            ]
        else:
            sub_depth = block_depth / 3
            return [
                (0, 0, block_width, sub_depth),
                (0, sub_depth, block_width, sub_depth),
                (0, sub_depth * 2, block_width, sub_depth)
            ]
    
    elif buildings_per_block == 4:
        # 4 bâtiments : grille 2x2
        sub_width = block_width / 2
        sub_depth = block_depth / 2
        return [
            (0, 0, sub_width, sub_depth),
            (sub_width, 0, sub_width, sub_depth),
            (0, sub_depth, sub_width, sub_depth),
            (sub_width, sub_depth, sub_width, sub_depth)
        ]
    
    else:
        # Pour 5-9 bâtiments : grille 3x3 ou 3x2
        if buildings_per_block <= 6:
            # Grille 3x2
            sub_width = block_width / 3
            sub_depth = block_depth / 2
            subdivisions = []
            for i in range(3):
                for j in range(2):
                    if len(subdivisions) < buildings_per_block:
                        subdivisions.append((i * sub_width, j * sub_depth, sub_width, sub_depth))
            return subdivisions
        else:
            # Grille 3x3
            sub_width = block_width / 3
            sub_depth = block_depth / 3
            subdivisions = []
            for i in range(3):
                for j in range(3):
                    if len(subdivisions) < buildings_per_block:
                        subdivisions.append((i * sub_width, j * sub_depth, sub_width, sub_depth))
            return subdivisions

def choose_building_type(variety_level, zone_type, width, depth, height, building_index=0):
    """Choisit intelligemment le type de bâtiment selon la variété demandée - VERSION AMÉLIORÉE"""
    import random
    
    # Types de bâtiments disponibles avec leurs conditions AMÉLIORÉES
    building_types = {
        'rectangular': {'weight': 25, 'min_size': 2.0},  # Réduit pour plus de variété
        'tower': {'weight': 18, 'min_size': 3.0, 'min_height': 10},  # Seuil abaissé
        'stepped': {'weight': 15, 'min_size': 3.5, 'min_height': 8},  # Plus accessible
        'l_shaped': {'weight': 20, 'min_size': 4.0},  # Taille min réduite
        'u_shaped': {'weight': 15, 'min_size': 4.5},  # Plus accessible
        't_shaped': {'weight': 18, 'min_size': 4.0},  # Plus accessible
        'circular': {'weight': 8, 'min_size': 3.5},   # Plus accessible
        'elliptical': {'weight': 6, 'min_size': 3.5}, # Plus accessible
        'complex': {'weight': 4, 'min_size': 5.0, 'min_height': 12},  # Seuil abaissé
        'pyramid': {'weight': 5, 'min_size': 3.5, 'min_height': 8}   # Plus accessible
    }
    
    # Variations par zone pour plus de réalisme
    zone_preferences = {
        'RESIDENTIAL': {
            'rectangular': 1.2, 'l_shaped': 1.5, 't_shaped': 1.3, 'u_shaped': 1.1,
            'tower': 0.7, 'complex': 0.5
        },
        'COMMERCIAL': {
            'tower': 1.8, 'rectangular': 1.1, 'stepped': 1.4, 'complex': 1.3,
            'circular': 1.2, 'l_shaped': 0.8
        },
        'INDUSTRIAL': {
            'rectangular': 1.5, 'l_shaped': 1.3, 'u_shaped': 1.4, 'stepped': 0.9,
            'tower': 0.6, 'circular': 0.7
        }
    }
    
    # Ajuster les poids selon le niveau de variété AVEC PLUS DE DIVERSITÉ
    if variety_level == 'LOW':
        # Variété modérée mais pas monotone
        weights = (['rectangular'] * 35 + ['l_shaped'] * 25 + ['t_shaped'] * 20 + 
                  ['tower'] * 15 + ['stepped'] * 5)
    elif variety_level == 'MEDIUM':
        # Bonne variété équilibrée
        weights = (['rectangular'] * 20 + ['l_shaped'] * 20 + ['t_shaped'] * 18 + 
                  ['u_shaped'] * 15 + ['tower'] * 15 + ['stepped'] * 12)
    elif variety_level == 'HIGH':
        # Maximum de variété
        weights = (['rectangular'] * 15 + ['l_shaped'] * 18 + ['t_shaped'] * 16 + 
                  ['u_shaped'] * 14 + ['tower'] * 12 + ['stepped'] * 10 + 
                  ['circular'] * 8 + ['elliptical'] * 5 + ['complex'] * 2)
    else:  # EXTREME
        # Variété extrême avec formes rares
        weights = (['rectangular'] * 10 + ['l_shaped'] * 15 + ['t_shaped'] * 15 + 
                  ['u_shaped'] * 12 + ['tower'] * 10 + ['stepped'] * 10 + 
                  ['circular'] * 10 + ['elliptical'] * 8 + ['complex'] * 6 + 
                  ['pyramid'] * 4) 
    
    # Appliquer les préférences de zone
    zone_prefs = zone_preferences.get(zone_type, {})
    
    # Choisir un type aléatoire avec pondération
    chosen_type = random.choice(weights)
    
    # Appliquer les préférences de zone pour affiner le choix
    if chosen_type in zone_prefs:
        zone_factor = zone_prefs[chosen_type]
        if random.random() > zone_factor:
            # Rechoisir avec les préférences de zone
            zone_weights = []
            for btype, factor in zone_prefs.items():
                count = int(building_types.get(btype, {}).get('weight', 10) * factor)
                zone_weights.extend([btype] * count)
            if zone_weights:
                chosen_type = random.choice(zone_weights)
    
    # Vérifier si le type choisi est approprié pour les dimensions
    type_info = building_types.get(chosen_type, building_types['rectangular'])
    min_size = type_info.get('min_size', 2.0)
    min_height = type_info.get('min_height', 0)
    
    # Si les dimensions ne conviennent pas, choisir un type plus simple
    if min(width, depth) < min_size or height < min_height:
        if min(width, depth) >= 3.0:
            chosen_type = random.choice(['rectangular', 'tower', 'stepped'])
        else:
            chosen_type = 'rectangular'
    
    # Ajouter de la variabilité avec l'index du bâtiment
    if building_index > 0 and variety_level in ['HIGH', 'EXTREME']:
        variation_types = ['l_shaped', 't_shaped', 'u_shaped', 'stepped']
        if building_index % 3 == 0 and min(width, depth) >= 4.0:
            chosen_type = random.choice(variation_types)
    
    print(f"   🏗️ Type choisi: {chosen_type} (variété: {variety_level}, zone: {zone_type})")
    
    # Retourner le type et ses informations
    type_info = building_types.get(chosen_type, building_types['rectangular'])
    
    return {
        'type': chosen_type,
        'weight': type_info.get('weight', 10),
        'min_size': type_info.get('min_size', 2.0),
        'suitable_for_zone': zone_type in zone_preferences and chosen_type in zone_preferences[zone_type]
    }
            chosen_type = 'rectangular'
    
    # Ajustement selon le type de zone
    if zone_type == 'COMMERCIAL' and chosen_type in ['rectangular', 'stepped']:
        if random.random() < 0.3:  # 30% de chance
            chosen_type = 'tower'
    elif zone_type == 'INDUSTRIAL' and chosen_type in ['tower', 'complex']:
        if random.random() < 0.5:  # 50% de chance
            chosen_type = random.choice(['rectangular', 'l_shaped'])
    
    print(f"   🎯 Type choisi: {chosen_type} (variété: {variety_level}, zone: {zone_type})")
    return chosen_type

def calculate_height_with_variation(base_height, max_floors, height_variation, zone_type, building_type):
    """Calcule la hauteur d'un bâtiment avec variation intelligente"""
    import random
    
    # Facteurs de base selon le type de zone
    zone_factors = {
        'COMMERCIAL': {'min_mult': 0.8, 'max_mult': 1.5, 'bonus': 6},
        'RESIDENTIAL': {'min_mult': 0.6, 'max_mult': 1.2, 'bonus': 3},
        'INDUSTRIAL': {'min_mult': 0.3, 'max_mult': 0.8, 'bonus': 0}
    }
    
    # Facteurs selon le type de bâtiment
    building_factors = {
        'tower': {'min_mult': 1.5, 'max_mult': 2.5},
        'stepped': {'min_mult': 1.2, 'max_mult': 1.8},
        'complex': {'min_mult': 1.3, 'max_mult': 2.0},
        'pyramid': {'min_mult': 1.0, 'max_mult': 1.6}
        # cone supprimé définitivement de la base de code
    }
    
    # Appliquer les facteurs de zone
    zone_info = zone_factors.get(zone_type, zone_factors['RESIDENTIAL'])
    min_height = max(3, int(base_height * zone_info['min_mult']))
    max_height = min(max_floors * 3, int(base_height * zone_info['max_mult']) + zone_info['bonus'])
    
    # Appliquer les facteurs de bâtiment
    if building_type in building_factors:
        building_info = building_factors[building_type]
        min_height = max(min_height, int(base_height * building_info['min_mult']))
        max_height = max(max_height, int(base_height * building_info['max_mult']))
    
    # Appliquer la variation
    if height_variation > 0:
        variation_range = int((max_height - min_height) * height_variation)
        if variation_range > 0:
            height_offset = random.randint(-variation_range//2, variation_range//2)
            final_height = base_height + height_offset
        else:
            final_height = base_height
    else:
        final_height = base_height
    
    # S'assurer que la hauteur reste dans les limites
    final_height = max(min_height, min(max_height, final_height))
    
    print(f"   📏 Hauteur calculée: base={base_height}, final={final_height} (zone={zone_type}, type={building_type})")
    return final_height

def generate_building_with_type(x, y, width, depth, height, mat, zone_type='RESIDENTIAL', district_materials=None, building_type='rectangular'):
    """Génère un bâtiment avec un type spécifique au lieu de AUTO"""
    global building_counter
    building_counter += 1
    
    try:
        # Validation des paramètres
        if width <= 0 or depth <= 0 or height <= 0:
            print(f"❌ ERREUR: Paramètres de bâtiment invalides pour bâtiment {building_counter}: w={width}, d={depth}, h={height}")
            return None
            
        if not mat:
            print(f"❌ ERREUR: Matériau invalide pour le bâtiment {building_counter}")
            return None
        
        print(f"🏗️ DÉBUT génération bâtiment {building_counter} (type: {building_type})")
        print(f"   Paramètres: pos=({x:.1f},{y:.1f}), taille=({width:.1f}x{depth:.1f}x{height:.1f})")
        print(f"   Matériau: {mat.name if mat else 'None'}, Zone: {zone_type}")
        print(f"   🚨 DEBUG: ENTRÉE dans generate_building_with_type - FONCTION APPELÉE")
        
        # Choisir le matériau approprié en fonction du type de zone
        final_mat = mat  # Matériau par défaut
        if district_materials and zone_type in district_materials:
            final_mat = district_materials[zone_type]
            print(f"   Application du matériau de district {zone_type}: {final_mat.name}")
        
        print(f"   Type de bâtiment spécifié: {building_type}")
        print(f"   🚨 DEBUG: Avant appel fonction de génération spécifique")
        
        result = None
        if building_type == 'rectangular':
            print(f"   ➡️ Appel generate_rectangular_building...")
            result = generate_rectangular_building(x, y, width, depth, height, final_mat, building_counter)
            print(f"   🚨 DEBUG: generate_rectangular_building retourné: {result}")
        elif building_type == 'tower':
            print(f"   ➡️ Appel generate_simple_tower_building...")
            result = generate_simple_tower_building(x, y, width, depth, height, final_mat, building_counter)
        elif building_type == 'stepped':
            print(f"   ➡️ Appel generate_simple_stepped_building...")
            result = generate_simple_stepped_building(x, y, width, depth, height, final_mat, building_counter)
        elif building_type == 'l_shaped':
            print(f"   ➡️ Appel generate_l_shaped_building...")
            result = generate_l_shaped_building(x, y, width, depth, height, final_mat, building_counter)
        elif building_type == 'u_shaped':
            print(f"   ➡️ Appel generate_u_shaped_building...")
            result = generate_u_shaped_building(x, y, width, depth, height, final_mat, building_counter)
        elif building_type == 't_shaped':
            print(f"   ➡️ Appel generate_t_shaped_building...")
            result = generate_t_shaped_building(x, y, width, depth, height, final_mat, building_counter)
        elif building_type == 'circular':
            print(f"   ➡️ Appel generate_circular_building...")
            result = generate_circular_building(x, y, width, depth, height, final_mat, building_counter)
        elif building_type == 'elliptical':
            print(f"   ➡️ Appel generate_elliptical_building...")
            result = generate_elliptical_building(x, y, width, depth, height, final_mat, building_counter)
        elif building_type == 'pyramid':
            print(f"   ➡️ Appel generate_pyramid_building...")
            result = generate_pyramid_building(x, y, width, depth, height, final_mat, building_counter)
        elif building_type == 'complex':
            print(f"   ➡️ Appel generate_complex_building...")
            result = generate_complex_building(x, y, width, depth, height, final_mat, building_counter)
        else:
            print(f"   ⚠️ Type de bâtiment non reconnu: {building_type}, utilisation du type rectangulaire")
            result = generate_rectangular_building(x, y, width, depth, height, final_mat, building_counter)
        
        print(f"   🚨 DEBUG: Résultat final de génération: {result}")
        
        if result:
            print(f"✅ Bâtiment {building_counter} créé avec succès: {result.name}")
            return result
        else:
            print(f"❌ ÉCHEC: Bâtiment {building_counter} - Objet None retourné")
            return None
            
    except Exception as e:
        print(f"❌ EXCEPTION lors de génération bâtiment {building_counter}: {str(e)}")
        return None

def generate_building(x, y, width, depth, height, mat, zone_type='RESIDENTIAL', district_materials=None, shape_mode='AUTO', building_variety='MEDIUM'):
    """Génère un bâtiment avec une forme selon le mode choisi et le système de variété intelligent"""
    global building_counter
    building_counter += 1
    
    try:
        # Validation des paramètres
        if width <= 0 or depth <= 0 or height <= 0:
            print(f"❌ ERREUR: Paramètres de bâtiment invalides pour bâtiment {building_counter}: w={width}, d={depth}, h={height}")
            return None
            
        if not mat:
            print(f"❌ ERREUR: Matériau invalide pour le bâtiment {building_counter}")
            return None
        
        print(f"🏗️ DÉBUT génération bâtiment {building_counter}")
        print(f"   Paramètres: pos=({x:.1f},{y:.1f}), taille=({width:.1f}x{depth:.1f}x{height:.1f})")
        print(f"   Matériau: {mat.name if mat else 'None'}, Zone: {zone_type}, Variété: {building_variety}")
        
        # Choisir le matériau approprié en fonction du type de zone
        final_mat = mat  # Matériau par défaut
        if district_materials and zone_type in district_materials:
            final_mat = district_materials[zone_type]
            print(f"   Application du matériau de district {zone_type}: {final_mat.name}")
        
        # Choisir le type de bâtiment selon le mode de forme
        if shape_mode == 'RECT':
            building_type = 'rectangular'
        elif shape_mode == 'L':
            building_type = 'l_shaped'
        elif shape_mode == 'U':
            building_type = 'u_shaped'
        elif shape_mode == 'T':
            building_type = 't_shaped'
        elif shape_mode == 'CIRC':
            building_type = 'circular'
        elif shape_mode == 'ELLIPSE':
            building_type = 'elliptical'
        else:  # shape_mode == 'AUTO' - Utiliser le système de variété intelligent AMÉLIORÉ
            building_info = choose_building_type(building_variety, zone_type, width, depth, height, building_counter)
            building_type = building_info['type'] if isinstance(building_info, dict) else building_info
        
        print(f"   🎨 Type de bâtiment sélectionné: {building_type} (mode: {shape_mode}, variété: {building_variety})")
        
        # Créer un matériau varié pour ce bâtiment spécifique
        varied_material = create_varied_material(building_counter, zone_type, building_type)
        final_mat = varied_material if varied_material else final_mat
        
        print(f"   🎨 Matériau varié créé: {final_mat.name if final_mat else 'Aucun'}")
        
        # Utiliser le système amélioré de génération avec type
        result = generate_building_with_type(x, y, width, depth, height, final_mat, zone_type, district_materials, building_type)
        
        if result:
            print(f"✅ Bâtiment {building_counter} créé avec succès: {result.name}")
            return result
        else:
            print(f"❌ ÉCHEC: Bâtiment {building_counter} - Objet None retourné")
            return None
            
    except Exception as e:
        print(f"Erreur critique lors de la génération du bâtiment {building_counter}: {str(e)}")
        print(f"Traceback: {traceback.format_exc()}")
        return None

def generate_rectangular_building(x, y, width, depth, height, mat, building_num):
    """Génère un bâtiment rectangulaire avec origine au centre bas"""
    try:
        print(f"🏢 DÉBUT generate_rectangular_building #{building_num}")
        print(f"   Paramètres reçus: pos=({x:.1f},{y:.1f}), taille=({width:.1f}x{depth:.1f}x{height:.1f})")
        
        # Validation des paramètres
        if width <= 0 or depth <= 0 or height <= 0:
            print(f"❌ Paramètres invalides pour le bâtiment {building_num}: w={width}, d={depth}, h={height}")
            return None
            
        if not mat:
            print(f"❌ Matériau invalide pour le bâtiment {building_num}")
            return None
        
        print(f"   ➡️ Appel create_cube_with_center_bottom_origin...")
        # Créer le cube avec origine au centre bas - Position Z=0 pour être au niveau du sol
        obj = create_cube_with_center_bottom_origin(width, depth, height, (x, y, 0.0))
        
        if not obj:
            print(f"❌ Échec de création du cube pour le bâtiment {building_num}")
            return None
        
        print(f"   ✅ Cube créé: {obj.name}")
        print(f"   📍 Position: ({obj.location.x:.1f}, {obj.location.y:.1f}, {obj.location.z:.1f})")
        print(f"   📏 Échelle: ({obj.scale.x:.1f}, {obj.scale.y:.1f}, {obj.scale.z:.1f})")
        
        obj.name = f"batiment_rectangular_{building_num}"
        print(f"   🏷️ Nom assigné: {obj.name}")

        # Appliquer le matériau avec validation
        try:
            if mat and obj.data:
                obj.data.materials.append(mat)
                print(f"   🎨 Matériau appliqué: {mat.name}")
            else:
                print(f"   ⚠️ Problème matériau: mat={mat}, obj.data={obj.data}")
        except Exception as e:
            print(f"❌ Erreur lors de l'application du matériau pour le bâtiment {building_num}: {e}")

        # Vérifications finales
        print(f"   🔍 Vérifications finales:")
        print(f"     - Objet visible viewport: {not getattr(obj, 'hide_viewport', True)}")
        print(f"     - Objet visible rendu: {not getattr(obj, 'hide_render', True)}")
        print(f"     - Dans collection: {obj.users_collection}")
        print(f"     - Données mesh valides: {obj.data is not None}")
        
        print(f"✅ generate_rectangular_building #{building_num} TERMINÉ avec succès")
        return obj
        
    except Exception as e:
        print(f"❌ Erreur critique lors de la génération du bâtiment rectangulaire {building_num}: {str(e)}")
        print(f"Traceback: {traceback.format_exc()}")
        return None

def generate_l_shaped_building(x, y, width, depth, height, mat, building_num):
    """Génère un bâtiment en forme de L - seulement orientation verticale (axe Z)"""
    try:
        print(f"🅻 Génération bâtiment L #{building_num} - Orientation verticale uniquement")
        
        # Dimensions des parties - L classique vertical
        main_width = width * 0.7
        main_depth = depth * 0.6
        secondary_width = width * 0.5  
        secondary_depth = depth * 0.4
        secondary_height = height * random.uniform(0.7, 1.0)
        
        parts = []
        
        # Partie principale (verticale du L)
        main_obj = create_cube_with_center_bottom_origin(
            main_width, main_depth, height,
            (x - width*0.15, y - depth*0.2, 0.0)
        )
        if main_obj:
            parts.append(main_obj)
        
        # Partie secondaire (horizontale du L)
        secondary_obj = create_cube_with_center_bottom_origin(
            secondary_width, secondary_depth, secondary_height,
            (x + width*0.25, y + depth*0.3, 0.0)
        )
        if secondary_obj:
            parts.append(secondary_obj)
        
        # Joindre les parties si nous en avons plusieurs
        if len(parts) >= 2:
            bpy.context.view_layer.objects.active = parts[0]
            bpy.ops.object.select_all(action='DESELECT')
            for part in parts:
                part.select_set(True)
            
            try:
                bpy.ops.object.join()
                final_obj = bpy.context.object
                final_obj.name = f"batiment_L_{building_num}_vertical"
                
                # Appliquer le matériau
                if mat and final_obj.data:
                    final_obj.data.materials.append(mat)
                    
                print(f"L-shaped building {final_obj.name} created at: x={x}, y={y}")
                return final_obj
                
            except Exception as e:
                print(f"Erreur jointure L {building_num}: {e}")
                return parts[0]
                
        elif len(parts) == 1:
            obj = parts[0]
            obj.name = f"batiment_L_{building_num}_vertical"
            obj.data.materials.append(mat)
            return obj
        else:
            print(f"Échec création bâtiment L {building_num}")
            return None
        
    except Exception as e:
        print(f"Erreur lors de la création du bâtiment en L {building_num}: {str(e)}")
        return None

def generate_u_shaped_building(x, y, width, depth, height, mat, building_num):
    """Génère un bâtiment en forme de U ou F - seulement orientation verticale (axe Z)"""
    import random
    
    # 40% de chance de créer un F-shaped au lieu d'un U-shaped
    is_f_shaped = random.random() < 0.4
    
    try:
        parts = []
        
        if is_f_shaped:
            print(f"🅵 Génération bâtiment F-shaped #{building_num} - Orientation verticale")
            # F vertical classique : tige verticale + 2 barres horizontales
            
            # Tige principale verticale (gauche)
            main_width = width * 0.3
            main = create_cube_with_center_bottom_origin(
                main_width, depth, height, 
                (x - width*0.35, y, 0.0)
            )
            if main:
                parts.append(main)
            
            # Barre horizontale haute
            top_bar = create_cube_with_center_bottom_origin(
                width * 0.7, depth * 0.2, height * 0.3, 
                (x + width*0.15, y + depth*0.4, height*0.7)
            )
            if top_bar:
                parts.append(top_bar)
            
            # Barre horizontale milieu
            mid_bar = create_cube_with_center_bottom_origin(
                width * 0.5, depth * 0.2, height * 0.25, 
                (x + width*0.05, y + depth*0.4, height*0.375)
            )
            if mid_bar:
                parts.append(mid_bar)
                
        else:
            print(f"� Génération bâtiment U-shaped #{building_num} - Orientation verticale")
            # U vertical classique : 2 tiges + barre de liaison
            
            # Tige gauche
            left_width = width * 0.25
            left_part = create_cube_with_center_bottom_origin(
                left_width, depth * 0.8, height, 
                (x - width*0.375, y, 0.0)
            )
            if left_part:
                parts.append(left_part)
            
            # Tige droite
            right_part = create_cube_with_center_bottom_origin(
                left_width, depth * 0.8, height, 
                (x + width*0.375, y, 0.0)
            )
            if right_part:
                parts.append(right_part)
            
            # Barre de liaison (arrière)
            back_part = create_cube_with_center_bottom_origin(
                width * 0.5, depth * 0.2, height, 
                (x, y + depth*0.4, 0.0)
            )
            if back_part:
                parts.append(back_part)
        
        # Joindre toutes les parties
        if len(parts) > 1:
            bpy.context.view_layer.objects.active = parts[0]
            for part in parts:
                part.select_set(True)
            try:
                bpy.ops.object.join()
                obj = bpy.context.active_object
                obj.name = f"batiment_u_shaped_{building_num}_vertical"
                
                # Appliquer le matériau
                obj.data.materials.append(mat)
                return obj
            except Exception as e:
                print(f"Erreur jointure U/F {building_num}: {e}")
                return parts[0]
        elif len(parts) == 1:
            obj = parts[0]
            obj.name = f"batiment_u_shaped_{building_num}_vertical"
            obj.data.materials.append(mat)
            return obj
        else:
            print(f"Échec création bâtiment U/F {building_num}")
            return None
            
    except Exception as e:
        print(f"Erreur création bâtiment U/F {building_num}: {str(e)}")
        return None

def generate_tower_building(x, y, width, depth, height, mat):
    """Génère un bâtiment tour avec plusieurs niveaux"""
    # Base large
    base_height = height * 0.3
    
    # Créer la base
    bpy.ops.mesh.primitive_cube_add(size=1, location=(0, 0, 0))
    base_obj = bpy.context.object
    base_obj.scale = (width/2, depth/2, base_height/2)
    bpy.context.view_layer.objects.active = base_obj
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    
    # Ajuster la position Z des sommets
    mesh = base_obj.data
    z_min = min(v.co.z for v in mesh.vertices)
    for v in mesh.vertices:
        v.co.z -= z_min
    
    base_obj.location = (x, y, 0.0)  # Au niveau du sol
    
    # Tour principale (plus étroite)
    tower_width = width * 0.7
    tower_depth = depth * 0.7
    tower_height = height * 0.7
    
    bpy.ops.mesh.primitive_cube_add(size=1, location=(0, 0, 0))
    tower_obj = bpy.context.object
    tower_obj.scale = (tower_width/2, tower_depth/2, tower_height/2)
    bpy.context.view_layer.objects.active = tower_obj
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    
    # Ajuster la position Z des sommets
    mesh = tower_obj.data
    z_min = min(v.co.z for v in mesh.vertices)
    for v in mesh.vertices:
        v.co.z -= z_min
    
    tower_obj.location = (x, y, base_height + 0.0)  # Position ajustée
    
    # Joindre les parties
    bpy.context.view_layer.objects.active = base_obj
    base_obj.select_set(True)
    tower_obj.select_set(True)
    bpy.ops.object.join()
    
    # Appliquer le matériau
    base_obj.data.materials.append(mat)

def generate_simple_tower_building(x, y, width, depth, height, mat, building_num):
    """Génère un bâtiment tour simple avec variation de hauteur et gestion d'erreurs"""
    try:
        # Validation des paramètres
        if width <= 0 or depth <= 0 or height <= 0:
            print(f"Paramètres tour invalides: w={width}, d={depth}, h={height}")
            return None
            
        if not mat:
            print(f"Matériau invalide pour la tour {building_num}")
            return None
        
        # Variation simple : juste changer les proportions
        tower_width = width * random.uniform(0.7, 1.0)
        tower_depth = depth * random.uniform(0.7, 1.0)
        
        # Créer le cube à l'origine
        result = safe_object_creation(bpy.ops.mesh.primitive_cube_add, size=1, location=(0, 0, 0))
        if not bpy.context.object:
            print(f"Échec de création du cube pour la tour {building_num}")
            return None
            
        obj = bpy.context.object
        obj.name = f"batiment_tower_{building_num}"

        # Appliquer l'échelle
        obj.scale.x = tower_width/2
        obj.scale.y = tower_depth/2
        obj.scale.z = height/2

        # Appliquer l'échelle avec gestion d'erreurs
        if not safe_mesh_operation(bpy.ops.object.transform_apply, obj, location=False, rotation=False, scale=True):
            print(f"Échec de l'application de l'échelle pour la tour {building_num}")
            return None

        # Ajuster la position Z des sommets avec validation
        mesh = obj.data
        if not mesh or not mesh.vertices:
            print(f"Mesh invalide pour la tour {building_num}")
            return None
            
        try:
            z_min = min(v.co.z for v in mesh.vertices)
            for v in mesh.vertices:
                v.co.z -= z_min
        except Exception as e:
            print(f"Erreur lors de l'ajustement des sommets pour la tour {building_num}: {e}")

        # Positionner l'objet
        obj.location.x = x
        obj.location.y = y
        obj.location.z = 0.0  # Au niveau du sol

        # Appliquer le matériau
        try:
            obj.data.materials.append(mat)
        except Exception as e:
            print(f"Erreur lors de l'application du matériau pour la tour {building_num}: {e}")
        
        return obj
        
    except Exception as e:
        print(f"Erreur critique lors de la génération de la tour {building_num}: {str(e)}")
        return None

def generate_simple_stepped_building(x, y, width, depth, height, mat, building_num):
    """Génère un bâtiment avec une variation simple de forme et gestion d'erreurs"""
    try:
        # Validation des paramètres
        if width <= 0 or depth <= 0 or height <= 0:
            print(f"Paramètres bâtiment étagé invalides: w={width}, d={depth}, h={height}")
            return None
            
        if not mat:
            print(f"Matériau invalide pour le bâtiment étagé {building_num}")
            return None
        
        # Variation simple : base plus large, sommet plus étroit
        base_scale = random.uniform(0.9, 1.0)
        base_width = width * base_scale
        base_depth = depth * base_scale
        
        # Créer le cube à l'origine
        result = safe_object_creation(bpy.ops.mesh.primitive_cube_add, size=1, location=(0, 0, 0))
        if not bpy.context.object:
            print(f"Échec de création du cube pour le bâtiment étagé {building_num}")
            return None
            
        obj = bpy.context.object
        obj.name = f"batiment_stepped_{building_num}"

        # Appliquer l'échelle
        obj.scale.x = base_width/2
        obj.scale.y = base_depth/2
        obj.scale.z = height/2

        # Appliquer l'échelle avec gestion d'erreurs
        if not safe_mesh_operation(bpy.ops.object.transform_apply, obj, location=False, rotation=False, scale=True):
            print(f"Échec de l'application de l'échelle pour le bâtiment étagé {building_num}")
            return None

        # Ajuster la position Z des sommets avec validation
        mesh = obj.data
        if not mesh or not mesh.vertices:
            print(f"Mesh invalide pour le bâtiment étagé {building_num}")
            return None
            
        try:
            z_min = min(v.co.z for v in mesh.vertices)
            for v in mesh.vertices:
                v.co.z -= z_min
        except Exception as e:
            print(f"Erreur lors de l'ajustement des sommets pour le bâtiment étagé {building_num}: {e}")

        # Positionner l'objet
        obj.location.x = x
        obj.location.y = y
        obj.location.z = 0.0  # Au niveau du sol

        # Appliquer le matériau
        try:
            obj.data.materials.append(mat)
        except Exception as e:
            print(f"Erreur lors de l'application du matériau pour le bâtiment étagé {building_num}: {e}")
        
        return obj
        
    except Exception as e:
        print(f"Erreur critique lors de la génération du bâtiment étagé {building_num}: {str(e)}")
        return None

def generate_circular_building(x, y, width, depth, height, mat, building_num):
    """Génère un bâtiment circulaire"""
    try:
        print(f"🔵 Génération bâtiment circulaire #{building_num}")
        
        # Utiliser le diamètre moyen pour le rayon
        radius = min(width, depth) / 2
        
        # Créer le cylindre avec origine au bottom-center
        result = safe_object_creation(bpy.ops.mesh.primitive_cylinder_add, 
                                    radius=radius, depth=height, location=(x, y, 0))
        if not bpy.context.object:
            print(f"Échec création cylindre pour bâtiment circulaire {building_num}")
            return None
            
        obj = bpy.context.object
        obj.name = f"batiment_circular_{building_num}"
        obj.location.z = height/2  # Placer le centre du cylindre à mi-hauteur (bottom à z=0)
        
        # Appliquer le matériau
        try:
            obj.data.materials.append(mat)
        except Exception as e:
            print(f"Erreur matériau bâtiment circulaire {building_num}: {e}")
        
        return obj
        
    except Exception as e:
        print(f"Erreur bâtiment circulaire {building_num}: {str(e)}")
        return None

def generate_elliptical_building(x, y, width, depth, height, mat, building_num):
    """Génère un bâtiment elliptique (cylindre écrasé)"""
    try:
        print(f"🥚 Génération bâtiment elliptique #{building_num}")
        
        # Créer un cylindre avec origine au bottom-center
        result = safe_object_creation(bpy.ops.mesh.primitive_cylinder_add, 
                                    radius=1, depth=height, location=(x, y, 0))
        if not bpy.context.object:
            print(f"Échec création cylindre pour bâtiment elliptique {building_num}")
            return None
            
        obj = bpy.context.object
        obj.name = f"batiment_elliptical_{building_num}"
        
        # Écraser pour faire une ellipse et positionner correctement
        obj.scale.x = width / 2
        obj.scale.y = depth / 2
        obj.location.z = height/2  # Placer le centre à mi-hauteur (bottom à z=0)
        
        # Appliquer le matériau
        try:
            obj.data.materials.append(mat)
        except Exception as e:
            print(f"Erreur matériau bâtiment elliptique {building_num}: {e}")
        
        return obj
        
    except Exception as e:
        print(f"Erreur bâtiment elliptique {building_num}: {str(e)}")
        return None

def generate_pyramid_building(x, y, width, depth, height, mat, building_num):
    """Génère un bâtiment en forme de pyramide"""
    try:
        print(f"🔺 Génération bâtiment pyramide #{building_num}")
        
        # Créer un cône avec origine au bottom-center
        result = safe_object_creation(bpy.ops.mesh.primitive_cone_add, 
                                    radius1=max(width, depth)/2, radius2=0, 
                                    depth=height, location=(x, y, 0))
        if not bpy.context.object:
            print(f"Échec création cône pour bâtiment pyramide {building_num}")
            return None
            
        obj = bpy.context.object
        obj.name = f"batiment_pyramid_{building_num}"
        obj.location.z = height/2  # Placer le centre à mi-hauteur (bottom à z=0)
        
        # Appliquer le matériau
        try:
            obj.data.materials.append(mat)
        except Exception as e:
            print(f"Erreur matériau bâtiment pyramide {building_num}: {e}")
        
        return obj
        
    except Exception as e:
        print(f"Erreur bâtiment pyramide {building_num}: {str(e)}")
        return None

def generate_t_shaped_building(x, y, width, depth, height, mat, building_num):
    """Génère un bâtiment en forme de T - seulement orientation verticale (axe Z)"""
    import random
    
    try:
        print(f"🅃 Génération bâtiment T #{building_num} - Orientation verticale uniquement")
        
        parts = []
        
        # T classique vertical : barre horizontale en haut, tige verticale en bas
        # Barre horizontale (partie supérieure du T)
        horizontal_width = width
        horizontal_depth = depth * 0.3
        horizontal = create_cube_with_center_bottom_origin(
            horizontal_width, horizontal_depth, height * 0.4, 
            (x, y + depth * 0.35, height * 0.6)  # Placée en haut
        )
        
        # Tige verticale (partie inférieure du T)
        vertical_width = width * 0.3
        vertical_depth = depth * 0.7
        vertical = create_cube_with_center_bottom_origin(
            vertical_width, vertical_depth, height, 
            (x, y - depth * 0.15, 0.0)  # Base au sol
        )
        
        # Collecter les parties créées
        if horizontal:
            parts.append(horizontal)
        if vertical:
            parts.append(vertical)
        
        # Joindre les parties si nous en avons plusieurs
        if len(parts) >= 2:
            bpy.context.view_layer.objects.active = parts[0]
            for part in parts:
                part.select_set(True)
            
            try:
                bpy.ops.object.join()
                obj = bpy.context.active_object
                obj.name = f"batiment_t_shaped_{building_num}_vertical"
                
                # Appliquer le matériau
                obj.data.materials.append(mat)
                return obj
                
            except Exception as e:
                print(f"Erreur jointure T {building_num}: {e}")
                return parts[0]  # Retourner au moins une partie
        elif len(parts) == 1:
            obj = parts[0]
            obj.name = f"batiment_t_shaped_{building_num}_vertical"
            obj.data.materials.append(mat)
            return obj
        else:
            print(f"Échec création bâtiment T {building_num}")
            return None
        
    except Exception as e:
        print(f"Erreur bâtiment T {building_num}: {str(e)}")
        return None

def generate_complex_building(x, y, width, depth, height, mat, building_num):
    """Génère un bâtiment complexe avec plusieurs éléments"""
    try:
        print(f"🏗️ Génération bâtiment complexe #{building_num}")
        
        # Base principale
        base_height = height * 0.6
        base = create_cube_with_center_bottom_origin(
            width, depth, base_height, (x, y, 0.0)
        )
        
        if not base:
            print(f"Échec création base complexe {building_num}")
            return None
        
        # Tour centrale plus haute
        tower_width = width * 0.4
        tower_depth = depth * 0.4
        tower_height = height * 0.8
        tower = create_cube_with_center_bottom_origin(
            tower_width, tower_depth, tower_height, 
            (x, y, base_height + 0.01)
        )
        
        if tower:
            # Joindre base et tour
            bpy.context.view_layer.objects.active = base
            base.select_set(True)
            tower.select_set(True)
            
            try:
                bpy.ops.object.join()
                obj = bpy.context.active_object
                obj.name = f"batiment_complex_{building_num}"
                
                # Appliquer le matériau
                obj.data.materials.append(mat)
                return obj
                
            except Exception as e:
                print(f"Erreur jointure complexe {building_num}: {e}")
                return base
        
        return base
        
    except Exception as e:
        print(f"Erreur bâtiment complexe {building_num}: {str(e)}")
        return None

def generate_sidewalk(x, y, width, depth, mat, sidewalk_width=1.0):
    """Génère un trottoir avec origine au centre bas"""
    try:
        if width <= 0 or depth <= 0:
            print(f"Paramètres trottoir invalides: w={width}, d={depth}")
            return False
            
        if not mat:
            print("Matériau trottoir invalide")
            return False
        
        # Créer un cube pour le trottoir avec origine centre bas
        obj = create_cube_with_center_bottom_origin(
            width, depth, 0.02,  # Hauteur de 2cm pour le trottoir
            (x, y, 0.01)  # Position avec élévation de 1cm
        )
        
        if not obj:
            print("Échec de création du cube trottoir")
            return False
            
        obj.name = f"sidewalk_{x:.1f}_{y:.1f}"
        
        # Appliquer le matériau
        try:
            obj.data.materials.append(mat)
            print(f"Sidewalk created at: x={x}, y={y} (origin: center bottom)")
            return True
        except Exception as e:
            print(f"Erreur application matériau trottoir: {e}")
            return False
            
    except Exception as e:
        print(f"Erreur création trottoir: {str(e)}")
        return False

def generate_road(x, y, width, length, mat, is_horizontal=True, rotation=0.0):
    """Génère une route avec origine au centre bas et rotation possible"""
    try:
        if width <= 0 or length <= 0:
            print(f"Paramètres route invalides: w={width}, l={length}")
            return False
            
        if not mat:
            print("Matériau route invalide")
            return False
        
        # Créer un cube pour la route avec origine centre bas
        if abs(rotation) < 0.01:  # Route standard (horizontale/verticale)
            if is_horizontal:
                # Route horizontale : largeur = length, profondeur = width
                obj = create_cube_with_center_bottom_origin(
                    length, width, 0.005,  # Hauteur de 5mm pour la route
                    (x, y, 0.001)  # Position au niveau du sol avec légère élévation
                )
            else:
                # Route verticale : largeur = width, profondeur = length  
                obj = create_cube_with_center_bottom_origin(
                    width, length, 0.005,  # Hauteur de 5mm pour la route
                    (x, y, 0.001)  # Position au niveau du sol avec légère élévation
                )
        else:
            # Route diagonale - utiliser toujours length comme longueur principale
            obj = create_cube_with_center_bottom_origin(
                length, width, 0.005,  # Hauteur de 5mm pour la route
                (x, y, 0.001)  # Position au niveau du sol avec légère élévation
            )
            # Appliquer la rotation autour de l'axe Z
            if obj:
                obj.rotation_euler[2] = rotation
        
        if not obj:
            print("Échec de création du cube route")
            return False
            
        # Nom selon le type de route
        if abs(rotation) > 0.01:
            obj.name = f"road_diag_{x:.1f}_{y:.1f}_{rotation:.2f}"
        else:
            obj.name = f"road_{'h' if is_horizontal else 'v'}_{x:.1f}_{y:.1f}"
        
        # Appliquer le matériau
        try:
            obj.data.materials.append(mat)
            road_type = "diagonale" if abs(rotation) > 0.01 else ("horizontale" if is_horizontal else "verticale")
            print(f"Road created at: x={x}, y={y}, {road_type} (rotation: {rotation:.2f})")
            return True
        except Exception as e:
            print(f"Erreur application matériau route: {e}")
            return False
            
    except Exception as e:
        print(f"Erreur création route: {str(e)}")
        return False

def generate_intersection(x, y, size, mat):
    """Génère un carrefour (intersection) à la position donnée"""
    try:
        if size <= 0:
            print(f"Taille carrefour invalide: {size}")
            return False
            
        if not mat:
            print("Matériau carrefour invalide")
            return False
        
        # Créer un cube carré pour le carrefour
        obj = create_cube_with_center_bottom_origin(
            size, size, 0.006,  # Légèrement plus épais que les routes (6mm)
            (x, y, 0.001)  # Position au niveau du sol
        )
        
        if not obj:
            print("Échec de création du cube carrefour")
            return False
            
        obj.name = f"intersection_{x:.1f}_{y:.1f}"
        
        # Appliquer le matériau
        try:
            obj.data.materials.append(mat)
            print(f"Intersection created at: x={x}, y={y}, size={size}")
            return True
        except Exception as e:
            print(f"Erreur application matériau carrefour: {e}")
            return False
            
    except Exception as e:
        print(f"Erreur création carrefour: {str(e)}")
        return False

def generate_diagonal_road(start_x, start_y, end_x, end_y, width, mat):
    """Génère une route diagonale entre deux points"""
    try:
        import math
        
        # Calculer la longueur et l'angle de la route diagonale
        dx = end_x - start_x
        dy = end_y - start_y
        length = math.sqrt(dx * dx + dy * dy)
        
        if length <= 0:
            print("Longueur route diagonale invalide")
            return False
        
        # Calculer l'angle de rotation
        angle = math.atan2(dy, dx)
        
        # Position du centre de la route
        center_x = (start_x + end_x) / 2
        center_y = (start_y + end_y) / 2
        
        # Générer la route avec rotation
        return generate_road(center_x, center_y, width, length, mat, is_horizontal=True, rotation=angle)
        
    except Exception as e:
        print(f"Erreur création route diagonale: {str(e)}")
        return False

def generate_unified_city_grid(block_sizes, road_width, road_mat, side_mat, build_mat, max_floors, regen_only, district_materials=None, sidewalk_width=1.0, shape_mode='AUTO', enable_diagonal_roads=False, diagonal_road_frequency=30.0, enable_intersections=True, intersection_size_factor=1.2, buildings_per_block=1, seamless_roads=True, building_variety='MEDIUM', height_variation=0.5):
    """Génère une grille unifiée de ville avec blocs et routes parfaitement alignés et gestion d'erreurs"""
    
    try:
        if not block_sizes or not isinstance(block_sizes, list):
            print("❌ ERREUR: block_sizes invalide")
            return False
            
        grid_width = len(block_sizes)
        grid_length = len(block_sizes[0]) if block_sizes else 0
        
        if grid_width == 0 or grid_length == 0:
            print("❌ ERREUR: Dimensions de grille invalides")
            return False
        
        # ⚠️ LIMITES DE PERFORMANCE pour éviter crashes
        total_blocks = grid_width * grid_length
        max_buildings = total_blocks * buildings_per_block
        
        if total_blocks > 25:  # Limite sécurisée
            print(f"⚠️ PERFORMANCE: {total_blocks} blocs demandés, limitation automatique")
            return False
            
        if max_buildings > 50:  # Limite de bâtiments
            print(f"⚠️ PERFORMANCE: {max_buildings} bâtiments demandés, trop pour la performance")
            return False
            
        print(f"✅ Génération grille {grid_width}x{grid_length} ({total_blocks} blocs, {max_buildings} bâtiments max)")
        
        # Calculer les positions absolues de début de chaque élément
        x_starts = []  # Position de début X pour chaque colonne
        y_starts = []  # Position de début Y pour chaque rangée
        
        # Calculer les positions X avec validation
        current_x = 0
        for i in range(grid_width):
            x_starts.append(current_x)
            try:
                # Prendre la largeur maximale de cette colonne
                # Adaptation pour la nouvelle structure de données
                max_width = max(
                    block_sizes[i][j]['size'][0] if isinstance(block_sizes[i][j], dict) else block_sizes[i][j][0] 
                    for j in range(grid_length)
                )
                if max_width <= 0:
                    print(f"AVERTISSEMENT: Largeur invalide à la position [{i}], utilisation valeur par défaut")
                    max_width = 10
                current_x += max_width
                if i < grid_width - 1:  # Ajouter une route sauf après la dernière colonne
                    current_x += road_width
            except (IndexError, TypeError, ValueError) as e:
                print(f"ERREUR lors du calcul position X pour colonne {i}: {e}")
                return False
        
        # Calculer les positions Y avec validation
        current_y = 0
        for j in range(grid_length):
            y_starts.append(current_y)
            try:
                # Prendre la profondeur maximale de cette rangée
                # Adaptation pour la nouvelle structure de données
                max_depth = max(
                    block_sizes[i][j]['size'][1] if isinstance(block_sizes[i][j], dict) else block_sizes[i][j][1] 
                    for i in range(grid_width)
                )
                if max_depth <= 0:
                    print(f"AVERTISSEMENT: Profondeur invalide à la position [{j}], utilisation valeur par défaut")
                    max_depth = 10
                current_y += max_depth
                if j < grid_length - 1:  # Ajouter une route sauf après la dernière rangée
                    current_y += road_width
            except (IndexError, TypeError, ValueError) as e:
                print(f"ERREUR lors du calcul position Y pour rangée {j}: {e}")
                return False
        
        # Générer les routes horizontales (entre les rangées)
        roads_created = 0
        print(f"Génération de {grid_length - 1} routes horizontales...")
        for j in range(grid_length - 1):
            try:
                # Position Y de la route entre les rangées j et j+1
                # Adaptation pour la nouvelle structure de données
                max_depth_j = max(
                    block_sizes[i][j]['size'][1] if isinstance(block_sizes[i][j], dict) else block_sizes[i][j][1] 
                    for i in range(grid_width)
                )
                y_road_start = y_starts[j] + max_depth_j  # Route commence directement après le bloc
                
                # Position du centre de la route (origine centre bas)
                y_road_center = y_road_start + road_width/2
                
                # La route s'étend sur TOUTE la largeur, incluant les intersections
                x_road_start = 0
                # Calculer la largeur totale incluant blocs ET routes verticales
                total_width = 0
                for i in range(grid_width):
                    max_width = max(
                        block_sizes[i][k]['size'][0] if isinstance(block_sizes[i][k], dict) else block_sizes[i][k][0] 
                        for k in range(grid_length)
                    )
                    total_width += max_width
                    if i < grid_width - 1:  # Ajouter largeur route verticale sauf après dernière colonne
                        total_width += road_width
                
                road_length = total_width
                x_road_center = x_road_start + road_length/2
                
                print(f"Route horizontale {j}: centre=({x_road_center}, {y_road_center}), largeur={road_width}, longueur={road_length}")
                
                if generate_road(x_road_center, y_road_center, road_width, road_length, road_mat, is_horizontal=True):
                    roads_created += 1
                    print(f"  ✓ Route horizontale {j} créée avec succès")
                else:
                    print(f"  ✗ AVERTISSEMENT: Échec création route horizontale {j}")
                    
            except Exception as e:
                print(f"ERREUR lors de la création route horizontale {j}: {e}")
        
        # Générer les routes verticales (entre les colonnes)
        print(f"Génération de {grid_width - 1} routes verticales...")
        for i in range(grid_width - 1):
            try:
                # Position X de la route entre les colonnes i et i+1
                # Adaptation pour la nouvelle structure de données
                max_width_i = max(
                    block_sizes[i][j]['size'][0] if isinstance(block_sizes[i][j], dict) else block_sizes[i][j][0] 
                    for j in range(grid_length)
                )
                x_road_start = x_starts[i] + max_width_i  # Route commence directement après le bloc
                
                # Position du centre de la route (origine centre bas)
                x_road_center = x_road_start + road_width/2
                
                # La route s'étend sur TOUTE la hauteur, incluant les intersections
                y_road_start = 0
                # Calculer la hauteur totale incluant blocs ET routes horizontales
                total_height = 0
                for j in range(grid_length):
                    max_depth = max(
                        block_sizes[k][j]['size'][1] if isinstance(block_sizes[k][j], dict) else block_sizes[k][j][1] 
                        for k in range(grid_width)
                    )
                    total_height += max_depth
                    if j < grid_length - 1:  # Ajouter largeur route horizontale sauf après dernière rangée
                        total_height += road_width
                
                road_length = total_height
                y_road_center = y_road_start + road_length/2
                
                print(f"Route verticale {i}: centre=({x_road_center}, {y_road_center}), largeur={road_width}, longueur={road_length}")
                
                if generate_road(x_road_center, y_road_center, road_width, road_length, road_mat, is_horizontal=False):
                    roads_created += 1
                    print(f"  ✓ Route verticale {i} créée avec succès")
                else:
                    print(f"  ✗ AVERTISSEMENT: Échec création route verticale {i}")
                    
            except Exception as e:
                print(f"ERREUR lors de la création route verticale {i}: {e}")
        
        print(f"Routes créées: {roads_created}")
        
        # Générer les blocs et trottoirs
        print(f"🏗️ DÉBUT GÉNÉRATION DES BLOCS ET BÂTIMENTS")
        print(f"📐 Grille: {grid_width}x{grid_length} = {grid_width * grid_length} blocs à traiter")
        print(f"🔧 Paramètres: regen_only={regen_only}, max_floors={max_floors}")
        print(f"🎨 Matériaux: road={road_mat.name if road_mat else None}, side={side_mat.name if side_mat else None}, build={build_mat.name if build_mat else None}")
        
        blocks_created = 0
        buildings_created = 0
        
        for i in range(grid_width):
            for j in range(grid_length):
                print(f"\n🔄 TRAITEMENT BLOC [{i}][{j}]:")
                try:
                    # Extraire les informations du bloc (nouvelle structure)
                    if isinstance(block_sizes[i][j], dict):
                        block_info = block_sizes[i][j]
                        block_width, block_depth = block_info['size']
                        zone_type = block_info.get('zone_type', 'RESIDENTIAL')
                        zone_info = block_info.get('zone_info', {})
                    else:
                        # Support de l'ancienne structure pour compatibilité
                        block_width, block_depth = block_sizes[i][j]
                        zone_type = 'RESIDENTIAL'
                        zone_info = {
                            'size_multiplier': 1.0,
                            'min_floors': 1,
                            'max_floors_multiplier': 1.0,
                            'shape_preference': ['RECT']
                        }
                        zone_info = {}
                    
                    if block_width <= 0 or block_depth <= 0:
                        print(f"AVERTISSEMENT: Taille de bloc invalide à [{i}][{j}]: {block_width}x{block_depth}")
                        continue
                    
                    # Position du bloc (coordonnées du coin)
                    x_block = x_starts[i]
                    y_block = y_starts[j]
                    
                    # Position du centre du bloc pour le trottoir (origine centre bas)
                    x_center_sidewalk = x_block + block_width/2
                    y_center_sidewalk = y_block + block_depth/2
                    
                    # Générer le trottoir aux coordonnées du centre
                    if generate_sidewalk(x_center_sidewalk, y_center_sidewalk, block_width, block_depth, side_mat, sidewalk_width):
                        blocks_created += 1
                    else:
                        print(f"AVERTISSEMENT: Échec création trottoir à [{i}][{j}]")
                    
                    # Position du centre du bloc pour le bâtiment (identique au trottoir)
                    x_center = x_center_sidewalk
                    y_center = y_center_sidewalk
                    
                    # Générer le bâtiment si ce n'est pas une régénération
                    print(f"   🏠 SECTION BÂTIMENT pour bloc [{i}][{j}]:")
                    print(f"      regen_only = {regen_only}")
                    print(f"      zone_type = {zone_type}")
                    print(f"      zone_info = {zone_info}")
                    print(f"      🔍 DÉBOGAGE: Condition 'not regen_only' = {not regen_only}")
                    print(f"      🔍 DÉBOGAGE: Type regen_only = {type(regen_only)}")
                    print(f"      🔍 DÉBOGAGE: Valeur regen_only = '{regen_only}'")
                    
                    if not regen_only:
                        print(f"      ✅ ENTRÉE dans génération bâtiment (pas de régénération)")
                        try:
                            # Calculer la hauteur avec le nouveau système de variation
                            print(f"         📏 Calcul hauteur avec variété: max_floors={max_floors}, variation={height_variation}")
                            
                            # Hauteur de base selon la zone
                            if zone_info and len(zone_info) > 0:
                                print(f"         ➡️ Utilisation zone_info pour hauteur de base")
                                min_floors = zone_info.get('min_floors', 1)
                                max_floors_multiplier = zone_info.get('max_floors_multiplier', 1.0)
                                zone_max_floors = max(min_floors, int(max_floors * max_floors_multiplier))
                                base_height = random.randint(min_floors, zone_max_floors) * 3
                            else:
                                print(f"         ➡️ Utilisation logique par défaut pour hauteur de base")
                                min_height = max(1, max_floors // 4)
                                base_height = random.randint(min_height, max_floors) * 3
                                if base_height < 3:
                                    base_height = 3
                            
                            print(f"         📐 Hauteur de base calculée: {base_height}m pour bloc [{i}][{j}]")
                            
                            # Appliquer la variation de hauteur
                            height = calculate_height_with_variation(base_height, max_floors, height_variation, zone_type, building_variety)
                            print(f"         🎯 Hauteur finale avec variation: {height}m")
                            
                            # Bâtiment légèrement plus petit que le bloc, en tenant compte de la largeur du trottoir
                            total_building_width = block_width - (2 * sidewalk_width)
                            total_building_depth = block_depth - (2 * sidewalk_width)
                            
                            # S'assurer que les dimensions du bâtiment sont positives
                            if total_building_width <= 0 or total_building_depth <= 0:
                                print(f"  AVERTISSEMENT: Dimensions bloc invalides [{i}][{j}]: {total_building_width}x{total_building_depth}")
                                total_building_width = max(1, total_building_width)
                                total_building_depth = max(1, total_building_depth)
                            
                            # Calculer les subdivisions pour placer plusieurs bâtiments
                            subdivisions = calculate_building_subdivisions(total_building_width, total_building_depth, buildings_per_block)
                            
                            print(f"  📐 GÉNÉRATION {len(subdivisions)} BÂTIMENT(S) dans le bloc [{i}][{j}]:")
                            print(f"    Zone: {zone_type}, Matériau: {build_mat.name if build_mat else 'None'}")
                            
                            # Générer chaque bâtiment dans ses subdivisions
                            buildings_created_in_block = 0
                            for sub_idx, (sub_x, sub_y, sub_width, sub_depth) in enumerate(subdivisions):
                                # Position absolue de ce sous-bâtiment
                                sub_x_center = x_center - total_building_width/2 + sub_x + sub_width/2
                                sub_y_center = y_center - total_building_depth/2 + sub_y + sub_depth/2
                                
                                # Calculer une hauteur spécifique pour ce sous-bâtiment (avec variation)
                                sub_height = calculate_height_with_variation(base_height, max_floors, height_variation, zone_type, building_variety)
                                
                                # Ajouter un petit espace entre les bâtiments s'il y en a plusieurs
                                margin = 0.5 if buildings_per_block > 1 else 0.0
                                final_width = max(0.5, sub_width - margin)
                                final_depth = max(0.5, sub_depth - margin)
                                
                                print(f"    Sous-bâtiment {sub_idx + 1}: ({sub_x_center:.1f}, {sub_y_center:.1f}) - {final_width:.1f}x{final_depth:.1f}x{sub_height:.1f}")
                                
                                # DÉBOGAGE: Vérifier les paramètres avant génération
                                if final_width <= 0 or final_depth <= 0 or sub_height <= 0:
                                    print(f"    ❌ ERREUR: Paramètres invalides - sous-bâtiment {sub_idx + 1} non créé")
                                    continue
                                
                                try:
                                    building_obj = generate_building(sub_x_center, sub_y_center, final_width, final_depth, sub_height, build_mat, zone_type, district_materials, shape_mode, building_variety)
                                    
                                    if building_obj:
                                        buildings_created += 1
                                        buildings_created_in_block += 1
                                        print(f"    ✅ Sous-bâtiment {sub_idx + 1} créé: {building_obj.name}")
                                        print(f"    � Position finale: ({building_obj.location.x:.1f}, {building_obj.location.y:.1f}, {building_obj.location.z:.1f})")
                                        
                                        # Vérifier que l'objet est visible
                                        if hasattr(building_obj, 'hide_viewport'):
                                            if building_obj.hide_viewport:
                                                print(f"    ⚠️ AVERTISSEMENT: Bâtiment masqué dans viewport")
                                                building_obj.hide_viewport = False
                                        if hasattr(building_obj, 'hide_render'):
                                            if building_obj.hide_render:
                                                print(f"    ⚠️ AVERTISSEMENT: Bâtiment masqué au rendu")
                                                building_obj.hide_render = False
                                    else:
                                        print(f"    ❌ ÉCHEC génération sous-bâtiment {sub_idx + 1} - Objet None retourné")
                                        
                                except Exception as e:
                                    print(f"❌ ERREUR lors de la création du sous-bâtiment {sub_idx + 1}: {e}")
                            
                            print(f"  📊 Bloc [{i}][{j}] terminé: {buildings_created_in_block}/{len(subdivisions)} bâtiments créés")
                            
                        except Exception as e:
                            print(f"❌ ERREUR lors de la création des bâtiments du bloc [{i}][{j}]: {e}")
                    else:
                        print(f"      ❌ SKIP bâtiment [{i}][{j}] - Mode régénération activé (regen_only={regen_only})")
                        print(f"      ⚠️ ALERTE: Les bâtiments ne seront PAS générés car regen_only=True")
                
                except Exception as e:
                    print(f"ERREUR lors de la création bloc à [{i}][{j}]: {e}")
        
        print(f"Blocs créés: {blocks_created}, Bâtiments créés: {buildings_created}")
        
        # Générer les carrefours aux intersections (si activé)
        intersections_created = 0
        if enable_intersections:
            print("Génération des carrefours...")
            intersection_size = road_width * intersection_size_factor
            
            # Carrefours aux intersections des routes horizontales et verticales
            for i in range(grid_width - 1):
                for j in range(grid_length - 1):
                    try:
                        # Position de l'intersection
                        # Calculer position X de la route verticale i
                        max_width_i = max(
                            block_sizes[i][k]['size'][0] if isinstance(block_sizes[i][k], dict) else block_sizes[i][k][0] 
                            for k in range(grid_length)
                        )
                        x_road_start = x_starts[i] + max_width_i
                        x_intersection = x_road_start + road_width/2
                        
                        # Calculer position Y de la route horizontale j
                        max_depth_j = max(
                            block_sizes[k][j]['size'][1] if isinstance(block_sizes[k][j], dict) else block_sizes[k][j][1] 
                            for k in range(grid_width)
                        )
                        y_road_start = y_starts[j] + max_depth_j
                        y_intersection = y_road_start + road_width/2
                        
                        if generate_intersection(x_intersection, y_intersection, intersection_size, road_mat):
                            intersections_created += 1
                            
                    except Exception as e:
                        print(f"ERREUR lors de la création carrefour [{i}][{j}]: {e}")
            
            print(f"Carrefours créés: {intersections_created}")
        
        # Générer les routes diagonales (si activé)
        diagonal_roads_created = 0
        if enable_diagonal_roads and diagonal_road_frequency > 0:
            print(f"Génération des routes diagonales (fréquence: {diagonal_road_frequency}%)...")
            
            # Routes diagonales entre blocs adjacents
            for i in range(grid_width - 1):
                for j in range(grid_length - 1):
                    # Chance de générer une route diagonale
                    if random.random() * 100 < diagonal_road_frequency:
                        try:
                            # Position du bloc [i][j]
                            block_info_1 = block_sizes[i][j]
                            if isinstance(block_info_1, dict):
                                block_width_1, block_depth_1 = block_info_1['size']
                            else:
                                block_width_1, block_depth_1 = block_info_1
                            
                            # Position du bloc [i+1][j+1] (diagonalement opposé)
                            block_info_2 = block_sizes[i+1][j+1]
                            if isinstance(block_info_2, dict):
                                block_width_2, block_depth_2 = block_info_2['size']
                            else:
                                block_width_2, block_depth_2 = block_info_2
                            
                            # Centre du premier bloc
                            x_center_1 = x_starts[i] + block_width_1/2
                            y_center_1 = y_starts[j] + block_depth_1/2
                            
                            # Centre du bloc diagonalement opposé
                            x_center_2 = x_starts[i+1] + block_width_2/2
                            y_center_2 = y_starts[j+1] + block_depth_2/2
                            
                            # Créer route diagonale entre les centres des blocs
                            if generate_diagonal_road(x_center_1, y_center_1, x_center_2, y_center_2, road_width * 0.7, road_mat):
                                diagonal_roads_created += 1
                                
                        except Exception as e:
                            print(f"ERREUR lors de la création route diagonale [{i}][{j}] -> [{i+1}][{j+1}]: {e}")
            
            # Routes diagonales dans l'autre direction (du nord-est au sud-ouest)
            for i in range(grid_width - 1):
                for j in range(1, grid_length):
                    # Chance de générer une route diagonale
                    if random.random() * 100 < diagonal_road_frequency:
                        try:
                            # Position du bloc [i][j] (en haut à gauche)
                            block_info_1 = block_sizes[i][j]
                            if isinstance(block_info_1, dict):
                                block_width_1, block_depth_1 = block_info_1['size']
                            else:
                                block_width_1, block_depth_1 = block_info_1
                            
                            # Position du bloc [i+1][j-1] (en bas à droite)
                            block_info_2 = block_sizes[i+1][j-1]
                            if isinstance(block_info_2, dict):
                                block_width_2, block_depth_2 = block_info_2['size']
                            else:
                                block_width_2, block_depth_2 = block_info_2
                            
                            # Centre du premier bloc
                            x_center_1 = x_starts[i] + block_width_1/2
                            y_center_1 = y_starts[j] + block_depth_1/2
                            
                            # Centre du bloc diagonalement opposé
                            x_center_2 = x_starts[i+1] + block_width_2/2
                            y_center_2 = y_starts[j-1] + block_depth_2/2
                            
                            # Créer route diagonale entre les centres des blocs
                            if generate_diagonal_road(x_center_1, y_center_1, x_center_2, y_center_2, road_width * 0.7, road_mat):
                                diagonal_roads_created += 1
                                
                        except Exception as e:
                            print(f"ERREUR lors de la création route diagonale [{i}][{j}] -> [{i+1}][{j-1}]: {e}")
            
            print(f"Routes diagonales créées: {diagonal_roads_created}")
        
        print(f"=== RÉSUMÉ DE GÉNÉRATION ===")
        print(f"Routes standard: {roads_created}")
        print(f"Carrefours: {intersections_created}")
        print(f"Routes diagonales: {diagonal_roads_created}")
        print(f"Blocs: {blocks_created}")
        print(f"Bâtiments: {buildings_created}")
        
        return True
        
    except Exception as e:
        print(f"ERREUR CRITIQUE lors de la génération de grille: {str(e)}")
        print(f"Traceback: {traceback.format_exc()}")
        return False

def safe_delete_objects(object_filter=None):
    """Supprime les objets de manière sécurisée avec filtrage optionnel"""
    try:
        # Désélectionner tout d'abord
        bpy.ops.object.select_all(action='DESELECT')
        
        objects_to_delete = []
        
        if object_filter:
            # Filtrer les objets selon les critères fournis
            for obj in bpy.context.scene.objects:
                if object_filter(obj):
                    objects_to_delete.append(obj)
        else:
            # Par défaut, supprimer tous les objets mesh
            for obj in bpy.context.scene.objects:
                if obj.type == 'MESH':
                    objects_to_delete.append(obj)
        
        print(f"Suppression de {len(objects_to_delete)} objets...")
        
        # Sélectionner et supprimer les objets
        for obj in objects_to_delete:
            try:
                obj.select_set(True)
            except Exception as e:
                print(f"Impossible de sélectionner l'objet {obj.name}: {e}")
        
        if objects_to_delete:
            try:
                bpy.ops.object.delete(use_global=False)
                print(f"Suppression réussie de {len(objects_to_delete)} objets")
            except Exception as e:
                print(f"Erreur lors de la suppression des objets: {e}")
                return False
        
        return True
        
    except Exception as e:
        print(f"Erreur critique lors de la suppression des objets: {str(e)}")
        return False

def regenerate_roads_and_sidewalks(context):
    """Régénère seulement les routes et trottoirs"""
    try:
        # Créer un filtre pour ne supprimer que routes et trottoirs, carrefours
        def road_sidewalk_filter(obj):
            return any(keyword in obj.name.lower() for keyword in ['road', 'route', 'sidewalk', 'trottoir', 'intersection'])
        
        # Supprimer seulement les routes, trottoirs et carrefours
        if safe_delete_objects(road_sidewalk_filter):
            return generate_city(context, regen_only=True)
        else:
            print("Échec de la suppression des routes, trottoirs et carrefours")
            return False
            
    except Exception as e:
        print(f"Erreur lors de la régénération des routes et trottoirs: {str(e)}")
        return False

def generate_city(context, regen_only=False):
    """Génère une ville complète avec gestion d'erreurs robuste et protection anti-crash"""
    try:
        # Réinitialiser le compteur de bâtiments
        global building_counter
        building_counter = 0
        
        print("🏙️ === DÉBUT GÉNÉRATION VILLE SÉCURISÉE ===")
        
        # Vérifications préliminaires renforcées
        state_errors = check_blender_state()
        if state_errors:
            for error in state_errors:
                print(f"❌ ERREUR ÉTAT BLENDER: {error}")
            return False
        
        # Accéder aux propriétés directement depuis la scène (nouvelle architecture)
        scene = context.scene
        
        # Vérifier que les propriétés citygen existent
        if not hasattr(scene, 'citygen_width'):
            print("❌ ERREUR: Propriétés citygen non trouvées. Addon mal installé ou propriétés non enregistrées.")
            return False
        
        # Utiliser notre fonction utilitaire pour convertir de façon sécurisée avec limites
        width = safe_int(getattr(scene, 'citygen_width', 3), 3)  # Défaut sécurisé 3x3
        width = max(1, min(width, 10))  # Limite absolue pour éviter les crashes
        length = safe_int(getattr(scene, 'citygen_length', 3), 3)  # Défaut sécurisé 3x3
        length = max(1, min(length, 10))  # Limite absolue pour éviter les crashes
        max_floors = safe_int(getattr(scene, 'citygen_max_floors', 5), 5)  # Défaut réduit
        max_floors = max(1, min(max_floors, 20))  # Limite pour éviter les crashes
        shape_mode = "AUTO"  # Valeur par défaut pour l'instant
        
        # Validation finale avec message d'information
        total_blocks = width * length
        if total_blocks > 25:  # Limite sécurisée
            print(f"⚠️ ATTENTION: {total_blocks} blocs demandés. Réduction automatique pour éviter les crashes.")
            if width > 5:
                width = 5
            if length > 5:
                length = 5
            total_blocks = width * length
            
        print(f"✅ Paramètres validés et sécurisés: {width}x{length} ({total_blocks} blocs), {max_floors} étages max")
        
        # Nouvelles propriétés pour bâtiments multiples et routes collées
        buildings_per_block = safe_int(getattr(scene, 'citygen_buildings_per_block', 1), 1)
        buildings_per_block = max(1, min(buildings_per_block, 4))  # Limite pour performance
        seamless_roads = getattr(scene, 'citygen_seamless_roads', True)
        building_variety = getattr(scene, 'citygen_building_variety', 'MEDIUM')
        height_variation = safe_float(getattr(scene, 'citygen_height_variation', 0.3), 0.3)  # Réduit pour stabilité
        
        # Nouveaux paramètres pour la variété des blocs (valeurs par défaut)
        base_size = 10.0
        block_variety = "MEDIUM"
        district_mode = False
        district_type = "MIXED"
        commercial_ratio = 0.2
        residential_ratio = 0.6
        industrial_ratio = 0.2
        
        # Nouveaux paramètres pour les largeurs des routes et trottoirs
        road_width = safe_float(getattr(scene, 'citygen_road_width', 4.0), 4.0)
        sidewalk_width = 0.0 if seamless_roads else 1.0  # Routes collées = pas de trottoirs
        
        # Nouveaux paramètres pour les routes diagonales et carrefours (valeurs par défaut)
        enable_diagonal_roads = False
        diagonal_road_frequency = 30.0
        enable_intersections = True
        intersection_size_factor = 1.2  # Valeur par défaut pour l'instant
        
        # Validation des paramètres
        param_errors = validate_parameters(width, length, max_floors)
        if param_errors:
            for error in param_errors:
                print(f"ERREUR PARAMÈTRE: {error}")
            return False
        
        print(f"Paramètres validés: width={width}, length={length}, max_floors={max_floors}, shape={shape_mode}")
        print(f"Infrastructure: road_width={road_width}, sidewalk_width={sidewalk_width}, seamless_roads={seamless_roads}")
        print(f"Bâtiments: {buildings_per_block} par bloc, variété={building_variety}, variation_hauteur={height_variation}")
        print(f"Routes avancées: diagonales={enable_diagonal_roads} ({diagonal_road_frequency}%), carrefours={enable_intersections} (x{intersection_size_factor})")

        # Créer les matériaux avec gestion d'erreurs
        # Forcer la suppression des anciens matériaux pour s'assurer des nouvelles couleurs
        old_materials = ["RoadMat", "SidewalkMat", "BuildingMat"]
        for mat_name in old_materials:
            if mat_name in bpy.data.materials:
                print(f"Suppression de l'ancien matériau: {mat_name}")
                bpy.data.materials.remove(bpy.data.materials[mat_name])
        
        road_mat = create_material("RoadMat", (1.0, 0.75, 0.8))  # Rose pâle pour les routes
        side_mat = create_material("SidewalkMat", (0.6, 0.6, 0.6))  # Gris pour les trottoirs
        build_mat = create_material("BuildingMat", (0.5, 1.0, 0.0))  # Vert pomme pour les bâtiments
        
        print(f"Matériaux créés - Route: {road_mat}, Trottoir: {side_mat}, Bâtiment: {build_mat}")
        
        # Vérifier que les matériaux ont été créés avec succès
        if not road_mat or not side_mat or not build_mat:
            print("ERREUR: Échec de création des matériaux")
            return False

        # Suppression sélective des objets
        if not regen_only:
            print("Suppression de tous les objets mesh...")
            if not safe_delete_objects():
                print("AVERTISSEMENT: Problème lors de la suppression des objets")
        
        # Créer les matériaux de districts si nécessaire
        district_materials = {}
        if district_mode:
            district_materials = create_district_materials()
        
        # Générer les tailles variables des blocs avec les nouveaux paramètres
        try:
            block_sizes = generate_block_sizes(
                width, length, base_size, block_variety, district_mode,
                commercial_ratio, residential_ratio, industrial_ratio, district_type
            )
            if not block_sizes:
                print("❌ ERREUR: Échec de génération des tailles de blocs")
                return False
            
            # 🌿 NOUVEAU: Ajouter de la variété urbaine pour éviter la monotonie
            print(f"🌿 Ajout de variété urbaine (niveau: {building_variety})")
            block_sizes = add_urban_variety(block_sizes, building_variety)
            print(f"✅ Variété urbaine appliquée")
            
        except Exception as e:
            print(f"❌ ERREUR lors de la génération des tailles de blocs: {str(e)}")
            return False
        
        # Générer la grille unifiée de ville avec gestion d'erreur globale
        print(f"🚀 DÉBUT génération unifiée ville - Paramètres: {width}x{length}, {buildings_per_block} bât/bloc")
        try:
            success = generate_unified_city_grid(
                block_sizes, road_width, road_mat, side_mat, build_mat, max_floors, regen_only, 
                district_materials, sidewalk_width, shape_mode, 
                enable_diagonal_roads, diagonal_road_frequency, enable_intersections, intersection_size_factor,
                buildings_per_block, seamless_roads, building_variety, height_variation
            )
            
            if not success:
                print("❌ ERREUR: Échec de la génération de la grille unifiée")
                return False
                
            print("✅ Génération de la ville terminée avec succès!")
            return True
            
        except Exception as e:
            print(f"❌ ERREUR CRITIQUE lors de la génération de la ville: {str(e)}")
            print(f"🔧 Type d'erreur: {type(e).__name__}")
            # Tentative de nettoyage en cas d'erreur
            try:
                bpy.ops.object.select_all(action='DESELECT')
                print("🧹 Nettoyage d'urgence effectué")
            except:
                pass
            return False
            if not success:
                print("ERREUR: Échec de génération de la grille de ville")
                return False
        except Exception as e:
            print(f"ERREUR lors de la génération de la grille: {str(e)}")
            print(f"Traceback: {traceback.format_exc()}")
            return False
        
        print("=== Génération terminée avec succès ===")
        return True
        
    except Exception as e:
        print(f"ERREUR CRITIQUE lors de la génération de ville: {str(e)}")
        print(f"Traceback: {traceback.format_exc()}")
        return False

def generate_uniform_district(grid_width, grid_length, district_type):
    """Génère un district uniforme du type spécifié"""
    # Mapper les types de district aux types de zone
    district_mapping = {
        'RESIDENTIAL': 'RESIDENTIAL',
        'COMMERCIAL': 'COMMERCIAL', 
        'INDUSTRIAL': 'INDUSTRIAL',
        'DOWNTOWN': 'COMMERCIAL',     # Centre-ville = commercial dense
        'SUBURBAN': 'RESIDENTIAL',    # Banlieue = résidentiel
        'BUSINESS': 'COMMERCIAL'      # Affaires = commercial
    }
    
    zone_type = district_mapping.get(district_type, 'RESIDENTIAL')
    
    # Créer une grille uniforme du type spécifié
    zone_assignments = []
    for i in range(grid_width):
        row = []
        for j in range(grid_length):
            row.append(zone_type)
        zone_assignments.append(row)
    
    return zone_assignments

def generate_block_sizes(grid_width, grid_length, base_size=10, variety='MEDIUM', district_mode=False, 
                        commercial_ratio=0.2, residential_ratio=0.6, industrial_ratio=0.2, district_type='MIXED'):
    """Génère une grille de tailles de blocs variées avec différents modes de variation"""
    try:
        if grid_width <= 0 or grid_length <= 0:
            print(f"Dimensions de grille invalides: {grid_width}x{grid_length}")
            return None
            
        if base_size <= 0:
            print(f"Taille de base invalide: {base_size}")
            return None
        
        print(f"Génération blocs - Mode: {variety}, Districts: {district_mode}, Base: {base_size}")
        
        # Définir les variations selon le mode choisi
        variation_ranges = {
            'UNIFORM': (1.0, 1.0),      # Pas de variation
            'LOW': (0.8, 1.2),          # ±20%
            'MEDIUM': (0.6, 1.4),       # ±40%
            'HIGH': (0.4, 1.6),         # ±60%
            'EXTREME': (0.25, 2.0),     # -75% à +100%
            'DISTRICTS': (0.7, 1.3),    # ±30% mais par zones
        }
        
        min_var, max_var = variation_ranges.get(variety, (0.6, 1.4))
        
        # Définir les types de zones et leurs caractéristiques étendues
        zone_types = {
            'COMMERCIAL': {
                'size_multiplier': 1.5,     # 50% plus grand
                'min_floors': 4,            # Bâtiments moyens à hauts
                'max_floors_multiplier': 1.5,
                'shape_preference': ['RECT', 'L', 'U']
            },
            'RESIDENTIAL': {
                'size_multiplier': 1.0,     # Taille normale
                'min_floors': 1,            # Bâtiments bas à moyens
                'max_floors_multiplier': 1.0,
                'shape_preference': ['RECT', 'L', 'T']
            },
            'INDUSTRIAL': {
                'size_multiplier': 2.0,     # Double de taille
                'min_floors': 1,            # Bâtiments bas
                'max_floors_multiplier': 0.3,  # Peu d'étages
                'shape_preference': ['RECT', 'L']
            }
        }
        
        # Ajuster les caractéristiques selon le type de district spécialisé
        if district_mode and district_type != 'MIXED':
            zone_adjustments = {
                'DOWNTOWN': {
                    'size_multiplier': 0.8,     # Blocs plus compacts
                    'min_floors': 8,            # Gratte-ciels
                    'max_floors_multiplier': 3.0,  # Très hauts
                    'shape_preference': ['RECT']
                },
                'SUBURBAN': {
                    'size_multiplier': 1.3,     # Blocs plus grands
                    'min_floors': 1,            # Maisons basses
                    'max_floors_multiplier': 0.5,  # 1-2 étages max
                    'shape_preference': ['RECT', 'L']
                },
                'BUSINESS': {
                    'size_multiplier': 1.2,     # Taille moyenne-grande
                    'min_floors': 6,            # Tours de bureaux
                    'max_floors_multiplier': 2.5,  # Hauts
                    'shape_preference': ['RECT', 'T']
                }
            }
            
            if district_type in zone_adjustments:
                # Appliquer les ajustements à tous les types de zones
                adjustments = zone_adjustments[district_type]
                for zone_type in zone_types:
                    zone_types[zone_type].update(adjustments)
        
        block_sizes = []
        zone_assignments = []
        
        # Générer les assignations de zones si mode districts activé
        if district_mode:
            if district_type == 'MIXED':
                # Mode mixte : utiliser les ratios comme avant
                zone_assignments = generate_district_zones(grid_width, grid_length, 
                                                         commercial_ratio, residential_ratio, industrial_ratio)
            else:
                # Mode spécialisé : tout le district est du même type
                zone_assignments = generate_uniform_district(grid_width, grid_length, district_type)
        
        for i in range(grid_width):
            row = []
            zone_row = []
            for j in range(grid_length):
                try:
                    # Déterminer le type de zone
                    if district_mode and i < len(zone_assignments) and j < len(zone_assignments[i]):
                        zone_type = zone_assignments[i][j]
                    else:
                        zone_type = 'RESIDENTIAL'  # Type par défaut
                    
                    zone_row.append(zone_type)
                    zone_info = zone_types[zone_type]
                    
                    # Calcul de la taille avec variation
                    if variety == 'DISTRICTS':
                        # Mode districts : variation par zones cohérentes
                        size_variation = generate_district_variation(i, j, grid_width, grid_length, min_var, max_var)
                    else:
                        # Mode normal : variation aléatoire
                        size_variation = random.uniform(min_var, max_var)
                    
                    # Appliquer le multiplicateur de zone
                    total_multiplier = size_variation * zone_info['size_multiplier']
                    
                    # Générer largeur et profondeur avec variations indépendantes
                    width_variation = random.uniform(0.8, 1.2)  # Variation fine supplémentaire
                    depth_variation = random.uniform(0.8, 1.2)
                    
                    width = base_size * total_multiplier * width_variation
                    depth = base_size * total_multiplier * depth_variation
                    
                    # Validation et ajustement des tailles
                    width = max(2.0, min(width, base_size * 3))  # Limites raisonnables
                    depth = max(2.0, min(depth, base_size * 3))
                    
                    # Stocker les informations étendues du bloc
                    block_info = {
                        'size': (width, depth),
                        'zone_type': zone_type,
                        'zone_info': zone_info,
                        'base_variation': size_variation
                    }
                    
                    row.append(block_info)
                    
                except Exception as e:
                    print(f"Erreur génération bloc à [{i}][{j}]: {e}, utilisation valeurs par défaut")
                    row.append({
                        'size': (base_size, base_size),
                        'zone_type': 'RESIDENTIAL',
                        'zone_info': zone_types['RESIDENTIAL'],
                        'base_variation': 1.0
                    })
            
            block_sizes.append(row)
        
        # Afficher un résumé de la génération
        total_blocks = grid_width * grid_length
        if district_mode:
            commercial_count = sum(1 for row in zone_assignments for zone in row if zone == 'COMMERCIAL')
            residential_count = sum(1 for row in zone_assignments for zone in row if zone == 'RESIDENTIAL')
            industrial_count = sum(1 for row in zone_assignments for zone in row if zone == 'INDUSTRIAL')
            
            print(f"Districts générés - Commercial: {commercial_count}/{total_blocks}, "
                  f"Résidentiel: {residential_count}/{total_blocks}, "
                  f"Industriel: {industrial_count}/{total_blocks}")
        
        print(f"Grille de blocs {grid_width}x{grid_length} générée avec variété '{variety}'")
        return block_sizes
        
    except Exception as e:
        print(f"Erreur critique lors de la génération des tailles de blocs: {str(e)}")
        return None

def generate_district_zones(grid_width, grid_length, commercial_ratio, residential_ratio, industrial_ratio):
    """Génère des zones de districts cohérentes avec algorithme amélioré"""
    try:
        print(f"Génération districts - Ratios: C={commercial_ratio:.2f}, R={residential_ratio:.2f}, I={industrial_ratio:.2f}")
        
        # Normaliser les ratios pour qu'ils totalisent 1.0
        total_ratio = commercial_ratio + residential_ratio + industrial_ratio
        if total_ratio > 0:
            commercial_ratio /= total_ratio
            residential_ratio /= total_ratio
            industrial_ratio /= total_ratio
        else:
            # Valeurs par défaut si ratios invalides
            commercial_ratio, residential_ratio, industrial_ratio = 0.2, 0.6, 0.2
        
        print(f"Ratios normalisés: C={commercial_ratio:.2f}, R={residential_ratio:.2f}, I={industrial_ratio:.2f}")
        
        zones = []
        total_blocks = grid_width * grid_length
        
        # Calculer le nombre de blocs pour chaque type
        commercial_blocks = int(total_blocks * commercial_ratio)
        industrial_blocks = int(total_blocks * industrial_ratio)
        residential_blocks = total_blocks - commercial_blocks - industrial_blocks
        
        print(f"Blocs prévus - Commercial: {commercial_blocks}, Industriel: {industrial_blocks}, Résidentiel: {residential_blocks}")
        
        # Améliorer la génération des centres de zones
        # Plus de centres pour une meilleure distribution
        num_commercial_centers = max(1, commercial_blocks // 8) if commercial_blocks > 0 else 0
        num_industrial_centers = max(1, industrial_blocks // 12) if industrial_blocks > 0 else 0
        
        commercial_centers = generate_zone_centers(grid_width, grid_length, num_commercial_centers)
        industrial_centers = generate_zone_centers(grid_width, grid_length, num_industrial_centers)
        
        print(f"Centres générés - Commercial: {len(commercial_centers)}, Industriel: {len(industrial_centers)}")
        
        # Utiliser un algorithme de Voronoi simplifié pour une meilleure distribution
        zone_counts = {'COMMERCIAL': 0, 'INDUSTRIAL': 0, 'RESIDENTIAL': 0}
        
        for i in range(grid_width):
            row = []
            for j in range(grid_length):
                zone_type = 'RESIDENTIAL'  # Type par défaut
                min_distance = float('inf')
                
                # Vérifier la distance aux centres commerciaux
                for cx, cy in commercial_centers:
                    distance = abs(i - cx) + abs(j - cy)  # Distance Manhattan
                    if distance < min_distance and zone_counts['COMMERCIAL'] < commercial_blocks:
                        min_distance = distance
                        zone_type = 'COMMERCIAL'
                
                # Vérifier la distance aux centres industriels (avec priorité sur commercial si très proche)
                for cx, cy in industrial_centers:
                    distance = abs(i - cx) + abs(j - cy)
                    if distance < min_distance and zone_counts['INDUSTRIAL'] < industrial_blocks:
                        min_distance = distance
                        zone_type = 'INDUSTRIAL'
                    elif distance <= 1 and zone_counts['INDUSTRIAL'] < industrial_blocks:  # Force industriel si très proche
                        zone_type = 'INDUSTRIAL'
                        break
                
                # Assigner le type et mettre à jour les compteurs
                zone_counts[zone_type] += 1
                row.append(zone_type)
            
            zones.append(row)
        
        # Afficher le résultat de la distribution
        print(f"Distribution finale - Commercial: {zone_counts['COMMERCIAL']}, "
              f"Industriel: {zone_counts['INDUSTRIAL']}, Résidentiel: {zone_counts['RESIDENTIAL']}")
        
        return zones
        
    except Exception as e:
        print(f"Erreur génération zones de districts: {e}")
        print(f"Traceback: {traceback.format_exc()}")
        # Retourner une assignation par défaut
        return [['RESIDENTIAL' for _ in range(grid_length)] for _ in range(grid_width)]

def generate_zone_centers(grid_width, grid_length, num_centers):
    """Génère des centres de zones aléatoires avec distribution améliorée"""
    centers = []
    if num_centers <= 0:
        return centers
    
    # S'assurer que les centres sont bien distribués
    if num_centers == 1:
        # Un seul centre au milieu
        x = grid_width // 2
        y = grid_length // 2
        centers.append((x, y))
    else:
        # Distribuer les centres avec un espacement minimal
        min_distance = max(2, min(grid_width, grid_length) // num_centers)
        
        for _ in range(num_centers * 3):  # Essayer plusieurs fois
            if len(centers) >= num_centers:
                break
                
            x = random.randint(0, grid_width - 1)
            y = random.randint(0, grid_length - 1)
            
            # Vérifier que le nouveau centre n'est pas trop proche des existants
            too_close = False
            for cx, cy in centers:
                if abs(x - cx) + abs(y - cy) < min_distance:
                    too_close = True
                    break
            
            if not too_close:
                centers.append((x, y))
    
    print(f"Centres générés: {centers}")
    return centers

def generate_district_variation(i, j, grid_width, grid_length, min_var, max_var):
    """Génère une variation basée sur la position pour créer des zones cohérentes"""
    # Utiliser la position pour créer des zones de tailles similaires
    zone_x = i // 3  # Diviser en zones de 3x3
    zone_y = j // 3
    
    # Utiliser la position de la zone comme seed pour la cohérence
    random.seed(zone_x * 1000 + zone_y)
    variation = random.uniform(min_var, max_var)
    
    # Restaurer le seed aléatoire
    random.seed()
    
    return variation

def create_district_materials():
    """Crée des matériaux distinctifs pour chaque type de zone en mode district."""
    materials = {}
    
    try:
        # Matériau commercial (vert pomme foncé)
        if "Commercial_District" not in bpy.data.materials:
            mat_commercial = bpy.data.materials.new(name="Commercial_District")
            mat_commercial.use_nodes = True
            principled = mat_commercial.node_tree.nodes.get("Principled BSDF")
            if principled:
                principled.inputs[0].default_value = (0.3, 0.8, 0.0, 1.0)  # Vert pomme foncé
                principled.inputs[7].default_value = 0.1  # Roughness
        materials['COMMERCIAL'] = bpy.data.materials["Commercial_District"]
        
        # Matériau résidentiel (vert pomme)
        if "Residential_District" not in bpy.data.materials:
            mat_residential = bpy.data.materials.new(name="Residential_District")
            mat_residential.use_nodes = True
            principled = mat_residential.node_tree.nodes.get("Principled BSDF")
            if principled:
                principled.inputs[0].default_value = (0.5, 1.0, 0.0, 1.0)  # Vert pomme
                principled.inputs[7].default_value = 0.3  # Roughness
        materials['RESIDENTIAL'] = bpy.data.materials["Residential_District"]
        
        # Matériau industriel (vert pomme clair)
        if "Industrial_District" not in bpy.data.materials:
            mat_industrial = bpy.data.materials.new(name="Industrial_District")
            mat_industrial.use_nodes = True
            principled = mat_industrial.node_tree.nodes.get("Principled BSDF")
            if principled:
                principled.inputs[0].default_value = (0.7, 1.0, 0.2, 1.0)  # Vert pomme clair
                principled.inputs[7].default_value = 0.5  # Roughness
        materials['INDUSTRIAL'] = bpy.data.materials["Industrial_District"]
        
        print("✓ Matériaux de districts créés avec succès")
        return materials
        
    except Exception as e:
        print(f"Erreur lors de la création des matériaux de districts: {e}")
        return {}
def set_origin_to_center_bottom(obj):
    """Déplace l'origine de l'objet au centre bas (center bottom)"""
    try:
        if not obj or not obj.data:
            return False
            
        # Sauvegarder la position actuelle
        current_location = obj.location.copy()
        
        # Aller en mode édition pour calculer les limites
        bpy.context.view_layer.objects.active = obj
        bpy.ops.object.mode_set(mode='EDIT')
        
        # Revenir en mode objet
        bpy.ops.object.mode_set(mode='OBJECT')
        
        # Calculer les limites du mesh
        mesh = obj.data
        if not mesh.vertices:
            return False
            
        # Trouver les limites
        x_coords = [v.co.x for v in mesh.vertices]
        y_coords = [v.co.y for v in mesh.vertices]
        z_coords = [v.co.z for v in mesh.vertices]
        
        x_min, x_max = min(x_coords), max(x_coords)
        y_min, y_max = min(y_coords), max(y_coords)
        z_min = min(z_coords)
        
        # Calculer le centre en X et Y, mais garder le minimum en Z
        center_x = (x_min + x_max) / 2
        center_y = (y_min + y_max) / 2
        
        # Déplacer tous les sommets pour ajuster l'origine
        for vertex in mesh.vertices:
            vertex.co.x -= center_x
            vertex.co.y -= center_y
            vertex.co.z -= z_min  # Le bas devient z=0
        
        # Ajuster la position de l'objet pour compenser le déplacement
        obj.location.x = current_location.x + center_x
        obj.location.y = current_location.y + center_y
        obj.location.z = current_location.z + z_min
        
        # Mettre à jour le mesh
        mesh.update()
        
        return True
        
    except Exception as e:
        print(f"Erreur lors du réglage de l'origine: {e}")
        return False

def create_cube_with_center_bottom_origin(size_x, size_y, size_z, location=(0, 0, 0)):
    """Crée un cube avec l'origine au centre bas - Version simplifiée"""
    try:
        print(f"🔨 create_cube_with_center_bottom_origin: taille=({size_x:.1f},{size_y:.1f},{size_z:.1f}), pos=({location[0]:.1f},{location[1]:.1f},{location[2]:.1f})")
        
        # Calculer la position finale directement (centre bas)
        final_x = location[0]
        final_y = location[1] 
        final_z = location[2] + (size_z / 2)  # Décaler vers le haut de la moitié de la hauteur
        
        print(f"   📍 Position finale calculée: ({final_x:.1f}, {final_y:.1f}, {final_z:.1f})")
        
        # Créer le cube directement à la bonne position
        bpy.ops.mesh.primitive_cube_add(size=2, location=(final_x, final_y, final_z))
        obj = bpy.context.object
        
        if not obj:
            print(f"   ❌ Échec création cube primitif")
            return None
        
        print(f"   ✅ Cube primitif créé: {obj.name}")
        print(f"   📏 Position avant échelle: ({obj.location.x:.1f}, {obj.location.y:.1f}, {obj.location.z:.1f})")
        
        # Appliquer les dimensions en redimensionnant
        obj.scale.x = size_x / 2  # Diviser par 2 car le cube fait size=2
        obj.scale.y = size_y / 2
        obj.scale.z = size_z / 2
        
        print(f"   🔧 Échelle appliquée: ({obj.scale.x:.1f}, {obj.scale.y:.1f}, {obj.scale.z:.1f})")
        
        # Optionnel: appliquer l'échelle définitivement
        try:
            bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
            print(f"   ✅ Transformation appliquée")
        except Exception as e:
            print(f"   ⚠️ Avertissement transformation: {e}")
        
        print(f"   📍 Position finale: ({obj.location.x:.1f}, {obj.location.y:.1f}, {obj.location.z:.1f})")
        print(f"   📐 Dimensions finales: échelle=({obj.scale.x:.1f}, {obj.scale.y:.1f}, {obj.scale.z:.1f})")
        
        return obj
        
    except Exception as e:
        print(f"❌ Erreur lors de la création du cube avec origine centre bas: {e}")
        return None

def generate_polygonal_block(center_x, center_y, vertices, width, depth, mat):
    """Génère un bloc polygonal avec un nombre variable d'arêtes"""
    import random
    import math
    
    try:
        print(f"🔷 Génération bloc polygonal {vertices} côtés au centre ({center_x:.1f}, {center_y:.1f})")
        
        # Créer le mesh polygonal avec une hauteur visible
        bpy.ops.mesh.primitive_cylinder_add(
            vertices=vertices, 
            radius=min(width, depth)/2, 
            depth=0.5,  # Hauteur plus visible pour le bloc
            location=(center_x, center_y, 0.25)  # Centré sur Z
        )
        
        obj = bpy.context.object
        if not obj:
            return None
        
        # Adapter les dimensions
        obj.scale.x = width / min(width, depth)
        obj.scale.y = depth / min(width, depth)
        obj.name = f"PolygonalBlock_{vertices}sides_{center_x:.1f}_{center_y:.1f}"
        
        # Stocker les informations du bloc pour l'orientation des bâtiments
        obj["block_sides"] = vertices
        obj["block_width"] = width
        obj["block_depth"] = depth
        obj["block_center_x"] = center_x
        obj["block_center_y"] = center_y
        
        # Appliquer le matériau de trottoir
        if mat and obj.data:
            obj.data.materials.clear()
            obj.data.materials.append(mat)
        
        print(f"✅ Bloc polygonal créé: {vertices} côtés, dimensions {width:.1f}x{depth:.1f}")
        return obj
        
    except Exception as e:
        print(f"Erreur création bloc polygonal: {e}")
        return None

def calculate_building_orientation_for_polygon(block_sides, building_x, building_y, block_center_x, block_center_y):
    """Calcule l'orientation optimale d'un bâtiment pour s'aligner avec un bloc polygonal"""
    import math
    
    try:
        # Pour les polygones réguliers, calculer l'angle de l'arête la plus proche
        if block_sides >= 3:
            # Angle entre le centre du bloc et la position du bâtiment
            dx = building_x - block_center_x
            dy = building_y - block_center_y
            angle_to_building = math.atan2(dy, dx)
            
            # Angle d'une arête du polygone
            edge_angle = (2 * math.pi) / block_sides
            
            # Trouver l'arête la plus proche
            closest_edge_index = round(angle_to_building / edge_angle) % block_sides
            closest_edge_angle = closest_edge_index * edge_angle
            
            # Orienter le bâtiment parallèlement à cette arête
            # Ajouter 90 degrés pour que la face soit parallèle (et non perpendiculaire)
            building_rotation = closest_edge_angle + math.pi/2
            
            return building_rotation
        else:
            return 0.0
            
    except Exception as e:
        print(f"Erreur calcul orientation: {e}")
        return 0.0

def generate_oriented_building(x, y, width, depth, height, mat, block_sides, block_center_x, block_center_y, variety='MEDIUM'):
    """Génère un bâtiment orienté selon un bloc polygonal"""
    import math
    
    try:
        # Calculer l'orientation optimale
        rotation = calculate_building_orientation_for_polygon(
            block_sides, x, y, block_center_x, block_center_y
        )
        
        print(f"🏢 Bâtiment orienté: rotation {math.degrees(rotation):.1f}° pour bloc {block_sides} côtés")
        
        # Créer le bâtiment standard
        building = generate_building(x, y, width, depth, height, mat, building_variety=variety)
        
        if building:
            # Appliquer la rotation
            building.rotation_euler.z = rotation
            building.name = f"OrientedBuilding_{block_sides}sides_{x:.1f}_{y:.1f}"
            
        return building
        
    except Exception as e:
        print(f"Erreur génération bâtiment orienté: {e}")
        return None

def generate_organic_road_network(block_zones, road_width, road_mat, curve_intensity):
    """Génère un réseau de routes organiques qui épousent les formes des blocs"""
    import math
    
    try:
        roads_created = 0
        print(f"🛣️ Génération réseau de routes organiques pour {len(block_zones)} blocs...")
        
        # Créer des routes qui contournent les blocs polygonaux
        for i, zone in enumerate(block_zones):
            # Rayon du bloc polygonal
            block_radius = min(zone['width'], zone['depth']) / 2
            
            # Créer un anneau de route autour du bloc
            if random.random() < 0.7:  # 70% de chance d'avoir une route périphérique
                road_ring = generate_polygonal_road_ring(
                    zone['x'], zone['y'], zone['sides'], 
                    block_radius + road_width, road_width, road_mat
                )
                if road_ring:
                    roads_created += 1
            
            # Connecter aux blocs voisins avec des routes courbes
            for j, other_zone in enumerate(block_zones[i+1:], i+1):
                distance = math.sqrt((zone['x'] - other_zone['x'])**2 + (zone['y'] - other_zone['y'])**2)
                
                # Connecter seulement les blocs proches
                if distance < 20:  # Distance augmentée
                    if random.random() < curve_intensity:
                        # Route courbe adaptative
                        roads = generate_adaptive_curved_road(
                            zone, other_zone, road_width, road_mat
                        )
                        if roads:
                            roads_created += len(roads)
                    else:
                        # Route droite simple
                        road = generate_diagonal_road(
                            zone['x'], zone['y'], other_zone['x'], other_zone['y'], 
                            road_width, road_mat
                        )
                        if road:
                            roads_created += 1
        
        return roads_created
        
    except Exception as e:
        print(f"Erreur génération réseau organique: {e}")
        return 0

def generate_polygonal_road_ring(center_x, center_y, sides, radius, width, mat):
    """Génère un anneau de route polygonal autour d'un bloc"""
    import math
    
    try:
        # Créer un cylindre polygonal pour l'anneau de route
        bpy.ops.mesh.primitive_cylinder_add(
            vertices=sides,
            radius=radius,
            depth=0.1,  # Hauteur fine pour la route
            location=(center_x, center_y, 0.05)
        )
        
        road_ring = bpy.context.object
        if not road_ring:
            return None
        
        # Passer en mode édition pour créer l'anneau
        bpy.context.view_layer.objects.active = road_ring
        bpy.ops.object.mode_set(mode='EDIT')
        
        # Sélectionner tout et faire un inset pour créer l'anneau
        bpy.ops.mesh.select_all(action='SELECT')
        bpy.ops.mesh.inset_faces(thickness=width/radius, depth=0)
        
        # Supprimer les faces intérieures pour créer l'anneau
        bpy.ops.mesh.select_all(action='DESELECT')
        bpy.ops.mesh.select_face_by_sides(number=sides, type='EQUAL')
        bpy.ops.mesh.delete(type='FACE')
        
        bpy.ops.object.mode_set(mode='OBJECT')
        
        # Nommer et matériau
        road_ring.name = f"PolygonalRoadRing_{sides}sides_{center_x:.1f}_{center_y:.1f}"
        if mat and road_ring.data:
            road_ring.data.materials.clear()
            road_ring.data.materials.append(mat)
        
        print(f"✅ Anneau de route polygonal créé: {sides} côtés")
        return road_ring
        
    except Exception as e:
        print(f"Erreur création anneau de route: {e}")
        # Retourner en mode objet si erreur
        try:
            bpy.ops.object.mode_set(mode='OBJECT')
        except:
            pass
        return None

def generate_adaptive_curved_road(zone1, zone2, width, mat):
    """Génère une route courbe qui s'adapte aux formes des blocs connectés"""
    import math
    import random
    
    try:
        # Points de départ et d'arrivée
        start_x, start_y = zone1['x'], zone1['y']
        end_x, end_y = zone2['x'], zone2['y']
        
        # Calculer les points de courbe en évitant les centres des blocs
        mid_x = (start_x + end_x) / 2
        mid_y = (start_y + end_y) / 2
        
        # Ajouter une déviation perpendiculaire pour la courbe
        dx = end_x - start_x
        dy = end_y - start_y
        distance = math.sqrt(dx*dx + dy*dy)
        
        if distance > 0:
            # Vecteur perpendiculaire normalisé
            perp_x = -dy / distance
            perp_y = dx / distance
            
            # Déviation aléatoire pour la courbe
            deviation = random.uniform(-distance*0.3, distance*0.3)
            curve_x = mid_x + perp_x * deviation
            curve_y = mid_y + perp_y * deviation
            
            # Générer la route courbe
            return generate_angled_road(start_x, start_y, end_x, end_y, width, mat, 
                                      curve_points=[(curve_x, curve_y)])
        
        return []
        
    except Exception as e:
        print(f"Erreur route courbe adaptative: {e}")
        return []

def generate_angled_road(start_x, start_y, end_x, end_y, width, mat, curve_points=None):
    """Génère une route avec angles variables et courbes optionnelles"""
    import random
    import math
    
    try:
        print(f"🛣️ Génération route angulaire de ({start_x:.1f},{start_y:.1f}) à ({end_x:.1f},{end_y:.1f})")
        
        # Si pas de points de courbe spécifiés, créer une route avec angle aléatoire
        if not curve_points:
            # Créer un point de courbe intermédiaire
            mid_x = (start_x + end_x) / 2
            mid_y = (start_y + end_y) / 2
            
            # Ajouter une déviation aléatoire
            deviation = random.uniform(-5, 5)
            perpendicular_angle = math.atan2(end_y - start_y, end_x - start_x) + math.pi/2
            mid_x += deviation * math.cos(perpendicular_angle)
            mid_y += deviation * math.sin(perpendicular_angle)
            
            curve_points = [(start_x, start_y), (mid_x, mid_y), (end_x, end_y)]
        
        # Créer les segments de route
        road_objects = []
        for i in range(len(curve_points) - 1):
            x1, y1 = curve_points[i]
            x2, y2 = curve_points[i + 1]
            
            # Calculer position et angle du segment
            seg_x = (x1 + x2) / 2
            seg_y = (y1 + y2) / 2
            length = math.sqrt((x2 - x1)**2 + (y2 - y1)**2)
            angle = math.atan2(y2 - y1, x2 - x1)
            
            # Créer le segment
            result = generate_road(seg_x, seg_y, width, length, mat, True, angle)
            if result:
                obj = bpy.context.object
                if obj:
                    obj.name = f"angled_road_seg_{i}_{seg_x:.1f}_{seg_y:.1f}"
                    road_objects.append(obj)
        
        return road_objects
        
    except Exception as e:
        print(f"Erreur création route angulaire: {e}")
        return []

def generate_organic_city_layout(context):
    """Génère un layout de ville organique avec blocs polygonaux et routes angulaires"""
    import random
    import math
    
    try:
        print("🌿 Début génération layout organique")
        
        # Nettoyage de la scène avant génération
        safe_delete_objects()
        
        # Récupérer les paramètres depuis la scène
        scene = context.scene
        width = safe_int(getattr(scene, 'citygen_width', 5), 5)
        length = safe_int(getattr(scene, 'citygen_length', 5), 5)
        road_width = getattr(scene, 'citygen_road_width', 4.0)
        
        # Récupérer les paramètres organiques
        polygon_min_sides = safe_int(getattr(scene, 'citygen_polygon_min_sides', 4), 4)
        polygon_max_sides = safe_int(getattr(scene, 'citygen_polygon_max_sides', 6), 6)
        road_curve_intensity = getattr(scene, 'citygen_road_curve_intensity', 0.5)
        block_size_variation = getattr(scene, 'citygen_block_size_variation', 0.3)
        
        print(f"🌿 Paramètres organiques: {width}x{length}, sides:{polygon_min_sides}-{polygon_max_sides}, curves:{road_curve_intensity}")
        
        # Créer les matériaux nécessaires
        road_mat = create_material("RoadMat_Organic", (1.0, 0.75, 0.8))  # Rose pâle pour les routes
        side_mat = create_material("SidewalkMat_Organic", (0.6, 0.6, 0.6))  # Gris pour les trottoirs
        build_mat = create_material("BuildingMat_Organic", (0.5, 1.0, 0.0))  # Vert pomme pour les bâtiments
        
        # Définir les zones de blocs avec formes variées - logique améliorée
        block_zones = []
        block_size = 8.0  # Taille de base d'un bloc
        
        print(f"🌿 Grille {width}x{length} -> Génération blocs organiques")
        
        # Créer une grille de blocs organiques
        for i in range(width):
            for j in range(length):
                # Position du centre du bloc
                center_x = (i - width/2) * block_size
                center_y = (j - length/2) * block_size
                
                # Choisir aléatoirement le nombre de côtés selon les paramètres
                sides = random.randint(polygon_min_sides, polygon_max_sides)
                
                # Taille variable des blocs selon le paramètre
                base_size = block_size * 0.8  # 80% de la grille pour laisser de l'espace
                variation = base_size * block_size_variation
                block_width = random.uniform(base_size - variation, base_size + variation)
                block_depth = random.uniform(base_size - variation, base_size + variation)
                
                # Nombre de bâtiments par défaut
                default_buildings = safe_int(getattr(scene, 'citygen_buildings_per_block', 1), 1)
                
                block_zones.append({
                    'x': center_x,
                    'y': center_y,
                    'width': block_width,
                    'depth': block_depth,
                    'sides': sides,
                    'buildings_count': default_buildings  # Nombre de base qui sera modifié par la densité
                })
        
        print(f"🌿 Génération de {len(block_zones)} blocs organiques")
        
        # === APPLIQUER LE RÉALISME URBAIN (VERSION SÉCURISÉE) ===
        # Récupérer les paramètres de réalisme avec valeurs par défaut sécurisées
        try:
            density_variation = getattr(scene, 'citygen_density_variation', 0.4)
            age_variation = getattr(scene, 'citygen_age_variation', True)
            mixed_use = getattr(scene, 'citygen_mixed_use', True)
            landmark_frequency = getattr(scene, 'citygen_landmark_frequency', 0.15)
            plaza_frequency = getattr(scene, 'citygen_plaza_frequency', 0.1)
            street_life = getattr(scene, 'citygen_street_life', False)
            weathering = getattr(scene, 'citygen_weathering', 0.3)
            irregular_lots = getattr(scene, 'citygen_irregular_lots', False)
            growth_pattern = getattr(scene, 'citygen_growth_pattern', 'ORGANIC')
            
            print(f"🎨 Paramètres réalisme chargés avec succès")
        except Exception as param_error:
            print(f"⚠️ Erreur paramètres réalisme, utilisation valeurs par défaut: {param_error}")
            density_variation = 0.4
            age_variation = True
            mixed_use = True
            landmark_frequency = 0.15
            plaza_frequency = 0.1
            street_life = False
            weathering = 0.3
            irregular_lots = False
            growth_pattern = 'ORGANIC'
        
        # Appliquer la densité réaliste (version sécurisée)
        try:
            if density_variation > 0:
                block_zones = generate_realistic_city_density(block_zones, density_variation)
                print(f"✅ Densité réaliste appliquée")
            else:
                print(f"⏩ Densité réaliste désactivée")
        except Exception as density_error:
            print(f"⚠️ Erreur densité réaliste, mode standard: {density_error}")
        
        # Créer matériaux supplémentaires pour le réalisme (version sécurisée)
        try:
            plaza_mat = create_material("PlazaMat_Realistic", (0.8, 0.9, 0.7))  # Vert pâle pour places
            tree_mat = create_material("TreeMat_Realistic", (0.2, 0.8, 0.2))   # Vert pour végétation
            landmark_mat = create_material("LandmarkMat_Realistic", (0.9, 0.8, 0.6))  # Doré pour monuments
        except Exception as mat_error:
            print(f"⚠️ Erreur création matériaux réalisme: {mat_error}")
            plaza_mat = side_mat  # Fallback
            tree_mat = build_mat  # Fallback
            landmark_mat = build_mat  # Fallback
        
        # Créer les blocs polygonaux avec bâtiments
        buildings_created = 0
        blocks_created = 0
        all_buildings = []  # Pour le vieillissement final
        
        for zone in block_zones:
            # Créer le bloc polygonal (fondation)
            block = generate_polygonal_block(
                zone['x'], zone['y'], zone['sides'], 
                zone['width'], zone['depth'], side_mat
            )
            if block:
                blocks_created += 1
                
                # Probabilité de place publique au lieu de bloc (version sécurisée)
                try:
                    if plaza_frequency > 0 and random.random() < plaza_frequency:
                        plaza = create_public_plaza(
                            zone['x'], zone['y'], 
                            min(zone['width'], zone['depth']) * 0.8, 
                            plaza_mat, tree_mat
                        )
                        if plaza:
                            print(f"🌳 Place publique créée à la place du bloc")
                            continue  # Passer au bloc suivant
                except Exception as plaza_error:
                    print(f"⚠️ Erreur création place publique: {plaza_error}")
                
                # Ajouter des bâtiments dans le bloc (utiliser la densité calculée avec sécurité)
                try:
                    buildings_in_block = zone.get('buildings_count', 1)
                    if buildings_in_block <= 0:  # Sécurité
                        buildings_in_block = 1
                except Exception:
                    buildings_in_block = 1  # Valeur par défaut sécurisée
                
                for b in range(buildings_in_block):
                    try:
                        # Position aléatoire dans le bloc (plus centrée)
                        offset_range = min(zone['width'], zone['depth']) * 0.3  # 30% de la taille du bloc
                        building_x = zone['x'] + random.uniform(-offset_range, offset_range)
                        building_y = zone['y'] + random.uniform(-offset_range, offset_range)
                        
                        # Vérifier si c'est un monument (version sécurisée)
                        is_landmark = False
                        try:
                            if landmark_frequency > 0:
                                is_landmark = random.random() < landmark_frequency
                        except Exception:
                            is_landmark = False
                        
                        if is_landmark:
                            # Créer un monument (version sécurisée)
                            try:
                                building = create_landmark_building(
                                    building_x, building_y, 1.5, landmark_mat
                                )
                            except Exception as landmark_error:
                                print(f"⚠️ Erreur création monument, bâtiment standard: {landmark_error}")
                                building = None
                        else:
                            building = None
                        
                        # Si pas de monument ou erreur, créer un bâtiment normal
                        if not building:
                            # Bâtiment normal avec variations d'âge (version sécurisée)
                            floors = safe_int(getattr(scene, 'citygen_max_floors', 8), 8)
                            variety = getattr(scene, 'citygen_building_variety', 'MEDIUM')
                            
                            # Variation d'âge - bâtiments plus anciens sont plus bas (version sécurisée)
                            try:
                                if age_variation and random.random() < 0.4:  # 40% de bâtiments "anciens"
                                    floors = max(1, int(floors * random.uniform(0.3, 0.7)))
                                    variety = random.choice(['LOW', 'MEDIUM'])  # Styles plus simples
                            except Exception:
                                pass  # Garder les valeurs par défaut
                            
                            # Usage mixte - varier les hauteurs dans un même bloc (version sécurisée)
                            try:
                                if mixed_use and b > 0:  # Pas le premier bâtiment
                                    floors = max(1, int(floors * random.uniform(0.5, 1.5)))
                            except Exception:
                                pass  # Garder les valeurs par défaut
                            
                            # Dimensions du bâtiment (adaptées au bloc)
                            base_width = min(zone['width'], zone['depth']) * 0.4
                            
                            # Parcelles irrégulières (version sécurisée)
                            try:
                                if irregular_lots:
                                    width_variation = random.uniform(0.7, 1.3)
                                    depth_variation = random.uniform(0.7, 1.3)
                                    build_width = base_width * width_variation
                                    build_depth = base_width * depth_variation
                                else:
                                    build_width = base_width
                                    build_depth = base_width
                            except Exception:
                                build_width = base_width
                                build_depth = base_width
                            
                            # Générer un bâtiment orienté selon le bloc polygonal
                            building = generate_oriented_building(
                                building_x, building_y, build_width, build_depth, floors,
                                build_mat, zone['sides'], zone['x'], zone['y'], variety
                            )
                        
                        if building:
                            buildings_created += 1
                            all_buildings.append(building)
                            # Stocker la référence au bloc parent
                            building["parent_block_sides"] = zone['sides']
                            building["parent_block_center"] = (zone['x'], zone['y'])
                            
                    except Exception as building_error:
                        print(f"⚠️ Erreur création bâtiment {b}: {building_error}")
                        continue  # Passer au bâtiment suivant
        
        # Créer un réseau de routes organiques connectant les blocs
        roads_created = 0
        print(f"🛣️ Génération de routes organiques entre {len(block_zones)} blocs...")
        
        # Utiliser le nouveau système de routes organiques qui épousent les blocs
        organic_roads_count = generate_organic_road_network(
            block_zones, road_width, road_mat, road_curve_intensity
        )
        roads_created += organic_roads_count
        
        # Ajouter quelques routes principales droites pour connecter le tout
        block_size = 8.0
        main_roads_created = 0
        
        # Routes principales verticales (réduites)
        for i in range(0, width + 1, 2):  # Une route sur deux seulement
            start_y = -length/2 * block_size
            end_y = length/2 * block_size
            road_x = (i - width/2) * block_size - block_size/2
            
            road = generate_road(road_x, (start_y + end_y)/2, road_width, abs(end_y - start_y), road_mat, is_horizontal=False)
            if road:
                main_roads_created += 1
        
        # Routes principales horizontales (réduites)
        for j in range(0, length + 1, 2):  # Une route sur deux seulement
            start_x = -width/2 * block_size
            end_x = width/2 * block_size
            road_y = (j - length/2) * block_size - block_size/2
            
            road = generate_road((start_x + end_x)/2, road_y, abs(end_x - start_x), road_width, road_mat, is_horizontal=True)
            if road:
                main_roads_created += 1
        
        roads_created += main_roads_created
        
        # === APPLIQUER LES EFFETS FINAUX DE RÉALISME (VERSION SÉCURISÉE) ===
        print(f"🎨 Application des effets de réalisme urbain...")
        
        # Ajouter le mobilier urbain (version sécurisée)
        try:
            if street_life:
                add_street_furniture(block_zones, street_life)
            else:
                print(f"⏩ Mobilier urbain désactivé")
        except Exception as furniture_error:
            print(f"⚠️ Erreur mobilier urbain: {furniture_error}")
        
        # Appliquer le vieillissement aux bâtiments (version sécurisée)
        try:
            if weathering > 0 and all_buildings:
                apply_building_aging(all_buildings, weathering)
            else:
                print(f"⏩ Vieillissement désactivé ou pas de bâtiments")
        except Exception as aging_error:
            print(f"⚠️ Erreur vieillissement: {aging_error}")
        
        # Statistiques finales avec réalisme (version sécurisée)
        try:
            landmarks_count = len([b for b in all_buildings if b and 'Landmark_' in b.name])
            plazas_count = len([obj for obj in bpy.context.scene.objects if 'Plaza_' in obj.name])
            furniture_count = len([obj for obj in bpy.context.scene.objects if any(furniture in obj.name for furniture in ['Lamppost_', 'Bench_', 'TrashBin_', 'Sign_'])])
        except Exception as stats_error:
            print(f"⚠️ Erreur calcul statistiques: {stats_error}")
            landmarks_count = 0
            plazas_count = 0 
            furniture_count = 0
        
        print(f"✅ Ville organique réaliste créée:")
        print(f"   📐 {blocks_created} blocs polygonaux")
        print(f"   🏢 {buildings_created} bâtiments (dont {landmarks_count} monuments)")
        print(f"   🛣️ {roads_created} segments de routes organiques")
        print(f"   🌳 {plazas_count} places publiques")
        print(f"   🪑 {furniture_count} éléments de mobilier urbain")
        print(f"   🎨 Densité variable, vieillissement, zones mixtes appliqués")
        
        return True
        
    except Exception as e:
        print(f"❌ Erreur génération layout organique: {e}")
        import traceback
        print(f"Traceback: {traceback.format_exc()}")
        return False

# =============================================
# FONCTIONS DE RÉALISME URBAIN
# =============================================

def generate_realistic_city_density(zones, density_variation):
    """Calcule des densités réalistes pour chaque zone selon les patterns urbains"""
    import random
    import math
    
    if not zones:
        return zones
    
    try:
        # Trouver le centre approximatif de la ville
        center_x = sum(zone['x'] for zone in zones) / len(zones)
        center_y = sum(zone['y'] for zone in zones) / len(zones)
        
        for zone in zones:
            # Distance au centre
            distance_to_center = math.sqrt((zone['x'] - center_x)**2 + (zone['y'] - center_y)**2)
            max_distance = max(abs(zone['x'] - center_x), abs(zone['y'] - center_y)) + 1
            
            # Densité de base selon la distance (centre plus dense)
            normalized_distance = distance_to_center / max_distance if max_distance > 0 else 0
            base_density = 1.0 - (normalized_distance * 0.6)  # Centre à 100%, périphérie à 40%
            
            # Ajouter variation aléatoire
            variation = random.uniform(-density_variation, density_variation)
            final_density = max(0.1, min(1.0, base_density + variation))
            
            zone['density'] = final_density
            
            # Calculer le nombre de bâtiments selon la densité
            base_buildings = zone.get('buildings_count', 1)
            zone['buildings_count'] = max(1, int(base_buildings * final_density))
            
        print(f"✅ Densités réalistes calculées pour {len(zones)} zones")
        return zones
        
    except Exception as e:
        print(f"Erreur calcul densité réaliste: {e}")
        return zones

def create_landmark_building(x, y, size_multiplier, mat, variety='LANDMARK'):
    """Crée un bâtiment remarquable (version sécurisée)"""
    import random
    
    try:
        # Version simplifiée et sécurisée - utilise les fonctions existantes
        base_size = 4.0 * size_multiplier
        
        # Choisir un type de bâtiment spécial
        landmark_varieties = ['TOWER', 'COMPLEX', 'T_SHAPED', 'U_SHAPED', 'ELLIPTICAL']
        selected_variety = random.choice(landmark_varieties)
        
        # Dimensions plus grandes pour un monument
        width = base_size * random.uniform(1.2, 2.0)
        depth = width * random.uniform(0.8, 1.2)
        height = base_size * random.uniform(2, 4)  # Plus haut
        
        # Utiliser la fonction generate_building existante
        building = generate_building(x, y, width, depth, height, mat, building_variety=selected_variety)
        
        if building:
            building.name = f"Landmark_{selected_variety}_{x:.1f}_{y:.1f}"
            print(f"🏛️ Monument {selected_variety} créé en ({x:.1f}, {y:.1f})")
            
        return building
        
    except Exception as e:
        print(f"Erreur création monument (fallback standard): {e}")
        # Fallback - créer un bâtiment normal mais plus grand
        try:
            width = 6.0
            depth = 6.0
            height = 12.0
            return generate_building(x, y, width, depth, height, mat, building_variety='TOWER')
        except Exception as fallback_error:
            print(f"Erreur fallback monument: {fallback_error}")
            return None

def create_public_plaza(x, y, size, plaza_mat, tree_mat=None):
    """Crée une place publique avec verdure (version sécurisée)"""
    import random
    
    try:
        # Créer la place (surface plate) - version simplifiée
        bpy.ops.mesh.primitive_cube_add(
            size=size,
            location=(x, y, 0.0)  # Au niveau du sol
        )
        
        plaza = bpy.context.object
        if not plaza:
            return None
        
        # Aplatir pour faire une place
        plaza.scale = (1, 1, 0.05)
        bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
        
        # Matériau et nom
        plaza.name = f"Plaza_{x:.1f}_{y:.1f}"
        if plaza_mat and plaza.data:
            plaza.data.materials.clear()
            plaza.data.materials.append(plaza_mat)
        
        # Ajouter quelques arbres/végétation de façon simplifiée
        if tree_mat:
            try:
                tree_count = random.randint(1, 3)  # Moins d'arbres pour éviter les erreurs
                for i in range(tree_count):
                    # Position aléatoire dans la place
                    tree_x = x + random.uniform(-size/4, size/4)  # Zone plus petite
                    tree_y = y + random.uniform(-size/4, size/4)
                    
                    # Créer un "arbre" simple (sphère verte)
                    bpy.ops.mesh.primitive_uv_sphere_add(
                        radius=1.0,
                        location=(tree_x, tree_y, 1.0)
                    )
                    tree = bpy.context.object
                    if tree:
                        tree.name = f"Tree_{i}_{x:.1f}_{y:.1f}"
                        if tree_mat and tree.data:
                            tree.data.materials.clear()
                            tree.data.materials.append(tree_mat)
            except Exception as tree_error:
                print(f"⚠️ Erreur création arbres: {tree_error}")
        
        print(f"🌳 Place publique créée en ({x:.1f}, {y:.1f})")
        return plaza
        
    except Exception as e:
        print(f"Erreur création place publique: {e}")
        return None

def add_street_furniture(zones, street_life_enabled):
    """Ajoute des éléments de mobilier urbain (lampadaires, bancs, etc.)"""
    import random
    
    if not street_life_enabled:
        return
        
    try:
        furniture_count = 0
        
        for zone in zones:
            # Densité de mobilier selon la densité de la zone
            density = zone.get('density', 0.5)
            furniture_per_zone = int(density * random.randint(2, 6))
            
            for i in range(furniture_per_zone):
                # Position aléatoire près des bords de la zone
                edge_offset = min(zone['width'], zone['depth']) * 0.4
                furniture_x = zone['x'] + random.uniform(-edge_offset, edge_offset)
                furniture_y = zone['y'] + random.uniform(-edge_offset, edge_offset)
                
                # Types de mobilier
                furniture_type = random.choice(['LAMPPOST', 'BENCH', 'TRASH_BIN', 'SIGN'])
                
                if furniture_type == 'LAMPPOST':
                    # Lampadaire
                    bpy.ops.mesh.primitive_cylinder_add(
                        radius=0.1,
                        depth=3.5,
                        location=(furniture_x, furniture_y, 1.75)
                    )
                    obj = bpy.context.object
                    if obj:
                        obj.name = f"Lamppost_{furniture_x:.1f}_{furniture_y:.1f}"
                        
                elif furniture_type == 'BENCH':
                    # Banc
                    bpy.ops.mesh.primitive_cube_add(
                        size=2.0,
                        location=(furniture_x, furniture_y, 0.4)
                    )
                    obj = bpy.context.object
                    if obj:
                        obj.scale = (1, 0.3, 0.2)
                        bpy.ops.object.transform_apply(scale=True)
                        obj.name = f"Bench_{furniture_x:.1f}_{furniture_y:.1f}"
                        
                elif furniture_type == 'TRASH_BIN':
                    # Poubelle
                    bpy.ops.mesh.primitive_cylinder_add(
                        radius=0.3,
                        depth=0.8,
                        location=(furniture_x, furniture_y, 0.4)
                    )
                    obj = bpy.context.object
                    if obj:
                        obj.name = f"TrashBin_{furniture_x:.1f}_{furniture_y:.1f}"
                        
                else:  # SIGN
                    # Panneau
                    bpy.ops.mesh.primitive_cube_add(
                        size=1.0,
                        location=(furniture_x, furniture_y, 1.5)
                    )
                    obj = bpy.context.object
                    if obj:
                        obj.scale = (0.1, 1, 0.6)
                        bpy.ops.object.transform_apply(scale=True)
                        obj.name = f"Sign_{furniture_x:.1f}_{furniture_y:.1f}"
                
                furniture_count += 1
        
        print(f"🪑 {furniture_count} éléments de mobilier urbain ajoutés")
        
    except Exception as e:
        print(f"Erreur ajout mobilier urbain: {e}")

def apply_building_aging(buildings, weathering_factor):
    """Applique des effets de vieillissement aux bâtiments"""
    import random
    
    if weathering_factor <= 0:
        return
        
    try:
        aged_count = 0
        
        for building in buildings:
            if not building or random.random() > weathering_factor:
                continue
                
            # Variation de hauteur pour simuler l'usure
            age_factor = random.uniform(0.85, 0.98)
            if hasattr(building, 'scale'):
                building.scale.z *= age_factor
                bpy.context.view_layer.objects.active = building
                bpy.ops.object.transform_apply(scale=True)
                
            # Légère rotation aléatoire pour les vieux bâtiments
            if random.random() < 0.3:  # 30% des bâtiments vieillis
                small_rotation = random.uniform(-0.02, 0.02)  # Très petit angle
                building.rotation_euler.z += small_rotation
                
            aged_count += 1
        
        print(f"🏚️ {aged_count} bâtiments vieillis (facteur: {weathering_factor:.2f})")
        
    except Exception as e:
        print(f"Erreur vieillissement bâtiments: {e}")

# =============================================
# NOUVEAU GÉNÉRATEUR : ROUTES D'ABORD
# =============================================

def generate_road_network_first(context):
    """Nouvelle approche : générer d'abord le réseau de routes, puis remplir les espaces"""
    print("🔥🔥🔥 V6.13.0 FONCTION ANTI-CRASH APPELÉE ! 🔥🔥🔥")
    
    try:
        print("✅ V6.13.0 Étape 1/10: Récupération contexte...")
        scene = context.scene
        
        print("✅ V6.13.0 Étape 2/10: Récupération paramètres...")
        # Récupérer les paramètres avec protection
        width = safe_int(getattr(scene, 'citygen_width', 3), 3)  # 3x3 plus sûr
        length = safe_int(getattr(scene, 'citygen_length', 3), 3)
        road_width = getattr(scene, 'citygen_road_width', 2.0)  # Plus petit
        
        print("✅ V6.13.0 Étape 3/10: Paramètres organiques...")
        # Paramètres organiques
        organic_mode = getattr(scene, 'citygen_organic_mode', False)
        road_curve_intensity = getattr(scene, 'citygen_road_curve_intensity', 0.2)  # Plus faible
        
        print(f"🛣️ V6.13.0 SYSTÈME SÉCURISÉ: Génération routes d'abord ({width}x{length})")
        
        print("✅ V6.13.0 Étape 4/10: Création matériaux...")
        # Créer les matériaux avec protection
        try:
            road_mat = create_material("RoadMat_First", (0.3, 0.3, 0.3))
            block_mat = create_material("BlockMat_First", (0.7, 0.7, 0.7))
            build_mat = create_material("BuildingMat_First", (0.8, 0.6, 0.4))
            print("✅ V6.13.0 Matériaux créés avec succès")
        except Exception as e:
            print(f"❌ V6.13.0 Erreur matériaux: {e}")
            return False
        
        # ÉTAPE 1: Créer le réseau de routes
        print(f"✅ V6.13.0 Étape 5/10: Début création routes...")
        try:
            road_network = create_primary_road_network_rf(width, length, road_width, road_mat, organic_mode, road_curve_intensity)
            print(f"✅ V6.13.0 Étape 6/10: {len(road_network)} routes créées - CONTINUONS...")
        except Exception as e:
            print(f"❌ V6.13.0 CRASH dans création routes: {e}")
            import traceback
            print(f"🔥 TRACEBACK ROUTES: {traceback.format_exc()}")
            return False
        
        # ÉTAPE 2: Identifier les zones entre les routes
        print(f"�🔥🔥 V6.12.8 ÉTAPE 2 DÉBUT: IDENTIFICATION ZONES ===")
        try:
            print(f"   🔥 Appel identify_block_zones_from_roads_rf...")
            block_zones = identify_block_zones_from_roads_rf(road_network, width, length, road_width)
            print(f"🔥🔥� V6.12.8 ZONES IDENTIFIÉES: {len(block_zones)} ===")
        except Exception as e:
            print(f"❌ ERREUR identification zones: {e}")
            import traceback
            print(f"Traceback zones: {traceback.format_exc()}")
            block_zones = []
        
        # ÉTAPE 3: Créer les blocs dans ces zones
        print(f"🏗️ === DÉBUT CRÉATION BLOCS ===")
        try:
            blocks_created = create_blocks_in_zones_rf(block_zones, block_mat)
            print(f"🏗️ === BLOCS CRÉÉS: {blocks_created} ===")
        except Exception as e:
            print(f"❌ ERREUR création blocs: {e}")
            blocks_created = 0
        
        # ÉTAPE 4: Ajouter les bâtiments dans les blocs
        print(f"🏢 === DÉBUT CRÉATION BÂTIMENTS ===")
        try:
            buildings_created = add_buildings_to_blocks_rf(block_zones, build_mat, scene)
            print(f"🏢 === BÂTIMENTS CRÉÉS: {buildings_created} ===")
        except Exception as e:
            print(f"❌ ERREUR création bâtiments: {e}")
            buildings_created = 0
        
        print(f"✅ Système routes-first complété:")
        print(f"   🛣️ {len(road_network)} segments de routes")
        print(f"   📐 {len(block_zones)} zones de blocs identifiées") 
        print(f"   🏗️ {blocks_created} blocs créés")
        print(f"   🏢 {buildings_created} bâtiments générés")
        
        print(f"🔥 V6.12.8 SUCCÈS COMPLET - TOUTES ÉTAPES TERMINÉES !")
        return True
        
    except Exception as e:
        print(f"❌ CRASH V6.12.8 génération routes-first: {e}")
        import traceback
        print(f"🔥 TRACEBACK COMPLET V6.12.8:")
        print(f"{traceback.format_exc()}")
        return False

def create_primary_road_network_rf(width, length, road_width, road_mat, organic_mode, curve_intensity):
    """Crée le réseau principal de routes"""
    road_network = []
    block_size = 12.0  # Taille d'un bloc avec sa route
    
    try:
        print(f"🛣️ Création réseau de routes principal...")
        
        # FORCER TOUJOURS LE SYSTÈME ULTRA-ORGANIQUE pour résultats satisfaisants
        print(f"� ACTIVATION FORCÉE du système ULTRA-ORGANIQUE (intensité: {curve_intensity})")
        road_network = create_smart_organic_road_grid_rf(width, length, block_size, road_width, road_mat, curve_intensity)
        
        print(f"✅ {len(road_network)} segments de routes créés")
        return road_network
        
    except Exception as e:
        print(f"Erreur création réseau routes: {e}")
        return []

def create_smart_organic_road_grid_rf(width, length, block_size, road_width, road_mat, curve_intensity):
    """Système hybride intelligent AMÉLIORÉ - courbes réelles + diagonales"""
    road_network = []
    import math
    import random
    import bmesh
    
    try:
        print(f"🧠🌊 === SYSTÈME ULTRA-HYBRIDE AMÉLIORÉ ===")
        print(f"   🎯 Grille urbaine + VRAIES courbes + diagonales organiques")
        print(f"   📊 Paramètres: {width}x{length}, intensité={curve_intensity}")
        
        # Intensité adaptative - plus d'intensité si demandée
        if curve_intensity > 0.6:
            smart_intensity = min(0.4, curve_intensity)  # Plus de courbes
            print(f"   🌊 Mode ULTRA-ORGANIQUE activé (intensité: {smart_intensity})")
        else:
            smart_intensity = min(0.15, curve_intensity * 0.5)  # Mode subtil
            
        variation_range = block_size * smart_intensity
        print(f"   🌿 Variation range: ±{variation_range:.1f}m")
        
        # === ROUTES PRINCIPALES COURBES ===
        # Routes verticales avec VRAIES courbes (using bmesh)
        for i in range(width + 1):
            base_x = (i - width/2) * block_size
            
            if curve_intensity > 0.6:
                # VRAIES COURBES avec bmesh
                mesh = bpy.data.meshes.new(f"CurvedRoad_V_{i}")
                obj = bpy.data.objects.new(f"CurvedRoad_V_{i}", mesh)
                bpy.context.collection.objects.link(obj)
                
                bm = bmesh.new()
                
                # Créer courbe avec points multiples (réduit pour performance)
                points = []
                num_points = min(12, 21)  # Réduction de 21 à 12 points max pour performance
                for p in range(num_points):
                    t = p / (num_points - 1.0)
                    y = (t - 0.5) * length * block_size
                    
                    # Courbe organique intelligente (optimisée)
                    curve1 = math.sin(t * 2 * math.pi + i * 0.5) * variation_range * 0.8
                    curve2 = math.sin(t * 4 * math.pi + i * 0.3) * variation_range * 0.3
                    
                    final_x = base_x + curve1 + curve2
                    points.append((final_x, y, 0.05))
                
                # Créer géométrie courbe
                for j, (x, y, z) in enumerate(points):
                    v = bm.verts.new((x, y, z))
                    if j > 0:
                        bm.edges.new([prev_v, v])
                    prev_v = v
                
                # Appliquer et matériau
                bm.to_mesh(mesh)
                bm.free()
                
                # Matériau courbe
                mat = create_material(f"CurvedMat_V_{i}", (0.2 + i*0.1, 0.4, 0.6))
                if obj.data:
                    obj.data.materials.append(mat)
                    
                road_network.append({'object': obj, 'type': 'curved_vertical', 'x': base_x})
                
            else:
                # Mode subtil comme avant
                center_factor = 1.0 - abs(i - width/2) / (width/2 + 1)
                organic_var = (
                    math.sin(i * 0.7 + 0.3) * variation_range * center_factor * 0.6 +
                    random.uniform(-variation_range, variation_range) * 0.3
                )
                
                final_x = base_x + organic_var
                
                bpy.ops.mesh.primitive_cube_add(size=2.0, location=(final_x, 0, 0.05))
                road = bpy.context.object
                if road:
                    width_var = 1.0 + random.uniform(-0.1, 0.1)
                    road.scale = (road_width/2 * width_var, length * block_size/2, 0.05)
                    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
                    
                    road.rotation_euler[2] = organic_var / block_size * 0.05
                    road.name = f"SmartRoad_V_{i}"
                    
                    mat = create_material(f"SmartMat_V_{i}", (0.3 + (i % 3) * 0.05, 0.3, 0.4))
                    if road.data:
                        road.data.materials.clear()
                        road.data.materials.append(mat)
                    
                    road_network.append({'object': road, 'type': 'vertical', 'x': final_x})
        
        # Routes horizontales (même logique)
        for j in range(length + 1):
            base_y = (j - length/2) * block_size
            
            if curve_intensity > 0.6:
                # VRAIES COURBES horizontales
                mesh = bpy.data.meshes.new(f"CurvedRoad_H_{j}")
                obj = bpy.data.objects.new(f"CurvedRoad_H_{j}", mesh)
                bpy.context.collection.objects.link(obj)
                
                bm = bmesh.new()
                points = []
                num_points = min(12, 21)  # Réduction pour performance
                for p in range(num_points):
                    t = p / (num_points - 1.0)
                    x = (t - 0.5) * width * block_size
                    
                    curve1 = math.sin(t * 2.5 * math.pi + j * 0.7) * variation_range * 0.7
                    curve2 = math.sin(t * 3.5 * math.pi + j * 0.4) * variation_range * 0.4
                    
                    final_y = base_y + curve1 + curve2
                    points.append((x, final_y, 0.05))
                
                for k, (x, y, z) in enumerate(points):
                    v = bm.verts.new((x, y, z))
                    if k > 0:
                        bm.edges.new([prev_v, v])
                    prev_v = v
                
                bm.to_mesh(mesh)
                bm.free()
                
                mat = create_material(f"CurvedMat_H_{j}", (0.6, 0.3 + j*0.1, 0.2))
                if obj.data:
                    obj.data.materials.append(mat)
                    
                road_network.append({'object': obj, 'type': 'curved_horizontal', 'y': base_y})
                
            else:
                # Mode subtil
                center_factor = 1.0 - abs(j - length/2) / (length/2 + 1)
                organic_var = (
                    math.sin(j * 0.8 + 0.7) * variation_range * center_factor * 0.5 +
                    random.uniform(-variation_range, variation_range) * 0.4
                )
                
                final_y = base_y + organic_var
                
                bpy.ops.mesh.primitive_cube_add(size=2.0, location=(0, final_y, 0.05))
                road = bpy.context.object
                if road:
                    width_var = 1.0 + random.uniform(-0.08, 0.08)
                    road.scale = (width * block_size/2, road_width/2 * width_var, 0.05)
                    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
                    
                    road.rotation_euler[2] = organic_var / block_size * 0.04
                    road.name = f"SmartRoad_H_{j}"
                    
                    mat = create_material(f"SmartMat_H_{j}", (0.5, 0.4 + (j % 4) * 0.04, 0.3))
                    if road.data:
                        road.data.materials.clear()
                        road.data.materials.append(mat)
                    
                    road_network.append({'object': road, 'type': 'horizontal', 'y': final_y})
        
        # === ROUTES DIAGONALES ORGANIQUES (si intensité élevée) ===
        if curve_intensity > 0.7 and width >= 4 and length >= 4:
            print(f"   🔀 Ajout de routes diagonales organiques...")
            
            # Diagonale principale
            mesh = bpy.data.meshes.new(f"DiagonalRoad_Main")
            obj = bpy.data.objects.new(f"DiagonalRoad_Main", mesh)
            bpy.context.collection.objects.link(obj)
            
            bm = bmesh.new()
            points = []
            for p in range(15):
                t = p / 14.0
                base_x = (t - 0.5) * width * block_size * 0.7
                base_y = (t - 0.5) * length * block_size * 0.7
                
                # Courbes diagonales
                diag_curve = math.sin(t * 3 * math.pi) * variation_range * 0.6
                
                final_x = base_x + diag_curve * 0.5
                final_y = base_y + diag_curve * 0.8
                points.append((final_x, final_y, 0.05))
            
            for k, (x, y, z) in enumerate(points):
                v = bm.verts.new((x, y, z))
                if k > 0:
                    bm.edges.new([prev_v, v])
                prev_v = v
            
            bm.to_mesh(mesh)
            bm.free()
            
            mat = create_material(f"DiagonalMat", (0.8, 0.6, 0.3))
            if obj.data:
                obj.data.materials.append(mat)
                
            road_network.append({'object': obj, 'type': 'diagonal'})
        
        print(f"✅ {len(road_network)} routes ULTRA-hybrides créées")
        if curve_intensity > 0.6:
            print(f"   🌊 VRAIES courbes avec bmesh générées")
        if curve_intensity > 0.7:
            print(f"   🔀 Routes diagonales organiques ajoutées")
        print(f"   🧠 Système adaptatif selon l'intensité demandée")
        
        return road_network
        
    except Exception as e:
        print(f"❌ Erreur routes ULTRA-hybrides: {e}")
        import traceback
        print(f"Traceback: {traceback.format_exc()}")
        return []

def create_realistic_organic_road_grid_rf(width, length, block_size, road_width, road_mat, curve_intensity):
    """Crée une grille organique RÉALISTE - garde la logique urbaine avec légères courbes"""
    road_network = []
    import math
    
    try:
        print(f"🌿 === GÉNÉRATION ROUTES ORGANIQUES RÉALISTES ===")
        print(f"   Paramètres: {width}x{length}, intensité={curve_intensity}")
        print(f"   🎯 Objectif: Routes urbaines avec légères courbes naturelles")
        
        # Intensité modérée pour garder l'aspect urbain
        curve_intensity = min(0.3, curve_intensity)  # Maximum 30% de courbure
        
        # Routes verticales avec légères courbes
        for i in range(width + 1):
            base_x = (i - width/2) * block_size
            
            # Léger décalage organique (pas chaotique)
            organic_offset = math.sin(i * 0.8) * curve_intensity * block_size * 0.5
            final_x = base_x + organic_offset
            
            # Créer route verticale légèrement courbe
            bpy.ops.mesh.primitive_cube_add(
                size=2.0,
                location=(final_x, 0, 0.05)
            )
            road = bpy.context.object
            if road:
                road.scale = (road_width/2, length * block_size/2, 0.05)
                bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
                road.name = f"OrganicRoad_V_{i}"
                
                # Rotation légère pour l'aspect organique
                road.rotation_euler[2] = math.sin(i * 0.5) * curve_intensity * 0.1
                
                # Matériau avec couleur variable
                color_var = 0.7 + (i % 3) * 0.1  # Variation subtile
                org_mat = create_material(f"OrganicMat_V_{i}", (color_var, 0.2, 0.1))
                if road.data:
                    road.data.materials.clear()
                    road.data.materials.append(org_mat)
                
                road_network.append({
                    'object': road,
                    'type': 'vertical',
                    'x': final_x
                })
        
        # Routes horizontales avec légères courbes  
        for j in range(length + 1):
            base_y = (j - length/2) * block_size
            
            # Léger décalage organique
            organic_offset = math.sin(j * 0.6) * curve_intensity * block_size * 0.4
            final_y = base_y + organic_offset
            
            # Créer route horizontale légèrement courbe
            bpy.ops.mesh.primitive_cube_add(
                size=2.0,
                location=(0, final_y, 0.05)
            )
            road = bpy.context.object
            if road:
                road.scale = (width * block_size/2, road_width/2, 0.05)
                bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
                road.name = f"OrganicRoad_H_{j}"
                
                # Rotation légère
                road.rotation_euler[2] = math.sin(j * 0.7) * curve_intensity * 0.08
                
                # Matériau avec couleur variable
                color_var = 0.5 + (j % 4) * 0.1
                org_mat = create_material(f"OrganicMat_H_{j}", (0.2, color_var, 0.1))
                if road.data:
                    road.data.materials.clear()
                    road.data.materials.append(org_mat)
                
                road_network.append({
                    'object': road,
                    'type': 'horizontal', 
                    'y': final_y
                })
        
        print(f"✅ {len(road_network)} routes organiques réalistes créées")
        print(f"   🌿 Courbes légères préservant la logique urbaine")
        return road_network
        
    except Exception as e:
        print(f"❌ Erreur routes organiques réalistes: {e}")
        return []

def create_rectangular_road_grid_rf(width, length, block_size, road_width, road_mat):
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

def create_highway_road(x, y, direction, width, length, road_mat, index):
    """Crée une autoroute large et droite"""
    import math
    try:
        bpy.ops.mesh.primitive_cube_add(size=2.0, location=(x, y, 0.05))
        road = bpy.context.object
        if road:
            if direction == 'vertical':
                road.scale = (width/2, length/2, 0.05)
            else:
                road.scale = (length/2, width/2, 0.05)
            
            bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
            road.name = f"Highway_{direction}_{index}"
            
            # Matériau autoroute plus sombre
            highway_mat = create_material(f"HighwayMat_{index}", (0.15, 0.15, 0.15))
            if road.data:
                road.data.materials.clear()
                road.data.materials.append(highway_mat)
            
            return {
                'object': road,
                'type': direction,
                'road_type': 'highway',
                'x': x,
                'y': y,
                'width': width if direction == 'vertical' else length,
                'length': length if direction == 'vertical' else width
            }
    except Exception as e:
        print(f"Erreur création autoroute: {e}")
        return None

def create_sinusoidal_road(x, y, direction, width, length, road_mat, curve_intensity, index):
    """Crée une route avec des courbes sinusoïdales organiques"""
    import math
    try:
        # Créer plusieurs segments pour faire une courbe
        segments = []
        num_segments = max(5, int(length / 20))  # Plus de segments = plus fluide
        
        for i in range(num_segments):
            segment_length = length / num_segments
            
            if direction == 'vertical':
                segment_y = y + (i - num_segments/2) * segment_length
                # Courbe sinusoïdale
                curve_offset = math.sin(i * 0.8) * curve_intensity * 3
                segment_x = x + curve_offset
                
                bpy.ops.mesh.primitive_cube_add(size=2.0, location=(segment_x, segment_y, 0.05))
                segment = bpy.context.object
                if segment:
                    segment.scale = (width/2, segment_length/2, 0.05)
                    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
                    segment.name = f"Avenue_Sin_V_{index}_{i}"
                    
                    # Matériau avenue
                    avenue_mat = create_material(f"AvenueMat_{index}_{i}", (0.25, 0.25, 0.25))
                    if segment.data:
                        segment.data.materials.clear()
                        segment.data.materials.append(avenue_mat)
                    
                    segments.append({
                        'object': segment,
                        'type': 'vertical',
                        'road_type': 'avenue',
                        'x': segment_x,
                        'y': segment_y,
                        'width': width,
                        'length': segment_length
                    })
            else:  # horizontal
                segment_x = x + (i - num_segments/2) * segment_length
                curve_offset = math.sin(i * 0.8) * curve_intensity * 3
                segment_y = y + curve_offset
                
                bpy.ops.mesh.primitive_cube_add(size=2.0, location=(segment_x, segment_y, 0.05))
                segment = bpy.context.object
                if segment:
                    segment.scale = (segment_length/2, width/2, 0.05)
                    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
                    segment.name = f"Avenue_Sin_H_{index}_{i}"
                    
                    avenue_mat = create_material(f"AvenueMat_{index}_{i}", (0.25, 0.25, 0.25))
                    if segment.data:
                        segment.data.materials.clear()
                        segment.data.materials.append(avenue_mat)
                    
                    segments.append({
                        'object': segment,
                        'type': 'horizontal',
                        'road_type': 'avenue',
                        'x': segment_x,
                        'y': segment_y,
                        'width': segment_length,
                        'length': width
                    })
        
        # Retourner le premier segment comme représentant
        return segments[0] if segments else None
        
    except Exception as e:
        print(f"Erreur route sinusoïdale: {e}")
        return None

def create_broken_road(start_x, start_y, end_x, end_y, direction, width, road_mat, index):
    """Crée une route brisée avec plusieurs segments"""
    import math
    try:
        # Points de brisure aléatoires
        num_breaks = random.randint(2, 4)
        points = [(start_x, start_y)]
        
        for i in range(1, num_breaks):
            if direction == 'vertical':
                break_y = start_y + (end_y - start_y) * (i / num_breaks)
                break_x = start_x + random.uniform(-3, 3)
                points.append((break_x, break_y))
            else:
                break_x = start_x + (end_x - start_x) * (i / num_breaks)
                break_y = start_y + random.uniform(-3, 3)
                points.append((break_x, break_y))
        
        points.append((end_x, end_y))
        
        # Créer des segments entre les points
        for i in range(len(points) - 1):
            p1, p2 = points[i], points[i + 1]
            segment_x = (p1[0] + p2[0]) / 2
            segment_y = (p1[1] + p2[1]) / 2
            
            segment_length = math.sqrt((p2[0] - p1[0])**2 + (p2[1] - p1[1])**2)
            
            bpy.ops.mesh.primitive_cube_add(size=2.0, location=(segment_x, segment_y, 0.05))
            segment = bpy.context.object
            if segment:
                if direction == 'vertical':
                    segment.scale = (width/2, segment_length/2, 0.05)
                else:
                    segment.scale = (segment_length/2, width/2, 0.05)
                
                # Rotation pour aligner avec la direction
                angle = math.atan2(p2[1] - p1[1], p2[0] - p1[0])
                if direction == 'vertical':
                    segment.rotation_euler[2] = angle
                
                bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
                segment.name = f"Street_Broken_{direction}_{index}_{i}"
                
                street_mat = create_material(f"StreetMat_{index}_{i}", (0.35, 0.35, 0.35))
                if segment.data:
                    segment.data.materials.clear()
                    segment.data.materials.append(street_mat)
        
        # Retourner une info basique
        return {
            'object': None,  # Segments multiples
            'type': direction,
            'road_type': 'street',
            'x': segment_x,
            'y': segment_y,
            'width': width,
            'length': segment_length
        }
        
    except Exception as e:
        print(f"Erreur route brisée: {e}")
        return None

def create_serpentine_lane(start_x, start_y, direction, width, road_mat, curve_intensity, index):
    """Crée une ruelle qui serpente de manière organique"""
    import math
    try:
        current_x, current_y = start_x, start_y
        segments = []
        
        for i in range(random.randint(3, 6)):  # 3-6 segments de ruelle
            # Avancer dans la direction avec déviation
            if direction in ['north', 'south']:
                step = 15 if direction == 'north' else -15
                next_y = current_y + step
                next_x = current_x + random.uniform(-8, 8) * curve_intensity
            elif direction in ['east', 'west']:
                step = 15 if direction == 'east' else -15
                next_x = current_x + step
                next_y = current_y + random.uniform(-8, 8) * curve_intensity
            else:  # diagonal
                next_x = current_x + random.uniform(-10, 10)
                next_y = current_y + random.uniform(-10, 10)
            
            # Créer le segment
            segment_x = (current_x + next_x) / 2
            segment_y = (current_y + next_y) / 2
            segment_length = math.sqrt((next_x - current_x)**2 + (next_y - current_y)**2)
            
            bpy.ops.mesh.primitive_cube_add(size=2.0, location=(segment_x, segment_y, 0.05))
            segment = bpy.context.object
            if segment:
                segment.scale = (width/2, segment_length/2, 0.05)
                
                # Rotation pour suivre la direction
                angle = math.atan2(next_y - current_y, next_x - current_x)
                segment.rotation_euler[2] = angle
                
                bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
                segment.name = f"Lane_Serpent_{index}_{i}"
                
                lane_mat = create_material(f"LaneMat_{index}_{i}", (0.45, 0.45, 0.45))
                if segment.data:
                    segment.data.materials.clear()
                    segment.data.materials.append(lane_mat)
                
                segments.append(segment)
            
            current_x, current_y = next_x, next_y
        
        return {
            'object': segments[0] if segments else None,
            'type': 'serpentine',
            'road_type': 'lane',
            'x': start_x,
            'y': start_y,
            'width': width,
            'length': 10
        }
        
    except Exception as e:
        print(f"Erreur ruelle serpentante: {e}")
        return None

def create_diagonal_curved_road(start_x, start_y, end_x, end_y, width, road_mat, curve_intensity, index):
    """Crée une route diagonale avec courbe"""
    import math
    try:
        # Point de contrôle pour la courbe
        mid_x = (start_x + end_x) / 2 + random.uniform(-5, 5) * curve_intensity
        mid_y = (start_y + end_y) / 2 + random.uniform(-5, 5) * curve_intensity
        
        # Créer plusieurs segments pour la courbe
        num_segments = 5
        for i in range(num_segments):
            t = i / (num_segments - 1)
            
            # Courbe de Bézier quadratique
            x = (1-t)**2 * start_x + 2*(1-t)*t * mid_x + t**2 * end_x
            y = (1-t)**2 * start_y + 2*(1-t)*t * mid_y + t**2 * end_y
            
            bpy.ops.mesh.primitive_cube_add(size=2.0, location=(x, y, 0.05))
            segment = bpy.context.object
            if segment:
                segment_length = math.sqrt((end_x - start_x)**2 + (end_y - start_y)**2) / num_segments
                segment.scale = (width/2, segment_length/2, 0.05)
                
                # Rotation selon la direction locale
                if i < num_segments - 1:
                    t_next = (i + 1) / (num_segments - 1)
                    x_next = (1-t_next)**2 * start_x + 2*(1-t_next)*t_next * mid_x + t_next**2 * end_x
                    y_next = (1-t_next)**2 * start_y + 2*(1-t_next)*t_next * mid_y + t_next**2 * end_y
                    
                    angle = math.atan2(y_next - y, x_next - x)
                    segment.rotation_euler[2] = angle
                
                bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
                segment.name = f"Diagonal_Curved_{index}_{i}"
                
                diag_mat = create_material(f"DiagonalMat_{index}_{i}", (0.3, 0.3, 0.3))
                if segment.data:
                    segment.data.materials.clear()
                    segment.data.materials.append(diag_mat)
        
        return {
            'object': None,
            'type': 'diagonal',
            'road_type': 'diagonal',
            'x': mid_x,
            'y': mid_y,
            'width': width,
            'length': math.sqrt((end_x - start_x)**2 + (end_y - start_y)**2)
        }
        
    except Exception as e:
        print(f"Erreur route diagonale: {e}")
        return None

def create_cul_de_sac(center_x, center_y, width, road_mat, index):
    """Crée un cul-de-sac avec route d'accès"""
    try:
        cul_roads = []
        
        # Route d'accès (droite)
        access_length = random.uniform(20, 40)
        access_direction = random.choice(['north', 'south', 'east', 'west'])
        
        if access_direction == 'north':
            access_x, access_y = center_x, center_y - access_length/2
            road_scale = (width/2, access_length/2, 0.05)
        elif access_direction == 'south':
            access_x, access_y = center_x, center_y + access_length/2
            road_scale = (width/2, access_length/2, 0.05)
        elif access_direction == 'east':
            access_x, access_y = center_x - access_length/2, center_y
            road_scale = (access_length/2, width/2, 0.05)
        else:  # west
            access_x, access_y = center_x + access_length/2, center_y
            road_scale = (access_length/2, width/2, 0.05)
        
        # Route d'accès
        bpy.ops.mesh.primitive_cube_add(size=2.0, location=(access_x, access_y, 0.05))
        access_road = bpy.context.object
        if access_road:
            access_road.scale = road_scale
            bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
            access_road.name = f"CulDeSac_Access_{index}"
            
            access_mat = create_material(f"CulDeSacAccessMat_{index}", (0.4, 0.4, 0.4))
            if access_road.data:
                access_road.data.materials.clear()
                access_road.data.materials.append(access_mat)
            
            cul_roads.append({
                'object': access_road,
                'type': access_direction,
                'road_type': 'cul_de_sac_access',
                'x': access_x,
                'y': access_y,
                'width': width,
                'length': access_length
            })
        
        # Cercle du cul-de-sac
        bpy.ops.mesh.primitive_cylinder_add(radius=width*1.5, depth=0.1, location=(center_x, center_y, 0.05))
        circle = bpy.context.object
        if circle:
            circle.name = f"CulDeSac_Circle_{index}"
            
            circle_mat = create_material(f"CulDeSacCircleMat_{index}", (0.35, 0.35, 0.35))
            if circle.data:
                circle.data.materials.clear()
                circle.data.materials.append(circle_mat)
            
            cul_roads.append({
                'object': circle,
                'type': 'circle',
                'road_type': 'cul_de_sac_circle',
                'x': center_x,
                'y': center_y,
                'width': width*3,
                'length': width*3
            })
        
        return cul_roads
        
    except Exception as e:
        print(f"Erreur cul-de-sac: {e}")
        return []

def create_organic_road_grid_rf(width, length, block_size, road_width, road_mat, curve_intensity):
    """Crée une grille organique de routes - COURBES BLENDER NATIVES MEGA VISIBLES"""
    road_network = []
    import math
    
    try:
        print(f"🎯🔥 === COURBES BLENDER NATIVES MEGA VISIBLES === 🔥🎯")
        print(f"   Paramètres: width={width}, length={length}, block_size={block_size}")
        print(f"   road_width={road_width}, curve_intensity={curve_intensity}")
        
        # FORCER une intensité EXTREME pour garantir la visibilité
        curve_intensity = max(1.5, curve_intensity * 3)  # TRIPLER l'intensité !
        print(f"   🔥🔥🔥 COURBE INTENSITÉ EXTREME: {curve_intensity}")
        
        # === COURBES BLENDER NATIVES - 100% GARANTIES VISIBLES ===
        
        # Routes verticales - COURBES BLENDER NATIVES
        print(f"   🎯 Génération routes verticales COURBES BLENDER NATIVES...")
        for i in range(width + 1):
            base_x = (i - width/2) * block_size
            
            # Créer une courbe Bézier native Blender
            curve_data = bpy.data.curves.new(f"SuperCurve_V_{i}", type='CURVE')
            curve_data.dimensions = '3D'
            curve_data.fill_mode = 'BOTH'
            curve_data.bevel_depth = road_width / 2  # Largeur automatique
            curve_data.resolution_u = 64  # MEGA haute résolution
            curve_data.bevel_resolution = 16  # Résolution du biseau
            
            # Créer un spline Bézier
            spline = curve_data.splines.new('BEZIER')
            
            # Points de contrôle pour des courbes ENORMES et visibles
            total_length = length * block_size
            segments = 12  # Plus de segments = plus de courbes
            
            # Redimensionner le spline
            spline.bezier_points.add(segments)
            
            # Définir les points avec des courbes GIGANTESQUES
            for seg in range(segments + 1):
                t = seg / segments
                y = (t - 0.5) * total_length
                
                # COURBES GIGANTESQUES - IMPOSSIBLE DE LES RATER !
                curve_amplitude = curve_intensity * block_size * 1.2  # MEGA amplitude !
                
                # Courbes sinusoïdales EXTREMES multiples
                curve_offset = math.sin(t * 6 * math.pi + i * 1.2) * curve_amplitude
                curve_offset += math.sin(t * 3 * math.pi + i * 2.1) * curve_amplitude * 0.8
                curve_offset += math.sin(t * 9 * math.pi + i * 0.7) * curve_amplitude * 0.5
                
                # Variation random EXTREME
                curve_offset += random.uniform(-0.4, 0.4) * curve_amplitude
                
                final_x = base_x + curve_offset
                
                # Définir le point de contrôle
                point = spline.bezier_points[seg]
                point.co = (final_x, y, 0)
                
                # Handles pour des courbes naturelles
                point.handle_left_type = 'AUTO'
                point.handle_right_type = 'AUTO'
                
                if seg % 3 == 0:  # Debug
                    print(f"      Point {seg}: x={final_x:.1f} (offset={curve_offset:.1f})")
            
            # Créer l'objet courbe
            curve_obj = bpy.data.objects.new(f"SuperCurveRoad_V_{i}", curve_data)
            bpy.context.collection.objects.link(curve_obj)
            
            # Convertir en mesh pour les matériaux
            bpy.context.view_layer.objects.active = curve_obj
            curve_obj.select_set(True)
            bpy.ops.object.convert(target='MESH')
            
            # Matériau MEGA vif
            hue = (i % 6) / 6.0
            road_color = (1.0, 0.3 + hue * 0.7, 0.8 - hue * 0.3)  # Couleurs vives
            
            road_material = create_material(f"SuperCurveMat_V_{i}", road_color)
            if curve_obj.data:
                curve_obj.data.materials.clear()
                curve_obj.data.materials.append(road_material)
            
            print(f"         🔥✅ SUPER COURBE BLENDER V_{i} créée - MEGA VISIBLE !")
            
            road_network.append({
                'object': curve_obj,
                'road_type': 'super_bezier_vertical',
                'curve_type': 'blender_native_mega',
                'x': base_x,
                'y': 0,
                'width': road_width,
                'length': total_length,
                'curve_segments': segments + 1,
                'curve_amplitude': curve_amplitude
            })
        
        # Routes horizontales - COURBES BLENDER NATIVES
        print(f"   🎯 Génération routes horizontales COURBES BLENDER NATIVES...")
        for j in range(length + 1):
            base_y = (j - length/2) * block_size
            
            # Créer une courbe Bézier native Blender
            curve_data = bpy.data.curves.new(f"SuperCurve_H_{j}", type='CURVE')
            curve_data.dimensions = '3D'
            curve_data.fill_mode = 'BOTH'
            curve_data.bevel_depth = road_width / 2
            curve_data.resolution_u = 64
            curve_data.bevel_resolution = 16
            
            # Créer un spline Bézier
            spline = curve_data.splines.new('BEZIER')
            
            # Points de contrôle
            total_length = width * block_size
            segments = 12
            
            # Redimensionner le spline
            spline.bezier_points.add(segments)
            
            # Définir les points avec des courbes GIGANTESQUES
            for seg in range(segments + 1):
                t = seg / segments
                x = (t - 0.5) * total_length
                
                # COURBES GIGANTESQUES horizontales
                curve_amplitude = curve_intensity * block_size * 1.2
                
                # Courbes sinusoïdales EXTREMES multiples
                curve_offset = math.sin(t * 5 * math.pi + j * 1.4) * curve_amplitude
                curve_offset += math.sin(t * 8 * math.pi + j * 1.8) * curve_amplitude * 0.7
                curve_offset += math.sin(t * 4 * math.pi + j * 0.9) * curve_amplitude * 0.6
                
                # Variation random EXTREME
                curve_offset += random.uniform(-0.4, 0.4) * curve_amplitude
                
                final_y = base_y + curve_offset
                
                # Définir le point de contrôle
                point = spline.bezier_points[seg]
                point.co = (x, final_y, 0)
                
                # Handles pour des courbes naturelles
                point.handle_left_type = 'AUTO'
                point.handle_right_type = 'AUTO'
            
            # Créer l'objet courbe
            curve_obj = bpy.data.objects.new(f"SuperCurveRoad_H_{j}", curve_data)
            bpy.context.collection.objects.link(curve_obj)
            
            # Convertir en mesh
            bpy.context.view_layer.objects.active = curve_obj
            curve_obj.select_set(True)
            bpy.ops.object.convert(target='MESH')
            
            # Matériau MEGA vif
            hue = (j % 6) / 6.0
            road_color = (0.8 - hue * 0.3, 1.0, 0.3 + hue * 0.7)  # Couleurs vives
            
            road_material = create_material(f"SuperCurveMat_H_{j}", road_color)
            if curve_obj.data:
                curve_obj.data.materials.clear()
                curve_obj.data.materials.append(road_material)
            
            print(f"         🔥✅ SUPER COURBE BLENDER H_{j} créée - MEGA VISIBLE !")
            
            road_network.append({
                'object': curve_obj,
                'road_type': 'super_bezier_horizontal',
                'curve_type': 'blender_native_mega',
                'x': 0,
                'y': base_y,
                'width': road_width,
                'length': total_length,
                'curve_segments': segments + 1,
                'curve_amplitude': curve_amplitude
            })
        
        print(f"🔥🎯 === COURBES BLENDER NATIVES CRÉÉES === 🎯🔥")
        print(f"   ✅ {width + 1} routes verticales MEGA courbes")
        print(f"   ✅ {length + 1} routes horizontales MEGA courbes")
        print(f"   🔥 AMPLITUDE MAXIMALE: {curve_intensity * block_size * 1.2:.1f}")
        print(f"   🎯 IMPOSSIBLE DE LES RATER - COURBES GIGANTESQUES !")
        
        return road_network
        
    except Exception as e:
        print(f"❌ Erreur courbes: {e}")
        import traceback
        traceback.print_exc()
        return []


def identify_block_zones_from_roads_rf(road_network, width, length, road_width):
    """Identifie les zones de blocs entre les routes - GRILLE COMPLÈTE CORRIGÉE V6.12.7"""
    block_zones = []
    block_size = 12.0
    
    try:
        print(f"🔥🔥🔥 FONCTION CORRIGÉE V6.12.7 APPELÉE ! 🔥🔥🔥")
        print(f"🔍 Identification zones bâtiments entre routes courbes...")
        print(f"   Paramètres: grille {width}x{length}, block_size={block_size}")
        print(f"   📊 CALCUL ATTENDU: {width} × {length} = {width * length} zones")
        
        # CRÉER UNE GRILLE COMPLÈTE DE ZONES
        # Au lieu d'essayer de détecter entre les routes courbes, 
        # on crée une grille régulière adaptée à nos routes
        
        print(f"   🏗️ Création grille complète {width}x{length} zones...")
        
        for i in range(width):
            for j in range(length):
                # Position de base de cette zone (centre de chaque cellule de grille)
                base_x = (i - width/2 + 0.5) * block_size
                base_y = (j - length/2 + 0.5) * block_size
                
                # Dimensions de la zone (plus petites que le bloc pour éviter les routes)
                zone_width = block_size * 0.6   # 60% du bloc pour éviter les routes
                zone_height = block_size * 0.6
                
                print(f"      🎯 Zone [{i},{j}]: centre=({base_x:.1f}, {base_y:.1f}), taille={zone_width:.1f}x{zone_height:.1f}")
                
                # Déterminer le type de zone selon la position
                if i == 0 or i == width-1 or j == 0 or j == length-1:
                    zone_type = 'commercial'  # Bordures = commercial
                elif (i + j) % 3 == 0:
                    zone_type = 'industrial'  # Quelques zones industrielles
                else:
                    zone_type = 'residential'  # Majorité résidentiel
                
                block_zones.append({
                    'x': base_x,
                    'y': base_y,
                    'width': zone_width,
                    'height': zone_height,
                    'grid_i': i,
                    'grid_j': j,
                    'zone_type': zone_type
                })
        
        print(f"   ✅🔥🔥 {len(block_zones)} zones de bâtiments créées ! 🔥🔥")
        print(f"   📊 Répartition: {width} x {length} = {width*length} zones au total")
        print(f"   🎉 SUCCÈS - Notre fonction corrigée fonctionne !")
        
        # Afficher quelques exemples pour debug
        if len(block_zones) >= 3:
            print(f"   🔍 Exemples de zones créées:")
            for idx in [0, len(block_zones)//2, -1]:
                zone = block_zones[idx]
                print(f"      Zone {idx}: ({zone['x']:.1f}, {zone['y']:.1f}) - {zone['zone_type']}")
        
        return block_zones
        
    except Exception as e:
        print(f"❌ Erreur identification zones: {e}")
        import traceback
        print(f"Traceback: {traceback.format_exc()}")
        return []

def create_blocks_in_zones_rf(block_zones, block_mat):
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

def add_buildings_to_blocks_rf(block_zones, build_mat, scene):
    """Ajoute des bâtiments dans chaque bloc - VERSION ÉNORME POUR DEBUG"""
    buildings_created = 0
    
    try:
        print(f"🏢 === CRÉATION BÂTIMENTS ÉNORMES DEBUG ===")
        print(f"🏢 Création bâtiments dans {len(block_zones)} zones...")
        
        # Paramètres des bâtiments
        buildings_per_block = safe_int(getattr(scene, 'citygen_buildings_per_block', 2), 2)
        max_floors = safe_int(getattr(scene, 'citygen_max_floors', 8), 8)
        
        print(f"   Paramètres: {buildings_per_block} bâtiments/bloc, {max_floors} étages max")
        print(f"   🔍 Zones reçues: {len(block_zones)}")
        
        # FORCER AU MOINS UN BÂTIMENT GÉANT POUR TEST
        if len(block_zones) == 0:
            print("   🚨 AUCUNE ZONE - Création bâtiment de test au centre")
            # Créer un bâtiment géant au centre pour test
            bpy.ops.mesh.primitive_cube_add(size=2.0, location=(0, 0, 25))
            giant_building = bpy.context.object
            if giant_building:
                giant_building.scale = (10, 10, 25)  # ÉNORME !
                bpy.ops.object.transform_apply(scale=True)
                giant_building.name = "GIANT_DEBUG_BUILDING"
                buildings_created = 1
                print(f"   ✅ Bâtiment géant de test créé: {giant_building.name}")
        
        for zone_idx, zone in enumerate(block_zones):
            print(f"   🏗️ ZONE {zone_idx}: centre=({zone['x']:.1f}, {zone['y']:.1f}), taille={zone['width']:.1f}x{zone['height']:.1f}")
            
            # FORCER 2 BÂTIMENTS ÉNORMES PAR ZONE
            for b in range(2):  # Toujours 2 bâtiments
                # Position dans la zone
                building_x = zone['x'] + (b-0.5) * zone['width'] * 0.3  # Espacer les 2 bâtiments
                building_y = zone['y']
                
                # DIMENSIONS ÉNORMES POUR ÊTRE VISIBLE
                building_width = min(15, zone['width'] * 0.8)   # Large !
                building_depth = min(15, zone['height'] * 0.8)  # Profond !
                
                # HAUTEUR ÉNORME
                floors = random.randint(8, 20)  # 8-20 étages !
                building_height = floors * 4.0  # 4m par étage = 32-80m !
                
                print(f"      🏢 Bâtiment {b}: pos=({building_x:.1f}, {building_y:.1f}), taille={building_width:.1f}x{building_depth:.1f}x{building_height:.1f}")
                
                # Créer le bâtiment ÉNORME
                bpy.ops.mesh.primitive_cube_add(
                    size=2.0, 
                    location=(building_x, building_y, building_height/2)
                )
                building = bpy.context.object
                
                if building:
                    # Échelle ÉNORME
                    building.scale = (building_width/2, building_depth/2, building_height/2)
                    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
                    
                    # Nom distinctif
                    building.name = f"MEGA_Building_Z{zone_idx}_B{b}_{floors}floors"
                    
                    # Couleur TRÈS contrastée selon hauteur
                    if floors < 12:
                        building_color = (1.0, 0.5, 0.5)  # ROUGE vif (bas)
                    elif floors < 16:
                        building_color = (0.5, 1.0, 0.5)  # VERT vif (moyen)  
                    else:
                        building_color = (0.5, 0.5, 1.0)  # BLEU vif (haut)
                    
                    building_material = create_material(f"MEGA_BuildingMat_{zone_idx}_{b}", building_color)
                    if building.data:
                        building.data.materials.clear()
                        building.data.materials.append(building_material)
                    
                    buildings_created += 1
                    
                    print(f"         ✅ MEGA BÂTIMENT créé: {building.name}")
                    print(f"         📍 Position: ({building_x:.1f}, {building_y:.1f}, {building_height/2:.1f})")
                    print(f"         📐 Échelle: ({building_width/2:.1f}, {building_depth/2:.1f}, {building_height/2:.1f})")
                    print(f"         🎨 Couleur: {building_color}")
        
        print(f"   🎯 === RÉSUMÉ CRÉATION BÂTIMENTS ===")
        print(f"   ✅ Total: {buildings_created} MEGA bâtiments créés!")
        print(f"   🏗️ Zones traitées: {len(block_zones)}")
        print(f"   🎨 Couleurs: ROUGE (bas), VERT (moyen), BLEU (haut)")
        print(f"   📏 Tailles: 15x15x32-80m (ÉNORMES !)")
        print(f"   👀 Les bâtiments DOIVENT être visibles maintenant !")
        
        return buildings_created
        
    except Exception as e:
        print(f"❌ Erreur création MEGA bâtiments: {e}")
        import traceback
        print(f"Traceback: {traceback.format_exc()}")
        return 0

def add_urban_variety(block_sizes, variety_level='MEDIUM'):
    """Ajoute de la variété urbaine : espaces verts, places, variations de taille"""
    import random
    
    if variety_level == 'LOW':
        return block_sizes  # Pas de modifications
    
    modified_blocks = []
    
    for i, row in enumerate(block_sizes):
        modified_row = []
        for j, block in enumerate(row):
            
            # Chance d'ajouter une variation selon le niveau
            variation_chance = {
                'MEDIUM': 0.15,
                'HIGH': 0.25,
                'EXTREME': 0.35
            }.get(variety_level, 0.15)
            
            if random.random() < variation_chance:
                # Types de variations urbaines
                variation_type = random.choice([
                    'small_park',    # Petit parc
                    'plaza',         # Place
                    'wide_street',   # Rue élargie
                    'small_block',   # Bloc réduit
                    'tall_block'     # Bloc élevé
                ])
                
                if isinstance(block, dict):
                    base_size = block['size']
                    zone_type = block.get('zone_type', 'RESIDENTIAL')
                else:
                    base_size = block
                    zone_type = 'RESIDENTIAL'
                
                if variation_type == 'small_park':
                    # Créer un petit espace vert
                    modified_block = {
                        'size': (base_size[0] * 0.7, base_size[1] * 0.7),
                        'zone_type': 'PARK',
                        'variation': 'small_park',
                        'zone_info': {
                            'building_count': 0,  # Pas de bâtiments
                            'green_space': True
                        }
                    }
                elif variation_type == 'plaza':
                    # Créer une place
                    modified_block = {
                        'size': (base_size[0] * 1.2, base_size[1] * 1.2),
                        'zone_type': 'PLAZA',
                        'variation': 'plaza',
                        'zone_info': {
                            'building_count': 0,
                            'open_space': True
                        }
                    }
                elif variation_type == 'small_block':
                    # Bloc plus petit
                    modified_block = {
                        'size': (base_size[0] * 0.8, base_size[1] * 0.8),
                        'zone_type': zone_type,
                        'variation': 'small_block',
                        'zone_info': {
                            'size_factor': 0.8,
                            'building_count': 1
                        }
                    }
                elif variation_type == 'tall_block':
                    # Bloc avec bâtiments plus hauts
                    modified_block = {
                        'size': base_size,
                        'zone_type': zone_type,
                        'variation': 'tall_block',
                        'zone_info': {
                            'height_multiplier': 1.5,
                            'building_count': 1
                        }
                    }
                else:  # wide_street
                    # Bloc normal mais avec espacement pour rues plus larges
                    modified_block = {
                        'size': (base_size[0] * 0.9, base_size[1] * 0.9),
                        'zone_type': zone_type,
                        'variation': 'wide_street',
                        'zone_info': {
                            'road_width_multiplier': 1.5
                        }
                    }
                
                modified_row.append(modified_block)
                print(f"   🌿 Variation urbaine ajoutée: {variation_type} à [{i}][{j}]")
            else:
                # Garder le bloc original
                modified_row.append(block)
        
        modified_blocks.append(modified_row)
    
    return modified_blocks

# =============================================================================
# 🚀 OPTIMISATIONS DE PERFORMANCE (AJOUTÉES POUR ÉVITER LES CRASHES)
# =============================================================================

def optimize_mesh_creation(vertices, faces, name="OptimizedMesh"):
    """Créer des meshes de façon optimisée pour réduire l'usage mémoire"""
    try:
        # Limiter le nombre de vertices pour éviter la surcharge
        max_vertices = 1000  # Limite sécurisée
        if len(vertices) > max_vertices:
            print(f"⚠️ OPTIMISATION: Réduction vertices de {len(vertices)} à {max_vertices}")
            # Prendre un échantillon régulier
            step = len(vertices) // max_vertices
            vertices = vertices[::step]
            # Recalculer les faces en conséquence
            face_map = {old_idx: new_idx for new_idx, old_idx in enumerate(range(0, len(vertices) * step, step))}
            faces = [[face_map.get(v, 0) for v in face if v in face_map] for face in faces if all(v in face_map for v in face)]
        
        mesh = bpy.data.meshes.new(name)
        mesh.from_pydata(vertices, [], faces)
        mesh.update()
        return mesh
        
    except Exception as e:
        print(f"❌ ERREUR optimisation mesh: {e}")
        # Fallback simple
        mesh = bpy.data.meshes.new(name)
        simple_vertices = [(0,0,0), (1,0,0), (1,1,0), (0,1,0)]
        simple_faces = [(0,1,2,3)]
        mesh.from_pydata(simple_vertices, [], simple_faces)
        mesh.update()
        return mesh

def check_performance_limits():
    """Vérifier les limites système pour éviter les crashes"""
    try:
        total_objects = len(bpy.data.objects)
        total_meshes = len(bpy.data.meshes)
        
        limits = {
            'max_objects': 100,  # Limite sécurisée d'objets
            'max_meshes': 150,   # Limite sécurisée de meshes
        }
        
        warnings = []
        if total_objects > limits['max_objects']:
            warnings.append(f"Trop d'objets: {total_objects}/{limits['max_objects']}")
        if total_meshes > limits['max_meshes']:
            warnings.append(f"Trop de meshes: {total_meshes}/{limits['max_meshes']}")
        
        if warnings:
            print("⚠️ AVERTISSEMENTS PERFORMANCE:")
            for warning in warnings:
                print(f"   - {warning}")
            return False
        
        return True
    except:
        return True  # En cas d'erreur, on continue

def safe_object_creation(name, mesh, location=(0, 0, 0)):
    """Créer un objet de façon sécurisée avec gestion d'erreur"""
    try:
        if not check_performance_limits():
            print(f"⚠️ Limitation performance: objet {name} non créé")
            return None
            
        obj = bpy.data.objects.new(name, mesh)
        obj.location = location
        bpy.context.collection.objects.link(obj)
        return obj
        
    except Exception as e:
        print(f"❌ ERREUR création objet {name}: {e}")
        return None
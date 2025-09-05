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
    """Choisit intelligemment le type de bâtiment selon la variété demandée"""
    import random
    
    # Types de bâtiments disponibles avec leurs conditions
    building_types = {
        'rectangular': {'weight': 35, 'min_size': 2.0},
        'tower': {'weight': 15, 'min_size': 3.0, 'min_height': 15},
        'stepped': {'weight': 12, 'min_size': 4.0, 'min_height': 12},
        'l_shaped': {'weight': 15, 'min_size': 5.0},  # Augmenté de 8 à 15
        'u_shaped': {'weight': 10, 'min_size': 6.0},  # Augmenté de 6 à 10 (utilisé comme F-shaped)
        't_shaped': {'weight': 12, 'min_size': 5.0},  # Augmenté de 5 à 12
        'circular': {'weight': 4, 'min_size': 4.0},
        'elliptical': {'weight': 3, 'min_size': 4.0},
        'complex': {'weight': 2, 'min_size': 6.0, 'min_height': 18},
        'pyramid': {'weight': 2, 'min_size': 4.0, 'min_height': 12}
        # cone supprimé comme demandé
    }
    
    # Ajuster les poids selon le niveau de variété avec plus de L, T et U shapes
    if variety_level == 'LOW':
        # Principalement rectangulaires mais avec quelques L et T
        weights = ['rectangular'] * 50 + ['tower'] * 20 + ['l_shaped'] * 20 + ['t_shaped'] * 10
    elif variety_level == 'MEDIUM':
        # Équilibre avec forte présence de L, T, U
        weights = (['rectangular'] * 20 + ['tower'] * 15 + ['stepped'] * 10 + 
                  ['l_shaped'] * 20 + ['u_shaped'] * 15 + ['t_shaped'] * 15 + 
                  ['circular'] * 3 + ['elliptical'] * 2)
    elif variety_level == 'HIGH':
        # Maximum de variété avec dominance L, T, U
        weights = (['rectangular'] * 10 + ['tower'] * 10 + ['stepped'] * 10 + 
                  ['l_shaped'] * 25 + ['u_shaped'] * 20 + ['t_shaped'] * 20 + 
                  ['circular'] * 3 + ['elliptical'] * 2)
    elif variety_level == 'MODERN':
        # Tours et formes modernes avec L et T
        weights = (['tower'] * 30 + ['stepped'] * 20 + ['complex'] * 15 + 
                  ['l_shaped'] * 15 + ['t_shaped'] * 15 + ['rectangular'] * 5)
    elif variety_level == 'CREATIVE':
        # Formes créatives avec L, T, U dominants
        weights = (['l_shaped'] * 25 + ['t_shaped'] * 25 + ['u_shaped'] * 20 + 
                  ['circular'] * 10 + ['elliptical'] * 8 + ['pyramid'] * 7 + 
                  ['complex'] * 3 + ['tower'] * 2)
    else:
        # Fallback avec forte présence de L et T
        weights = ['rectangular'] * 25 + ['l_shaped'] * 25 + ['t_shaped'] * 20 + ['tower'] * 15 + ['u_shaped'] * 15
    
    # Choisir un type aléatoire
    chosen_type = random.choice(weights)
    
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
        else:  # shape_mode == 'AUTO' - Utiliser le système de variété intelligent
            building_type = choose_building_type(building_variety, zone_type, width, depth, height)
        
        print(f"   Type de bâtiment sélectionné: {building_type} (mode: {shape_mode})")
        
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
        # Créer le cube avec origine au centre bas
        obj = create_cube_with_center_bottom_origin(width, depth, height, (x, y, 0.02))
        
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
            (x - width*0.15, y - depth*0.2, 0.02)
        )
        if main_obj:
            parts.append(main_obj)
        
        # Partie secondaire (horizontale du L)
        secondary_obj = create_cube_with_center_bottom_origin(
            secondary_width, secondary_depth, secondary_height,
            (x + width*0.25, y + depth*0.3, 0.02)
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
                (x - width*0.35, y, 0.02)
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
                (x - width*0.375, y, 0.02)
            )
            if left_part:
                parts.append(left_part)
            
            # Tige droite
            right_part = create_cube_with_center_bottom_origin(
                left_width, depth * 0.8, height, 
                (x + width*0.375, y, 0.02)
            )
            if right_part:
                parts.append(right_part)
            
            # Barre de liaison (arrière)
            back_part = create_cube_with_center_bottom_origin(
                width * 0.5, depth * 0.2, height, 
                (x, y + depth*0.4, 0.02)
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
    
    base_obj.location = (x, y, 0.02)  # Hauteur ajustée
    
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
    
    tower_obj.location = (x, y, base_height + 0.02)  # Hauteur ajustée
    
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
        obj.location.z = 0.02  # Hauteur légèrement au-dessus du trottoir

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
        obj.location.z = 0.02  # Hauteur légèrement au-dessus du trottoir

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
            (x, y - depth * 0.15, 0.02)  # Base au sol
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
            width, depth, base_height, (x, y, 0.02)
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
            print("ERREUR: block_sizes invalide")
            return False
            
        grid_width = len(block_sizes)
        grid_length = len(block_sizes[0]) if block_sizes else 0
        
        if grid_width == 0 or grid_length == 0:
            print("ERREUR: Dimensions de grille invalides")
            return False
        
        print(f"Génération grille {grid_width}x{grid_length}")
        
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
    """Génère une ville complète avec gestion d'erreurs robuste"""
    try:
        # Réinitialiser le compteur de bâtiments
        global building_counter
        building_counter = 0
        
        print("=== Début de génération de ville ===")
        
        # Vérifications préliminaires
        state_errors = check_blender_state()
        if state_errors:
            for error in state_errors:
                print(f"ERREUR ÉTAT: {error}")
            return False
        
        # Accéder aux propriétés directement depuis la scène (nouvelle architecture)
        scene = context.scene
        
        # Utiliser notre fonction utilitaire pour convertir de façon sécurisée
        width = safe_int(getattr(scene, 'citygen_width', 5), 5)
        length = safe_int(getattr(scene, 'citygen_length', 5), 5)
        max_floors = safe_int(getattr(scene, 'citygen_max_floors', 8), 8)
        shape_mode = "AUTO"  # Valeur par défaut pour l'instant
        
        # Nouvelles propriétés pour bâtiments multiples et routes collées
        buildings_per_block = safe_int(getattr(scene, 'citygen_buildings_per_block', 1), 1)
        seamless_roads = getattr(scene, 'citygen_seamless_roads', True)
        building_variety = getattr(scene, 'citygen_building_variety', 'MEDIUM')
        height_variation = safe_float(getattr(scene, 'citygen_height_variation', 0.5), 0.5)
        
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
                print("ERREUR: Échec de génération des tailles de blocs")
                return False
        except Exception as e:
            print(f"ERREUR lors de la génération des tailles de blocs: {str(e)}")
            return False
        
        # Générer la grille unifiée de ville
        print(f"🚀 APPEL generate_unified_city_grid avec regen_only={regen_only}")
        try:
            success = generate_unified_city_grid(
                block_sizes, road_width, road_mat, side_mat, build_mat, max_floors, regen_only, 
                district_materials, sidewalk_width, shape_mode, 
                enable_diagonal_roads, diagonal_road_frequency, enable_intersections, intersection_size_factor,
                buildings_per_block, seamless_roads, building_variety, height_variation
            )
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
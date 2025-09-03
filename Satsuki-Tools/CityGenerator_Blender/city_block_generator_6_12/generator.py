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
    """Crée un matériau avec gestion d'erreurs"""
    try:
        mat = bpy.data.materials.get(name)
        if not mat:
            mat = bpy.data.materials.new(name)
            mat.diffuse_color = (*color, 1)
        return mat
    except Exception as e:
        print(f"Erreur lors de la création du matériau '{name}': {str(e)}")
        # Retourner un matériau par défaut ou None
        try:
            # Essayer de créer un matériau de base
            default_mat = bpy.data.materials.new(f"default_{name}")
            default_mat.diffuse_color = (0.5, 0.5, 0.5, 1)
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

def generate_building(x, y, width, depth, height, mat, zone_type='RESIDENTIAL', district_materials=None):
    """Génère un bâtiment avec une forme aléatoire et gestion d'erreurs"""
    global building_counter
    building_counter += 1
    
    try:
        # Validation des paramètres
        if width <= 0 or depth <= 0 or height <= 0:
            print(f"Paramètres de bâtiment invalides: w={width}, d={depth}, h={height}")
            return None
            
        if not mat:
            print(f"Matériau invalide pour le bâtiment {building_counter}")
            return None
        
        # Choisir le matériau approprié en fonction du type de zone
        final_mat = mat  # Matériau par défaut
        if district_materials and zone_type in district_materials:
            final_mat = district_materials[zone_type]
            print(f"Application du matériau de district {zone_type} au bâtiment {building_counter}")
        
        # Choisir aléatoirement un type de bâtiment (plus simple)
        building_type = random.choice(['rectangular', 'rectangular', 'rectangular', 'tower', 'stepped'])
        
        print(f"Génération bâtiment {building_counter} de type {building_type} (zone: {zone_type})")
        
        if building_type == 'rectangular':
            return generate_rectangular_building(x, y, width, depth, height, final_mat, building_counter)
        elif building_type == 'tower':
            return generate_simple_tower_building(x, y, width, depth, height, final_mat, building_counter)
        elif building_type == 'stepped':
            return generate_simple_stepped_building(x, y, width, depth, height, final_mat, building_counter)
        else:
            # Fallback vers rectangulaire si type non reconnu
            print(f"Type de bâtiment non reconnu: {building_type}, utilisation du type rectangulaire")
            return generate_rectangular_building(x, y, width, depth, height, final_mat, building_counter)
            
    except Exception as e:
        print(f"Erreur critique lors de la génération du bâtiment {building_counter}: {str(e)}")
        print(f"Traceback: {traceback.format_exc()}")
        return None

def generate_rectangular_building(x, y, width, depth, height, mat, building_num):
    """Génère un bâtiment rectangulaire avec gestion d'erreurs"""
    try:
        # Validation des paramètres
        if width <= 0 or depth <= 0 or height <= 0:
            print(f"Paramètres invalides pour le bâtiment {building_num}: w={width}, d={depth}, h={height}")
            return None
            
        if not mat:
            print(f"Matériau invalide pour le bâtiment {building_num}")
            return None
        
        # Créer le cube à l'origine
        result = safe_object_creation(bpy.ops.mesh.primitive_cube_add, size=1, location=(0, 0, 0))
        if not bpy.context.object:
            print(f"Échec de création du cube pour le bâtiment {building_num}")
            return None
            
        obj = bpy.context.object
        obj.name = f"batiment_rectangular_{building_num}"

        # Appliquer l'échelle pour définir la largeur, profondeur et hauteur
        obj.scale.x = width/2
        obj.scale.y = depth/2
        obj.scale.z = height/2

        # Appliquer l'échelle avec gestion d'erreurs
        if not safe_mesh_operation(bpy.ops.object.transform_apply, obj, location=False, rotation=False, scale=True):
            print(f"Échec de l'application de l'échelle pour le bâtiment {building_num}")
            return None

        # Trouver les limites du mesh avec validation
        mesh = obj.data
        if not mesh or not mesh.vertices:
            print(f"Mesh invalide pour le bâtiment {building_num}")
            return None
            
        # Un cube standard dans Blender a des sommets à -0.5 et 0.5 sur tous les axes
        try:
            z_min = min(v.co.z for v in mesh.vertices)
        except (AttributeError, ValueError) as e:
            print(f"Erreur lors du calcul des limites pour le bâtiment {building_num}: {e}")
            z_min = -0.5  # Valeur par défaut
        
        # Déplacer tous les sommets pour que le point le plus bas soit à z=0
        try:
            for v in mesh.vertices:
                v.co.z -= z_min
        except Exception as e:
            print(f"Erreur lors du déplacement des sommets pour le bâtiment {building_num}: {e}")

        # Positionner l'objet pour que la base soit au niveau du trottoir
        obj.location.x = x
        obj.location.y = y
        obj.location.z = 0.02  # Hauteur légèrement au-dessus du trottoir (0.01)

        # Appliquer le matériau avec validation
        try:
            if mat and obj.data:
                obj.data.materials.append(mat)
        except Exception as e:
            print(f"Erreur lors de l'application du matériau pour le bâtiment {building_num}: {e}")

        # Log de la position du bâtiment
        print(f"Building {obj.name} placed at: x={obj.location.x}, y={obj.location.y}, z={obj.location.z}")
        return obj
        
    except Exception as e:
        print(f"Erreur critique lors de la génération du bâtiment rectangulaire {building_num}: {str(e)}")
        print(f"Traceback: {traceback.format_exc()}")
        return None

def generate_l_shaped_building(x, y, width, depth, height, mat, building_num):
    """Génère un bâtiment en forme de L"""
    # Partie principale (plus grande)
    main_width = width * 0.7
    main_depth = depth * 0.6
    
    # Créer la partie principale
    bpy.ops.mesh.primitive_cube_add(size=1, location=(0, 0, 0))
    main_obj = bpy.context.object
    main_obj.scale = (main_width/2, main_depth/2, height/2)
    
    # Appliquer l'échelle
    bpy.context.view_layer.objects.active = main_obj
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    
    # Ajuster la position Z des sommets
    mesh = main_obj.data
    z_min = min(v.co.z for v in mesh.vertices)
    for v in mesh.vertices:
        v.co.z -= z_min
    
    # Positionner la partie principale
    main_obj.location = (x - width/4, y - depth/4, 0.02)  # Hauteur ajustée
    
    # Partie secondaire (plus petite)
    secondary_width = width * 0.5
    secondary_depth = depth * 0.4
    secondary_height = height * random.uniform(0.6, 0.9)
    
    # Créer la partie secondaire
    bpy.ops.mesh.primitive_cube_add(size=1, location=(0, 0, 0))
    secondary_obj = bpy.context.object
    secondary_obj.scale = (secondary_width/2, secondary_depth/2, secondary_height/2)
    
    # Appliquer l'échelle
    bpy.context.view_layer.objects.active = secondary_obj
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    
    # Ajuster la position Z des sommets
    mesh = secondary_obj.data
    z_min = min(v.co.z for v in mesh.vertices)
    for v in mesh.vertices:
        v.co.z -= z_min
    
    # Positionner la partie secondaire
    secondary_obj.location = (x + width/4, y + depth/4, 0.02)  # Hauteur ajustée
    
    # Joindre les deux parties
    bpy.context.view_layer.objects.active = main_obj
    main_obj.select_set(True)
    secondary_obj.select_set(True)
    bpy.ops.object.join()
    
    # Nommer le bâtiment
    main_obj.name = f"batiment_l_shaped_{building_num}"
    
    # Appliquer le matériau
    main_obj.data.materials.append(mat)

def generate_u_shaped_building(x, y, width, depth, height, mat):
    """Génère un bâtiment en forme de U"""
    # Trois parties : gauche, droite, et arrière
    part_width = width * 0.25
    part_depth = depth * 0.8
    back_width = width * 0.5
    back_depth = depth * 0.2
    
    parts = []
    
    # Partie gauche
    bpy.ops.mesh.primitive_cube_add(size=1, location=(0, 0, 0))
    left_obj = bpy.context.object
    left_obj.scale = (part_width/2, part_depth/2, height/2)
    bpy.context.view_layer.objects.active = left_obj
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    
    # Ajuster la position Z des sommets
    mesh = left_obj.data
    z_min = min(v.co.z for v in mesh.vertices)
    for v in mesh.vertices:
        v.co.z -= z_min
    
    left_obj.location = (x - width/2 + part_width/2, y, 0.02)  # Hauteur ajustée
    parts.append(left_obj)
    
    # Partie droite
    bpy.ops.mesh.primitive_cube_add(size=1, location=(0, 0, 0))
    right_obj = bpy.context.object
    right_obj.scale = (part_width/2, part_depth/2, height/2)
    bpy.context.view_layer.objects.active = right_obj
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    
    # Ajuster la position Z des sommets
    mesh = right_obj.data
    z_min = min(v.co.z for v in mesh.vertices)
    for v in mesh.vertices:
        v.co.z -= z_min
    
    right_obj.location = (x + width/2 - part_width/2, y, 0.02)  # Hauteur ajustée
    parts.append(right_obj)
    
    # Partie arrière
    bpy.ops.mesh.primitive_cube_add(size=1, location=(0, 0, 0))
    back_obj = bpy.context.object
    back_obj.scale = (back_width/2, back_depth/2, height/2)
    bpy.context.view_layer.objects.active = back_obj
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    
    # Ajuster la position Z des sommets
    mesh = back_obj.data
    z_min = min(v.co.z for v in mesh.vertices)
    for v in mesh.vertices:
        v.co.z -= z_min
    
    back_obj.location = (x, y + depth/2 - back_depth/2, 0.02)  # Hauteur ajustée
    parts.append(back_obj)
    
    # Joindre toutes les parties
    bpy.context.view_layer.objects.active = parts[0]
    for part in parts:
        part.select_set(True)
    bpy.ops.object.join()
    
    # Appliquer le matériau
    parts[0].data.materials.append(mat)

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

def generate_sidewalk(x, y, width, depth, mat):
    """Génère un trottoir avec gestion d'erreurs"""
    try:
        if width <= 0 or depth <= 0:
            print(f"Paramètres trottoir invalides: w={width}, d={depth}")
            return False
            
        if not mat:
            print("Matériau trottoir invalide")
            return False
        
        # Créer un plan pour le trottoir légèrement au-dessus de la route
        # Le trottoir doit être positionné exactement comme les routes pour un alignement parfait
        result = safe_object_creation(bpy.ops.mesh.primitive_plane_add, size=1, location=(0, 0, 0.01))
        if not bpy.context.object:
            print("Échec de création du plan trottoir")
            return False
            
        obj = bpy.context.object
        obj.name = f"sidewalk_{x:.1f}_{y:.1f}"
        obj.scale = (width/2, depth/2, 0.02)  # Trottoir plus épais pour être plus visible
        obj.location = (x + width/2, y + depth/2, 0.01)  # Position centre exact du trottoir
        
        # Appliquer le matériau
        try:
            obj.data.materials.append(mat)
            return True
        except Exception as e:
            print(f"Erreur application matériau trottoir: {e}")
            return False
            
    except Exception as e:
        print(f"Erreur création trottoir: {str(e)}")
        return False

def generate_road(x, y, width, length, mat, is_horizontal=True):
    """Génère une route avec gestion d'erreurs"""
    try:
        if width <= 0 or length <= 0:
            print(f"Paramètres route invalides: w={width}, l={length}")
            return False
            
        if not mat:
            print("Matériau route invalide")
            return False
        
        # Créer un plan pour la route au niveau du sol, légèrement sous les trottoirs
        # Les routes doivent être positionnées EXACTEMENT aux coordonnées calculées
        result = safe_object_creation(bpy.ops.mesh.primitive_plane_add, size=1, location=(0, 0, 0.001))
        if not bpy.context.object:
            print("Échec de création du plan route")
            return False
        obj = bpy.context.object
        
        if is_horizontal:
            # Route horizontale : largeur = length, hauteur = width
            obj.scale = (length/2, width/2, 0.005)  # Échelle selon dimensions
            obj.location = (x + length/2, y + width/2, 0.001)  # Centre exact de la route
        else:
            # Route verticale : largeur = width, hauteur = length  
            obj.scale = (width/2, length/2, 0.005)  # Échelle selon dimensions
            obj.location = (x + width/2, y + length/2, 0.001)  # Centre exact de la route
            
        obj.name = f"road_{'h' if is_horizontal else 'v'}_{x:.1f}_{y:.1f}"
        
        # Appliquer le matériau
        try:
            obj.data.materials.append(mat)
            return True
        except Exception as e:
            print(f"Erreur application matériau route: {e}")
            return False
            
    except Exception as e:
        print(f"Erreur création route: {str(e)}")
        return False

def generate_unified_city_grid(block_sizes, road_width, road_mat, side_mat, build_mat, max_floors, regen_only, district_materials=None):
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
                
                print(f"Route horizontale {j}: position=({x_road_start}, {y_road_start}), largeur={road_width}, longueur={road_length}")
                
                if generate_road(x_road_start, y_road_start, road_width, road_length, road_mat, is_horizontal=True):
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
                
                print(f"Route verticale {i}: position=({x_road_start}, {y_road_start}), largeur={road_width}, longueur={road_length}")
                
                if generate_road(x_road_start, y_road_start, road_width, road_length, road_mat, is_horizontal=False):
                    roads_created += 1
                    print(f"  ✓ Route verticale {i} créée avec succès")
                else:
                    print(f"  ✗ AVERTISSEMENT: Échec création route verticale {i}")
                    
            except Exception as e:
                print(f"ERREUR lors de la création route verticale {i}: {e}")
        
        print(f"Routes créées: {roads_created}")
        
        # Générer les blocs et trottoirs
        blocks_created = 0
        buildings_created = 0
        
        for i in range(grid_width):
            for j in range(grid_length):
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
                        zone_info = {}
                    
                    if block_width <= 0 or block_depth <= 0:
                        print(f"AVERTISSEMENT: Taille de bloc invalide à [{i}][{j}]: {block_width}x{block_depth}")
                        continue
                    
                    # Position du bloc (coordonnées du coin)
                    x_block = x_starts[i]
                    y_block = y_starts[j]
                    
                    # Générer le trottoir aux coordonnées exactes du coin
                    if generate_sidewalk(x_block, y_block, block_width, block_depth, side_mat):
                        blocks_created += 1
                    else:
                        print(f"AVERTISSEMENT: Échec création trottoir à [{i}][{j}]")
                    
                    # Position du centre du bloc pour le bâtiment
                    x_center = x_block + block_width/2
                    y_center = y_block + block_depth/2
                    
                    # Générer le bâtiment si ce n'est pas une régénération
                    if not regen_only:
                        try:
                            # Calculer la hauteur selon le type de zone
                            if zone_info:
                                min_floors = zone_info.get('min_floors', 1)
                                max_floors_multiplier = zone_info.get('max_floors_multiplier', 1.0)
                                zone_max_floors = max(min_floors, int(max_floors * max_floors_multiplier))
                                height = random.randint(min_floors, zone_max_floors) * 3
                                
                                # Type de zone affecte la variabilité
                                if zone_type == 'COMMERCIAL':
                                    height += random.randint(3, 8)  # Bâtiments commerciaux plus hauts
                                elif zone_type == 'INDUSTRIAL':
                                    height = random.randint(1, 2) * 3  # Bâtiments industriels bas
                                elif zone_type == 'RESIDENTIAL':
                                    if random.random() > 0.7:  # 30% de chance d'être plus haut
                                        height += random.randint(2, 6)
                            else:
                                # Logique par défaut
                                height = random.randint(1, max_floors) * 3
                                if random.random() > 0.7:
                                    height += random.randint(5, 10)
                            
                            # Bâtiment légèrement plus petit que le bloc
                            building_width = block_width * 0.9
                            building_depth = block_depth * 0.9
                            
                            if generate_building(x_center, y_center, building_width, building_depth, height, build_mat, zone_type, district_materials):
                                buildings_created += 1
                            else:
                                print(f"AVERTISSEMENT: Échec création bâtiment à [{i}][{j}]")
                                
                        except Exception as e:
                            print(f"ERREUR lors de la création bâtiment à [{i}][{j}]: {e}")
                
                except Exception as e:
                    print(f"ERREUR lors de la création bloc à [{i}][{j}]: {e}")
        
        print(f"Blocs créés: {blocks_created}, Bâtiments créés: {buildings_created}")
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
        # Créer un filtre pour ne supprimer que routes et trottoirs
        def road_sidewalk_filter(obj):
            return any(keyword in obj.name.lower() for keyword in ['road', 'route', 'sidewalk', 'trottoir'])
        
        # Supprimer seulement les routes et trottoirs
        if safe_delete_objects(road_sidewalk_filter):
            return generate_city(context, regen_only=True)
        else:
            print("Échec de la suppression des routes et trottoirs")
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
        
        # Assurons-nous que les propriétés existent avant d'y accéder
        if not hasattr(context.scene, 'citygen_props'):
            print("ERREUR: Les propriétés citygen_props ne sont pas disponibles")
            return False
            
        props = context.scene.citygen_props
        
        # Utiliser notre fonction utilitaire pour convertir de façon sécurisée
        width = safe_int(props.width, 5)
        length = safe_int(props.length, 5)
        max_floors = safe_int(props.max_floors, 8)
        shape_mode = props.shape_mode if hasattr(props, "shape_mode") else "AUTO"
        
        # Nouveaux paramètres pour la variété des blocs
        base_size = safe_float(props.base_block_size, 10.0) if hasattr(props, "base_block_size") else 10.0
        block_variety = props.block_variety if hasattr(props, "block_variety") else "MEDIUM"
        district_mode = props.district_mode if hasattr(props, "district_mode") else False
        commercial_ratio = safe_float(props.commercial_ratio, 0.2) if hasattr(props, "commercial_ratio") else 0.2
        residential_ratio = safe_float(props.residential_ratio, 0.6) if hasattr(props, "residential_ratio") else 0.6
        industrial_ratio = safe_float(props.industrial_ratio, 0.2) if hasattr(props, "industrial_ratio") else 0.2
        
        # Validation des paramètres
        param_errors = validate_parameters(width, length, max_floors)
        if param_errors:
            for error in param_errors:
                print(f"ERREUR PARAMÈTRE: {error}")
            return False
        
        print(f"Paramètres validés: width={width}, length={length}, max_floors={max_floors}, shape={shape_mode}")

        # Créer les matériaux avec gestion d'erreurs
        road_width = 4
        
        road_mat = create_material("RoadMat", (0.1, 0.1, 0.1))
        side_mat = create_material("SidewalkMat", (0.6, 0.6, 0.6))
        build_mat = create_material("BuildingMat", (0.5, 0.5, 0.5))
        
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
                commercial_ratio, residential_ratio, industrial_ratio
            )
            if not block_sizes:
                print("ERREUR: Échec de génération des tailles de blocs")
                return False
        except Exception as e:
            print(f"ERREUR lors de la génération des tailles de blocs: {str(e)}")
            return False
        
        # Générer la grille unifiée de ville
        try:
            success = generate_unified_city_grid(block_sizes, road_width, road_mat, side_mat, build_mat, max_floors, regen_only, district_materials)
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

def generate_block_sizes(grid_width, grid_length, base_size=10, variety='MEDIUM', district_mode=False, 
                        commercial_ratio=0.2, residential_ratio=0.6, industrial_ratio=0.2):
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
        
        # Définir les types de zones et leurs caractéristiques
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
        
        block_sizes = []
        zone_assignments = []
        
        # Générer les assignations de zones si mode districts activé
        if district_mode:
            zone_assignments = generate_district_zones(grid_width, grid_length, 
                                                     commercial_ratio, residential_ratio, industrial_ratio)
        
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
        # Matériau commercial (bleu)
        if "Commercial_District" not in bpy.data.materials:
            mat_commercial = bpy.data.materials.new(name="Commercial_District")
            mat_commercial.use_nodes = True
            principled = mat_commercial.node_tree.nodes.get("Principled BSDF")
            if principled:
                principled.inputs[0].default_value = (0.2, 0.4, 0.8, 1.0)  # Bleu
                principled.inputs[7].default_value = 0.1  # Roughness
        materials['COMMERCIAL'] = bpy.data.materials["Commercial_District"]
        
        # Matériau résidentiel (vert)
        if "Residential_District" not in bpy.data.materials:
            mat_residential = bpy.data.materials.new(name="Residential_District")
            mat_residential.use_nodes = True
            principled = mat_residential.node_tree.nodes.get("Principled BSDF")
            if principled:
                principled.inputs[0].default_value = (0.3, 0.7, 0.3, 1.0)  # Vert
                principled.inputs[7].default_value = 0.3  # Roughness
        materials['RESIDENTIAL'] = bpy.data.materials["Residential_District"]
        
        # Matériau industriel (rouge/orange)
        if "Industrial_District" not in bpy.data.materials:
            mat_industrial = bpy.data.materials.new(name="Industrial_District")
            mat_industrial.use_nodes = True
            principled = mat_industrial.node_tree.nodes.get("Principled BSDF")
            if principled:
                principled.inputs[0].default_value = (0.8, 0.4, 0.2, 1.0)  # Orange
                principled.inputs[7].default_value = 0.5  # Roughness
        materials['INDUSTRIAL'] = bpy.data.materials["Industrial_District"]
        
        print("✓ Matériaux de districts créés avec succès")
        return materials
        
    except Exception as e:
        print(f"Erreur lors de la création des matériaux de districts: {e}")
        return {}
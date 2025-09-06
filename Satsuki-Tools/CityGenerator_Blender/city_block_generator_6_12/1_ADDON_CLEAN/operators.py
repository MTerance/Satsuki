import bpy
import traceback
import sys
import importlib

# Fonction pour accéder aux propriétés de manière uniforme
def get_citygen_properties(context):
    """Retourne un objet avec les propriétés city generator"""
    class PropertyAccessor:
        def __init__(self, scene):
            self.scene = scene
        
        @property
        def width(self):
            return getattr(self.scene, 'citygen_width', 5)
        
        @property
        def length(self):
            return getattr(self.scene, 'citygen_length', 5)
        
        @property
        def max_floors(self):
            return getattr(self.scene, 'citygen_max_floors', 8)
        
        @property
        def road_width(self):
            return getattr(self.scene, 'citygen_road_width', 4.0)
            
        @property 
        def buildings_per_block(self):
            return getattr(self.scene, 'citygen_buildings_per_block', 3)
            
        @property
        def sidewalk_width(self):
            return getattr(self.scene, 'citygen_sidewalk_width', 1.5)
            
        @property
        def organic_mode(self):
            return getattr(self.scene, 'citygen_organic_mode', False)
            
        @property
        def building_variety(self):
            return getattr(self.scene, 'citygen_building_variety', 'MEDIUM')
            
        @property
        def road_curve_intensity(self):
            return getattr(self.scene, 'citygen_road_curve_intensity', 0.5)
            
        @property
        def plaza_frequency(self):
            return getattr(self.scene, 'citygen_plaza_frequency', 0.1)
            
        @property
        def landmark_frequency(self):
            return getattr(self.scene, 'citygen_landmark_frequency', 0.05)
            
        @property
        def urban_furniture(self):
            return getattr(self.scene, 'citygen_urban_furniture', True)
            
        @property
        def building_aging(self):
            return getattr(self.scene, 'citygen_building_aging', 0.2)
            
        @property
        def density_variation(self):
            return getattr(self.scene, 'citygen_density_variation', True)
            
        @property
        def block_size_variation(self):
            return getattr(self.scene, 'citygen_block_size_variation', 0.3)
            
        @property
        def seamless_roads(self):
            return getattr(self.scene, 'citygen_seamless_roads', True)
            
        @property
        def height_variation(self):
            return getattr(self.scene, 'citygen_height_variation', 0.5)
            
        @property
        def age_variation(self):
            return getattr(self.scene, 'citygen_age_variation', 0.3)
            
        @property
        def mixed_use(self):
            return getattr(self.scene, 'citygen_mixed_use', True)
            
        @property
        def street_life(self):
            return getattr(self.scene, 'citygen_street_life', True)
            
        @property
        def weathering(self):
            return getattr(self.scene, 'citygen_weathering', 0.2)
            
        @property
        def irregular_lots(self):
            return getattr(self.scene, 'citygen_irregular_lots', False)
            
        @property
        def growth_pattern(self):
            return getattr(self.scene, 'citygen_growth_pattern', 'ORGANIC')
    
    return PropertyAccessor(context.scene)

class CITYGEN_OT_Generate(bpy.types.Operator):
    bl_idname = "citygen.generate_city"
    bl_label = "Générer Quartier"
    bl_description = "Génère un quartier complet avec bâtiments, routes et trottoirs"
    bl_options = {'REGISTER', 'UNDO'}
    
    def execute(self, context):
        try:
            # Validation préliminaire du contexte
            if not context:
                self.report({'ERROR'}, "Contexte Blender invalide")
                return {'CANCELLED'}
            
            # Vérifier le mode de génération
            organic_mode = getattr(context.scene, 'citygen_organic_mode', False)
            road_first_method = getattr(context.scene, 'citygen_road_first_method', True)
            
            # Import différé pour éviter les crashes de chargement
            try:
                if organic_mode and road_first_method:
                    # Nouvelle approche : routes d'abord - fonction intégrée
                    from .generator import generate_road_network_first
                    print("🛣️ NOUVEAU MODE ORGANIQUE: Routes d'abord, puis blocs")
                elif organic_mode and not road_first_method:
                    # Ancienne approche organique
                    from .generator import generate_organic_city_layout
                    print("🌿 ANCIEN MODE ORGANIQUE: Blocs polygonaux puis routes")
                else:
                    from .generator import generate_city
                    print("🏙️ MODE STANDARD: Utilisation de generate_city")
            except Exception as import_error:
                self.report({'ERROR'}, f"Impossible d'importer le générateur: {import_error}")
                return {'CANCELLED'}
            
            # Tentative de génération selon le mode
            if organic_mode and road_first_method:
                print("🚀 OPÉRATEUR: Appel generate_road_network_first")
                success = generate_road_network_first(context)
            elif organic_mode and not road_first_method:
                print("🚀 OPÉRATEUR: Appel generate_organic_city_layout (ancien)")
                success = generate_organic_city_layout(context)
            else:
                print("🚀 OPÉRATEUR: Appel generate_city avec regen_only=False EXPLICITE")
                success = generate_city(context, regen_only=False)
            
            if success:
                mode_text = "organique" if organic_mode else "standard"
                method_text = " (routes→blocs)" if (organic_mode and road_first_method) else ""
                self.report({'INFO'}, f"Quartier {mode_text}{method_text} généré avec succès!")
                return {'FINISHED'}
            else:
                self.report({'ERROR'}, "Échec de la génération de ville")
                return {'CANCELLED'}
                
        except Exception as e:
            error_msg = f"Erreur lors de la génération: {str(e)}"
            print(f"❌ {error_msg}")
            print(f"Traceback: {traceback.format_exc()}")
            self.report({'ERROR'}, error_msg)
            return {'CANCELLED'}

class CITYGEN_OT_Clear(bpy.types.Operator):
    bl_idname = "citygen.clear_city"
    bl_label = "Nettoyer Scène"
    bl_description = "Supprime tous les objets générés par le city generator"
    bl_options = {'REGISTER', 'UNDO'}
    
    def execute(self, context):
        try:
            # Liste des préfixes d'objets à supprimer
            prefixes_to_remove = [
                "Building_", "Road_", "Sidewalk_", "Block_", "Plaza_", "Landmark_",
                "StreetLight_", "Bench_", "Tree_", "Car_", "Fountain_",
                "OrganicRoad_", "OrganicBlock_", "Block_Zone_"
            ]
            
            # Compter les objets supprimés
            removed_count = 0
            
            # Collecter les objets à supprimer
            objects_to_remove = []
            for obj in bpy.data.objects:
                if any(obj.name.startswith(prefix) for prefix in prefixes_to_remove):
                    objects_to_remove.append(obj)
            
            # Supprimer les objets
            for obj in objects_to_remove:
                try:
                    bpy.data.objects.remove(obj, do_unlink=True)
                    removed_count += 1
                except Exception as e:
                    print(f"Erreur lors de la suppression de {obj.name}: {e}")
            
            # Nettoyer les données orphelines
            bpy.ops.outliner.orphans_purge(
                do_local_ids=True, do_linked_ids=True, do_recursive=True
            )
            
            message = f"{removed_count} objets de ville supprimés"
            print(f"✅ {message}")
            self.report({'INFO'}, message)
            return {'FINISHED'}
            
        except Exception as e:
            error_msg = f"Erreur lors du nettoyage: {str(e)}"
            print(f"❌ {error_msg}")
            self.report({'ERROR'}, error_msg)
            return {'CANCELLED'}

class CITYGEN_OT_RegenerateBuildings(bpy.types.Operator):
    bl_idname = "citygen.regenerate_buildings"
    bl_label = "Régénérer Bâtiments"
    bl_description = "Régénère uniquement les bâtiments en gardant les routes"
    bl_options = {'REGISTER', 'UNDO'}
    
    def execute(self, context):
        try:
            # Import différé
            from .generator import generate_city
            
            print("🏢 RÉGÉNÉRATION: Appel generate_city avec regen_only=True")
            success = generate_city(context, regen_only=True)
            
            if success:
                self.report({'INFO'}, "Bâtiments régénérés avec succès!")
                return {'FINISHED'}
            else:
                self.report({'ERROR'}, "Échec de la régénération des bâtiments")
                return {'CANCELLED'}
                
        except Exception as e:
            error_msg = f"Erreur lors de la régénération: {str(e)}"
            print(f"❌ {error_msg}")
            print(f"Traceback: {traceback.format_exc()}")
            self.report({'ERROR'}, error_msg)
            return {'CANCELLED'}

class CITYGEN_OT_RegenerateRoadsSidewalks(bpy.types.Operator):
    bl_idname = "citygen.regenerate_roads_sidewalks"
    bl_label = "Régénérer Routes et Trottoirs"
    bl_description = "Régénère uniquement les routes et trottoirs en gardant les bâtiments"
    bl_options = {'REGISTER', 'UNDO'}
    
    def execute(self, context):
        try:
            # Supprimer les routes et trottoirs existants
            prefixes_roads = ["Road_", "Sidewalk_", "OrganicRoad_"]
            removed_count = 0
            
            # Collecter les objets à supprimer
            objects_to_remove = []
            for obj in bpy.data.objects:
                if any(obj.name.startswith(prefix) for prefix in prefixes_roads):
                    objects_to_remove.append(obj)
            
            # Supprimer les objets
            for obj in objects_to_remove:
                try:
                    bpy.data.objects.remove(obj, do_unlink=True)
                    removed_count += 1
                except Exception as e:
                    print(f"Erreur lors de la suppression de {obj.name}: {e}")
            
            print(f"🛣️ {removed_count} routes/trottoirs supprimés")
            
            # Régénérer complètement (pas de paramètre roads_only disponible)
            from .generator import generate_city
            success = generate_city(context, regen_only=False)
            
            if success:
                self.report({'INFO'}, f"Routes et trottoirs régénérés! ({removed_count} supprimés)")
                return {'FINISHED'}
            else:
                self.report({'ERROR'}, "Échec de la régénération des routes")
                return {'CANCELLED'}
                
        except Exception as e:
            error_msg = f"Erreur lors de la régénération des routes: {str(e)}"
            print(f"❌ {error_msg}")
            print(f"Traceback: {traceback.format_exc()}")
            self.report({'ERROR'}, error_msg)
            return {'CANCELLED'}

class CITYGEN_OT_Diagnostic(bpy.types.Operator):
    bl_idname = "citygen.diagnostic"
    bl_label = "Diagnostic Système"
    bl_description = "Affiche des informations de diagnostic sur l'addon"
    bl_options = {'REGISTER'}
    
    def execute(self, context):
        try:
            print("=== DIAGNOSTIC CITY BLOCK GENERATOR ===")
            
            # Vérifier les propriétés
            scene = context.scene
            required_props = [
                'citygen_width', 'citygen_length', 'citygen_max_floors', 'citygen_road_width', 
                'citygen_buildings_per_block', 'citygen_seamless_roads', 'citygen_building_variety', 
                'citygen_height_variation', 'citygen_organic_mode', 'citygen_road_first_method'
            ]
            
            missing_props = [prop for prop in required_props if not hasattr(scene, prop)]
            
            if missing_props:
                print(f"❌ Propriétés manquantes: {missing_props}")
                self.report({'ERROR'}, f"Propriétés manquantes: {len(missing_props)}")
            else:
                print("✅ Toutes les propriétés principales sont présentes")
            
            # Vérifier les objets existants
            city_objects = []
            prefixes = ["Building_", "Road_", "Sidewalk_", "Block_", "OrganicRoad_", "Block_Zone_"]
            
            for obj in bpy.data.objects:
                if any(obj.name.startswith(prefix) for prefix in prefixes):
                    city_objects.append(obj)
            
            print(f"🏙️ Objets de ville trouvés: {len(city_objects)}")
            
            # Statistiques par type
            for prefix in prefixes:
                count = len([obj for obj in city_objects if obj.name.startswith(prefix)])
                if count > 0:
                    print(f"   {prefix}: {count}")
            
            # Paramètres actuels
            print("📊 Paramètres actuels:")
            print(f"   Grille: {getattr(scene, 'citygen_width', 'N/A')}x{getattr(scene, 'citygen_length', 'N/A')}")
            print(f"   Mode organique: {getattr(scene, 'citygen_organic_mode', 'N/A')}")
            print(f"   Routes d'abord: {getattr(scene, 'citygen_road_first_method', 'N/A')}")
            
            message = f"Diagnostic terminé. {len(city_objects)} objets trouvés"
            print(f"✅ {message}")
            self.report({'INFO'}, message)
            return {'FINISHED'}
            
        except Exception as e:
            error_msg = f"Erreur diagnostic: {str(e)}"
            print(f"❌ {error_msg}")
            print(f"Traceback: {traceback.format_exc()}")
            self.report({'ERROR'}, error_msg)
            return {'CANCELLED'}

# Propriétés principales
def get_city_properties():
    """Retourne un dictionnaire avec toutes les propriétés du city generator"""
    return {
        'citygen_width': bpy.props.IntProperty(
            name="Largeur",
            description="Nombre de blocs en largeur",
            default=5,
            min=1,
            max=50
        ),
        'citygen_length': bpy.props.IntProperty(
            name="Longueur", 
            description="Nombre de blocs en longueur",
            default=5,
            min=1,
            max=50
        ),
        'citygen_max_floors': bpy.props.IntProperty(
            name="Étages Maximum",
            description="Nombre maximum d'étages pour les bâtiments",
            default=8,
            min=1,
            max=50
        ),
        'citygen_road_width': bpy.props.FloatProperty(
            name="Largeur Route",
            description="Largeur des routes",
            default=4.0,
            min=1.0,
            max=10.0
        ),
        'citygen_buildings_per_block': bpy.props.IntProperty(
            name="Bâtiments par Bloc",
            description="Nombre de bâtiments par bloc",
            default=3,
            min=1,
            max=10
        ),
        'citygen_sidewalk_width': bpy.props.FloatProperty(
            name="Largeur Trottoir",
            description="Largeur des trottoirs",
            default=1.5,
            min=0.5,
            max=3.0
        ),
        'citygen_organic_mode': bpy.props.BoolProperty(
            name="Mode Organique",
            description="Active la génération organique avec formes irrégulières",
            default=True  # ACTIVÉ PAR DÉFAUT pour le système ultra-organique
        ),
        'citygen_road_first_method': bpy.props.BoolProperty(
            name="Méthode Routes d'Abord",
            description="Génère d'abord les routes, puis remplit les espaces avec des blocs (recommandé)",
            default=True
        ),
        'citygen_building_variety': bpy.props.EnumProperty(
            name="Variété Bâtiments",
            description="Niveau de variété dans les bâtiments",
            items=[
                ('LOW', "Faible", "Formes similaires"),
                ('MEDIUM', "Moyen", "Quelques variations"),
                ('HIGH', "Élevé", "Très variés"),
                ('EXTREME', "Extrême", "Maximum de diversité")
            ],
            default='MEDIUM'
        ),
        'citygen_road_curve_intensity': bpy.props.FloatProperty(
            name="Intensité Courbes Routes",
            description="Intensité des courbes dans les routes organiques",
            default=0.5,
            min=0.0,
            max=2.0
        ),
        'citygen_plaza_frequency': bpy.props.FloatProperty(
            name="Fréquence Places",
            description="Probabilité d'avoir des places publiques",
            default=0.1,
            min=0.0,
            max=1.0
        ),
        'citygen_landmark_frequency': bpy.props.FloatProperty(
            name="Fréquence Monuments",
            description="Probabilité d'avoir des monuments/landmarks",
            default=0.05,
            min=0.0,
            max=0.5
        ),
        'citygen_urban_furniture': bpy.props.BoolProperty(
            name="Mobilier Urbain",
            description="Ajoute lampadaires, bancs, arbres, etc.",
            default=True
        ),
        'citygen_building_aging': bpy.props.FloatProperty(
            name="Vieillissement Bâtiments",
            description="Facteur de vieillissement (0=neuf, 1=très vieux)",
            default=0.2,
            min=0.0,
            max=1.0
        ),
        'citygen_density_variation': bpy.props.BoolProperty(
            name="Variation Densité",
            description="Varie la densité selon les zones (centre/périphérie)",
            default=True
        ),
        'citygen_block_size_variation': bpy.props.FloatProperty(
            name="Variation Taille Blocs",
            description="Variation de taille des blocs (0=uniforme, 1=très varié)",
            default=0.3,
            min=0.0,
            max=1.0
        ),
        # Propriétés supplémentaires pour l'interface utilisateur
        'citygen_seamless_roads': bpy.props.BoolProperty(
            name="Routes Collées",
            description="Routes parfaitement collées aux blocs sans espaces",
            default=True
        ),
        'citygen_height_variation': bpy.props.FloatProperty(
            name="Variation Hauteur",
            description="Variation de hauteur des bâtiments",
            default=0.5,
            min=0.0,
            max=1.0
        ),
        'citygen_age_variation': bpy.props.FloatProperty(
            name="Variation Âge",
            description="Variation d'âge des bâtiments",
            default=0.3,
            min=0.0,
            max=1.0
        ),
        'citygen_mixed_use': bpy.props.BoolProperty(
            name="Usage Mixte",
            description="Mélange résidentiel et commercial",
            default=True
        ),
        'citygen_street_life': bpy.props.BoolProperty(
            name="Vie de Rue",
            description="Ajoute de la vie dans les rues (voitures, piétons)",
            default=True
        ),
        'citygen_weathering': bpy.props.FloatProperty(
            name="Vieillissement",
            description="Niveau de vieillissement des bâtiments",
            default=0.2,
            min=0.0,
            max=1.0
        ),
        'citygen_irregular_lots': bpy.props.BoolProperty(
            name="Lots Irréguliers",
            description="Utilise des formes de lots irrégulières",
            default=False
        ),
        'citygen_growth_pattern': bpy.props.EnumProperty(
            name="Modèle de Croissance",
            description="Modèle de croissance urbaine",
            items=[
                ('ORGANIC', "Organique", "Croissance naturelle"),
                ('PLANNED', "Planifié", "Développement planifié"),
                ('MIXED', "Mixte", "Combinaison des deux")
            ],
            default='ORGANIC'
        )
    }

# Liste des classes à enregistrer
classes = [
    CITYGEN_OT_Generate,
    CITYGEN_OT_Clear,
    CITYGEN_OT_RegenerateBuildings,
    CITYGEN_OT_RegenerateRoadsSidewalks,
    CITYGEN_OT_Diagnostic,
]

def register():
    """Enregistre les classes et propriétés avec gestion d'erreurs robuste"""
    try:
        print("=== Début d'enregistrement City Block Generator ===")
        
        # Enregistrer chaque classe individuellement
        for cls in classes:
            try:
                bpy.utils.register_class(cls)
                print(f"Classe {cls.__name__} enregistrée avec succès")
            except Exception as e:
                print(f"ERREUR lors de l'enregistrement de {cls.__name__}: {str(e)}")
                # Continue with other classes
        
        # Enregistrer les propriétés
        try:
            city_props = get_city_properties()
            for prop_name, prop_def in city_props.items():
                if not hasattr(bpy.types.Scene, prop_name):
                    setattr(bpy.types.Scene, prop_name, prop_def)
                    print(f"Propriété {prop_name} enregistrée")
                else:
                    print(f"Propriété {prop_name} déjà présente")
        except Exception as e:
            print(f"ERREUR lors de l'enregistrement des propriétés: {str(e)}")
        
        print("=== City Block Generator: Enregistrement terminé ===")
        
    except Exception as e:
        print(f"❌ ERREUR CRITIQUE lors de l'enregistrement: {str(e)}")
        print(f"Traceback: {traceback.format_exc()}")

def unregister():
    """Désenregistre les classes avec gestion d'erreurs robuste"""
    try:
        print("=== Début de désenregistrement City Block Generator ===")
        
        # Désenregistrer les propriétés
        try:
            city_props = get_city_properties()
            for prop_name in city_props.keys():
                if hasattr(bpy.types.Scene, prop_name):
                    delattr(bpy.types.Scene, prop_name)
                    print(f"Propriété {prop_name} désenregistrée")
        except Exception as e:
            print(f"Erreur lors du désenregistrement des propriétés: {e}")
        
        # Désenregistrer chaque classe individuellement
        for cls in reversed(classes):
            try:
                bpy.utils.unregister_class(cls)
                print(f"Classe {cls.__name__} désenregistrée avec succès")
            except Exception as e:
                print(f"ERREUR lors du désenregistrement de {cls.__name__}: {str(e)}")
        
        print("=== City Block Generator: Désenregistrement terminé ===")
        
    except Exception as e:
        print(f"ERREUR CRITIQUE lors du désenregistrement: {str(e)}")
        print(f"Traceback: {traceback.format_exc()}")

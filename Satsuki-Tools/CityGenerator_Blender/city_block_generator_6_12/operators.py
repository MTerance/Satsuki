import bpy
import traceback
from .generator import generate_city, regenerate_roads_and_sidewalks

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
            
            if not hasattr(context.scene, 'citygen_props'):
                self.report({'ERROR'}, "Propriétés City Generator non initialisées")
                return {'CANCELLED'}
            
            # Tentative de génération
            success = generate_city(context)
            
            if success:
                self.report({'INFO'}, "Quartier généré avec succès")
                return {'FINISHED'}
            else:
                self.report({'ERROR'}, "Échec de la génération du quartier")
                return {'CANCELLED'}
                
        except Exception as e:
            error_msg = f"Erreur lors de la génération: {str(e)}"
            print(f"ERREUR CRITIQUE dans CITYGEN_OT_Generate: {error_msg}")
            print(f"Traceback: {traceback.format_exc()}")
            self.report({'ERROR'}, error_msg)
            return {'CANCELLED'}

class CITYGEN_OT_RegenRoads(bpy.types.Operator):
    bl_idname = "citygen.regenerate_roads_sidewalks"
    bl_label = "Régénérer Routes + Trottoirs"
    bl_description = "Régénère seulement les routes et trottoirs en gardant les bâtiments"
    bl_options = {'REGISTER', 'UNDO'}
    
    def execute(self, context):
        try:
            # Validation préliminaire du contexte
            if not context:
                self.report({'ERROR'}, "Contexte Blender invalide")
                return {'CANCELLED'}
            
            if not hasattr(context.scene, 'citygen_props'):
                self.report({'ERROR'}, "Propriétés City Generator non initialisées")
                return {'CANCELLED'}
            
            # Tentative de régénération
            success = regenerate_roads_and_sidewalks(context)
            
            if success:
                self.report({'INFO'}, "Routes et trottoirs régénérés avec succès")
                return {'FINISHED'}
            else:
                self.report({'ERROR'}, "Échec de la régénération des routes et trottoirs")
                return {'CANCELLED'}
                
        except Exception as e:
            error_msg = f"Erreur lors de la régénération: {str(e)}"
            print(f"ERREUR CRITIQUE dans CITYGEN_OT_RegenRoads: {error_msg}")
            print(f"Traceback: {traceback.format_exc()}")
            self.report({'ERROR'}, error_msg)
            return {'CANCELLED'}

class CITYGEN_OT_ResetProperties(bpy.types.Operator):
    bl_idname = "citygen.reset_properties"
    bl_label = "Réinitialiser Paramètres"
    bl_description = "Remet les paramètres aux valeurs par défaut"
    bl_options = {'REGISTER', 'UNDO'}
    
    def execute(self, context):
        try:
            if not hasattr(context.scene, 'citygen_props'):
                self.report({'ERROR'}, "Propriétés City Generator non initialisées")
                return {'CANCELLED'}
            
            props = context.scene.citygen_props
            props.width = 5
            props.length = 5
            props.max_floors = 8
            props.shape_mode = 'AUTO'
            props.block_variety = 'MEDIUM'
            props.base_block_size = 10.0
            props.district_mode = True
            props.commercial_ratio = 0.2
            props.residential_ratio = 0.6
            props.industrial_ratio = 0.2
            
            self.report({'INFO'}, "Paramètres réinitialisés aux valeurs par défaut")
            return {'FINISHED'}
            
        except Exception as e:
            error_msg = f"Erreur lors de la réinitialisation: {str(e)}"
            print(f"ERREUR CRITIQUE dans CITYGEN_OT_ResetProperties: {error_msg}")
            self.report({'ERROR'}, error_msg)
            return {'CANCELLED'}

class CityGenProperties(bpy.types.PropertyGroup):
    # Propriétés sans fonctions de validation pour éviter les PropertyDeferred
    
    width = bpy.props.IntProperty(
        name="Largeur", 
        description="Largeur de la grille de ville (1-50)",
        default=5, 
        min=1, 
        max=50
    )
    
    length = bpy.props.IntProperty(
        name="Longueur", 
        description="Longueur de la grille de ville (1-50)",
        default=5, 
        min=1, 
        max=50
    )
    
    max_floors = bpy.props.IntProperty(
        name="Étages max", 
        description="Nombre maximum d'étages pour les bâtiments (1-100)",
        default=8, 
        min=1, 
        max=100
    )
    
    shape_mode = bpy.props.EnumProperty(
        name="Forme",
        description="Mode de forme des bâtiments",
        items=[
            ('AUTO', "Auto (selon position)", "Formes automatiques basées sur la position"),
            ('RECT', "Rectangle", "Bâtiments rectangulaires uniquement"),
            ('L', "Forme L", "Bâtiments en forme de L"),
            ('U', "Forme U", "Bâtiments en forme de U"),
            ('T', "Forme T", "Bâtiments en forme de T"),
            ('CIRC', "Cercle", "Bâtiments circulaires"),
            ('ELLIPSE', "Ellipse", "Bâtiments elliptiques"),
        ],
        default='AUTO'
    )
    
    # Nouvelles propriétés pour la variété des blocs
    block_variety = bpy.props.EnumProperty(
        name="Variété des blocs",
        description="Niveau de variété dans les tailles de blocs",
        items=[
            ('UNIFORM', "Uniforme", "Tous les blocs ont la même taille"),
            ('LOW', "Faible", "Variation de 80% à 120% de la taille de base"),
            ('MEDIUM', "Moyenne", "Variation de 60% à 140% de la taille de base"),
            ('HIGH', "Élevée", "Variation de 40% à 160% de la taille de base"),
            ('EXTREME', "Extrême", "Variation de 25% à 200% de la taille de base"),
            ('DISTRICTS', "Quartiers", "Zones distinctes avec tailles similaires"),
        ],
        default='MEDIUM'
    )
    
    base_block_size = bpy.props.FloatProperty(
        name="Taille de bloc de base",
        description="Taille de base des blocs en unités Blender",
        default=10.0,
        min=2.0,
        max=50.0
    )
    
    district_mode = bpy.props.BoolProperty(
        name="Mode quartiers",
        description="Crée des zones distinctes avec des caractéristiques différentes",
        default=True
    )
    
    commercial_ratio = bpy.props.FloatProperty(
        name="Ratio commercial",
        description="Pourcentage de blocs commerciaux (plus grands)",
        default=0.2,
        min=0.0,
        max=1.0
    )
    
    residential_ratio = bpy.props.FloatProperty(
        name="Ratio résidentiel",
        description="Pourcentage de blocs résidentiels (taille moyenne)",
        default=0.6,
        min=0.0,
        max=1.0
    )
    
    industrial_ratio = bpy.props.FloatProperty(
        name="Ratio industriel",
        description="Pourcentage de blocs industriels (très grands, peu d'étages)",
        default=0.2,
        min=0.0,
        max=1.0
    )

classes = [CITYGEN_OT_Generate, CITYGEN_OT_RegenRoads, CITYGEN_OT_ResetProperties, CityGenProperties]

def register():
    """Enregistre les classes avec gestion d'erreurs robuste"""
    try:
        print("=== Début d'enregistrement City Block Generator ===")
        
        # Enregistrer chaque classe individuellement avec gestion d'erreurs
        for cls in classes:
            try:
                bpy.utils.register_class(cls)
                print(f"Classe {cls.__name__} enregistrée avec succès")
            except Exception as e:
                print(f"ERREUR lors de l'enregistrement de {cls.__name__}: {str(e)}")
                print(f"Traceback: {traceback.format_exc()}")
                # Continuer avec les autres classes
        
        # Enregistrer les propriétés avec gestion d'erreurs
        try:
            bpy.types.Scene.citygen_props = bpy.props.PointerProperty(type=CityGenProperties)
            print("Propriétés citygen_props enregistrées avec succès")
            
            # Forcer l'initialisation des valeurs par défaut pour la scène active
            if bpy.context.scene:
                props = bpy.context.scene.citygen_props
                # Forcer les valeurs par défaut
                props.width = 5
                props.length = 5
                props.max_floors = 8
                props.shape_mode = 'AUTO'
                props.block_variety = 'MEDIUM'
                props.base_block_size = 10.0
                props.district_mode = False
                props.commercial_ratio = 0.2
                props.residential_ratio = 0.6
                props.industrial_ratio = 0.2
                print("Valeurs par défaut forcées pour la scène active")
                
            # Initialiser également pour toutes les scènes existantes
            for scene in bpy.data.scenes:
                try:
                    if hasattr(scene, 'citygen_props'):
                        props = scene.citygen_props
                        props.width = 5
                        props.length = 5
                        props.max_floors = 8
                        props.shape_mode = 'AUTO'
                except Exception as e:
                    print(f"Erreur initialisation scène {scene.name}: {e}")
                        
        except Exception as e:
            print(f"ERREUR lors de l'enregistrement des propriétés: {str(e)}")
            print(f"Traceback: {traceback.format_exc()}")
        
        print("=== City Block Generator: Enregistrement terminé ===")
        
    except Exception as e:
        print(f"ERREUR CRITIQUE lors de l'enregistrement: {str(e)}")
        print(f"Traceback: {traceback.format_exc()}")

def unregister():
    """Désenregistre les classes avec gestion d'erreurs robuste"""
    try:
        print("=== Début de désenregistrement City Block Generator ===")
        
        # Désenregistrer les propriétés avec gestion d'erreurs
        try:
            if hasattr(bpy.types.Scene, "citygen_props"):
                del bpy.types.Scene.citygen_props
                print("Propriétés citygen_props désenregistrées avec succès")
        except Exception as e:
            print(f"ERREUR lors du désenregistrement des propriétés: {str(e)}")
        
        # Désenregistrer chaque classe individuellement avec gestion d'erreurs
        for cls in reversed(classes):
            try:
                bpy.utils.unregister_class(cls)
                print(f"Classe {cls.__name__} désenregistrée avec succès")
            except Exception as e:
                print(f"ERREUR lors du désenregistrement de {cls.__name__}: {str(e)}")
                # Continuer avec les autres classes
        
        print("=== City Block Generator: Désenregistrement terminé ===")
        
    except Exception as e:
        print(f"ERREUR CRITIQUE lors du désenregistrement: {str(e)}")
        print(f"Traceback: {traceback.format_exc()}")
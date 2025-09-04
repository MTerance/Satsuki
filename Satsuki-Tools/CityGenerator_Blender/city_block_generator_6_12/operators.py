import bpy
import traceback
import sys
import importlib
# Import différé de generator pour éviter les crashes au chargement

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
            return getattr(self.scene, 'citygen_buildings_per_block', 1)
        
        @property
        def seamless_roads(self):
            return getattr(self.scene, 'citygen_seamless_roads', True)
        
        @property
        def building_variety(self):
            return getattr(self.scene, 'citygen_building_variety', 'MEDIUM')
        
        @property
        def height_variation(self):
            return getattr(self.scene, 'citygen_height_variation', 0.5)
    
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
            
            # Import différé pour éviter les crashes de chargement
            try:
                from .generator import generate_city
            except Exception as import_error:
                self.report({'ERROR'}, f"Impossible d'importer le générateur: {import_error}")
                return {'CANCELLED'}
            
            # Tentative de génération AVEC BÂTIMENTS (regen_only=False explicite)
            print("🚀 OPÉRATEUR: Appel generate_city avec regen_only=False EXPLICITE")
            success = generate_city(context, regen_only=False)
            
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
    bl_label = "Régénérer Routes et Trottoirs"
    bl_description = "Régénère uniquement les routes et trottoirs"
    bl_options = {'REGISTER', 'UNDO'}
    
    def execute(self, context):
        try:
            # Validation préliminaire du contexte
            if not context:
                self.report({'ERROR'}, "Contexte Blender invalide")
                return {'CANCELLED'}
            
            # Import différé pour éviter les crashes de chargement
            try:
                from .generator import regenerate_roads_and_sidewalks
            except Exception as import_error:
                self.report({'ERROR'}, f"Impossible d'importer le générateur: {import_error}")
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

class CITYGEN_OT_Diagnostic(bpy.types.Operator):
    bl_idname = "citygen.diagnostic"
    bl_label = "Diagnostic Addon"
    bl_description = "Effectue un diagnostic complet de l'addon"
    bl_options = {'REGISTER'}
    
    def execute(self, context):
        try:
            print("\n=== DIAGNOSTIC CITY BLOCK GENERATOR ===")
            
            # Vérification de base
            print("📋 Informations de base:")
            print(f"   • Version Blender: {bpy.app.version_string}")
            print(f"   • Scène active: {context.scene.name}")
            
            # Vérification des propriétés
            print("\n🔧 Vérification des propriétés:")
            props = get_citygen_properties(context)
            try:
                print(f"   • Largeur: {props.width}")
                print(f"   • Longueur: {props.length}")
                print(f"   • Étages max: {props.max_floors}")
                print(f"   • Largeur routes: {props.road_width}")
                print("   ✅ Toutes les propriétés accessibles")
            except Exception as e:
                print(f"   ❌ Erreur d'accès aux propriétés: {e}")
            
            print("=== FIN DIAGNOSTIC ===")
            self.report({'INFO'}, "Diagnostic terminé - voir console")
            return {'FINISHED'}
            
        except Exception as e:
            error_msg = f"Erreur durant le diagnostic: {str(e)}"
            print(f"❌ ERREUR DIAGNOSTIC: {error_msg}")
            self.report({'ERROR'}, error_msg)
            return {'CANCELLED'}

# SOLUTION ALTERNATIVE: Propriétés directes sans PropertyGroup
def get_city_properties():
    """Retourne les définitions de propriétés pour l'addon"""
    return {
        'citygen_width': bpy.props.IntProperty(
            name="Largeur", 
            description="Largeur de la grille de ville",
            default=5, 
            min=1, 
            max=50
        ),
        'citygen_length': bpy.props.IntProperty(
            name="Longueur", 
            description="Longueur de la grille de ville",
            default=5, 
            min=1, 
            max=50
        ),
        'citygen_max_floors': bpy.props.IntProperty(
            name="Étages max", 
            description="Nombre maximum d'étages",
            default=8, 
            min=1, 
            max=100
        ),
        'citygen_road_width': bpy.props.FloatProperty(
            name="Largeur des routes",
            description="Largeur des routes en unités Blender",
            default=4.0,
            min=0.5,
            max=20.0
        ),
        'citygen_buildings_per_block': bpy.props.IntProperty(
            name="Bâtiments par bloc",
            description="Nombre de bâtiments à générer par bloc",
            default=1,
            min=1,
            max=9
        ),
        'citygen_seamless_roads': bpy.props.BoolProperty(
            name="Routes collées",
            description="Coller les routes aux trottoirs (pas d'espace)",
            default=True
        ),
        'citygen_building_variety': bpy.props.EnumProperty(
            name="Variété des formes",
            description="Niveau de variété des formes de bâtiments",
            items=[
                ('LOW', 'Faible', 'Principalement rectangulaires'),
                ('MEDIUM', 'Moyenne', 'Mélange équilibré de formes'),
                ('HIGH', 'Élevée', 'Maximum de variété et formes complexes'),
                ('MODERN', 'Moderne', 'Tours et gratte-ciels'),
                ('CREATIVE', 'Créatif', 'Formes artistiques et uniques')
            ],
            default='MEDIUM'
        ),
        'citygen_height_variation': bpy.props.FloatProperty(
            name="Variation hauteur",
            description="Facteur de variation des hauteurs (0.0 = uniforme, 1.0 = très varié)",
            default=0.5,
            min=0.0,
            max=1.0
        )
    }

classes = [CITYGEN_OT_Generate, CITYGEN_OT_RegenRoads, CITYGEN_OT_Diagnostic]

def register():
    """Enregistre les classes avec gestion d'erreurs robuste - Version simplifiée"""
    try:
        print("=== Début d'enregistrement City Block Generator ===")
        
        # ÉTAPE 1: Enregistrer les propriétés directement sur Scene
        try:
            print("🔹 Enregistrement des propriétés directes...")
            city_props = get_city_properties()
            
            for prop_name, prop_def in city_props.items():
                setattr(bpy.types.Scene, prop_name, prop_def)
                print(f"   ✓ Propriété {prop_name} enregistrée")
            
            print("✅ Toutes les propriétés enregistrées avec succès")
                
        except Exception as e:
            print(f"❌ ERREUR CRITIQUE: Impossible d'enregistrer les propriétés: {e}")
            return
        
        # ÉTAPE 2: Enregistrer les classes (opérateurs, etc.)
        for i, cls in enumerate(classes):
            try:
                print(f"🔹 Enregistrement {cls.__name__}...")
                bpy.utils.register_class(cls)
                print(f"✅ {cls.__name__} enregistrée avec succès")
                
            except Exception as e:
                print(f"❌ ERREUR lors de l'enregistrement de {cls.__name__}: {str(e)}")
                # Continuer avec les autres classes
        
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

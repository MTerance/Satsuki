import bpy
import traceback

# Importer la fonction safe_int du module generator
from .generator import safe_int

class CITYGEN_PT_Panel(bpy.types.Panel):
    bl_label = "City Block Generator"
    bl_idname = "CITYGEN_PT_panel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'CityGen'

    def draw(self, context):
        """Interface utilisateur avec validation et feedback"""
        layout = self.layout
        
        try:
            # Créer les propriétés si elles n'existent pas
            if not hasattr(context.scene, 'citygen_props'):
                print("ERREUR: citygen_props manquant, tentative de création...")
                layout.label(text="Erreur: Propriétés manquantes", icon='ERROR')
                layout.operator("citygen.generate_city", text="Réinitialiser Addon")
                return
            
            props = context.scene.citygen_props
            
            # Interface des paramètres avec valeurs par défaut forcées
            box = layout.box()
            box.label(text="Paramètres:", icon='SETTINGS')
            
            # Affichage direct des propriétés avec valeurs visibles
            try:
                # Largeur
                row = box.row()
                row.label(text="Largeur:")
                row.prop(props, "width", text="")
                
                # Longueur  
                row = box.row()
                row.label(text="Longueur:")
                row.prop(props, "length", text="")
                
                # Étages maximum
                row = box.row()
                row.label(text="Étages max:")
                row.prop(props, "max_floors", text="")
                
                # Mode de forme
                row = box.row()
                row.label(text="Forme:")
                row.prop(props, "shape_mode", text="")
                
                # Nouvelle section pour la variété des blocs
                layout.separator()
                variety_box = layout.box()
                variety_box.label(text="Variété des blocs:", icon='MOD_ARRAY')
                
                # Taille de base
                row = variety_box.row()
                row.label(text="Taille de base:")
                row.prop(props, "base_block_size", text="")
                
                # Variété
                row = variety_box.row()
                row.label(text="Variété:")
                row.prop(props, "block_variety", text="")
                
                # Mode quartiers - Plus visible avec icône et séparateur
                variety_box.separator()
                row = variety_box.row()
                row.label(text="Mode quartiers:", icon='GROUP')
                row = variety_box.row()
                row.prop(props, "district_mode", text="Activer les zones distinctes", toggle=True)
                
                # Ratios des types de zones (si mode quartiers activé)
                if props.district_mode:
                    variety_box.separator()
                    variety_box.label(text="Configuration des zones:", icon='SETTINGS')
                    
                    # Commercial
                    row = variety_box.row()
                    row.label(text="🏢 Commercial:")
                    row.prop(props, "commercial_ratio", text="", slider=True)
                    
                    # Résidentiel
                    row = variety_box.row()
                    row.label(text="🏠 Résidentiel:")
                    row.prop(props, "residential_ratio", text="", slider=True)
                    
                    # Industriel
                    row = variety_box.row()
                    row.label(text="🏭 Industriel:")
                    row.prop(props, "industrial_ratio", text="", slider=True)
                    
                    # Information sur les matériaux
                    variety_box.separator()
                    info_row = variety_box.row()
                    info_row.label(text="💡 Zones colorées automatiquement", icon='INFO')
                else:
                    # Message informatif quand mode district désactivé
                    variety_box.separator()
                    info_row = variety_box.row()
                    info_row.label(text="💡 Activez le mode quartiers pour les zones", icon='INFO')
                
            except Exception as e:
                print(f"Erreur affichage propriétés: {e}")
                box.label(text="Erreur propriétés", icon='ERROR')
                box.label(text="Valeurs par défaut: 5x5, 8 étages")
            
            # Section des actions
            layout.separator()
            action_box = layout.box()
            action_box.label(text="Actions:", icon='PLAY')
            
            # Boutons d'action
            col = action_box.column(align=True)
            col.scale_y = 1.2
            col.operator("citygen.generate_city", text="Générer Quartier", icon='MESH_CUBE')
            col.operator("citygen.regenerate_roads_sidewalks", text="Régénérer Routes", icon='MOD_BUILD')
            col.separator()
            col.operator("citygen.reset_properties", text="Réinitialiser Paramètres", icon='LOOP_BACK')
            
            # Informations basiques
            layout.separator()
            info_box = layout.box()
            info_box.label(text="Conseils:", icon='INFO')
            info_box.label(text="• Grilles > 10x10 = lent")
            info_box.label(text="• Sauvegardez avant génération")
            
        except Exception as e:
            # Interface d'erreur de secours ultra-simple
            layout.alert = True
            layout.label(text="ERREUR INTERFACE", icon='ERROR')
            layout.separator()
            layout.operator("citygen.generate_city", text="Essayer la génération")
            layout.separator()
            layout.label(text="Erreur:", icon='CANCEL')
            error_text = str(e)[:30] + "..." if len(str(e)) > 30 else str(e)
            layout.label(text=error_text)
            print(f"ERREUR UI City Generator: {str(e)}")
            print(f"Traceback: {traceback.format_exc()}")

classes = [CITYGEN_PT_Panel]

def register():
    """Enregistre l'interface avec gestion d'erreurs"""
    try:
        for cls in classes:
            bpy.utils.register_class(cls)
            print(f"Interface {cls.__name__} enregistrée avec succès")
    except Exception as e:
        print(f"ERREUR lors de l'enregistrement de l'interface: {str(e)}")
        print(f"Traceback: {traceback.format_exc()}")

def unregister():
    """Désenregistre l'interface avec gestion d'erreurs"""
    try:
        for cls in reversed(classes):
            bpy.utils.unregister_class(cls)
            print(f"Interface {cls.__name__} désenregistrée avec succès")
    except Exception as e:
        print(f"ERREUR lors du désenregistrement de l'interface: {str(e)}")
        print(f"Traceback: {traceback.format_exc()}")
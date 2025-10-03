import bpy
from bpy.types import Panel

class CITYGEN_PT_Panel(Panel):
    bl_label = "City Block Generator"
    bl_idname = "CITYGEN_PT_Panel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "CityGen"

    def draw(self, context):
        """Interface utilisateur simplifiée avec propriétés directes"""
        layout = self.layout
        scene = context.scene
        
        # Vérifier l'existence des propriétés directes
        required_props = [
            'citygen_width', 'citygen_length', 'citygen_max_floors', 'citygen_road_width', 
            'citygen_buildings_per_block', 'citygen_seamless_roads', 'citygen_building_variety', 
            'citygen_height_variation', 'citygen_organic_mode', 'citygen_road_first_method',
            'citygen_density_variation', 'citygen_age_variation', 'citygen_mixed_use', 
            'citygen_landmark_frequency', 'citygen_plaza_frequency', 'citygen_street_life', 
            'citygen_weathering', 'citygen_irregular_lots', 'citygen_growth_pattern'
        ]
        missing_props = [prop for prop in required_props if not hasattr(scene, prop)]
        
        if missing_props:
            layout.alert = True
            layout.label(text="Propriétés non initialisées", icon='ERROR')
            layout.label(text="Redémarrez Blender ou rechargez l'addon")
            return
        
        # Interface des paramètres de base
        layout.label(text="Paramètres de génération:", icon='SETTINGS')
        
        # ⚠️ AVERTISSEMENTS DE SÉCURITÉ
        total_blocks = scene.citygen_width * scene.citygen_length
        total_buildings = total_blocks * scene.citygen_buildings_per_block
        
        # Vérifications de sécurité
        if total_blocks > 25:
            warning_box = layout.box()
            warning_box.alert = True
            warning_box.label(text="⚠️ ATTENTION: Configuration dangereuse!", icon='ERROR')
            warning_box.label(text=f"Blocs: {total_blocks} (MAX recommandé: 25)")
            warning_box.label(text="Réduisez largeur/longueur pour éviter crashes")
        elif total_buildings > 35:
            warning_box = layout.box()
            warning_box.alert = True
            warning_box.label(text="⚠️ PERFORMANCE: Beaucoup de bâtiments", icon='INFO')
            warning_box.label(text=f"Bâtiments: {total_buildings} (MAX recommandé: 35)")
        else:
            # Indication sécurisée
            safe_box = layout.box()
            safe_box.label(text=f"✅ Configuration sûre: {total_blocks} blocs, {total_buildings} bâtiments", icon='CHECKMARK')
        
        layout.separator()
        
        # Grille des paramètres
        grid = layout.grid_flow(columns=2, align=True)
        
        # Largeur et longueur
        grid.prop(scene, "citygen_width", text="Largeur")
        grid.prop(scene, "citygen_length", text="Longueur")
        
        # Étages et routes
        grid.prop(scene, "citygen_max_floors", text="Étages max")
        grid.prop(scene, "citygen_road_width", text="Routes")
        
        # Nouveaux paramètres
        grid.prop(scene, "citygen_buildings_per_block", text="Bât./Bloc")
        grid.prop(scene, "citygen_seamless_roads", text="Routes collées")
        
        layout.separator()
        
        # Section variété des bâtiments
        layout.label(text="Variété des bâtiments:", icon='HOME')
        
        # Paramètres de variété
        variety_grid = layout.grid_flow(columns=1, align=True)
        variety_grid.prop(scene, "citygen_building_variety", text="Formes")
        variety_grid.prop(scene, "citygen_height_variation", text="Hauteurs")
        
        layout.separator()
        
        # Section Mode Organique
        layout.label(text="Mode Organique:", icon='OUTLINER_OB_MESH')
        organic_box = layout.box()
        organic_box.prop(scene, "citygen_organic_mode", text="Activer Mode Organique")
        
        # Afficher les contrôles organiques seulement si le mode est activé
        if scene.citygen_organic_mode:
            organic_col = organic_box.column(align=True)
            
            # === NOUVELLE MÉTHODE ROUTES D'ABORD ===
            method_box = organic_col.box()
            method_col = method_box.column(align=True)
            method_col.label(text="🛣️ NOUVEAU : Méthode Routes d'Abord", icon='FORWARD')
            method_col.prop(scene, "citygen_road_first_method", text="Routes → Blocs → Bâtiments")
            
            if getattr(scene, 'citygen_road_first_method', True):
                method_col.label(text="✅ Routes créées en premier", icon='INFO')
                method_col.label(text="   Blocs générés dans les espaces")
            else:
                method_col.label(text="⚠️ Ancienne méthode (peut bugger)", icon='ERROR')
            
            organic_col.separator()
            
            # Contrôles pour les courbes et variations
            organic_col.label(text="Paramètres Organiques:")
            organic_col.prop(scene, "citygen_road_curve_intensity", text="Courbes Routes")
            organic_col.prop(scene, "citygen_block_size_variation", text="Variation Blocs")
            organic_col.prop(scene, "citygen_growth_pattern", text="Croissance")
        
        layout.separator()
        
        # === SECTION RÉALISME URBAIN ===
        layout.label(text="Réalisme Urbain:", icon='WORLD')
        
        # Colonne principale réalisme
        realism_box = layout.box()
        realism_col = realism_box.column(align=True)
        
        # Paramètres de densité et variation
        realism_col.label(text="Densité et Variation:")
        density_grid = realism_col.grid_flow(columns=2, align=True)
        density_grid.prop(scene, "citygen_density_variation", text="Densité")
        density_grid.prop(scene, "citygen_weathering", text="Usure")
        
        # Options booléennes
        realism_col.separator(factor=0.5)
        realism_col.label(text="Options Réalisme:")
        bool_grid = realism_col.grid_flow(columns=2, align=True)
        bool_grid.prop(scene, "citygen_age_variation", text="Âges Variés")
        bool_grid.prop(scene, "citygen_mixed_use", text="Zones Mixtes")
        bool_grid.prop(scene, "citygen_irregular_lots", text="Parcelles Irrég.")
        bool_grid.prop(scene, "citygen_street_life", text="Vie de Rue")
        
        # Fréquences
        realism_col.separator(factor=0.5)
        realism_col.label(text="Fréquences:")
        freq_grid = realism_col.grid_flow(columns=2, align=True)
        freq_grid.prop(scene, "citygen_landmark_frequency", text="Monuments")
        freq_grid.prop(scene, "citygen_plaza_frequency", text="Places")
        
        layout.separator()
        
        # Section génération
        layout.label(text="Actions:", icon='PLAY')
        col = layout.column(align=True)
        col.scale_y = 1.2
        col.operator("citygen.generate_city", text="Générer Quartier", icon='MESH_CUBE')
        col.operator("citygen.regenerate_roads_sidewalks", text="Régénérer Routes", icon='MOD_BUILD')
        
        layout.separator()
        
        # Section outils
        layout.label(text="Outils:", icon='TOOL_SETTINGS')
        col = layout.column(align=True)
        col.operator("citygen.diagnostic", text="Diagnostic", icon='CONSOLE')

classes = [CITYGEN_PT_Panel]

def register():
    for cls in classes:
        bpy.utils.register_class(cls)

def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)

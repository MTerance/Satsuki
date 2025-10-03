import bpy

def diagnose_citygen_addon():
    """Script de diagnostic pour identifier les problèmes de l'addon City Block Generator"""
    
    print("=== DIAGNOSTIC CITY BLOCK GENERATOR ===")
    
    # 1. Vérifier si l'addon est activé
    addon_enabled = False
    for addon in bpy.context.preferences.addons:
        if "city_block_generator" in addon.module.lower():
            addon_enabled = True
            print(f"✅ Addon trouvé et activé: {addon.module}")
            break
    
    if not addon_enabled:
        print("❌ Addon non trouvé dans les addons activés")
        return
    
    # 2. Vérifier les classes enregistrées
    print("\n=== CLASSES ENREGISTRÉES ===")
    
    # Vérifier le panneau UI
    if hasattr(bpy.types, 'CITYGEN_PT_Panel'):
        print("✅ Panneau UI enregistré: CITYGEN_PT_Panel")
    else:
        print("❌ Panneau UI non enregistré")
    
    # Vérifier les opérateurs
    operators_to_check = [
        'CITYGEN_OT_Generate',
        'CITYGEN_OT_RegenRoads', 
        'CITYGEN_OT_ReloadAddon',
        'CITYGEN_OT_UpdateColors',
        'CITYGEN_OT_ResetProperties'
    ]
    
    for op in operators_to_check:
        if hasattr(bpy.types, op):
            print(f"✅ Opérateur enregistré: {op}")
        else:
            print(f"❌ Opérateur non enregistré: {op}")
    
    # Vérifier les propriétés
    if hasattr(bpy.types, 'CityGenProperties'):
        print("✅ Classe propriétés enregistrée: CityGenProperties")
    else:
        print("❌ Classe propriétés non enregistrée")
    
    # 3. Vérifier les propriétés de scène
    print("\n=== PROPRIÉTÉS DE SCÈNE ===")
    
    if hasattr(bpy.context.scene, 'citygen_props'):
        print("✅ Propriétés citygen_props disponibles")
        props = bpy.context.scene.citygen_props
        
        # Vérifier chaque propriété
        prop_checks = [
            ('width', 'Largeur'),
            ('length', 'Longueur'),
            ('max_floors', 'Étages max'),
            ('shape_mode', 'Mode forme'),
            ('road_width', 'Largeur routes'),
            ('sidewalk_width', 'Largeur trottoirs'),
            ('base_block_size', 'Taille bloc base'),
            ('block_variety', 'Variété blocs'),
            ('district_mode', 'Mode districts'),
            ('commercial_ratio', 'Ratio commercial'),
            ('residential_ratio', 'Ratio résidentiel'),
            ('industrial_ratio', 'Ratio industriel')
        ]
        
        for prop_name, prop_desc in prop_checks:
            if hasattr(props, prop_name):
                value = getattr(props, prop_name)
                print(f"  ✅ {prop_desc}: {value}")
            else:
                print(f"  ❌ {prop_desc}: manquant")
                
    else:
        print("❌ Propriétés citygen_props non disponibles")
    
    # 4. Vérifier les panneaux dans l'interface
    print("\n=== PANNEAUX INTERFACE ===")
    
    # Lister tous les panneaux de la catégorie VIEW_3D
    view3d_panels = []
    for panel_name in dir(bpy.types):
        if panel_name.startswith('CITYGEN_'):
            panel_cls = getattr(bpy.types, panel_name)
            if hasattr(panel_cls, 'bl_space_type') and panel_cls.bl_space_type == 'VIEW_3D':
                view3d_panels.append(panel_name)
                print(f"  ✅ Panneau VIEW_3D: {panel_name}")
                if hasattr(panel_cls, 'bl_category'):
                    print(f"    → Catégorie: {panel_cls.bl_category}")
    
    if not view3d_panels:
        print("  ❌ Aucun panneau CITYGEN trouvé dans VIEW_3D")
    
    # 5. Instructions de résolution
    print("\n=== INSTRUCTIONS DE RÉSOLUTION ===")
    
    if not addon_enabled:
        print("1. Installer et activer l'addon dans Edit > Preferences > Add-ons")
    elif not hasattr(bpy.context.scene, 'citygen_props'):
        print("1. Cliquer sur 'Initialiser les propriétés' dans le panneau")
        print("2. Ou utiliser l'opérateur: bpy.ops.citygen.reset_properties()")
    elif not view3d_panels:
        print("1. Vérifier l'onglet 'CityGen' dans le panneau latéral (N)")
        print("2. Redémarrer Blender")
        print("3. Réinstaller l'addon")
    else:
        print("✅ Addon semble correctement configuré")
        print("→ Vérifier l'onglet 'CityGen' dans le panneau latéral (touche N)")
    
    print("\n=== FIN DIAGNOSTIC ===")

# Exécuter le diagnostic
if __name__ == "__main__":
    diagnose_citygen_addon()

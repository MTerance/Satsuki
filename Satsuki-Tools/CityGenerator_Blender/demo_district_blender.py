"""
Démonstration du mode district - À exécuter dans Blender Text Editor
Copier-coller ce code dans l'éditeur de texte de Blender et l'exécuter.
"""

import bpy

def demo_district_mode():
    """Démonstration du mode district avec différentes configurations."""
    
    print("=" * 50)
    print("DÉMONSTRATION DU MODE DISTRICT")
    print("=" * 50)
    
    # Nettoyer la scène
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete(use_global=False)
    
    # Vérifier les propriétés
    if not hasattr(bpy.context.scene, 'citygen_props'):
        print("ERREUR: Propriétés citygen_props non trouvées !")
        print("Assurez-vous que l'addon City Block Generator est activé.")
        return
    
    props = bpy.context.scene.citygen_props
    
    # Configuration pour une démonstration efficace
    print("\nConfiguration du mode district:")
    props.width = 7
    props.length = 7
    props.max_floors = 15
    props.shape_mode = 'AUTO'
    props.block_variety = 'HIGH'
    props.base_block_size = 12.0
    props.district_mode = True
    props.commercial_ratio = 0.35  # Plus de commercial pour voir la différence
    props.residential_ratio = 0.45
    props.industrial_ratio = 0.20
    
    print(f"✓ Grille: {props.width}x{props.length}")
    print(f"✓ Mode district: {props.district_mode}")
    print(f"✓ Variété: {props.block_variety}")
    print(f"✓ Taille de base: {props.base_block_size}")
    print(f"✓ Ratios - Commercial: {props.commercial_ratio}, Résidentiel: {props.residential_ratio}, Industriel: {props.industrial_ratio}")
    
    # Générer le quartier
    print("\nGénération du quartier...")
    try:
        result = bpy.ops.citygen.generate_city()
        if result == {'FINISHED'}:
            print("✓ Quartier généré avec succès !")
            analyze_district_result()
        else:
            print("✗ Échec de la génération")
    except Exception as e:
        print(f"✗ Erreur: {e}")

def analyze_district_result():
    """Analyse le résultat de la génération en mode district."""
    
    print("\nAnalyse du résultat:")
    
    # Compter les objets
    all_objects = list(bpy.context.scene.objects)
    buildings = [obj for obj in all_objects if 'building' in obj.name.lower() or 'bloc' in obj.name.lower()]
    roads = [obj for obj in all_objects if 'road' in obj.name.lower() or 'route' in obj.name.lower()]
    sidewalks = [obj for obj in all_objects if 'sidewalk' in obj.name.lower() or 'trottoir' in obj.name.lower()]
    
    print(f"📊 Objets générés:")
    print(f"   - Bâtiments/Blocs: {len(buildings)}")
    print(f"   - Routes: {len(roads)}")
    print(f"   - Trottoirs: {len(sidewalks)}")
    print(f"   - Total: {len(all_objects)}")
    
    if buildings:
        # Analyser la variété des bâtiments
        building_data = []
        for building in buildings:
            if building.dimensions:
                width = building.dimensions.x
                length = building.dimensions.y
                height = building.dimensions.z
                area = width * length
                building_data.append({
                    'name': building.name,
                    'area': area,
                    'height': height,
                    'width': width,
                    'length': length
                })
        
        if building_data:
            # Statistiques des tailles
            areas = [b['area'] for b in building_data]
            heights = [b['height'] for b in building_data]
            
            print(f"\n📏 Variété des bâtiments:")
            print(f"   - Superficie min: {min(areas):.1f} u²")
            print(f"   - Superficie max: {max(areas):.1f} u²")
            print(f"   - Superficie moyenne: {sum(areas)/len(areas):.1f} u²")
            print(f"   - Hauteur min: {min(heights):.1f} u")
            print(f"   - Hauteur max: {max(heights):.1f} u")
            print(f"   - Hauteur moyenne: {sum(heights)/len(heights):.1f} u")
            
            # Identifier les types probables
            sorted_by_area = sorted(building_data, key=lambda x: x['area'])
            small_buildings = [b for b in building_data if b['area'] < sum(areas)/len(areas) * 0.8]
            large_buildings = [b for b in building_data if b['area'] > sum(areas)/len(areas) * 1.2]
            
            print(f"\n🏢 Répartition probable des types:")
            print(f"   - Petits bâtiments (résidentiel): {len(small_buildings)}")
            print(f"   - Bâtiments moyens: {len(building_data) - len(small_buildings) - len(large_buildings)}")
            print(f"   - Grands bâtiments (commercial/industriel): {len(large_buildings)}")
    
    # Vérifier les matériaux
    materials = set()
    for obj in all_objects:
        if obj.data and hasattr(obj.data, 'materials'):
            for mat in obj.data.materials:
                if mat:
                    materials.add(mat.name)
    
    if materials:
        print(f"\n🎨 Matériaux utilisés: {len(materials)}")
        for mat in sorted(materials):
            print(f"   - {mat}")
    
    print(f"\n✅ Analyse terminée !")
    print(f"💡 Regardez la vue 3D pour observer la répartition des zones.")
    print(f"💡 Les bâtiments de tailles différentes représentent les zones urbaines.")

# Exécuter la démonstration
demo_district_mode()

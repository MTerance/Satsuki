# DEBUG ALIGNEMENT - Analyse détaillée des positions
# À exécuter dans l'éditeur de texte de Blender

import bpy

def debug_alignment():
    """Debug détaillé de l'alignement routes-blocs."""
    
    print("=== DEBUG ALIGNEMENT DÉTAILLÉ ===")
    
    # Nettoyer la scène
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete(use_global=False)
    
    if not hasattr(bpy.context.scene, 'citygen_props'):
        print("❌ Addon non activé")
        return False
    
    props = bpy.context.scene.citygen_props
    
    # Configuration très simple pour debug
    props.width = 2  # Grille 2x2 pour debug facile
    props.length = 2
    props.max_floors = 3
    props.block_variety = 'UNIFORM'  # Uniforme pour éliminer variations
    props.base_block_size = 10.0     # Taille fixe
    props.district_mode = False      # Pas de districts
    
    print(f"Configuration debug: {props.width}x{props.length}, taille {props.base_block_size}")
    
    # Générer
    try:
        result = bpy.ops.citygen.generate_city()
        if result == {'FINISHED'}:
            print("✅ Génération réussie")
            analyze_positions()
            return True
        else:
            print("❌ Échec génération")
            return False
    except Exception as e:
        print(f"❌ Erreur: {e}")
        return False

def analyze_positions():
    """Analyse détaillée des positions pour identifier les espaces."""
    
    print("\n--- ANALYSE DÉTAILLÉE POSITIONS ---")
    
    # Récupérer objets par type
    roads_h = [obj for obj in bpy.context.scene.objects if 'road_h' in obj.name]
    roads_v = [obj for obj in bpy.context.scene.objects if 'road_v' in obj.name]
    sidewalks = [obj for obj in bpy.context.scene.objects if 'sidewalk' in obj.name]
    buildings = [obj for obj in bpy.context.scene.objects if 'batiment' in obj.name]
    
    print(f"Objets trouvés:")
    print(f"  - Routes horizontales: {len(roads_h)}")
    print(f"  - Routes verticales: {len(roads_v)}")
    print(f"  - Trottoirs: {len(sidewalks)}")
    print(f"  - Bâtiments: {len(buildings)}")
    
    # Analyser les trottoirs (blocs)
    print(f"\n📐 TROTTOIRS (BLOCS):")
    sidewalk_bounds = []
    for sidewalk in sorted(sidewalks, key=lambda x: (x.location.y, x.location.x)):
        x, y, z = sidewalk.location
        sx, sy, sz = sidewalk.scale
        
        # Calculer les limites réelles du trottoir
        left = x - sx
        right = x + sx
        bottom = y - sy
        top = y + sy
        
        sidewalk_bounds.append((left, right, bottom, top))
        print(f"  {sidewalk.name}: centre=({x:.2f}, {y:.2f}), limites=({left:.2f} à {right:.2f}, {bottom:.2f} à {top:.2f})")
    
    # Analyser les routes horizontales
    print(f"\n📐 ROUTES HORIZONTALES:")
    for road in sorted(roads_h, key=lambda x: x.location.y):
        x, y, z = road.location
        sx, sy, sz = road.scale
        
        # Calculer les limites réelles de la route
        left = x - sx
        right = x + sx
        bottom = y - sy
        top = y + sy
        
        print(f"  {road.name}: centre=({x:.2f}, {y:.2f}), limites=({left:.2f} à {right:.2f}, {bottom:.2f} à {top:.2f})")
        
        # Vérifier proximité avec trottoirs
        for i, (t_left, t_right, t_bottom, t_top) in enumerate(sidewalk_bounds):
            # Distance entre route et trottoir
            if abs(bottom - t_top) < 0.1:  # Route en dessous du trottoir
                gap = bottom - t_top
                print(f"    ↔️ Espace avec trottoir {i}: {gap:.3f} unités")
            elif abs(top - t_bottom) < 0.1:  # Route au dessus du trottoir
                gap = t_bottom - top
                print(f"    ↔️ Espace avec trottoir {i}: {gap:.3f} unités")
    
    # Analyser les routes verticales
    print(f"\n📐 ROUTES VERTICALES:")
    for road in sorted(roads_v, key=lambda x: x.location.x):
        x, y, z = road.location
        sx, sy, sz = road.scale
        
        # Calculer les limites réelles de la route
        left = x - sx
        right = x + sx
        bottom = y - sy
        top = y + sy
        
        print(f"  {road.name}: centre=({x:.2f}, {y:.2f}), limites=({left:.2f} à {right:.2f}, {bottom:.2f} à {top:.2f})")
        
        # Vérifier proximité avec trottoirs
        for i, (t_left, t_right, t_bottom, t_top) in enumerate(sidewalk_bounds):
            # Distance entre route et trottoir
            if abs(left - t_right) < 0.1:  # Route à gauche du trottoir
                gap = left - t_right
                print(f"    ↔️ Espace avec trottoir {i}: {gap:.3f} unités")
            elif abs(right - t_left) < 0.1:  # Route à droite du trottoir
                gap = t_left - right
                print(f"    ↔️ Espace avec trottoir {i}: {gap:.3f} unités")
    
    # Analyse des espaces
    print(f"\n🔍 DIAGNOSTIC:")
    print(f"Si les espaces sont > 0.001, il y a un problème d'alignement")
    print(f"Les routes doivent être EXACTEMENT contiguës aux trottoirs")

def quick_fix_test():
    """Test rapide avec alignement forcé."""
    
    print("\n=== TEST ALIGNEMENT FORCÉ ===")
    
    # Nettoyer
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete(use_global=False)
    
    # Créer manuellement un test simple
    create_manual_test()

def create_manual_test():
    """Crée manuellement un test d'alignement parfait."""
    
    print("Création manuelle d'un test d'alignement...")
    
    # Matériaux
    road_mat = bpy.data.materials.new("TestRoad")
    road_mat.diffuse_color = (0.1, 0.1, 0.1, 1)
    
    sidewalk_mat = bpy.data.materials.new("TestSidewalk") 
    sidewalk_mat.diffuse_color = (0.6, 0.6, 0.6, 1)
    
    # Taille de bloc
    block_size = 10.0
    road_width = 4.0
    
    # Créer 2 blocs avec 1 route entre
    # Bloc 1: position (0, 0)
    bpy.ops.mesh.primitive_plane_add(size=1, location=(0, 0, 0.01))
    block1 = bpy.context.object
    block1.name = "test_block_1"
    block1.scale = (block_size/2, block_size/2, 0.02)
    block1.location = (block_size/2, block_size/2, 0.01)
    block1.data.materials.append(sidewalk_mat)
    
    # Route verticale: position (10, 0)
    bpy.ops.mesh.primitive_plane_add(size=1, location=(0, 0, 0.001))
    road = bpy.context.object
    road.name = "test_road_v"
    road.scale = (road_width/2, block_size/2, 0.005)
    road.location = (block_size + road_width/2, block_size/2, 0.001)
    road.data.materials.append(road_mat)
    
    # Bloc 2: position (14, 0)
    bpy.ops.mesh.primitive_plane_add(size=1, location=(0, 0, 0.01))
    block2 = bpy.context.object
    block2.name = "test_block_2"
    block2.scale = (block_size/2, block_size/2, 0.02)
    block2.location = (block_size + road_width + block_size/2, block_size/2, 0.01)
    block2.data.materials.append(sidewalk_mat)
    
    print("✅ Test manuel créé")
    print("📐 Bloc 1: 0-10, Route: 10-14, Bloc 2: 14-24")
    print("💡 Vérifiez dans la vue 3D si ils sont contigus")

# Choisir le test
print("🔧 TESTS DEBUG DISPONIBLES:")
print("1. debug_alignment() - Debug complet")
print("2. quick_fix_test() - Test manuel alignement")

# Exécuter le debug par défaut
success = debug_alignment()
if success:
    print("\n📊 Debug terminé ! Analysez les données ci-dessus")
else:
    print("\n❌ Debug échoué")

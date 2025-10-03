"""
FORCE COURBES VISIBLES V6.13.7
Remplace le système de courbes par des courbes Blender natives MEGA visibles
"""

import shutil
import os

def patch_courbes_visibles():
    """Applique le patch pour des courbes MEGA visibles"""
    
    addon_path = r"C:\Users\sshom\Documents\assets\Tools\city_block_generator"
    workspace_path = r"C:\Users\sshom\source\repos\Satsuki\Satsuki-Tools\CityGenerator_Blender\city_block_generator"
    
    print("🔥🔥🔥 PATCH COURBES MEGA VISIBLES V6.13.7 🔥🔥🔥")
    
    # Lire le fichier generator.py actuel
    generator_file = os.path.join(workspace_path, "generator.py")
    
    with open(generator_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Nouveau système de courbes MEGA visibles
    new_curve_system = '''def create_organic_road_grid_rf(width, length, block_size, road_width, road_mat, curve_intensity):
    """Crée une grille organique de routes - COURBES BLENDER NATIVES MEGA VISIBLES"""
    road_network = []
    import math
    
    try:
        print(f"🎯🔥 === COURBES BLENDER NATIVES MEGA VISIBLES === 🔥🎯")
        print(f"   Paramètres: width={width}, length={length}, block_size={block_size}")
        print(f"   road_width={road_width}, curve_intensity={curve_intensity}")
        
        # FORCER une intensité EXTREME pour garantir la visibilité
        curve_intensity = max(1.5, curve_intensity * 3)  # TRIPLER l'intensité !
        print(f"   🔥🔥🔥 COURBE INTENSITÉ EXTREME: {curve_intensity}")
        
        # === COURBES BLENDER NATIVES - 100% GARANTIES VISIBLES ===
        
        # Routes verticales - COURBES BLENDER NATIVES
        print(f"   🎯 Génération routes verticales COURBES BLENDER NATIVES...")
        for i in range(width + 1):
            base_x = (i - width/2) * block_size
            
            # Créer une courbe Bézier native Blender
            curve_data = bpy.data.curves.new(f"SuperCurve_V_{i}", type='CURVE')
            curve_data.dimensions = '3D'
            curve_data.fill_mode = 'BOTH'
            curve_data.bevel_depth = road_width / 2  # Largeur automatique
            curve_data.resolution_u = 64  # MEGA haute résolution
            curve_data.bevel_resolution = 16  # Résolution du biseau
            
            # Créer un spline Bézier
            spline = curve_data.splines.new('BEZIER')
            
            # Points de contrôle pour des courbes ENORMES et visibles
            total_length = length * block_size
            segments = 12  # Plus de segments = plus de courbes
            
            # Redimensionner le spline
            spline.bezier_points.add(segments)
            
            # Définir les points avec des courbes GIGANTESQUES
            for seg in range(segments + 1):
                t = seg / segments
                y = (t - 0.5) * total_length
                
                # COURBES GIGANTESQUES - IMPOSSIBLE DE LES RATER !
                curve_amplitude = curve_intensity * block_size * 1.2  # MEGA amplitude !
                
                # Courbes sinusoïdales EXTREMES multiples
                curve_offset = math.sin(t * 6 * math.pi + i * 1.2) * curve_amplitude
                curve_offset += math.sin(t * 3 * math.pi + i * 2.1) * curve_amplitude * 0.8
                curve_offset += math.sin(t * 9 * math.pi + i * 0.7) * curve_amplitude * 0.5
                
                # Variation random EXTREME
                curve_offset += random.uniform(-0.4, 0.4) * curve_amplitude
                
                final_x = base_x + curve_offset
                
                # Définir le point de contrôle
                point = spline.bezier_points[seg]
                point.co = (final_x, y, 0)
                
                # Handles pour des courbes naturelles
                point.handle_left_type = 'AUTO'
                point.handle_right_type = 'AUTO'
                
                if seg % 3 == 0:  # Debug
                    print(f"      Point {seg}: x={final_x:.1f} (offset={curve_offset:.1f})")
            
            # Créer l'objet courbe
            curve_obj = bpy.data.objects.new(f"SuperCurveRoad_V_{i}", curve_data)
            bpy.context.collection.objects.link(curve_obj)
            
            # Convertir en mesh pour les matériaux
            bpy.context.view_layer.objects.active = curve_obj
            curve_obj.select_set(True)
            bpy.ops.object.convert(target='MESH')
            
            # Matériau MEGA vif
            hue = (i % 6) / 6.0
            road_color = (1.0, 0.3 + hue * 0.7, 0.8 - hue * 0.3)  # Couleurs vives
            
            road_material = create_material(f"SuperCurveMat_V_{i}", road_color)
            if curve_obj.data:
                curve_obj.data.materials.clear()
                curve_obj.data.materials.append(road_material)
            
            print(f"         🔥✅ SUPER COURBE BLENDER V_{i} créée - MEGA VISIBLE !")
            
            road_network.append({
                'object': curve_obj,
                'road_type': 'super_bezier_vertical',
                'curve_type': 'blender_native_mega',
                'x': base_x,
                'y': 0,
                'width': road_width,
                'length': total_length,
                'curve_segments': segments + 1,
                'curve_amplitude': curve_amplitude
            })
        
        # Routes horizontales - COURBES BLENDER NATIVES
        print(f"   🎯 Génération routes horizontales COURBES BLENDER NATIVES...")
        for j in range(length + 1):
            base_y = (j - length/2) * block_size
            
            # Créer une courbe Bézier native Blender
            curve_data = bpy.data.curves.new(f"SuperCurve_H_{j}", type='CURVE')
            curve_data.dimensions = '3D'
            curve_data.fill_mode = 'BOTH'
            curve_data.bevel_depth = road_width / 2
            curve_data.resolution_u = 64
            curve_data.bevel_resolution = 16
            
            # Créer un spline Bézier
            spline = curve_data.splines.new('BEZIER')
            
            # Points de contrôle
            total_length = width * block_size
            segments = 12
            
            # Redimensionner le spline
            spline.bezier_points.add(segments)
            
            # Définir les points avec des courbes GIGANTESQUES
            for seg in range(segments + 1):
                t = seg / segments
                x = (t - 0.5) * total_length
                
                # COURBES GIGANTESQUES horizontales
                curve_amplitude = curve_intensity * block_size * 1.2
                
                # Courbes sinusoïdales EXTREMES multiples
                curve_offset = math.sin(t * 5 * math.pi + j * 1.4) * curve_amplitude
                curve_offset += math.sin(t * 8 * math.pi + j * 1.8) * curve_amplitude * 0.7
                curve_offset += math.sin(t * 4 * math.pi + j * 0.9) * curve_amplitude * 0.6
                
                # Variation random EXTREME
                curve_offset += random.uniform(-0.4, 0.4) * curve_amplitude
                
                final_y = base_y + curve_offset
                
                # Définir le point de contrôle
                point = spline.bezier_points[seg]
                point.co = (x, final_y, 0)
                
                # Handles pour des courbes naturelles
                point.handle_left_type = 'AUTO'
                point.handle_right_type = 'AUTO'
            
            # Créer l'objet courbe
            curve_obj = bpy.data.objects.new(f"SuperCurveRoad_H_{j}", curve_data)
            bpy.context.collection.objects.link(curve_obj)
            
            # Convertir en mesh
            bpy.context.view_layer.objects.active = curve_obj
            curve_obj.select_set(True)
            bpy.ops.object.convert(target='MESH')
            
            # Matériau MEGA vif
            hue = (j % 6) / 6.0
            road_color = (0.8 - hue * 0.3, 1.0, 0.3 + hue * 0.7)  # Couleurs vives
            
            road_material = create_material(f"SuperCurveMat_H_{j}", road_color)
            if curve_obj.data:
                curve_obj.data.materials.clear()
                curve_obj.data.materials.append(road_material)
            
            print(f"         🔥✅ SUPER COURBE BLENDER H_{j} créée - MEGA VISIBLE !")
            
            road_network.append({
                'object': curve_obj,
                'road_type': 'super_bezier_horizontal',
                'curve_type': 'blender_native_mega',
                'x': 0,
                'y': base_y,
                'width': road_width,
                'length': total_length,
                'curve_segments': segments + 1,
                'curve_amplitude': curve_amplitude
            })
        
        print(f"🔥🎯 === COURBES BLENDER NATIVES CRÉÉES === 🎯🔥")
        print(f"   ✅ {width + 1} routes verticales MEGA courbes")
        print(f"   ✅ {length + 1} routes horizontales MEGA courbes")
        print(f"   🔥 AMPLITUDE MAXIMALE: {curve_intensity * block_size * 1.2:.1f}")
        print(f"   🎯 IMPOSSIBLE DE LES RATER - COURBES GIGANTESQUES !")
        
        return road_network
        
    except Exception as e:
        print(f"❌ Erreur courbes: {e}")
        import traceback
        traceback.print_exc()
        return []'''
    
    # Chercher et remplacer la fonction create_organic_road_grid_rf
    start_marker = "def create_organic_road_grid_rf(width, length, block_size, road_width, road_mat, curve_intensity):"
    
    start_idx = content.find(start_marker)
    if start_idx == -1:
        print("❌ Fonction create_organic_road_grid_rf non trouvée!")
        return
    
    # Chercher la fin de la fonction (prochaine fonction ou fin de fichier)
    next_def_idx = content.find("\ndef ", start_idx + 1)
    if next_def_idx == -1:
        next_def_idx = len(content)
    
    # Remplacer la fonction
    new_content = content[:start_idx] + new_curve_system + "\n\n" + content[next_def_idx:]
    
    # Écrire le nouveau fichier
    with open(generator_file, 'w', encoding='utf-8') as f:
        f.write(new_content)
    
    print(f"✅ create_organic_road_grid_rf remplacée par COURBES MEGA VISIBLES")
    
    # Mettre à jour la version
    init_file = os.path.join(workspace_path, "__init__.py")
    with open(init_file, 'r', encoding='utf-8') as f:
        init_content = f.read()
    
    # Changer la version
    init_content = init_content.replace('"version": (6, 13, 6)', '"version": (6, 13, 7)')
    
    with open(init_file, 'w', encoding='utf-8') as f:
        f.write(init_content)
    
    print(f"✅ Version mise à jour vers 6.13.7")
    
    # Copier vers le dossier addon
    print(f"📁 Copie vers addon...")
    
    if os.path.exists(addon_path):
        shutil.rmtree(addon_path)
    
    shutil.copytree(workspace_path, addon_path)
    print(f"✅ Addon copié vers: {addon_path}")
    
    # Statistiques
    with open(generator_file, 'r', encoding='utf-8') as f:
        size = len(f.read().encode('utf-8'))
    
    print(f"📊 generator.py: {size} bytes")
    print(f"🔥🔥🔥 PATCH COURBES MEGA VISIBLES V6.13.7 APPLIQUÉ ! 🔥🔥🔥")
    print(f"🎯 Les courbes sont maintenant IMPOSSIBLES à rater !")
    print(f"🌊 Courbes Blender natives avec amplitude GIGANTESQUE !")

if __name__ == "__main__":
    patch_courbes_visibles()

def create_smart_organic_road_grid_rf(width, length, block_size, road_width, road_mat, curve_intensity):
    """Système hybride intelligent - Grille urbaine avec variations organiques subtiles"""
    road_network = []
    import math
    import random
    
    try:
        print(f"🧠 === SYSTÈME HYBRIDE INTELLIGENT ===")
        print(f"   🎯 Objectif: Grille urbaine + variations organiques subtiles")
        print(f"   📊 Paramètres: {width}x{length}, intensité={curve_intensity}")
        
        # Intensité intelligente selon la taille
        smart_intensity = min(0.15, curve_intensity * 0.5)  # Très subtil
        variation_range = block_size * smart_intensity
        
        print(f"   🌿 Variation range: ±{variation_range:.1f}m")
        
        # Routes verticales avec variations intelligentes
        for i in range(width + 1):
            base_x = (i - width/2) * block_size
            
            # Variation organique intelligente
            # Plus de variation au centre, moins aux bords
            center_factor = 1.0 - abs(i - width/2) / (width/2 + 1)
            
            # Variation basée sur position + randomness contrôlé
            organic_var = (
                math.sin(i * 0.7 + 0.3) * variation_range * center_factor * 0.6 +
                random.uniform(-variation_range, variation_range) * 0.3
            )
            
            final_x = base_x + organic_var
            
            # Créer route verticale
            bpy.ops.mesh.primitive_cube_add(
                size=2.0,
                location=(final_x, 0, 0.05)
            )
            road = bpy.context.object
            if road:
                # Échelle avec légère variation de largeur
                width_var = 1.0 + random.uniform(-0.1, 0.1)
                road.scale = (road_width/2 * width_var, length * block_size/2, 0.05)
                bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
                
                # Rotation très subtile
                road.rotation_euler[2] = organic_var / block_size * 0.05
                
                road.name = f"SmartRoad_V_{i}"
                
                # Matériau avec variation subtile
                color_var = 0.3 + (i % 3) * 0.05
                mat = create_material(f"SmartMat_V_{i}", (color_var, 0.3, 0.4))
                if road.data:
                    road.data.materials.clear()
                    road.data.materials.append(mat)
                
                road_network.append({'object': road, 'type': 'vertical', 'x': final_x})
        
        # Routes horizontales avec variations intelligentes
        for j in range(length + 1):
            base_y = (j - length/2) * block_size
            
            # Variation organique intelligente
            center_factor = 1.0 - abs(j - length/2) / (length/2 + 1)
            
            organic_var = (
                math.sin(j * 0.8 + 0.7) * variation_range * center_factor * 0.5 +
                random.uniform(-variation_range, variation_range) * 0.4
            )
            
            final_y = base_y + organic_var
            
            # Créer route horizontale
            bpy.ops.mesh.primitive_cube_add(
                size=2.0,
                location=(0, final_y, 0.05)
            )
            road = bpy.context.object
            if road:
                # Échelle avec légère variation
                width_var = 1.0 + random.uniform(-0.08, 0.08)
                road.scale = (width * block_size/2, road_width/2 * width_var, 0.05)
                bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
                
                # Rotation très subtile
                road.rotation_euler[2] = organic_var / block_size * 0.04
                
                road.name = f"SmartRoad_H_{j}"
                
                # Matériau avec variation
                color_var = 0.4 + (j % 4) * 0.04
                mat = create_material(f"SmartMat_H_{j}", (0.5, color_var, 0.3))
                if road.data:
                    road.data.materials.clear()
                    road.data.materials.append(mat)
                
                road_network.append({'object': road, 'type': 'horizontal', 'y': final_y})
        
        print(f"✅ {len(road_network)} routes hybrides intelligentes créées")
        print(f"   🧠 Grille urbaine + variations organiques subtiles")
        print(f"   🌿 Aspect naturel sans chaos ni rigidité")
        
        return road_network
        
    except Exception as e:
        print(f"❌ Erreur routes hybrides: {e}")
        return []

"""
TEST MEGA COURBES - VERSION EXTRÊME
Pour tester si Blender peut afficher des courbes visibles

À exécuter dans Blender :
1. Coller ce code dans Text Editor
2. Run Script
3. Observer les résultats dans la vue 3D
"""

import bpy
import bmesh
import math
import random

def clear_scene():
    """Nettoie la scène"""
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete(use_global=False)

def create_mega_curved_road():
    """Crée une route avec courbes MEGA EXTRÊMES"""
    print("🚧 CRÉATION ROUTE MEGA COURBE...")
    
    # Paramètres EXTRÊMES
    segments = 20
    curve_amplitude = 50  # 50 unités Blender !
    road_length = 100
    
    # Créer un mesh pour la route courbe
    mesh = bpy.data.meshes.new("MegaCurvedRoad")
    obj = bpy.data.objects.new("MegaCurvedRoad", mesh)
    bpy.context.collection.objects.link(obj)
    
    # Créer les vertices avec courbe sinusoïdale EXTREME
    vertices = []
    faces = []
    
    for i in range(segments + 1):
        # Position le long de la route
        t = i / segments
        y = (t - 0.5) * road_length
        
        # Courbe sinusoïdale MEGA EXTRÊME
        x_curve = math.sin(t * 4 * math.pi) * curve_amplitude
        
        print(f"  Segment {i}: y={y:.1f}, x_curve={x_curve:.1f}")
        
        # Créer largeur de route (2 vertices par segment)
        road_width = 10
        vertices.append((x_curve - road_width/2, y, 0))  # Côté gauche
        vertices.append((x_curve + road_width/2, y, 0))  # Côté droit
        
        # Créer face si pas le premier segment
        if i > 0:
            # Face entre segments précédent et actuel
            v1 = (i-1) * 2      # Gauche précédent
            v2 = (i-1) * 2 + 1  # Droite précédent
            v3 = i * 2 + 1      # Droite actuel
            v4 = i * 2          # Gauche actuel
            faces.append((v1, v2, v3, v4))
    
    # Appliquer au mesh
    mesh.from_pydata(vertices, [], faces)
    mesh.update()
    
    # Matériau rouge vif
    mat = bpy.data.materials.new("MegaCurveMat")
    mat.use_nodes = True
    mat.node_tree.nodes["Principled BSDF"].inputs[0].default_value = (1.0, 0.0, 0.0, 1.0)
    obj.data.materials.append(mat)
    
    print(f"✅ Route MEGA courbe créée avec {len(vertices)} vertices et {len(faces)} faces")
    return obj

def create_comparison_straight_road():
    """Crée une route droite pour comparaison"""
    print("📏 CRÉATION ROUTE DROITE COMPARAISON...")
    
    bpy.ops.mesh.primitive_cube_add(size=2.0, location=(0, 0, -1))
    road = bpy.context.object
    road.scale = (5, 50, 0.1)  # Route droite longue
    bpy.ops.object.transform_apply(scale=True)
    road.name = "StraightRoadComparison"
    
    # Matériau gris
    mat = bpy.data.materials.new("StraightMat")
    mat.use_nodes = True
    mat.node_tree.nodes["Principled BSDF"].inputs[0].default_value = (0.5, 0.5, 0.5, 1.0)
    road.data.materials.append(mat)
    
    print("✅ Route droite créée pour comparaison")
    return road

def test_mega_courbes():
    """Test principal"""
    print("🎯 === TEST MEGA COURBES DÉMARRÉ ===")
    
    # Nettoyer
    clear_scene()
    
    # Créer route courbe EXTRÊME
    curved_road = create_mega_curved_road()
    
    # Créer route droite pour comparaison
    straight_road = create_comparison_straight_road()
    
    # Position de la caméra pour voir les deux
    if bpy.context.scene.camera:
        bpy.context.scene.camera.location = (0, 0, 150)
        bpy.context.scene.camera.rotation_euler = (0, 0, 0)
    
    print("🎯 === TEST TERMINÉ ===")
    print("🔴 Route ROUGE = MEGA courbe avec amplitude 50")
    print("⚫ Route GRISE = droite pour comparaison")
    print("👀 Regardez en vue 3D - les courbes DOIVENT être visibles !")

if __name__ == "__main__":
    test_mega_courbes()

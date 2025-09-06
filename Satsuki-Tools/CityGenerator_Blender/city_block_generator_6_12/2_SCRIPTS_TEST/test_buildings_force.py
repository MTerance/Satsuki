"""
TEST FORÇAGE BÂTIMENTS
À exécuter dans Blender pour tester la création directe de bâtiments
"""

import bpy
import random

def clear_buildings():
    """Supprime tous les bâtiments existants"""
    for obj in bpy.context.scene.objects:
        if "Building" in obj.name:
            bpy.data.objects.remove(obj, do_unlink=True)

def create_material(name, color):
    """Crée un matériau avec la couleur donnée"""
    if name in bpy.data.materials:
        return bpy.data.materials[name]
    
    mat = bpy.data.materials.new(name=name)
    mat.use_nodes = True
    
    if mat.node_tree:
        bsdf = mat.node_tree.nodes.get("Principled BSDF")
        if bsdf:
            bsdf.inputs[0].default_value = (*color, 1.0)
    
    return mat

def force_create_buildings():
    """Force la création de bâtiments en grille simple"""
    print("🏢 === TEST FORÇAGE BÂTIMENTS ===")
    
    # Nettoyer les anciens bâtiments
    clear_buildings()
    
    # Paramètres de test
    grid_size = 5
    spacing = 12.0
    buildings_created = 0
    
    for i in range(grid_size):
        for j in range(grid_size):
            # Position du bâtiment
            x = (i - grid_size/2) * spacing
            y = (j - grid_size/2) * spacing
            
            # Dimensions aléatoires
            width = random.uniform(3, 8)
            depth = random.uniform(3, 8)
            floors = random.randint(2, 12)
            height = floors * 3.0
            
            print(f"  Bâtiment {i},{j}: ({x:.1f}, {y:.1f}) - {width:.1f}x{depth:.1f}x{height:.1f}")
            
            # Créer le bâtiment
            bpy.ops.mesh.primitive_cube_add(
                size=2.0,
                location=(x, y, height/2)
            )
            
            building = bpy.context.object
            if building:
                # Échelle
                building.scale = (width/2, depth/2, height/2)
                bpy.ops.object.transform_apply(scale=True)
                
                # Nom
                building.name = f"TEST_Building_{i}_{j}_{floors}f"
                
                # Couleur selon hauteur
                height_ratio = height / 36.0  # Max 12 étages * 3m
                if height_ratio < 0.3:
                    color = (0.9, 0.8, 0.7)  # Beige clair
                elif height_ratio < 0.6:
                    color = (0.8, 0.7, 0.6)  # Beige moyen
                else:
                    color = (0.7, 0.6, 0.5)  # Beige foncé
                
                # Matériau
                mat = create_material(f"TestBuildingMat_{height_ratio:.1f}", color)
                if building.data:
                    building.data.materials.clear()
                    building.data.materials.append(mat)
                
                buildings_created += 1
                print(f"    ✅ Créé: {building.name}")
    
    print(f"🎯 Total: {buildings_created} bâtiments de test créés !")
    print("👀 Vous devriez voir des bâtiments beiges de différentes hauteurs")

if __name__ == "__main__":
    force_create_buildings()

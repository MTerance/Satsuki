# Test pour vérifier le positionnement des cubes avec origine bottom-center
# À exécuter dans Blender pour diagnostiquer le positionnement

import bpy

def test_cube_positioning():
    # Nettoyer la scène
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete(use_global=False)
    
    # Test de la fonction _add_cube corrigée
    def _add_cube(name, size=(2,2,2), loc=(0,0,0), mat=None):
        # Créer un cube à l'origine
        bpy.ops.mesh.primitive_cube_add(size=2.0, location=(0,0,0))
        o = bpy.context.active_object
        o.name = name
        
        # Appliquer la taille
        o.scale = (size[0]/2.0, size[1]/2.0, size[2]/2.0)
        
        # Appliquer les transformations pour fixer l'échelle
        bpy.context.view_layer.objects.active = o
        bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
        
        # Maintenant le cube fait exactement la taille demandée
        # Déplacer l'origine vers le bottom-center
        bpy.ops.object.mode_set(mode='EDIT')
        bpy.ops.mesh.select_all(action='SELECT')
        # Déplacer tous les vertices de la moitié de la hauteur vers le haut
        bpy.ops.transform.translate(value=(0, 0, size[2]/2.0))
        bpy.ops.object.mode_set(mode='OBJECT')
        
        # Maintenant positionner l'objet à la location désirée
        o.location = loc
        
        return o
    
    # Créer un plan de référence à Z=0
    bpy.ops.mesh.primitive_plane_add(size=10.0, location=(0, 0, 0))
    plane = bpy.context.active_object
    plane.name = "REFERENCE_Ground"
    
    # Test 1: Cube posé sur le sol (Z=0)
    cube1 = _add_cube("TEST_Podium", (6, 4, 2), (0, 0, 0))
    print(f"Cube1 - Position: {cube1.location}, Dimensions: {cube1.dimensions}")
    
    # Test 2: Cube empilé (Z=2)
    cube2 = _add_cube("TEST_Tower", (4, 3, 8), (0, 0, 2))
    print(f"Cube2 - Position: {cube2.location}, Dimensions: {cube2.dimensions}")
    
    # Test 3: Petit cube pour vérifier l'alignement
    cube3 = _add_cube("TEST_Small", (2, 2, 1), (5, 0, 0))
    print(f"Cube3 - Position: {cube3.location}, Dimensions: {cube3.dimensions}")
    
    print("Test terminé. Vérifiez que :")
    print("- Le plan gris est à Z=0")
    print("- Tous les cubes touchent le sol ou sont empilés correctement")
    print("- Aucun cube n'est enfoncé dans le sol")

if __name__ == "__main__":
    test_cube_positioning()
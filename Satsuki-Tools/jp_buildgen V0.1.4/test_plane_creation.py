# Test pour vérifier la création du plan
# À exécuter dans Blender pour vérifier que _add_plane fonctionne

import bpy

def test_plane_creation():
    # Nettoyer la scène
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete(use_global=False)
    
    # Test de création de plan
    def _add_plane(name, size=(2,2), loc=(0,0,0), mat=None):
        # Créer un plan à l'origine avec la taille directement
        bpy.ops.mesh.primitive_plane_add(size=2.0, location=loc)
        o = bpy.context.active_object
        o.name = name
        
        # Appliquer la taille correctement (diviser par 2 car le plan par défaut fait 2x2)
        o.scale = (size[0]/2.0, size[1]/2.0, 1.0)
        
        # Appliquer les transformations pour fixer l'échelle
        bpy.context.view_layer.objects.active = o
        bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
        
        return o
    
    # Créer un plan de test
    plane = _add_plane("TEST_Ground", (10, 8), (0, 0, 0))
    print(f"Plan créé: {plane.name}")
    print(f"Position: {plane.location}")
    print(f"Dimensions: {plane.dimensions}")
    
    # Créer un cube pour comparaison
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0, 0, 1))
    cube = bpy.context.active_object
    cube.name = "TEST_Cube"
    cube.scale = (3, 3, 2)
    
    print("Test terminé. Vérifiez que le plan est bien à Z=0 et le cube au-dessus.")

if __name__ == "__main__":
    test_plane_creation()
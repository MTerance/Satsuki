# Script de test rapide pour Blender - City Block Generator v6.13.8
# Copier-coller ce code dans l'éditeur de texte de Blender et cliquer "Run Script"

import bpy

# Test d'import de l'addon
try:
    import city_block_generator_clean
    print("✅ Addon city_block_generator_clean trouvé!")
except ImportError:
    print("❌ Addon non trouvé - Vérifier l'installation")

# Test de création basique
print("\\n🏙️ Test de génération basique...")

# Nettoyer la scène
bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete()

# Test simple de cubes avec couleurs
for i in range(3):
    # Créer un cube
    bpy.ops.mesh.primitive_cube_add(
        size=2,
        location=(i * 5, 0, 1)
    )
    
    obj = bpy.context.active_object
    obj.name = f"TestBuilding_{i}"
    
    # Créer un matériau coloré
    mat = bpy.data.materials.new(name=f"TestMat_{i}")
    mat.use_nodes = True
    
    bsdf = mat.node_tree.nodes.get("Principled BSDF")
    if bsdf:
        if i == 0:
            bsdf.inputs['Base Color'].default_value = (0.85, 0.82, 0.75, 1.0)  # Beige
        elif i == 1:
            bsdf.inputs['Base Color'].default_value = (0.65, 0.72, 0.78, 1.0)  # Bleu-gris
        else:
            bsdf.inputs['Base Color'].default_value = (0.70, 0.72, 0.75, 1.0)  # Gris moderne
    
    if obj.data.materials:
        obj.data.materials[0] = mat
    else:
        obj.data.materials.append(mat)

print("✅ Test basique terminé!")
print("\\n📋 INSTRUCTIONS:")
print("1. Si vous voyez 3 cubes colorés, les fonctions basiques marchent")
print("2. Ouvrir le panneau CityGen dans la sidebar (N)")
print("3. Cliquer 'Generate Varied City'")
print("4. Commencer avec Width=3, Length=3, Variety=MEDIUM")
# VALIDATION RAPIDE DU MODE DISTRICT
# Copiez-collez ce code dans l'éditeur de texte de Blender et exécutez-le

import bpy

def test_district_activation():
    """Test rapide pour valider l'activation du mode district."""
    
    print("=== TEST MODE DISTRICT ===")
    
    # Vérifier l'existence des propriétés
    if not hasattr(bpy.context.scene, 'citygen_props'):
        print("❌ ERREUR: Addon non activé ou propriétés manquantes")
        return False
    
    props = bpy.context.scene.citygen_props
    
    # Vérifier que le mode district est bien activé par défaut
    if props.district_mode:
        print("✅ Mode district ACTIVÉ par défaut")
    else:
        print("⚠️ Mode district DÉSACTIVÉ - Activation manuelle...")
        props.district_mode = True
    
    # Configuration de test
    print("\n--- Configuration de test ---")
    props.width = 6
    props.length = 6
    props.max_floors = 12
    props.block_variety = 'HIGH'
    props.base_block_size = 12.0
    props.commercial_ratio = 0.3
    props.residential_ratio = 0.5
    props.industrial_ratio = 0.2
    
    print(f"Grille: {props.width}x{props.length}")
    print(f"Variété: {props.block_variety}")
    print(f"Mode district: {props.district_mode}")
    print(f"Ratios - C:{props.commercial_ratio} R:{props.residential_ratio} I:{props.industrial_ratio}")
    
    # Nettoyage de la scène
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete(use_global=False)
    
    # Génération
    print("\n--- Génération en cours ---")
    try:
        result = bpy.ops.citygen.generate_city()
        if result == {'FINISHED'}:
            print("✅ Génération réussie !")
            
            # Compter les objets créés
            buildings = len([obj for obj in bpy.context.scene.objects if 'building' in obj.name.lower() or 'batiment' in obj.name.lower()])
            materials = set()
            for obj in bpy.context.scene.objects:
                if obj.data and hasattr(obj.data, 'materials'):
                    for mat in obj.data.materials:
                        if mat:
                            materials.add(mat.name)
            
            print(f"📊 Résultats:")
            print(f"   - Bâtiments créés: {buildings}")
            print(f"   - Matériaux: {len(materials)}")
            
            # Vérifier les matériaux de district
            district_materials = [mat for mat in materials if 'District' in mat]
            if district_materials:
                print(f"   - Matériaux de district détectés: {', '.join(district_materials)}")
                print("✅ Mode district FONCTIONNE !")
            else:
                print("⚠️ Aucun matériau de district détecté")
            
            return True
        else:
            print("❌ Échec de la génération")
            return False
    except Exception as e:
        print(f"❌ Erreur: {e}")
        return False

# Exécuter le test
success = test_district_activation()

if success:
    print("\n🎉 MODE DISTRICT VALIDÉ !")
    print("💡 Regardez la vue 3D pour voir les zones colorées")
    print("💡 Bleu=Commercial, Vert=Résidentiel, Orange=Industriel")
else:
    print("\n❌ PROBLÈME DÉTECTÉ")
    print("🔧 Vérifiez l'installation de l'addon")

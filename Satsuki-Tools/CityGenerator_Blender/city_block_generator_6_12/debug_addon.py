# Script de Débogage City Block Generator

import bpy

def debug_citygen_addon():
    """Script de débogage pour diagnostiquer les problèmes de génération"""
    
    print("=== DÉBUT DÉBOGAGE CITY BLOCK GENERATOR ===")
    
    # 1. Vérifier l'existence des propriétés (nouveau système direct)
    print("\n1. VÉRIFICATION DES PROPRIÉTÉS (système direct):")
    scene = bpy.context.scene
    
    print(f"✓ Propriétés directes sur la scène:")
    print(f"  citygen_width: {getattr(scene, 'citygen_width', 'NON DÉFINI')}")
    print(f"  citygen_length: {getattr(scene, 'citygen_length', 'NON DÉFINI')}")
    print(f"  citygen_max_floors: {getattr(scene, 'citygen_max_floors', 'NON DÉFINI')}")
    print(f"  citygen_road_width: {getattr(scene, 'citygen_road_width', 'NON DÉFINI')}")
    
    # Vérifier si les anciennes propriétés existent encore
    if hasattr(scene, 'citygen_props'):
        print("⚠ ATTENTION: Anciennes propriétés citygen_props encore présentes!")
    else:
        print("✓ Ancien système citygen_props correctement supprimé")
    
    # 2. Vérifier les objets existants
    print("\n2. OBJETS DANS LA SCÈNE:")
    total_objects = len(bpy.context.scene.objects)
    print(f"  Total objets: {total_objects}")
    
    # Compter par type
    roads = [obj for obj in bpy.context.scene.objects if 'road' in obj.name.lower() or 'route' in obj.name.lower()]
    sidewalks = [obj for obj in bpy.context.scene.objects if 'sidewalk' in obj.name.lower() or 'trottoir' in obj.name.lower()]
    buildings = [obj for obj in bpy.context.scene.objects if 'building' in obj.name.lower() or 'batiment' in obj.name.lower()]
    intersections = [obj for obj in bpy.context.scene.objects if 'intersection' in obj.name.lower() or 'carrefour' in obj.name.lower()]
    
    print(f"  Routes: {len(roads)}")
    for road in roads[:3]:  # Afficher les 3 premiers
        print(f"    - {road.name}")
    
    print(f"  Trottoirs: {len(sidewalks)}")
    for sidewalk in sidewalks[:3]:
        print(f"    - {sidewalk.name}")
    
    print(f"  Bâtiments: {len(buildings)}")
    for building in buildings[:3]:
        print(f"    - {building.name}")
    
    print(f"  Intersections: {len(intersections)}")
    for intersection in intersections[:3]:
        print(f"    - {intersection.name}")
    
    # 3. Vérifier les matériaux
    print("\n3. MATÉRIAUX:")
    road_mat = bpy.data.materials.get("RoadMat")
    side_mat = bpy.data.materials.get("SidewalkMat")  
    build_mat = bpy.data.materials.get("BuildingMat")
    
    print(f"  RoadMat: {'✓' if road_mat else '✗'}")
    print(f"  SidewalkMat: {'✓' if side_mat else '✗'}")
    print(f"  BuildingMat: {'✓' if build_mat else '✗'}")
    
    # 4. Test de génération simple
    print("\n4. TEST DE GÉNÉRATION:")
    try:
        # Configuration de test simple avec nouveau système
        scene.citygen_width = 2
        scene.citygen_length = 2
        scene.citygen_max_floors = 4
        scene.citygen_road_width = 4.0
        
        print("  Configuration de test appliquée (2x2, 4 étages max)")
        print("  Lancez maintenant la génération depuis l'interface Blender")
        
    except Exception as e:
        print(f"  ✗ Erreur lors de la configuration: {e}")
    
    print("\n=== FIN DÉBOGAGE ===")
    print("\nSI AUCUN BÂTIMENT N'APPARAÎT:")
    print("1. Vérifiez que 'District Mode' est activé")
    print("2. Essayez différents types de districts")
    print("3. Augmentez 'Max Floors' si nécessaire")
    print("4. Vérifiez la console Blender pour les messages d'erreur")

# Lancer le débogage
if __name__ == "__main__":
    debug_citygen_addon()

# Test complet d'ancrage pour tous les types de bâtiments jp_buildgen
# À exécuter dans Blender pour valider l'ancrage de chaque catégorie

import bpy
import random

def test_all_building_types():
    """Test d'ancrage pour tous les types de bâtiments"""
    
    # Nettoyer la scène
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete(use_global=False)
    
    # Constantes
    GROUND_LEVEL = 0.0
    PREFIX = "TEST_"
    
    def _add_cube(name, size=(2,2,2), loc=(0,0,0)):
        bpy.ops.mesh.primitive_cube_add(size=2.0, location=(0,0,0))
        o = bpy.context.active_object
        o.name = name
        o.scale = (size[0]/2.0, size[1]/2.0, size[2]/2.0)
        bpy.context.view_layer.objects.active = o
        bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
        bpy.ops.object.mode_set(mode='EDIT')
        bpy.ops.mesh.select_all(action='SELECT')
        bpy.ops.transform.translate(value=(0, 0, size[2]/2.0))
        bpy.ops.object.mode_set(mode='OBJECT')
        o.location = loc
        return o
    
    def _add_plane(name, size=(2,2), loc=(0,0,0)):
        bpy.ops.mesh.primitive_plane_add(size=2.0, location=loc)
        o = bpy.context.active_object
        o.name = name
        o.scale = (size[0]/2.0, size[1]/2.0, 1.0)
        bpy.context.view_layer.objects.active = o
        bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
        return o
    
    # Créer un plan de référence
    ground = _add_plane("REFERENCE_Ground", (50, 50), (0, 0, 0))
    print("Plan de référence créé à Z=0")
    
    # Test positions pour éviter les chevauchements
    positions = [
        (-15, -15),  # Office
        (0, -15),    # Mall
        (15, -15),   # Restaurant
        (-15, 0),    # Konbini
        (0, 0),      # Apartment
        (15, 0)      # House
    ]
    
    foot_x, foot_y = 8.0, 6.0
    floors, fh = 6, 3.5
    
    results = []
    
    # 1. TEST OFFICE
    x, y = positions[0]
    print(f"\n=== TEST OFFICE à position ({x}, {y}) ===")
    slab_th = 0.20
    total_h = floors * fh
    podium_h = fh * 2.0
    
    podium = _add_cube(f"{PREFIX}Office_Podium", (foot_x*1.2, foot_y*1.1, podium_h), (x, y, GROUND_LEVEL))
    tower = _add_cube(f"{PREFIX}Office_Tower", (foot_x*0.9, foot_y*0.9, total_h - podium_h), (x, y, GROUND_LEVEL + podium_h))
    roof = _add_cube(f"{PREFIX}Office_Roof", (foot_x*0.9, foot_y*0.9, slab_th*1.25), (x, y, GROUND_LEVEL + total_h))
    
    results.append(f"Office - Podium Z: {podium.location.z:.2f}, Tour Z: {tower.location.z:.2f}, Toit Z: {roof.location.z:.2f}")
    
    # 2. TEST MALL
    x, y = positions[1]
    print(f"\n=== TEST MALL à position ({x}, {y}) ===")
    slab_th = 0.22
    podium_f = max(2, min(floors, 3))
    podium_h = podium_f * fh
    
    podium = _add_cube(f"{PREFIX}Mall_Podium", (foot_x*1.6, foot_y*1.4, podium_h), (x, y, GROUND_LEVEL))
    roof = _add_cube(f"{PREFIX}Mall_Roof", (foot_x*1.6, foot_y*1.4, slab_th*1.2), (x, y, GROUND_LEVEL + podium_h))
    module = _add_cube(f"{PREFIX}Mall_Box_1", (foot_x*0.7, foot_y*0.6, fh*3.0), (x, y, GROUND_LEVEL + podium_h + slab_th*1.2))
    
    results.append(f"Mall - Podium Z: {podium.location.z:.2f}, Toit Z: {roof.location.z:.2f}, Module Z: {module.location.z:.2f}")
    
    # 3. TEST RESTAURANT
    x, y = positions[2]
    print(f"\n=== TEST RESTAURANT à position ({x}, {y}) ===")
    floors_rest = max(2, min(floors, 3))
    gfh = fh * 1.3
    total_h = gfh + (floors_rest-1)*fh
    
    body = _add_cube(f"{PREFIX}Rest_Body", (foot_x, foot_y*0.8, total_h), (x, y, GROUND_LEVEL))
    roof = _add_cube(f"{PREFIX}Rest_Roof", (foot_x, foot_y*0.8, 0.20), (x, y, GROUND_LEVEL + total_h))
    awning = _add_cube(f"{PREFIX}Rest_Awning", (foot_x*0.9, 0.06, 0.08), (x, y + (foot_y*0.8)/2 + 0.03, GROUND_LEVEL + 2.1))
    
    results.append(f"Restaurant - Corps Z: {body.location.z:.2f}, Toit Z: {roof.location.z:.2f}, Auvent Z: {awning.location.z:.2f}")
    
    # 4. TEST KONBINI
    x, y = positions[3]
    print(f"\n=== TEST KONBINI à position ({x}, {y}) ===")
    floors_konb = max(1, min(floors, 2))
    total_h = floors_konb * fh
    w, d = foot_x*1.2, foot_y*0.9
    
    body = _add_cube(f"{PREFIX}Konb_Body", (w, d, total_h), (x, y, GROUND_LEVEL))
    roof = _add_cube(f"{PREFIX}Konb_Roof", (w, d, 0.20), (x, y, GROUND_LEVEL + total_h))
    sign = _add_cube(f"{PREFIX}Konb_Sign", (w*0.85, 0.02, 0.6), (x, y + d/2 + 0.01, GROUND_LEVEL + 2.0))
    
    results.append(f"Konbini - Corps Z: {body.location.z:.2f}, Toit Z: {roof.location.z:.2f}, Enseigne Z: {sign.location.z:.2f}")
    
    # 5. TEST APARTMENT
    x, y = positions[4]
    print(f"\n=== TEST APARTMENT à position ({x}, {y}) ===")
    floors_apt = max(4, floors)
    total_h = floors_apt * fh
    
    body = _add_cube(f"{PREFIX}Apt_Body", (foot_x, foot_y*0.8, total_h), (x, y, GROUND_LEVEL))
    balcon = _add_cube(f"{PREFIX}Bal_3_1", (foot_x*0.22, 0.30, 0.12), (x, y + (foot_y*0.8)/2 + 0.15, GROUND_LEVEL + 3*fh - fh*0.35))
    shaft = _add_cube(f"{PREFIX}Apt_Shaft", (foot_x*0.2, foot_y*0.3, fh*1.2), (x + foot_x*0.32, y, GROUND_LEVEL + total_h))
    
    results.append(f"Apartment - Corps Z: {body.location.z:.2f}, Balcon Z: {balcon.location.z:.2f}, Gaine Z: {shaft.location.z:.2f}")
    
    # 6. TEST HOUSE
    x, y = positions[5]
    print(f"\n=== TEST HOUSE à position ({x}, {y}) ===")
    floors_house = max(1, min(floors, 2))
    h = floors_house * fh * 0.95
    w = max(6.0, min(foot_x, 12.0))
    d = max(6.0, min(foot_y, 10.0))
    
    body = _add_cube(f"{PREFIX}House_Body", (w, d, h), (x, y, GROUND_LEVEL))
    ridge_z = GROUND_LEVEL + h + 0.8 - 0.1
    roof_l = _add_cube(f"{PREFIX}House_Roof_L", (w*0.55, d*1.02, 0.2), (x - w*0.225, y, ridge_z))
    porch = _add_cube(f"{PREFIX}House_Porch", (w*0.5, 0.6, 0.2), (x, y + d/2 + 0.30, GROUND_LEVEL + 1.6))
    
    results.append(f"House - Corps Z: {body.location.z:.2f}, Toit Z: {roof_l.location.z:.2f}, Porche Z: {porch.location.z:.2f}")
    
    # Affichage des résultats
    print("\n" + "="*60)
    print("RÉSULTATS DU TEST D'ANCRAGE")
    print("="*60)
    for result in results:
        print(result)
    
    print(f"\nPlan de référence à Z={GROUND_LEVEL}")
    print("Vérifiez visuellement que tous les éléments principaux touchent le sol (Z=0)")
    print("et que les éléments empilés sont correctement positionnés.")

if __name__ == "__main__":
    test_all_building_types()
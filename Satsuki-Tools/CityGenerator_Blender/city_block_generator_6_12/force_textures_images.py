# FORCE APPLICATION TEXTURES IMAGES - À copier-coller dans la console Blender
# Ce script va forcer l'application de vraies textures images sur tous les bâtiments

import bpy
import os

def forcer_textures_images():
    print("🔄 FORCE APPLICATION TEXTURES IMAGES")
    print("=" * 60)
    
    # Vérifier le système de textures
    try:
        import sys
        if 'tokyo_city_generator' in sys.modules:
            module = sys.modules['tokyo_city_generator']
            if hasattr(module, 'tokyo_texture_system'):
                texture_system = module.tokyo_texture_system
                print("✅ Système de textures trouvé")
            else:
                print("❌ Système de textures manquant")
                return
        else:
            print("❌ Module tokyo_city_generator manquant")
            return
    except Exception as e:
        print(f"❌ Erreur accès système: {e}")
        return
    
    # Parcourir tous les bâtiments Tokyo
    buildings = [obj for obj in bpy.data.objects if 'tokyo' in obj.name.lower() and 'building' in obj.name.lower()]
    
    if not buildings:
        print("❌ Aucun bâtiment Tokyo trouvé")
        return
    
    print(f"🏢 {len(buildings)} bâtiments trouvés")
    
    textures_appliquees = 0
    
    for building in buildings:
        try:
            # Identifier le type de bâtiment
            building_type = "residential"  # Défaut
            
            if "commercial" in building.name.lower():
                building_type = "commercial"
            elif "skyscraper" in building.name.lower():
                building_type = "skyscrapers"
            elif "house" in building.name.lower():
                building_type = "residential"
            
            # Créer un nouveau matériau avec texture
            width = building.dimensions.x
            height = building.dimensions.z
            depth = building.dimensions.y
            
            # Nettoyer les anciens matériaux
            building.data.materials.clear()
            
            # Créer nouveau matériau avec texture forcée
            new_material = texture_system.create_advanced_building_material(
                building_type, width, height, depth, f"ForceTexture_{building.name}", ""
            )
            
            if new_material:
                # Assigner le nouveau matériau
                building.data.materials.append(new_material)
                
                # Vérifier si des textures images sont présentes
                if new_material.use_nodes and new_material.node_tree:
                    tex_nodes = [n for n in new_material.node_tree.nodes if n.type == 'TEX_IMAGE']
                    if tex_nodes:
                        print(f"✅ {building.name}: {len(tex_nodes)} textures appliquées")
                        textures_appliquees += 1
                    else:
                        print(f"⚠️ {building.name}: matériau procédural (pas d'image)")
                else:
                    print(f"❌ {building.name}: échec matériau")
            else:
                print(f"❌ {building.name}: échec création matériau")
                
        except Exception as e:
            print(f"❌ {building.name}: erreur {e}")
    
    print("=" * 60)
    print(f"🎯 RÉSULTAT: {textures_appliquees}/{len(buildings)} bâtiments avec textures images")
    
    if textures_appliquees == 0:
        print("\n🔍 DIAGNOSTIC CHEMIN TEXTURES:")
        scene = bpy.context.scene
        if hasattr(scene, 'tokyo_texture_base_path'):
            base_path = scene.tokyo_texture_base_path
            print(f"📁 Chemin configuré: {base_path}")
            
            # Vérifier les sous-dossiers
            for subdir in ['residential', 'commercial', 'skyscrapers']:
                full_path = os.path.join(base_path, subdir)
                if os.path.exists(full_path):
                    try:
                        files = os.listdir(full_path)
                        img_files = [f for f in files if f.lower().endswith(('.png', '.jpg', '.jpeg'))]
                        print(f"   {subdir}: {len(img_files)} images trouvées")
                        if img_files:
                            print(f"      Exemples: {img_files[:3]}")
                    except:
                        print(f"   {subdir}: erreur lecture")
                else:
                    print(f"   {subdir}: dossier manquant")

# Exécuter
forcer_textures_images()

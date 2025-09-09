# FORCE CORRECTION COMPLETE CHEMINS - À copier-coller dans la console Blender
# Ce script va forcer l'utilisation du bon chemin partout et régénérer les matériaux

import bpy
import os
import sys

def force_correction_complete():
    print("🔧 FORCE CORRECTION COMPLETE CHEMINS")
    print("=" * 60)
    
    # 1. Corriger le chemin de base
    scene = bpy.context.scene
    bon_chemin = r"C:\Users\sshom\Documents\assets\Tools\tokyo_textures"
    scene.tokyo_texture_base_path = bon_chemin
    print(f"✅ Chemin forcé: {bon_chemin}")
    
    # 2. Accéder au système de textures
    try:
        module = sys.modules['tokyo_city_generator']
        texture_system = module.tokyo_texture_system
        print("✅ Système de textures accessible")
    except Exception as e:
        print(f"❌ Erreur système: {e}")
        return
    
    # 3. Forcer la mise à jour du chemin dans le système
    if hasattr(texture_system, 'base_path'):
        texture_system.base_path = bon_chemin
        print("✅ Chemin système mis à jour")
    
    # 4. Vérifier tous les dossiers de textures
    dossiers_requis = ['residential', 'commercial', 'skyscrapers', 'lowrise', 'midrise']
    
    for dossier in dossiers_requis:
        chemin_dossier = os.path.join(bon_chemin, dossier)
        if os.path.exists(chemin_dossier):
            files = os.listdir(chemin_dossier)
            images = [f for f in files if f.lower().endswith(('.png', '.jpg', '.jpeg', '.tiff'))]
            print(f"📁 {dossier}: {len(images)} images")
            
            if len(images) > 0:
                print(f"   Exemples: {images[:3]}")
        else:
            print(f"❌ {dossier}: dossier manquant")
    
    # 5. Régénérer tous les matériaux des bâtiments existants
    print("\n🔄 RÉGÉNÉRATION MATÉRIAUX:")
    
    buildings = [obj for obj in bpy.data.objects if 'tokyo' in obj.name.lower() and 'building' in obj.name.lower()]
    
    if buildings:
        print(f"🏢 {len(buildings)} bâtiments trouvés")
        
        materiaux_avec_textures = 0
        
        for building in buildings:
            try:
                # Identifier le type de bâtiment
                building_type = "residential"  # Par défaut
                
                if "commercial" in building.name.lower():
                    building_type = "commercial"
                elif "skyscraper" in building.name.lower():
                    building_type = "skyscrapers"
                elif any(x in building.name.lower() for x in ["house", "residential"]):
                    building_type = "residential"
                elif "lowrise" in building.name.lower():
                    building_type = "lowrise"
                elif "midrise" in building.name.lower():
                    building_type = "midrise"
                
                # Nettoyer les anciens matériaux
                building.data.materials.clear()
                
                # Créer nouveau matériau avec le bon chemin
                width = building.dimensions.x
                height = building.dimensions.z
                depth = building.dimensions.y
                
                nouveau_materiau = texture_system.create_advanced_building_material(
                    building_type, width, height, depth, f"Fixed_{building.name}", ""
                )
                
                if nouveau_materiau:
                    building.data.materials.append(nouveau_materiau)
                    
                    # Vérifier si des textures images sont présentes
                    if nouveau_materiau.use_nodes and nouveau_materiau.node_tree:
                        tex_nodes = [n for n in nouveau_materiau.node_tree.nodes if n.type == 'TEX_IMAGE']
                        if tex_nodes and any(n.image for n in tex_nodes):
                            materiaux_avec_textures += 1
                            print(f"✅ {building.name}: {len(tex_nodes)} textures appliquées")
                        else:
                            print(f"⚠️ {building.name}: matériau procédural")
                    else:
                        print(f"❌ {building.name}: pas de nodes")
                else:
                    print(f"❌ {building.name}: échec création")
                    
            except Exception as e:
                print(f"❌ {building.name}: erreur {e}")
        
        print(f"\n🎯 RÉSULTAT: {materiaux_avec_textures}/{len(buildings)} bâtiments avec vraies textures")
        
        if materiaux_avec_textures > 0:
            print("✅ SUCCÈS! Certains bâtiments ont maintenant des textures!")
            print("💡 Passez en mode MATERIAL ou RENDERED pour les voir")
        else:
            print("⚠️ Aucune texture image chargée - vérifiez le contenu des dossiers")
    else:
        print("❌ Aucun bâtiment trouvé")
    
    print("\n" + "=" * 60)
    print("🎯 CORRECTION TERMINÉE")

# Exécuter
force_correction_complete()

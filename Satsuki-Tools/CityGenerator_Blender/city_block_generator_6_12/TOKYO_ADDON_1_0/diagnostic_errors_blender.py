# DIAGNOSTIC ERREURS TOKYO v1.3.0
# Script à exécuter DANS Blender pour diagnostiquer les erreurs

import bpy
import sys
import os
import traceback

def diagnostic_tokyo_errors():
    """Diagnostic complet des erreurs Tokyo City Generator"""
    
    print("🔍 DIAGNOSTIC ERREURS TOKYO CITY GENERATOR")
    print("=" * 50)
    
    # 1. Vérifier si l'addon est installé
    print("📦 1. VÉRIFICATION INSTALLATION")
    print("-" * 30)
    
    addon_name = "tokyo_city_generator"
    if addon_name in bpy.context.preferences.addons:
        addon = bpy.context.preferences.addons[addon_name]
        print(f"✅ Addon trouvé: {addon_name}")
        
        # Récupérer les infos de l'addon
        try:
            module = addon.module
            if hasattr(module, 'bl_info'):
                info = module.bl_info
                print(f"📋 Nom: {info.get('name', 'Non défini')}")
                print(f"🔢 Version: {info.get('version', 'Non définie')}")
                print(f"👤 Auteur: {info.get('author', 'Non défini')}")
                print(f"📝 Description: {info.get('description', 'Non définie')}")
            else:
                print("⚠️ bl_info non trouvé")
        except Exception as e:
            print(f"❌ Erreur lecture addon: {e}")
    else:
        print(f"❌ Addon non trouvé: {addon_name}")
        print("🔧 L'addon n'est peut-être pas activé")
        return False
    
    # 2. Vérifier les modules importés
    print(f"\n🧩 2. VÉRIFICATION MODULES")
    print("-" * 30)
    
    try:
        # Tester l'import du module principal
        import tokyo_city_generator
        print("✅ Module principal importé")
        
        # Vérifier les sous-modules
        modules_to_check = [
            'texture_system',
            '__init__'
        ]
        
        for module_name in modules_to_check:
            try:
                if hasattr(tokyo_city_generator, module_name.replace('__init__', '')):
                    print(f"✅ Module {module_name} disponible")
                else:
                    print(f"⚠️ Module {module_name} non trouvé")
            except Exception as e:
                print(f"❌ Erreur module {module_name}: {e}")
                
    except ImportError as e:
        print(f"❌ Impossible d'importer tokyo_city_generator: {e}")
        return False
    except Exception as e:
        print(f"❌ Erreur inattendue lors de l'import: {e}")
        return False
    
    # 3. Vérifier les opérateurs
    print(f"\n⚙️ 3. VÉRIFICATION OPÉRATEURS")
    print("-" * 30)
    
    operators_to_check = [
        'mesh.tokyo_city_generator',
        'mesh.tokyo_setup_textures'
    ]
    
    for op_name in operators_to_check:
        if hasattr(bpy.ops, op_name.split('.')[0]):
            category = getattr(bpy.ops, op_name.split('.')[0])
            if hasattr(category, op_name.split('.')[1]):
                print(f"✅ Opérateur {op_name} disponible")
            else:
                print(f"❌ Opérateur {op_name} manquant")
        else:
            print(f"❌ Catégorie {op_name.split('.')[0]} manquante")
    
    # 4. Vérifier les propriétés
    print(f"\n🎛️ 4. VÉRIFICATION PROPRIÉTÉS")
    print("-" * 30)
    
    scene = bpy.context.scene
    properties_to_check = [
        'tokyo_grid_size',
        'tokyo_block_size',
        'tokyo_use_advanced_textures',
        'tokyo_texture_base_path'
    ]
    
    for prop_name in properties_to_check:
        if hasattr(scene, prop_name):
            prop_value = getattr(scene, prop_name)
            print(f"✅ Propriété {prop_name}: {prop_value}")
        else:
            print(f"❌ Propriété {prop_name} manquante")
    
    # 5. Vérifier l'interface utilisateur
    print(f"\n🖥️ 5. VÉRIFICATION INTERFACE")
    print("-" * 30)
    
    try:
        # Chercher le panneau Tokyo
        for area in bpy.context.screen.areas:
            if area.type == 'VIEW_3D':
                for space in area.spaces:
                    if space.type == 'VIEW_3D':
                        print("✅ Vue 3D trouvée")
                        break
        
        # Vérifier si les panneaux sont enregistrés
        panels_to_check = [
            'VIEW3D_PT_tokyo_city_generator'
        ]
        
        for panel_name in panels_to_check:
            try:
                # Essayer de trouver le panneau dans les classes enregistrées
                found = False
                for cls in bpy.types.__dict__.values():
                    if hasattr(cls, '__name__') and cls.__name__ == panel_name:
                        print(f"✅ Panneau {panel_name} enregistré")
                        found = True
                        break
                
                if not found:
                    print(f"❌ Panneau {panel_name} non enregistré")
                    
            except Exception as e:
                print(f"❌ Erreur vérification panneau {panel_name}: {e}")
                
    except Exception as e:
        print(f"❌ Erreur vérification interface: {e}")
    
    # 6. Test de génération basique
    print(f"\n🧪 6. TEST GÉNÉRATION BASIQUE")
    print("-" * 30)
    
    try:
        # Sauvegarder la sélection actuelle
        original_selection = bpy.context.selected_objects.copy()
        
        # Nettoyer la scène pour le test
        bpy.ops.object.select_all(action='SELECT')
        bpy.ops.object.delete(use_global=False)
        
        # Test de génération minimale
        bpy.context.scene.tokyo_grid_size = 2
        bpy.context.scene.tokyo_block_size = 20.0
        
        # Essayer de lancer la génération
        result = bpy.ops.mesh.tokyo_city_generator()
        
        if result == {'FINISHED'}:
            print("✅ Test de génération réussi")
            
            # Compter les objets créés
            objects_created = len(bpy.context.scene.objects)
            print(f"📊 {objects_created} objets créés")
            
        else:
            print(f"❌ Test de génération échoué: {result}")
            
    except Exception as e:
        print(f"❌ Erreur test génération: {e}")
        traceback.print_exc()
    
    # 7. Vérifier les chemins de textures
    print(f"\n🎨 7. VÉRIFICATION TEXTURES")
    print("-" * 30)
    
    try:
        if hasattr(bpy.context.scene, 'tokyo_texture_base_path'):
            texture_path = bpy.context.scene.tokyo_texture_base_path
            print(f"📁 Chemin textures: {texture_path}")
            
            if os.path.exists(texture_path):
                print("✅ Dossier textures existe")
                
                # Compter les sous-dossiers
                subdirs = [d for d in os.listdir(texture_path) 
                          if os.path.isdir(os.path.join(texture_path, d))]
                print(f"📊 {len(subdirs)} sous-dossiers trouvés")
                
                for subdir in subdirs[:5]:  # Afficher les 5 premiers
                    print(f"  📂 {subdir}")
                    
            else:
                print("❌ Dossier textures n'existe pas")
        else:
            print("❌ Propriété chemin textures manquante")
            
    except Exception as e:
        print(f"❌ Erreur vérification textures: {e}")
    
    print(f"\n✅ DIAGNOSTIC TERMINÉ")
    print("🔧 Si des erreurs sont trouvées, vérifiez:")
    print("   - L'addon est activé dans les préférences")
    print("   - Blender a été redémarré après installation")
    print("   - Aucun conflit avec d'autres addons")
    print("   - Le dossier de textures existe")

def run_diagnostic():
    """Lance le diagnostic"""
    try:
        diagnostic_tokyo_errors()
    except Exception as e:
        print(f"❌ ERREUR CRITIQUE DIAGNOSTIC: {e}")
        traceback.print_exc()

# Exécuter le diagnostic si lancé directement
if __name__ == "__main__":
    run_diagnostic()

# Instructions pour utilisation dans Blender
"""
UTILISATION DANS BLENDER:
1. Ouvrez Blender
2. Allez dans Scripting workspace
3. Copiez ce script dans l'éditeur de texte
4. Cliquez sur "Run Script"
5. Regardez la console pour les résultats

OU

1. Ouvrez la console Python dans Blender (Window > Toggle System Console)
2. Copiez et collez ce script
3. Appuyez sur Entrée
"""

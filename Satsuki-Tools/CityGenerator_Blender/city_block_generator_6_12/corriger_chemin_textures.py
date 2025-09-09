# CORRECTION CHEMIN TEXTURES - À copier-coller dans la console Blender
# Ce script va corriger le chemin vers vos vraies textures

import bpy
import os

def corriger_chemin_textures():
    print("🔧 CORRECTION CHEMIN TEXTURES")
    print("=" * 50)
    
    # Chemin actuel (incorrect)
    scene = bpy.context.scene
    ancien_chemin = scene.tokyo_texture_base_path
    print(f"❌ Ancien chemin: {ancien_chemin}")
    
    # Nouveau chemin (correct)
    nouveau_chemin = r"C:\Users\sshom\Documents\assets\Tools\tokyo_textures"
    print(f"✅ Nouveau chemin: {nouveau_chemin}")
    
    # Vérifier que le nouveau chemin existe
    if os.path.exists(nouveau_chemin):
        print("✅ Le nouveau chemin existe")
        
        # Lister le contenu pour confirmation
        contenu = os.listdir(nouveau_chemin)
        print(f"📁 Contenu: {contenu}")
        
        # Appliquer le nouveau chemin
        scene.tokyo_texture_base_path = nouveau_chemin
        print("✅ Chemin mis à jour")
        
        # Vérifier les sous-dossiers
        for subdir in ['residential', 'commercial', 'skyscrapers', 'lowrise', 'midrise']:
            full_path = os.path.join(nouveau_chemin, subdir)
            if os.path.exists(full_path):
                files = os.listdir(full_path)
                images = [f for f in files if f.lower().endswith(('.png', '.jpg', '.jpeg'))]
                print(f"   {subdir}: {len(images)} images")
            else:
                print(f"   {subdir}: dossier manquant")
        
        print("\n🎯 MAINTENANT RÉGÉNÉREZ VOS BÂTIMENTS !")
        print("   1. Supprimez votre ville actuelle")
        print("   2. Régénérez avec le bon chemin")
        print("   3. Les textures devraient apparaître !")
        
    else:
        print(f"❌ Le nouveau chemin n'existe pas: {nouveau_chemin}")
        print("📁 Vérifiez l'emplacement de vos textures")

# Exécuter
corriger_chemin_textures()

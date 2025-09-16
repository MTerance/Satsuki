#!/usr/bin/env python3
"""
TOKYO CITY GENERATOR v2.2.0 EXTENDED - DÉPLOIEMENT
================================================================

✨ NOUVELLES FONCTIONNALITÉS v2.2.0 ✨
🏥 6 NOUVEAUX TYPES DE BÂTIMENTS :
   - Hospitals (hôpitaux) - hauts et larges, couleurs médicales
   - Temples - traditionnels avec toits pyramidaux  
   - Factories (usines) - industriels avec conduits
   - Malls (centres commerciaux) - forme en L/U, colorés
   - Stations (gares) - allongées avec toits arrondis
   - Skyscrapers (gratte-ciels) - structure étagée ultra-haute

🎨 MATÉRIAUX SPÉCIALISÉS :
   - Hospital: Blanc/vert médical
   - Temple: Rouge vermillon traditionnel
   - Factory: Gris acier/rouille industriel  
   - Mall: Couleurs vives commerciales
   - Station: Gris/bleu transport
   - Skyscraper: Noir/bleu acier ultra-moderne

🏗️ FORMES ARCHITECTURALES UNIQUES :
   - Temples avec toits coniques 
   - Usines avec conduits cylindriques
   - Stations avec toits arrondis
   - Gratte-ciels étagés (base + milieu + sommet)
   - Centres commerciaux en forme de L

🎯 TOTAL : 14 TYPES DE BÂTIMENTS !
   Previous: residential, office, commercial, tower, hotel, mixed_use, warehouse, school
   NEW: hospital, temple, factory, mall, station, skyscraper

📦 Ce script génère tokyo_v2_2_0_EXTENDED.zip pour installation Blender
"""

import os
import shutil
import zipfile

def deploy_extended_tokyo():
    print("🏗️ DÉPLOIEMENT TOKYO CITY GENERATOR v2.2.0 EXTENDED")
    print("=" * 60)
    
    # Répertoires
    source_dir = "TOKYO_SIMPLE_V2_1"
    temp_dir = "TOKYO_EXTENDED_V2_2_0"
    zip_name = "tokyo_v2_2_0_EXTENDED.zip"
    
    # Nettoyer le répertoire temporaire
    if os.path.exists(temp_dir):
        shutil.rmtree(temp_dir)
    
    # Copier les fichiers
    print(f"📁 Copie de {source_dir} vers {temp_dir}...")
    shutil.copytree(source_dir, temp_dir)
    
    # Supprimer l'ancien ZIP s'il existe
    if os.path.exists(zip_name):
        os.remove(zip_name)
        print(f"🗑️ Ancien {zip_name} supprimé")
    
    # Créer le ZIP avec la structure correcte pour Blender
    print(f"📦 Création de {zip_name}...")
    with zipfile.ZipFile(zip_name, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(temp_dir):
            for file in files:
                file_path = os.path.join(root, file)
                # Structure: TOKYO_EXTENDED_V2_2_0/__init__.py
                arcname = os.path.relpath(file_path, ".")
                zipf.write(file_path, arcname)
    
    # Nettoyer le répertoire temporaire  
    shutil.rmtree(temp_dir)
    
    # Vérifier la création
    if os.path.exists(zip_name):
        size = os.path.getsize(zip_name) // 1024
        print(f"✅ {zip_name} créé avec succès ({size} KB)")
        
        # Vérifier le contenu du ZIP
        with zipfile.ZipFile(zip_name, 'r') as zipf:
            files = zipf.namelist()
            print(f"📋 Contenu du ZIP ({len(files)} fichiers):")
            for f in files[:5]:  # Afficher les 5 premiers
                print(f"   {f}")
            if len(files) > 5:
                print(f"   ... et {len(files)-5} autres fichiers")
    else:
        print("❌ Erreur lors de la création du ZIP")
        return False
    
    print("\n" + "="*60)
    print("🎉 TOKYO v2.2.0 EXTENDED PRÊT POUR INSTALLATION !")
    print("="*60)
    print("📋 INSTRUCTIONS D'INSTALLATION :")
    print("1. Ouvrez Blender 4.0+")
    print("2. Edit > Preferences > Add-ons")  
    print("3. Install > Sélectionnez tokyo_v2_2_0_EXTENDED.zip")
    print("4. Activez 'Tokyo City Generator v2.2.0 Extended'")
    print("5. Dans la vue 3D : sidebar (N) > CityGen")
    
    print("\n🏗️ NOUVEAUX TYPES DISPONIBLES :")
    print("   🏥 Hospital - Hôpitaux modernes")
    print("   ⛩️ Temple - Sanctuaires traditionnels") 
    print("   🏭 Factory - Complexes industriels")
    print("   🏬 Mall - Centres commerciaux")
    print("   🚉 Station - Gares et stations")
    print("   🏢 Skyscraper - Gratte-ciels ultra-hauts")
    
    print("\n✨ TEST RECOMMANDÉ :")
    print("   - Grille: 4x4 ou 5x5")
    print("   - Style: Mixed pour voir tous les types")
    print("   - Densité: 0.7-0.8 pour variété optimale")
    print("   - Mode: Material Preview pour voir les couleurs")
    
    return True

if __name__ == "__main__":
    deploy_extended_tokyo()
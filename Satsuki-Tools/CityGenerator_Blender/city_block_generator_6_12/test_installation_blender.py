# TEST INSTALLATION TOKYO SIMPLE V2.1 DANS BLENDER

# 🎯 PROCÉDURE DE TEST COMPLÈTE

import os
import subprocess
import sys

def test_blender_installation():
    """Test complet de l'installation de Tokyo Simple v2.1 dans Blender"""
    
    print("🚀 DÉBUT DU TEST D'INSTALLATION TOKYO SIMPLE V2.1")
    print("=" * 60)
    
    # Étape 1: Vérifier l'existence du ZIP
    zip_path = "tokyo_simple_v2_1.zip"
    
    if not os.path.exists(zip_path):
        print("❌ ERREUR: tokyo_simple_v2_1.zip non trouvé!")
        return False
    
    print(f"✅ ZIP trouvé: {zip_path}")
    print(f"   Taille: {os.path.getsize(zip_path)} bytes")
    
    # Étape 2: Vérifier le contenu du ZIP
    try:
        import zipfile
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            files = zip_ref.namelist()
            print(f"✅ Contenu ZIP: {len(files)} fichier(s)")
            for file in files:
                print(f"   - {file}")
            
            # Vérifier la structure attendue
            expected_files = ["TOKYO_SIMPLE_V2_1/__init__.py"]
            for expected in expected_files:
                if expected in files:
                    print(f"✅ Structure correcte: {expected}")
                else:
                    print(f"❌ MANQUE: {expected}")
                    return False
    
    except Exception as e:
        print(f"❌ ERREUR lors de la lecture du ZIP: {e}")
        return False
    
    # Étape 3: Instructions d'installation dans Blender
    print("\n🔧 INSTRUCTIONS D'INSTALLATION DANS BLENDER:")
    print("-" * 50)
    print("1. Ouvrir Blender 4.0+")
    print("2. Edit → Preferences → Add-ons")
    print("3. Cliquer 'Install...'")
    print(f"4. Sélectionner le fichier: {os.path.abspath(zip_path)}")
    print("5. Activer 'Tokyo City Generator v2.1 SIMPLE'")
    print("6. Fermer les Preferences")
    print("7. Vue 3D → Sidebar (N) → Onglet 'Tokyo'")
    
    # Étape 4: Checklist de validation
    print("\n✅ CHECKLIST DE VALIDATION:")
    print("-" * 40)
    print("□ L'addon apparaît dans la liste des Add-ons")
    print("□ L'addon s'active sans erreur")
    print("□ L'onglet 'Tokyo' apparaît dans la sidebar")
    print("□ Le panneau 'Tokyo City Generator' est visible")
    print("□ Les 4 paramètres sont affichés:")
    print("  - City Size (3-10)")
    print("  - Building Style (Low/Mixed/High)")
    print("  - Density (slider 0.3-1.0)")
    print("  - Better Materials (checkbox)")
    print("□ Le bouton 'Generate Tokyo City' est visible")
    print("□ Le bouton 'Clear City' est visible")
    
    # Étape 5: Test de génération
    print("\n🏙️ TEST DE GÉNÉRATION:")
    print("-" * 30)
    print("1. Paramètres recommandés pour le premier test:")
    print("   - City Size: 5")
    print("   - Building Style: Mixed")
    print("   - Density: 70%")
    print("   - Better Materials: ON")
    print("2. Cliquer 'Generate Tokyo City'")
    print("3. Vérifier:")
    print("   □ Génération sans erreur (< 5 secondes)")
    print("   □ Routes grises visibles en grille")
    print("   □ Bâtiments de hauteurs variées")
    print("   □ Pas de chevauchement routes/bâtiments")
    print("   □ Matériaux colorés différents")
    print("   □ Message de succès affiché")
    
    # Étape 6: Test de nettoyage
    print("\n🗑️ TEST DE NETTOYAGE:")
    print("-" * 25)
    print("1. Cliquer 'Clear City'")
    print("2. Vérifier:")
    print("   □ Tous les objets Tokyo disparaissent")
    print("   □ Message de confirmation affiché")
    print("   □ Scène vide prête pour nouvelle génération")
    
    print("\n🎯 RÉSULTATS ATTENDUS:")
    print("-" * 30)
    print("✅ Interface simple et claire (4 paramètres)")
    print("✅ Génération rapide et fiable")
    print("✅ Ville avec routes + bâtiments bien séparés")
    print("✅ Variété visuelle automatique")
    print("✅ Contrôles fonctionnels")
    
    print("\n" + "=" * 60)
    print("🎉 PRÊT POUR LE TEST DANS BLENDER!")
    print(f"📁 Fichier à installer: {os.path.abspath(zip_path)}")
    
    return True

if __name__ == "__main__":
    test_blender_installation()
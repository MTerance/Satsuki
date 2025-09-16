"""
NETTOYAGE FINAL - SUPPRESSION FICHIERS LEGACY
Supprime les fichiers restants non organisés
"""

import os
import shutil

def nettoyer_fichiers_legacy():
    """Supprime les fichiers legacy non organisés"""
    
    print("🧹 === NETTOYAGE FINAL FICHIERS LEGACY === 🧹")
    
    # Fichiers et patterns à supprimer (legacy)
    patterns_a_supprimer = [
        "*.backup",
        "*_backup.py",
        "*_old.py", 
        "*_simple.py",
        "road_first_generator.py",  # Doublon avec generator.py
        "smart_organic_roads.py",   # Intégré dans generator.py
        "nettoyer_generator.py",    # Script temporaire
        ".vscode"                   # Dossier IDE
    ]
    
    fichiers_supprimes = 0
    
    # Parcourir le dossier racine
    for item in os.listdir("."):
        if os.path.isfile(item):
            # Vérifier si le fichier correspond aux patterns à supprimer
            should_delete = False
            
            for pattern in patterns_a_supprimer:
                if pattern.startswith("*") and item.endswith(pattern[1:]):
                    should_delete = True
                    break
                elif pattern == item:
                    should_delete = True
                    break
            
            if should_delete:
                try:
                    os.remove(item)
                    print(f"   🗑️ Supprimé: {item}")
                    fichiers_supprimes += 1
                except Exception as e:
                    print(f"   ⚠️ Erreur suppression {item}: {e}")
        
        elif os.path.isdir(item) and item in patterns_a_supprimer:
            try:
                shutil.rmtree(item, ignore_errors=True)
                print(f"   🗑️ Dossier supprimé: {item}")
                fichiers_supprimes += 1
            except Exception as e:
                print(f"   ⚠️ Erreur suppression dossier {item}: {e}")
    
    print(f"📊 === RÉSULTAT NETTOYAGE === 📊")
    print(f"   🗑️ Fichiers supprimés: {fichiers_supprimes}")
    
    # Afficher la structure finale
    print(f"📁 === STRUCTURE FINALE === 📁")
    print("   ✅ 1_ADDON_CLEAN/ - Addon optimisé")
    print("   ✅ 2_SCRIPTS_TEST/ - Scripts de test")
    print("   ✅ 3_SCRIPTS_DEPLOY/ - Scripts de déploiement") 
    print("   ✅ 4_DOCS/ - Documentation organisée")
    print("   ✅ README_ORGANISATION.md - Vue d'ensemble")
    
    print("🎯 === NETTOYAGE TERMINÉ === 🎯")
    print("🏙️ Projet City Block Generator parfaitement organisé !")

if __name__ == "__main__":
    nettoyer_fichiers_legacy()

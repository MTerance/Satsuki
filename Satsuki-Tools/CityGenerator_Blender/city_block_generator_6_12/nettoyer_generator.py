"""
NETTOYAGE AUTOMATIQUE GENERATOR.PY V6.14.0
Supprime les fonctions mortes et optimise le code
"""

import re

def nettoyer_generator():
    """Nettoie generator.py en supprimant les fonctions inutilisées"""
    
    print("🧹 === NETTOYAGE GENERATOR.PY === 🧹")
    
    # Lire le fichier original
    with open("generator.py", 'r', encoding='utf-8') as f:
        content = f.read()
    
    print(f"📄 Taille originale: {len(content)} caractères")
    
    # Fonctions à supprimer (code mort)
    fonctions_mortes = [
        "create_realistic_organic_road_grid_rf",
        "create_rectangular_road_grid_rf", 
        "create_organic_road_grid_rf"  # L'ancienne version
    ]
    
    content_nettoye = content
    
    for fonction in fonctions_mortes:
        print(f"🗑️ Suppression de {fonction}...")
        
        # Trouver le début de la fonction
        pattern_debut = rf"def {fonction}\([^)]*\):"
        match_debut = re.search(pattern_debut, content_nettoye)
        
        if match_debut:
            debut_idx = match_debut.start()
            
            # Trouver la fin (prochaine fonction ou fin de fichier)
            # Chercher la prochaine fonction au même niveau d'indentation
            reste_contenu = content_nettoye[debut_idx:]
            
            # Chercher la prochaine fonction def au début de ligne
            pattern_fin = r"\ndef [a-zA-Z_]"
            match_fin = re.search(pattern_fin, reste_contenu[1:])  # Skip première ligne
            
            if match_fin:
                fin_idx = debut_idx + match_fin.start() + 1
            else:
                fin_idx = len(content_nettoye)
            
            # Supprimer la fonction
            avant = content_nettoye[:debut_idx]
            apres = content_nettoye[fin_idx:]
            content_nettoye = avant + apres
            
            print(f"   ✅ {fonction} supprimée")
        else:
            print(f"   ⚠️ {fonction} non trouvée")
    
    # Nettoyer les commentaires excessifs et debug prints
    print("🧹 Nettoyage des commentaires debug...")
    
    # Supprimer les lignes de debug trop verbeuses
    lignes = content_nettoye.split('\n')
    lignes_nettoyees = []
    
    for ligne in lignes:
        # Garder les print importants, supprimer le debug excessif
        if 'print(f"      Point' in ligne:  # Debug points trop détaillé
            continue
        if 'print(f"         ✅ Route courbe' in ligne and 'créée avec' in ligne:
            continue
        if '# Debug tous les 10 points' in ligne:
            continue
            
        lignes_nettoyees.append(ligne)
    
    content_nettoye = '\n'.join(lignes_nettoyees)
    
    # Supprimer les espaces multiples
    content_nettoye = re.sub(r'\n\n\n+', '\n\n', content_nettoye)
    
    print(f"📄 Taille nettoyée: {len(content_nettoye)} caractères")
    print(f"💾 Réduction: {len(content) - len(content_nettoye)} caractères")
    
    # Sauvegarder
    with open("1_ADDON_CLEAN/generator.py", 'w', encoding='utf-8') as f:
        f.write(content_nettoye)
    
    print("✅ generator.py nettoyé sauvegardé dans 1_ADDON_CLEAN/")

if __name__ == "__main__":
    nettoyer_generator()

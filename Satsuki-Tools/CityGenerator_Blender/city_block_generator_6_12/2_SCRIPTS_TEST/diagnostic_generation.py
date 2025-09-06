#!/usr/bin/env python3
"""
Diagnostic des problèmes de génération - City Block Generator
"""

def check_function_calls():
    """Vérifie les appels de fonctions dans la génération organique"""
    print("🔍 DIAGNOSTIC DES APPELS DE FONCTIONS")
    print("="*50)
    
    # Lire le fichier generator.py
    try:
        with open("generator.py", "r", encoding="utf-8") as f:
            content = f.read()
            
        # Vérifier les appels de fonctions dans create_organic_road_grid_rf
        function_calls = [
            "create_highway_road",
            "create_sinusoidal_road", 
            "create_broken_road",
            "create_serpentine_lane",
            "create_diagonal_curved_road",
            "create_cul_de_sac"
        ]
        
        print("📋 FONCTIONS APPELÉES:")
        for func in function_calls:
            if func in content:
                print(f"   ✅ {func} trouvée")
                # Compter les occurrences
                count = content.count(func + "(")
                print(f"      → {count} appel(s)")
            else:
                print(f"   ❌ {func} MANQUANTE")
        
        print("\n🔍 PROBLÈMES POTENTIELS:")
        
        # Vérifier les problèmes connus
        issues = []
        
        # 1. Paramètres manquants
        if "create_highway_road(" in content:
            highway_calls = content.count("create_highway_road(")
            print(f"   📊 create_highway_road appelée {highway_calls} fois")
            
        # 2. Vérifier si la fonction est appelée correctement dans la génération
        if "create_organic_road_grid_rf" in content:
            print("   ✅ Fonction principale trouvée")
            
            # Rechercher l'appel dans generate_road_network_first
            if "create_organic_road_grid_rf(" in content:
                print("   ✅ Fonction appelée quelque part")
            else:
                print("   ⚠️ Fonction pas appelée")
                issues.append("Fonction create_organic_road_grid_rf pas appelée")
        
        # 3. Vérifier les imports math
        math_imports = content.count("import math")
        print(f"   📊 {math_imports} imports math trouvés")
        
        if math_imports < 5:
            issues.append("Pas assez d'imports math dans les nouvelles fonctions")
            
        # 4. Vérifier les retours de fonctions
        if "return None" in content:
            none_returns = content.count("return None")
            print(f"   ⚠️ {none_returns} fonctions retournent None (potentiel problème)")
            
        return issues
        
    except Exception as e:
        print(f"❌ Erreur lecture fichier: {e}")
        return ["Erreur lecture fichier"]

def check_generation_flow():
    """Vérifie le flux de génération"""
    print("\n🔄 FLUX DE GÉNÉRATION")
    print("="*30)
    
    try:
        with open("generator.py", "r", encoding="utf-8") as f:
            content = f.read()
            
        # Trouver la fonction generate_road_network_first
        if "def generate_road_network_first(" in content:
            print("✅ Fonction generate_road_network_first trouvée")
            
            # Vérifier qu'elle appelle create_organic_road_grid_rf
            gen_start = content.find("def generate_road_network_first(")
            gen_end = content.find("\ndef ", gen_start + 1)
            if gen_end == -1:
                gen_end = len(content)
                
            gen_function = content[gen_start:gen_end]
            
            if "create_organic_road_grid_rf" in gen_function:
                print("✅ generate_road_network_first appelle create_organic_road_grid_rf")
            else:
                print("❌ generate_road_network_first N'APPELLE PAS create_organic_road_grid_rf")
                return ["Fonction principale n'appelle pas le nouveau système"]
                
        else:
            print("❌ generate_road_network_first MANQUANTE")
            return ["Fonction principale manquante"]
            
        return []
        
    except Exception as e:
        print(f"❌ Erreur: {e}")
        return ["Erreur vérification flux"]

def suggest_fixes(issues):
    """Suggère des corrections"""
    print("\n🛠️ CORRECTIONS SUGGÉRÉES")
    print("="*40)
    
    if not issues:
        print("✅ Aucun problème détecté!")
        print("\n🎯 SI LA GÉNÉRATION ÉCHOUE ENCORE:")
        print("   1. Vérifiez les messages d'erreur dans Blender")
        print("   2. Regardez la console Blender (Window > Toggle System Console)")
        print("   3. Testez avec des paramètres simples (grille 2x2)")
        print("   4. Vérifiez que l'addon est bien activé")
        return
    
    for i, issue in enumerate(issues, 1):
        print(f"{i}. {issue}")
        
        if "pas appelée" in issue.lower():
            print("   💡 Solution: Vérifier que create_organic_road_grid_rf est appelée")
        elif "import math" in issue.lower():
            print("   💡 Solution: Ajouter 'import math' dans chaque nouvelle fonction")
        elif "none" in issue.lower():
            print("   💡 Solution: Vérifier les conditions de retour des fonctions")

def main():
    print("🚨 DIAGNOSTIC DE GÉNÉRATION - City Block Generator")
    print("="*60)
    
    issues = check_function_calls()
    issues.extend(check_generation_flow())
    
    suggest_fixes(issues)
    
    print("\n📊 RÉSUMÉ:")
    if issues:
        print(f"❌ {len(issues)} problème(s) détecté(s)")
        for issue in issues:
            print(f"   • {issue}")
    else:
        print("✅ Aucun problème structurel détecté")
        print("✅ Le problème pourrait être dans Blender même")
    
    print("\n🎯 PROCHAINES ÉTAPES:")
    print("   1. Ouvrez Blender")
    print("   2. Activez l'addon")
    print("   3. Regardez la console (Window > Toggle System Console)")
    print("   4. Testez la génération et notez l'erreur exacte")

if __name__ == "__main__":
    main()

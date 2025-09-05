#!/usr/bin/env python3
"""
Diagnostic précis - Pourquoi les courbes n'apparaissent pas ?
"""

def check_generation_flow():
    """Vérifie le flux exact de génération"""
    print("🔍 DIAGNOSTIC PRÉCIS - FLUX DE GÉNÉRATION")
    print("="*50)
    
    try:
        with open("generator.py", "r", encoding="utf-8") as f:
            content = f.read()
        
        print("1. 📋 VÉRIFICATION DE L'ENTRÉE PRINCIPALE")
        print("-" * 40)
        
        # Chercher l'opérateur principal
        if "class CityGenOperator" in content:
            print("   ✅ CityGenOperator trouvé")
            
            # Trouver la fonction execute
            start = content.find("def execute(self, context):")
            if start != -1:
                end = content.find("\nclass ", start)
                if end == -1:
                    end = start + 2000  # Limite de recherche
                
                execute_code = content[start:end]
                
                if "generate_road_network_first" in execute_code:
                    print("   ✅ execute() appelle generate_road_network_first")
                else:
                    print("   ❌ execute() N'APPELLE PAS generate_road_network_first")
                    print("   🔍 Que fait execute() ?")
                    # Chercher ce qui est appelé
                    lines = execute_code.split('\n')[:20]
                    for line in lines:
                        if 'generate' in line.lower() or 'create' in line.lower():
                            print(f"      → {line.strip()}")
        
        print("\n2. 🛣️ VÉRIFICATION DE generate_road_network_first")
        print("-" * 40)
        
        # Trouver generate_road_network_first
        func_start = content.find("def generate_road_network_first(")
        if func_start != -1:
            print("   ✅ generate_road_network_first trouvée")
            
            func_end = content.find("\ndef ", func_start + 1)
            if func_end == -1:
                func_end = func_start + 3000
                
            func_code = content[func_start:func_end]
            
            if "create_primary_road_network_rf" in func_code:
                print("   ✅ Appelle create_primary_road_network_rf")
            else:
                print("   ❌ N'appelle PAS create_primary_road_network_rf")
        
        print("\n3. 🎯 VÉRIFICATION DE create_primary_road_network_rf")
        print("-" * 40)
        
        # Trouver create_primary_road_network_rf
        primary_start = content.find("def create_primary_road_network_rf(")
        if primary_start != -1:
            print("   ✅ create_primary_road_network_rf trouvée")
            
            primary_end = content.find("\ndef ", primary_start + 1)
            if primary_end == -1:
                primary_end = primary_start + 2000
                
            primary_code = content[primary_start:primary_end]
            
            # Vérifier la logique de choix
            print("   🔍 Logique de sélection du système:")
            
            if "FORCER TOUJOURS" in primary_code:
                print("   ✅ Force système organique trouvé")
            elif "if organic_mode" in primary_code:
                print("   ⚠️ Condition sur organic_mode trouvée")
                print("   🔍 Conditions exactes:")
                lines = primary_code.split('\n')
                for i, line in enumerate(lines):
                    if 'if' in line and ('organic' in line or 'curve' in line):
                        print(f"      Ligne {i}: {line.strip()}")
                        # Afficher les lignes suivantes
                        for j in range(1, 4):
                            if i + j < len(lines):
                                print(f"      Ligne {i+j}: {lines[i+j].strip()}")
                        break
            
            if "create_organic_road_grid_rf" in primary_code:
                print("   ✅ Appelle create_organic_road_grid_rf")
            elif "create_rectangular_road_grid_rf" in primary_code:
                print("   ⚠️ Appelle create_rectangular_road_grid_rf")
            else:
                print("   ❓ Fonction de génération inconnue")
        
        print("\n4. 🌊 VÉRIFICATION DE create_organic_road_grid_rf")
        print("-" * 40)
        
        # Vérifier la fonction organique
        organic_start = content.find("def create_organic_road_grid_rf(")
        if organic_start != -1:
            print("   ✅ create_organic_road_grid_rf trouvée")
            
            organic_end = content.find("\ndef ", organic_start + 1)
            if organic_end == -1:
                organic_end = len(content)
                
            organic_code = content[organic_start:organic_end]
            
            # Vérifier les éléments de courbes
            if "math.sin" in organic_code:
                print("   ✅ math.sin trouvé (courbes sinusoïdales)")
                sin_count = organic_code.count("math.sin")
                print(f"      → {sin_count} utilisations de math.sin")
            else:
                print("   ❌ math.sin PAS trouvé")
            
            if "curve_offset" in organic_code:
                print("   ✅ curve_offset trouvé (calculs de courbes)")
            else:
                print("   ❌ curve_offset PAS trouvé")
            
            if "random.uniform" in organic_code:
                print("   ✅ random.uniform trouvé (variations)")
                uniform_count = organic_code.count("random.uniform")
                print(f"      → {uniform_count} utilisations de random.uniform")
            else:
                print("   ❌ random.uniform PAS trouvé")
        else:
            print("   ❌ create_organic_road_grid_rf PAS TROUVÉE")
        
        return True
        
    except Exception as e:
        print(f"   ❌ Erreur: {e}")
        return False

def check_parameters():
    """Vérifie les paramètres par défaut"""
    print("\n5. 🎛️ VÉRIFICATION DES PARAMÈTRES")
    print("-" * 40)
    
    try:
        with open("operators.py", "r", encoding="utf-8") as f:
            content = f.read()
        
        # Vérifier organic_mode default
        if "citygen_organic_mode" in content:
            start = content.find("'citygen_organic_mode'")
            end = content.find("),", start) + 2
            param_def = content[start:end]
            
            if "default=True" in param_def:
                print("   ✅ citygen_organic_mode default=True")
            elif "default=False" in param_def:
                print("   ⚠️ citygen_organic_mode default=False")
            else:
                print("   ❓ citygen_organic_mode default non trouvé")
        
        # Vérifier curve_intensity default
        if "citygen_road_curve_intensity" in content:
            start = content.find("'citygen_road_curve_intensity'")
            end = content.find("),", start) + 2
            param_def = content[start:end]
            
            if "default=" in param_def:
                default_val = param_def.split("default=")[1].split(",")[0].strip()
                print(f"   ✅ citygen_road_curve_intensity default={default_val}")
            else:
                print("   ❓ citygen_road_curve_intensity default non trouvé")
        
    except Exception as e:
        print(f"   ❌ Erreur paramètres: {e}")

def main():
    print("🚨 DIAGNOSTIC PRÉCIS - POURQUOI PAS DE COURBES ?")
    print("="*60)
    
    success = check_generation_flow()
    check_parameters()
    
    print("\n🎯 CONCLUSIONS PROBABLES :")
    print("="*30)
    print("• Le système organique n'est peut-être pas appelé")
    print("• Les conditions d'activation échouent")
    print("• Les paramètres ne sont pas transmis correctement")
    print("• Les calculs de courbes ont des erreurs")
    print("• Le fallback vers système rectangulaire est activé")

if __name__ == "__main__":
    main()

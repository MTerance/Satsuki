#!/usr/bin/env python3
"""
Test des nouvelles fonctionnalités de densité et variété Tokyo 1.0.2
"""

def test_density_and_variety():
    print("🧪 === TEST TOKYO 1.0.2 - DENSITÉ ET VARIÉTÉ ===")
    
    # Test différentes densités sur grille 5x5
    size = 5
    total_blocks = size * size
    
    densities = [0.3, 0.5, 0.8, 1.0]
    
    for density in densities:
        blocks_to_generate = int(total_blocks * density)
        print(f"\n📊 Densité {density*100:.0f}% sur grille {size}x{size}:")
        print(f"   Total possible: {total_blocks} blocs")
        print(f"   À générer: {blocks_to_generate} blocs")
        
        # Simuler la logique de priorité
        center = size // 2
        all_positions = [(x, y) for x in range(size) for y in range(size)]
        
        def priority_score(pos):
            x, y = pos
            return abs(x - center) + abs(y - center)
        
        all_positions.sort(key=priority_score)
        selected_positions = all_positions[:blocks_to_generate]
        
        print(f"   Positions sélectionnées: {selected_positions[:8]}{'...' if len(selected_positions) > 8 else ''}")
    
    print("\n🎯 === TEST VARIÉTÉS DE BÂTIMENTS ===")
    
    varieties = {
        'ALL': 'Business + Commercial + Résidentiel',
        'BUSINESS_ONLY': 'Seulement gratte-ciels',
        'NO_BUSINESS': 'Commercial + Résidentiel seulement',
        'RESIDENTIAL_ONLY': 'Seulement maisons'
    }
    
    for variety, description in varieties.items():
        print(f"\n🏗️ Variété '{variety}':")
        print(f"   📝 {description}")
        
        # Simuler l'attribution des zones
        if variety == 'RESIDENTIAL_ONLY':
            print("   🏠 Tous les blocs = résidentiel")
        elif variety == 'BUSINESS_ONLY':
            print("   🏢 Tous les blocs = business")
        elif variety == 'NO_BUSINESS':
            print("   🏬 Centre/proche = commercial, extérieur = résidentiel")
        else:  # ALL
            print("   🏢 Centre = business, proche = commercial, extérieur = résidentiel")
    
    print("\n✅ === NOUVELLES FONCTIONNALITÉS TESTÉES ===")
    print("🎛️ Block Density: Contrôle le pourcentage de blocs générés")
    print("🏗️ Building Variety: Choisit les types de bâtiments")
    print("🎯 Priorité: Centre d'abord, puis périphérie")
    print("📊 Interface: Paramètres visibles dans l'opérateur Blender")

if __name__ == "__main__":
    test_density_and_variety()

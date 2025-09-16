"""
Test ultra-simple pour identifier le problème avec PropertyGroup
"""
import bpy

# Version 1: Ultra-simple avec une seule propriété
class TestProperties1(bpy.types.PropertyGroup):
    test_value = bpy.props.IntProperty(default=5)

# Version 2: Avec les mêmes propriétés que notre classe problématique
class TestProperties2(bpy.types.PropertyGroup):
    width = bpy.props.IntProperty(name="Largeur", default=5, min=1, max=50)
    length = bpy.props.IntProperty(name="Longueur", default=5, min=1, max=50)

def test_registration():
    """Test d'enregistrement pour identifier le problème"""
    print("=== TEST ENREGISTREMENT PROPERTYGROUP ===")
    
    # Test 1: Classe ultra-simple
    try:
        bpy.utils.register_class(TestProperties1)
        print("✅ TestProperties1 enregistrée avec succès")
        
        if hasattr(bpy.types, 'TestProperties1'):
            print("✅ TestProperties1 accessible dans bpy.types")
        else:
            print("❌ TestProperties1 NON accessible dans bpy.types")
            
        bpy.utils.unregister_class(TestProperties1)
        print("✅ TestProperties1 désenregistrée")
        
    except Exception as e:
        print(f"❌ ERREUR TestProperties1: {e}")
    
    # Test 2: Classe avec propriétés nommées
    try:
        bpy.utils.register_class(TestProperties2)
        print("✅ TestProperties2 enregistrée avec succès")
        
        if hasattr(bpy.types, 'TestProperties2'):
            print("✅ TestProperties2 accessible dans bpy.types")
        else:
            print("❌ TestProperties2 NON accessible dans bpy.types")
            
        bpy.utils.unregister_class(TestProperties2)
        print("✅ TestProperties2 désenregistrée")
        
    except Exception as e:
        print(f"❌ ERREUR TestProperties2: {e}")
    
    print("=== FIN TEST PROPERTYGROUP ===")

if __name__ == "__main__":
    test_registration()

# Version minimale de CityGenProperties pour diagnostic
import bpy

class CityGenPropertiesMinimal(bpy.types.PropertyGroup):
    """Version minimale de CityGenProperties pour diagnostic"""
    
    # Seulement les propriétés essentielles
    width: bpy.props.IntProperty(
        name="Largeur", 
        description="Largeur de la grille de ville",
        default=5, 
        min=1, 
        max=50
    )
    
    length: bpy.props.IntProperty(
        name="Longueur", 
        description="Longueur de la grille de ville",
        default=5, 
        min=1, 
        max=50
    )
    
    max_floors: bpy.props.IntProperty(
        name="Étages max", 
        description="Nombre maximum d'étages",
        default=8, 
        min=1, 
        max=100
    )

def register_minimal():
    """Test d'enregistrement minimal"""
    try:
        print("=== TEST ENREGISTREMENT MINIMAL ===")
        bpy.utils.register_class(CityGenPropertiesMinimal)
        print("✅ CityGenPropertiesMinimal enregistrée")
        
        if hasattr(bpy.types, 'CityGenPropertiesMinimal'):
            print("✅ Accessible dans bpy.types")
            
            # Test de création du lien
            bpy.types.Scene.test_props = bpy.props.PointerProperty(type=CityGenPropertiesMinimal)
            print("✅ Lien créé avec succès")
            
            return True
        else:
            print("❌ Non accessible dans bpy.types")
            return False
            
    except Exception as e:
        print(f"❌ Erreur: {e}")
        return False

def unregister_minimal():
    """Désenregistrement du test"""
    try:
        if hasattr(bpy.types.Scene, 'test_props'):
            del bpy.types.Scene.test_props
        bpy.utils.unregister_class(CityGenPropertiesMinimal)
        print("Test minimal désenregistré")
    except:
        pass

if __name__ == "__main__":
    register_minimal()


import bpy
from bpy.props import IntProperty, EnumProperty, FloatProperty, BoolProperty, PointerProperty

class JPBG_Props(bpy.types.PropertyGroup):
    seed: IntProperty(name="Seed", default=1234, min=0)
    building_type: EnumProperty(
        name="Type",
        description="Type d'immeuble à générer",
        items=[
            ("OFFICE", "Bureau", ""),
            ("MALL", "Centre commercial", ""),
            ("RESTAURANT", "Restaurant", ""),
            ("KONBINI", "Konbini", ""),
            ("APARTMENT", "Immeuble d'habitation", ""),
            ("HOUSE", "Maison individuelle", "")
        ],
        default="OFFICE"
    )
    floors: IntProperty(name="Étages", default=8, min=1, max=60)
    floor_height: FloatProperty(name="Hauteur d'étage", default=3.0, min=2.5, max=6.0, subtype='DISTANCE')
    footprint_x: FloatProperty(name="Largeur (X)", default=12.0, min=4.0, max=80.0, subtype='DISTANCE')
    footprint_y: FloatProperty(name="Profondeur (Y)", default=8.0, min=4.0, max=80.0, subtype='DISTANCE')

    # Parcelle
    front_sidewalk: FloatProperty(name="Trottoir avant", default=3.0, min=1.0, max=6.0, subtype='DISTANCE')
    other_margin: FloatProperty(name="Marges autres côtés", default=0.8, min=0.2, max=1.0, subtype='DISTANCE')

    # Textures
    texture_category: EnumProperty(
        name="Catégorie de textures",
        description="Choisir la catégorie d'images à utiliser",
        items=[
            ("AUTO", "Auto (selon type)", ""),
            ("OFFICE", "Office", ""),
            ("MALL", "Mall", ""),
            ("RESTAURANT", "Restaurant", ""),
            ("KONBINI", "Konbini", ""),
            ("APARTMENT", "Apartment", ""),
            ("HOUSE", "House", ""),
        ],
        default="AUTO"
    )

    add_rooftop_units: BoolProperty(name="Équipements toiture", default=True)
    add_signage: BoolProperty(name="Enseigne / Bandeaux", default=True)

def register():
    bpy.utils.register_class(JPBG_Props)
    bpy.types.Scene.jpbg = PointerProperty(type=JPBG_Props)

def unregister():
    del bpy.types.Scene.jpbg
    bpy.utils.unregister_class(JPBG_Props)

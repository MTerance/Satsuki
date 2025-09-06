    
    def create_district_blocks(self, size, zones, roads):
        """Crée les blocs du district"""
        blocks = []
        block_size = 20.0
        
        for x in range(size):
            for y in range(size):
                # Position du bloc
                block_x = (x - size/2 + 0.5) * block_size
                block_y = (y - size/2 + 0.5) * block_size
                
                # Zone du bloc
                zone_type = zones.get((x, y), 'residential')
                
                # Créer le bloc
                block_obj = self.create_block(block_x, block_y, block_size * 0.8, zone_type, f"TokyoBlock_{x}_{y}")
                if block_obj:
                    blocks.append({'object': block_obj, 'zone': zone_type, 'pos': (x, y)})
        
        print(f"🏘️ {len(blocks)} blocs créés")
        return blocks
    
    def create_block(self, x, y, size, zone_type, name):
        """Crée un bloc de terrain"""
        try:
            # Créer mesh bloc
            mesh = bpy.data.meshes.new(name)
            obj = bpy.data.objects.new(name, mesh)
            bpy.context.collection.objects.link(obj)
            
            bm = bmesh.new()
            
            # Créer un carré simple
            half_size = size / 2
            v1 = bm.verts.new((x - half_size, y - half_size, 0))
            v2 = bm.verts.new((x + half_size, y - half_size, 0))
            v3 = bm.verts.new((x + half_size, y + half_size, 0))
            v4 = bm.verts.new((x - half_size, y + half_size, 0))
            
            bm.faces.new([v1, v2, v3, v4])
            
            bm.to_mesh(mesh)
            bm.free()
            
            # Matériau selon la zone
            mat = self.create_zone_material(zone_type)
            obj.data.materials.append(mat)
            
            return obj
            
        except Exception as e:
            print(f"❌ Erreur création bloc {name}: {e}")
            return None
    
    def create_tokyo_buildings(self, blocks, zones):
        """Crée les bâtiments Tokyo selon les zones"""
        buildings = []
        
        for block in blocks:
            zone_type = block['zone']
            pos = block['pos']
            block_obj = block['object']
            
            # Obtenir position du bloc
            block_loc = block_obj.location
            
            if zone_type == 'business':
                # GRATTE-CIELS (15-40 étages)
                building_height = random.uniform(60, 160)  # 15-40 étages * 4m
                building = self.create_skyscraper(block_loc.x, block_loc.y, building_height, f"TokyoSkyscraper_{pos[0]}_{pos[1]}")
                
            elif zone_type == 'commercial':
                # CENTRES COMMERCIAUX (3-8 étages)
                building_height = random.uniform(12, 32)  # 3-8 étages * 4m
                building = self.create_commercial_center(block_loc.x, block_loc.y, building_height, f"TokyoCommercial_{pos[0]}_{pos[1]}")
                
            else:  # residential
                # MAISONS/IMMEUBLES (1-5 étages)
                building_height = random.uniform(4, 20)  # 1-5 étages * 4m
                building = self.create_residential_building(block_loc.x, block_loc.y, building_height, f"TokyoResidential_{pos[0]}_{pos[1]}")
            
            if building:
                buildings.append(building)
        
        print(f"🏢 {len(buildings)} bâtiments Tokyo créés")
        return buildings
    
    def create_skyscraper(self, x, y, height, name):
        """Crée un gratte-ciel style Tokyo"""
        try:
            # Ajouter un cube et l'extruder
            bpy.ops.mesh.primitive_cube_add(location=(x, y, height/2))
            building = bpy.context.object
            building.name = name
            
            # Redimensionner pour faire un gratte-ciel
            building.scale = (
                random.uniform(6, 10),    # Largeur
                random.uniform(6, 10),    # Profondeur  
                height / 2               # Hauteur
            )
            
            # Matériau gratte-ciel (vitré)
            mat = self.create_skyscraper_material()
            building.data.materials.append(mat)
            
            print(f"🏢 Gratte-ciel créé: {height:.1f}m")
            return building
            
        except Exception as e:
            print(f"❌ Erreur gratte-ciel {name}: {e}")
            return None
    
    def create_commercial_center(self, x, y, height, name):
        """Crée un centre commercial"""
        try:
            bpy.ops.mesh.primitive_cube_add(location=(x, y, height/2))
            building = bpy.context.object
            building.name = name
            
            # Plus large que haut (centre commercial)
            building.scale = (
                random.uniform(8, 12),    # Large
                random.uniform(6, 10),    # Profond
                height / 2               # Modérément haut
            )
            
            # Matériau commercial (coloré)
            mat = self.create_commercial_material()
            building.data.materials.append(mat)
            
            print(f"🏬 Centre commercial créé: {height:.1f}m")
            return building
            
        except Exception as e:
            print(f"❌ Erreur centre commercial {name}: {e}")
            return None
    
    def create_residential_building(self, x, y, height, name):
        """Crée un bâtiment résidentiel"""
        try:
            bpy.ops.mesh.primitive_cube_add(location=(x, y, height/2))
            building = bpy.context.object
            building.name = name
            
            # Plus petit et carré (résidentiel)
            building.scale = (
                random.uniform(4, 7),     # Modeste largeur
                random.uniform(4, 7),     # Modeste profondeur
                height / 2               # Bas
            )
            
            # Matériau résidentiel
            mat = self.create_residential_material()
            building.data.materials.append(mat)
            
            print(f"🏠 Bâtiment résidentiel créé: {height:.1f}m")
            return building
            
        except Exception as e:
            print(f"❌ Erreur résidentiel {name}: {e}")
            return None
    
    # MATÉRIAUX TOKYO
    def create_road_material(self):
        """Matériau route asphaltée"""
        mat = bpy.data.materials.new(name="TokyoRoad")
        mat.use_nodes = True
        mat.node_tree.nodes.clear()
        
        # Couleur asphalte foncé
        bsdf = mat.node_tree.nodes.new(type="ShaderNodeBsdfPrincipled")
        bsdf.inputs[0].default_value = (0.1, 0.1, 0.1, 1.0)  # Gris très foncé
        bsdf.inputs[7].default_value = 0.8  # Rugosité
        
        output = mat.node_tree.nodes.new(type="ShaderNodeOutputMaterial")
        mat.node_tree.links.new(bsdf.outputs[0], output.inputs[0])
        
        return mat
    
    def create_zone_material(self, zone_type):
        """Matériau terrain selon zone"""
        mat = bpy.data.materials.new(name=f"TokyoZone_{zone_type}")
        mat.use_nodes = True
        mat.node_tree.nodes.clear()
        
        bsdf = mat.node_tree.nodes.new(type="ShaderNodeBsdfPrincipled")
        
        if zone_type == 'business':
            bsdf.inputs[0].default_value = (0.2, 0.2, 0.3, 1.0)  # Bleu foncé business
        elif zone_type == 'commercial':
            bsdf.inputs[0].default_value = (0.3, 0.2, 0.2, 1.0)  # Rouge commercial
        else:  # residential
            bsdf.inputs[0].default_value = (0.2, 0.3, 0.2, 1.0)  # Vert résidentiel
        
        output = mat.node_tree.nodes.new(type="ShaderNodeOutputMaterial")
        mat.node_tree.links.new(bsdf.outputs[0], output.inputs[0])
        
        return mat
    
    def create_skyscraper_material(self):
        """Matériau gratte-ciel vitré"""
        mat = bpy.data.materials.new(name="TokyoSkyscraper")
        mat.use_nodes = True
        mat.node_tree.nodes.clear()
        
        bsdf = mat.node_tree.nodes.new(type="ShaderNodeBsdfPrincipled")
        bsdf.inputs[0].default_value = (0.7, 0.8, 0.9, 1.0)  # Bleu vitré
        bsdf.inputs[4].default_value = 0.9  # Metallic
        bsdf.inputs[7].default_value = 0.1  # Très lisse
        
        output = mat.node_tree.nodes.new(type="ShaderNodeOutputMaterial")
        mat.node_tree.links.new(bsdf.outputs[0], output.inputs[0])
        
        return mat
    
    def create_commercial_material(self):
        """Matériau centre commercial coloré"""
        mat = bpy.data.materials.new(name="TokyoCommercial")
        mat.use_nodes = True
        mat.node_tree.nodes.clear()
        
        bsdf = mat.node_tree.nodes.new(type="ShaderNodeBsdfPrincipled")
        # Couleurs vives commerciales
        colors = [
            (0.9, 0.3, 0.3, 1.0),  # Rouge
            (0.3, 0.9, 0.3, 1.0),  # Vert
            (0.3, 0.3, 0.9, 1.0),  # Bleu
            (0.9, 0.9, 0.3, 1.0),  # Jaune
        ]
        bsdf.inputs[0].default_value = random.choice(colors)
        
        output = mat.node_tree.nodes.new(type="ShaderNodeOutputMaterial")
        mat.node_tree.links.new(bsdf.outputs[0], output.inputs[0])
        
        return mat
    
    def create_residential_material(self):
        """Matériau résidentiel"""
        mat = bpy.data.materials.new(name="TokyoResidential")
        mat.use_nodes = True
        mat.node_tree.nodes.clear()
        
        bsdf = mat.node_tree.nodes.new(type="ShaderNodeBsdfPrincipled")
        bsdf.inputs[0].default_value = (0.8, 0.7, 0.6, 1.0)  # Beige résidentiel
        
        output = mat.node_tree.nodes.new(type="ShaderNodeOutputMaterial")
        mat.node_tree.links.new(bsdf.outputs[0], output.inputs[0])
        
        return mat


# INTERFACE UTILISATEUR SIMPLE
class TOKYO_PT_main_panel(Panel):
    """Panneau principal Tokyo"""
    bl_label = "Tokyo City Generator 1.0"
    bl_idname = "TOKYO_PT_main_panel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Tokyo'
    
    def draw(self, context):
        layout = self.layout
        
        # Titre
        layout.label(text="🗾 Tokyo District Generator", icon='WORLD')
        layout.separator()
        
        # Bouton principal
        layout.operator("tokyo.generate_district", text="Generate Tokyo District", icon='MESH_CUBE')
        
        layout.separator()
        layout.label(text="🏢 Features:")
        layout.label(text="• Business: Skyscrapers 15-40 floors")
        layout.label(text="• Commercial: Centers 3-8 floors") 
        layout.label(text="• Residential: Houses 1-5 floors")
        layout.label(text="• Organic curved streets")


# ENREGISTREMENT BLENDER
classes = [
    TOKYO_OT_generate_district,
    TOKYO_PT_main_panel,
]

def register():
    for cls in classes:
        bpy.utils.register_class(cls)
    print("🗾 Tokyo City Generator 1.0 registered!")

def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)
    print("🗾 Tokyo City Generator 1.0 unregistered!")

if __name__ == "__main__":
    register()

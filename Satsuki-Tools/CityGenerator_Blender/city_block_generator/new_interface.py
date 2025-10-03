    def draw(self, context):
        layout = self.layout
        
        # Titre avec icône
        row = layout.row()
        row.label(text="🗾 Tokyo District Generator", icon='WORLD')
        layout.separator()
        
        # Boîte pour les paramètres
        box = layout.box()
        box.label(text="⚙️ Configuration", icon='PREFERENCES')
        
        # District Size
        row = box.row()
        row.label(text="District Size:")
        row.prop(context.scene, "tokyo_size", text="")
        
        # Block Density  
        row = box.row()
        row.label(text="Block Density:")
        row.prop(context.scene, "tokyo_density", text="", slider=True)
        
        # Building Variety
        row = box.row()
        row.label(text="Building Variety:")
        row.prop(context.scene, "tokyo_variety", text="")
        
        # Organic Factor
        row = box.row()
        row.label(text="Organic Streets:")
        row.prop(context.scene, "tokyo_organic", text="", slider=True)
        
        layout.separator()
        
        # Bouton de génération
        layout.operator("tokyo.generate_district", text="🚀 Generate Tokyo District", icon='MESH_CUBE')
        
        layout.separator()
        
        # Informations
        box2 = layout.box()
        box2.label(text="📊 Building Types", icon='INFO')
        box2.label(text="• Business: Skyscrapers 15-40 floors")
        box2.label(text="• Commercial: Centers 3-8 floors") 
        box2.label(text="• Residential: Houses 1-5 floors")

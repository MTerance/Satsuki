
import os, bpy, random
from mathutils import Euler
PREFIX = "JPB_"
GROUND_LEVEL = 0.0  # Sol = plan à Z=0, bâtiments posés directement dessus

# ---------- Textures ----------
_IMG_CACHE = {}
def _addon_dir():
    return os.path.dirname(__file__)

def _load_image(category, name):
    global _IMG_CACHE
    key = (category, name)
    if key in _IMG_CACHE:
        return _IMG_CACHE[key]
    texdir = os.path.join(_addon_dir(), "textures", category.lower())
    if not os.path.isdir(texdir):
        _IMG_CACHE[key] = None
        return None
    for ext in (".png", ".jpg", ".jpeg"):
        path = os.path.join(texdir, name + ext)
        if os.path.exists(path):
            try:
                img = bpy.data.images.load(path, check_existing=True)
            except:
                img = None
            _IMG_CACHE[key] = img
            return img
    _IMG_CACHE[key] = None
    return None

def _mat_from_image(name, img, fallback_rgba=(0.8,0.8,0.8,1.0), emission=False, strength=3.0):
    m = bpy.data.materials.new(name=name)
    m.use_nodes = True
    nt = m.node_tree
    nodes, links = nt.nodes, nt.links
    for n in list(nodes): nodes.remove(n)
    out = nodes.new("ShaderNodeOutputMaterial"); out.location = (400, 0)
    if img:
        tex = nodes.new("ShaderNodeTexImage"); tex.location = (-400, 0); tex.image = img; tex.projection = 'BOX'; tex.projection_blend = 0.2
        texcoord = nodes.new("ShaderNodeTexCoord"); texcoord.location = (-600, 0)
        mapn = nodes.new("ShaderNodeMapping"); mapn.location = (-500, -120)
        mapn.inputs["Scale"].default_value = (0.2,0.2,0.2)
        links.new(texcoord.outputs["Object"], mapn.inputs["Vector"])
        links.new(mapn.outputs["Vector"], tex.inputs["Vector"])
        if emission:
            e = nodes.new("ShaderNodeEmission"); e.location = (100, 0); e.inputs["Strength"].default_value = strength
            links.new(tex.outputs["Color"], e.inputs["Color"])
            links.new(e.outputs["Emission"], out.inputs["Surface"])
        else:
            bsdf = nodes.new("ShaderNodeBsdfPrincipled"); bsdf.location = (100, 0)
            links.new(tex.outputs["Color"], bsdf.inputs["Base Color"])
            if "Roughness" in bsdf.inputs: bsdf.inputs["Roughness"].default_value = 0.45
            links.new(bsdf.outputs["BSDF"], out.inputs["Surface"])
    else:
        bsdf = nodes.new("ShaderNodeBsdfPrincipled"); bsdf.location = (0, 0)
        if "Base Color" in bsdf.inputs: bsdf.inputs["Base Color"].default_value = fallback_rgba
        if "Roughness" in bsdf.inputs: bsdf.inputs["Roughness"].default_value = 0.45
        if emission:
            e = nodes.new("ShaderNodeEmission"); e.location = (150, 0)
            e.inputs["Color"].default_value = fallback_rgba
            e.inputs["Strength"].default_value = strength
            mix = nodes.new("ShaderNodeAddShader"); mix.location = (300, 0)
            links.new(bsdf.outputs["BSDF"], mix.inputs[0])
            links.new(e.outputs["Emission"], mix.inputs[1])
            links.new(mix.outputs[0], out.inputs["Surface"])
        else:
            links.new(bsdf.outputs["BSDF"], out.inputs["Surface"])
    return m

def _materials_for_category(cat):
    img_conc = _load_image(cat, "concrete")
    img_gls  = _load_image(cat, "glass")
    img_roof = _load_image(cat, "roof")
    img_grnd = _load_image(cat, "ground")
    img_sign = _load_image(cat, "signage")
    mats = {
        "core":   _mat_from_image(PREFIX+"MatCore_"+cat,   img_conc, (0.85,0.85,0.86,1)),
        "glass":  _mat_from_image(PREFIX+"MatGlass_"+cat,  img_gls,  (0.62,0.75,0.90,1)),
        "roof":   _mat_from_image(PREFIX+"MatRoof_"+cat,   img_roof, (0.40,0.40,0.42,1)),
        "ground": _mat_from_image(PREFIX+"MatGround_"+cat, img_grnd, (0.20,0.20,0.22,1)),
        "sign":   _mat_from_image(PREFIX+"MatSign_"+cat,   img_sign, (1.0,0.35,0.2,1), emission=True, strength=4.0),
    }
    return mats

def _get_category(props):
    return (props.texture_category.lower() if props.texture_category != "AUTO" else props.building_type.lower())

# ---------- Utilities ----------
def _clean_previous():
    for obj in list(bpy.data.objects):
        if obj.name.startswith(PREFIX):
            bpy.data.objects.remove(obj, do_unlink=True)

def _add_cube(name, size=(2,2,2), loc=(0,0,0), mat=None):
    # Créer un cube à l'origine
    bpy.ops.mesh.primitive_cube_add(size=2.0, location=(0,0,0))
    o = bpy.context.active_object
    o.name = name
    
    # Appliquer la taille
    o.scale = (size[0]/2.0, size[1]/2.0, size[2]/2.0)
    
    # Appliquer les transformations pour fixer l'échelle
    bpy.context.view_layer.objects.active = o
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    
    # Maintenant le cube fait exactement la taille demandée
    # Déplacer l'origine vers le bottom-center
    bpy.ops.object.mode_set(mode='EDIT')
    bpy.ops.mesh.select_all(action='SELECT')
    # Déplacer tous les vertices de la moitié de la hauteur vers le haut
    bpy.ops.transform.translate(value=(0, 0, size[2]/2.0))
    bpy.ops.object.mode_set(mode='OBJECT')
    
    # Maintenant positionner l'objet à la location désirée
    # La base du cube est maintenant à l'origine locale
    o.location = loc
    
    # Appliquer le matériau
    if mat:
        if len(o.data.materials): 
            o.data.materials[0] = mat
        else: 
            o.data.materials.append(mat)
    
    return o

def _add_plane(name, size=(2,2), loc=(0,0,0), mat=None):
    # Créer un plan à l'origine avec la taille directement
    bpy.ops.mesh.primitive_plane_add(size=2.0, location=loc)
    o = bpy.context.active_object
    o.name = name
    
    # Appliquer la taille correctement (diviser par 2 car le plan par défaut fait 2x2)
    o.scale = (size[0]/2.0, size[1]/2.0, 1.0)
    
    # Appliquer les transformations pour fixer l'échelle
    bpy.context.view_layer.objects.active = o
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    
    # Appliquer le matériau
    if mat:
        if len(o.data.materials): 
            o.data.materials[0] = mat
        else: 
            o.data.materials.append(mat)
    
    return o
    
    return o

# ---------- Parcel (block) ----------
def _make_parcel(root, foot_x, foot_y, front=3.0, others=0.8, M=None):
    # Sol comme plan à Z=0 (référence absolue)
    ground = _add_plane(PREFIX+"Ground", (foot_x + 2*others, foot_y + others + front),
                        (0, (front-others)*0.5, 0), M["ground"] if M else None)
    ground.parent = root
    # Trottoir comme cube fin posé sur le plan
    sw = _add_cube(PREFIX+"Sidewalk_Front", (foot_x + 2*others, front, 0.02),
                   (0, foot_y/2 + front/2, 0), M["ground"] if M else None)
    sw.parent = root

# ---------- Details ----------
def _rooftop_units(top_z, foot_x, foot_y, rng, M):
    for i in range(rng.randint(2,5)):
        x = rng.uniform(-foot_x*0.35, foot_x*0.35)
        y = rng.uniform(-foot_y*0.35, foot_y*0.35)
        z = top_z + 0.5
        _add_cube(PREFIX+f"AC_{i}", (rng.uniform(0.8,1.4), rng.uniform(0.8,1.4), rng.uniform(0.6,1.2)), (x,y,z), M["core"])

def _signage(foot_x, foot_y, btype, M):
    if btype in {"RESTAURANT","KONBINI","MALL"}:
        y = foot_y*0.51 + 0.01
        z = GROUND_LEVEL + (2.1 if btype in {"RESTAURANT","KONBINI"} else 4.0)
        w = foot_x*0.75
        h = 0.6 if btype!="MALL" else 1.0
        _add_cube(PREFIX+"Sign", (w, 0.02, h), (0, foot_y/2 + 0.01, z), M["sign"])

# ---------- Massings ----------
def _build_office(root, rng, foot_x, foot_y, floors, fh, M):
    slab_th = 0.20
    total_h = floors * fh
    podium_h = fh * 2.0
    # Avec origin au bottom center, poser directement sur le sol
    _add_cube(PREFIX+"Office_Podium", (foot_x*1.2, foot_y*1.1, podium_h), (0,0,GROUND_LEVEL), M["core"]).parent = root
    tower_w, tower_d = foot_x*0.9, foot_y*0.9
    tower_h = total_h - podium_h
    # Tour posée sur le podium
    _add_cube(PREFIX+"Office_Tower", (tower_w, tower_d, tower_h), (0,0,GROUND_LEVEL + podium_h), M["glass"]).parent = root
    # Toit posé sur la tour
    _add_cube(PREFIX+"Office_Roof", (tower_w, tower_d, slab_th*1.25), (0,0,GROUND_LEVEL + total_h), M["roof"]).parent = root

def _build_mall(root, rng, foot_x, foot_y, floors, fh, M):
    slab_th = 0.22
    podium_f = max(2, min(floors, 3))
    podium_h = podium_f * fh
    # Podium posé sur le sol
    _add_cube(PREFIX+"Mall_Podium", (foot_x*1.6, foot_y*1.4, podium_h), (0,0,GROUND_LEVEL), M["core"]).parent = root
    # Toit posé sur le podium
    _add_cube(PREFIX+"Mall_Roof", (foot_x*1.6, foot_y*1.4, slab_th*1.2), (0,0,GROUND_LEVEL + podium_h), M["roof"]).parent = root
    for i in range(rng.randint(1,3)):
        bw = rng.uniform(foot_x*0.5, foot_x*0.9)
        bd = rng.uniform(foot_y*0.4, foot_y*0.8)
        bh = rng.uniform(fh*2.0, fh*4.0)
        x  = rng.uniform(-foot_x*0.25, foot_x*0.25)
        y  = rng.uniform(-foot_y*0.25, foot_y*0.25)
        # Modules posés sur le toit du podium (pas dans l'air)
        _add_cube(PREFIX+f"Mall_Box_{i}", (bw, bd, bh), (x,y,GROUND_LEVEL + podium_h + slab_th*1.2), M["core"]).parent = root

def _build_restaurant(root, rng, foot_x, foot_y, floors, fh, M):
    slab_th = 0.20
    floors = max(2, min(floors, 3))
    gfh = fh * 1.3
    total_h = gfh + (floors-1)*fh
    # Corps posé sur le sol
    _add_cube(PREFIX+"Rest_Body", (foot_x, foot_y*0.8, total_h), (0,0,GROUND_LEVEL), M["core"]).parent = root
    # Toit posé sur le corps
    _add_cube(PREFIX+"Rest_Roof", (foot_x, foot_y*0.8, slab_th), (0,0,GROUND_LEVEL + total_h), M["roof"]).parent = root
    # Auvent positionné correctement à hauteur fixe
    awning_y = (foot_y*0.8)/2 + 0.03
    awning_z = GROUND_LEVEL + 2.1
    _add_cube(PREFIX+"Rest_Awning", (foot_x*0.9, 0.06, 0.08), (0, awning_y, awning_z), M["sign"]).parent = root

def _build_konbini(root, rng, foot_x, foot_y, floors, fh, M):
    slab_th = 0.20
    floors  = max(1, min(floors, 2))
    total_h = floors * fh
    w, d = foot_x*1.2, foot_y*0.9
    # Corps posé sur le sol
    _add_cube(PREFIX+"Konb_Body", (w, d, total_h), (0,0,GROUND_LEVEL), M["core"]).parent = root
    # Toit posé sur le corps
    _add_cube(PREFIX+"Konb_Roof", (w, d, slab_th), (0,0,GROUND_LEVEL + total_h), M["roof"]).parent = root
    y = d/2 + 0.01
    # Enseignes à hauteurs fixes
    _add_cube(PREFIX+"Konb_Sign", (w*0.85, 0.02, 0.6), (0, y, GROUND_LEVEL + 2.0), M["sign"]).parent = root
    _add_cube(PREFIX+"Konb_Stripe1", (w*0.88, 0.02, 0.12), (0, y, GROUND_LEVEL + 1.6), M["glass"]).parent = root
    _add_cube(PREFIX+"Konb_Stripe2", (w*0.88, 0.02, 0.12), (0, y, GROUND_LEVEL + 1.4), M["glass"]).parent = root

def _build_apartment(root, rng, foot_x, foot_y, floors, fh, M):
    floors = max(4, floors)
    total_h = floors * fh
    # Corps posé sur le sol
    _add_cube(PREFIX+"Apt_Body", (foot_x, foot_y*0.8, total_h), (0,0,GROUND_LEVEL), M["core"]).parent = root
    count = 3 if foot_x >= 14 else 2
    for f in range(1, floors+1):
        # Balcons positionnés par étage
        z = GROUND_LEVEL + f*fh - fh*0.35
        for i in range(count):
            t = (i - (count-1)/2)
            bx = (t * (foot_x * (0.6 if count==3 else 0.5))) / ((count-1) if count>1 else 1)
            _add_cube(PREFIX+f"Bal_{f}_{i}", (foot_x*0.22, 0.30, 0.12), (bx, (foot_y*0.8)/2 + 0.15, z), M["core"]).parent = root
            _add_cube(PREFIX+f"BalRail_{f}_{i}", (foot_x*0.22, 0.02, 0.7), (bx, (foot_y*0.8)/2 + 0.01, z+0.25), M["glass"]).parent = root
    shaft_h = fh * 1.2
    # Gaine technique posée sur le toit
    _add_cube(PREFIX+"Apt_Shaft", (foot_x*0.2, foot_y*0.3, shaft_h), (foot_x*0.32, 0, GROUND_LEVEL + total_h), M["core"]).parent = root

def _build_house(root, rng, foot_x, foot_y, floors, fh, M):
    floors = max(1, min(floors, 2))
    h = floors * fh * 0.95
    w = max(6.0, min(foot_x, 12.0))
    d = max(6.0, min(foot_y, 10.0))
    # Corps posé sur le sol
    _add_cube(PREFIX+"House_Body", (w, d, h), (0,0,GROUND_LEVEL), M["core"]).parent = root
    roof_th = 0.2; 
    # Position du faîte: base du corps + hauteur du corps + surélévation - demi-épaisseur du toit
    ridge_z = GROUND_LEVEL + h + 0.8 - roof_th/2; slope = 0.6
    # Toits positionnés au faîte (centre des toits en pente)
    left = _add_cube(PREFIX+"House_Roof_L", (w*0.55, d*1.02, roof_th), (-w*0.225, 0, ridge_z), M["roof"]); left.parent = root
    right= _add_cube(PREFIX+"House_Roof_R", (w*0.55, d*1.02, roof_th), ( w*0.225, 0, ridge_z), M["roof"]); right.parent = root
    left.rotation_euler = Euler((0,  slope, 0))
    right.rotation_euler= Euler((0, -slope, 0))
    # Porche posé à hauteur relative au sol
    porch_z = GROUND_LEVEL + 1.6
    _add_cube(PREFIX+"House_Porch", (w*0.5, 0.6, 0.2), (0, d/2 + 0.30, porch_z), M["roof"]).parent = root

# ---------- Dispatcher ----------
def generate_building(context, props):
    rng = random.Random(props.seed)
    _clean_previous()

    floors  = int(props.floors)
    fh      = float(props.floor_height)
    foot_x  = float(props.footprint_x)
    foot_y  = float(props.footprint_y)
    btype   = props.building_type
    cat     = (props.texture_category.lower() if props.texture_category != "AUTO" else props.building_type.lower())
    M       = _materials_for_category(cat)

    root = bpy.data.objects.new(PREFIX+"Building", None)
    context.collection.objects.link(root)

    _make_parcel(root, foot_x, foot_y, front=props.front_sidewalk, others=props.other_margin, M=M)

    if btype == "OFFICE":
        _build_office(root, rng, foot_x, foot_y, floors, fh, M)
    elif btype == "MALL":
        _build_mall(root, rng, foot_x, foot_y, floors, fh, M)
    elif btype == "RESTAURANT":
        _build_restaurant(root, rng, foot_x, foot_y, floors, fh, M)
    elif btype == "KONBINI":
        _build_konbini(root, rng, foot_x, foot_y, floors, fh, M)
    elif btype == "APARTMENT":
        _build_apartment(root, rng, foot_x, foot_y, floors, fh, M)
    elif btype == "HOUSE":
        _build_house(root, rng, foot_x, foot_y, floors, fh, M)
    else:
        _build_office(root, rng, foot_x, foot_y, floors, fh, M)

    if props.add_rooftop_units and btype not in {"HOUSE"}:
        top = 0.0
        for o in bpy.data.objects:
            if o.name.startswith(PREFIX) and o.type == 'MESH':
                # Avec origin au bottom center: top = base + hauteur totale
                top = max(top, o.location.z + o.dimensions.z)
        _rooftop_units(top, foot_x, foot_y, rng, M)

    if props.add_signage:
        _signage(foot_x, foot_y, btype, M)

    for o in context.selected_objects: o.select_set(False)
    root.select_set(True)
    context.view_layer.objects.active = root

def register(): pass
def unregister(): pass

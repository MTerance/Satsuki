bl_info = {
    "name": "CityGen — Non-Rect City v1.7.5",
    "author": "ChatGPT",
    "version": (1, 7, 5),
    "blender": (3, 6, 0),
    "location": "View3D > N > CityGen",
    "description": "Ville procédurale: lots non uniformes, fusions aléatoires, diagonales qui découpent les routes HV, textures aléatoires, nettoyage, export GLB.",
    "category": "Add Mesh",
}

import bpy, bmesh, random, math, os, glob
from mathutils import Vector

# ======================
#   Matériaux utilitaires
# ======================
def ensure_principled(name, base_color=(0.8,0.8,0.8,1), **kw):
    mat = bpy.data.materials.get(name) or bpy.data.materials.new(name)
    mat.use_nodes = True
    nt = mat.node_tree
    for n in list(nt.nodes): nt.nodes.remove(n)
    out = nt.nodes.new("ShaderNodeOutputMaterial"); out.location = (400, 0)
    use_emis = bool(kw.get("emission_strength"))
    want_trans = kw.get("transmission") is not None

    main_shader = nt.nodes.new("ShaderNodeBsdfPrincipled"); main_shader.location = (0, 0)
    if "Base Color" in main_shader.inputs: main_shader.inputs["Base Color"].default_value = base_color
    if "Roughness" in main_shader.inputs:   main_shader.inputs["Roughness"].default_value = kw.get("roughness", 0.6)

    if want_trans:
        try:
            main_shader.inputs["Transmission"].default_value = kw["transmission"]
            main_shader.inputs["Roughness"].default_value = 0.02
            main_shader.inputs["IOR"].default_value = 1.45
        except KeyError:
            nt.nodes.remove(main_shader)
            main_shader = nt.nodes.new("ShaderNodeBsdfGlass"); main_shader.location = (0, 0)
            if "Color" in main_shader.inputs:     main_shader.inputs["Color"].default_value = base_color
            if "Roughness" in main_shader.inputs: main_shader.inputs["Roughness"].default_value = 0.02
            if "IOR" in main_shader.inputs:       main_shader.inputs["IOR"].default_value = 1.45

    if use_emis:
        emis = nt.nodes.new("ShaderNodeEmission"); emis.location = (0, -200)
        emis.inputs["Color"].default_value = kw.get("emission_color",(1,1,1,1))
        emis.inputs["Strength"].default_value = kw["emission_strength"]
        add = nt.nodes.new("ShaderNodeAddShader"); add.location = (200, -60)
        nt.links.new(main_shader.outputs[0], add.inputs[0])
        nt.links.new(emis.outputs["Emission"], add.inputs[1])
        nt.links.new(add.outputs["Shader"], out.inputs["Surface"])
    else:
        nt.links.new(main_shader.outputs[0], out.inputs["Surface"])
    return mat

# Placeholders matériaux
MAT_GROUND = MAT_ROAD = MAT_SIDE = MAT_GLASS = MAT_LIT = MAT_ROOF = MAT_METAL = MAT_GRASS = None
MAT_PEDESTRIAN = MAT_ALLEY = None

def init_materials_if_needed():
    global MAT_GROUND, MAT_ROAD, MAT_SIDE, MAT_GLASS, MAT_LIT, MAT_ROOF, MAT_METAL, MAT_GRASS
    global MAT_PEDESTRIAN, MAT_ALLEY
    if MAT_GROUND is not None: return
    MAT_GROUND = ensure_principled("CG_Mat_Ground", (0.12,0.12,0.12,1))
    MAT_ROAD   = ensure_principled("CG_Mat_Road",   (0.10,0.10,0.11,1))
    MAT_SIDE   = ensure_principled("CG_Mat_Side",   (0.68,0.68,0.69,1))
    MAT_GLASS  = ensure_principled("CG_Mat_Glass",  (0.6,0.8,1.0,1), transmission=1.0)
    MAT_LIT    = ensure_principled("CG_Mat_WindowLit", (1,1,0.85,1), emission_strength=3.2)
    MAT_ROOF   = ensure_principled("CG_Mat_Roof",   (0.08,0.08,0.08,1), roughness=0.85)
    MAT_METAL  = ensure_principled("CG_Mat_Metal",  (0.55,0.56,0.6,1), roughness=0.35)
    MAT_GRASS  = ensure_principled("CG_Mat_Grass",  (0.22,0.48,0.26,1), roughness=0.7)
    MAT_PEDESTRIAN = ensure_principled("CG_Mat_Pedestrian", (0.75,0.75,0.78,1), roughness=0.9)
    MAT_ALLEY      = ensure_principled("CG_Mat_Alley",      (0.16,0.16,0.18,1), roughness=0.8)

PALETTE = [(0.78,0.34,0.18,1),(0.28,0.37,0.48,1),(0.55,0.55,0.55,1),(0.36,0.46,0.28,1),(0.73,0.66,0.50,1)]
def facade_mat_random_color():
    col = random.choice(PALETTE)
    return ensure_principled(f"CG_Fac_{hash(col)}", col)

# ======================
#   Utils scène & mesh
# ======================
def safe_clear_scene():
    scene = bpy.context.scene
    for obj in list(scene.objects):
        try: obj.parent = None
        except: pass
    for obj in list(scene.objects):
        try:
            for col in list(obj.users_collection):
                try: col.objects.unlink(obj)
                except: pass
            bpy.data.objects.remove(obj, do_unlink=True)
        except: pass

def join_objects(objs, name):
    mesh_objs = [o for o in objs if getattr(o, "type", None) == 'MESH']
    if not mesh_objs:
        empty = bpy.data.objects.new(name, None)
        bpy.context.collection.objects.link(empty)
        for o in objs:
            try: o.parent = empty
            except: pass
        return empty

    deps = bpy.context.evaluated_depsgraph_get()
    all_vertices, faces = [], []
    poly_material_indices, smooth_flags = [], []
    materials_master = []
    vert_offset = 0

    def mat_index_in_master(mat):
        if mat is None: return -1
        for idx, m in enumerate(materials_master):
            if m and m.name == mat.name: return idx
        materials_master.append(mat); return len(materials_master) - 1

    for obj in mesh_objs:
        obj_eval = obj.evaluated_get(deps)
        me = bpy.data.meshes.new_from_object(obj_eval, preserve_all_data_layers=False, depsgraph=deps)
        mw = obj.matrix_world
        for v in me.vertices:
            co = mw @ v.co; all_vertices.append((co.x, co.y, co.z))
        for poly in me.polygons:
            faces.append([vi + vert_offset for vi in poly.vertices])
            src_idx = poly.material_index
            src_mat = obj.material_slots[src_idx].material if (0 <= src_idx < len(obj.material_slots)) else None
            poly_material_indices.append(mat_index_in_master(src_mat))
            smooth_flags.append(poly.use_smooth)
        vert_offset += len(me.vertices)
        bpy.data.meshes.remove(me)

    merged = bpy.data.meshes.new(name + "_Mesh")
    merged.from_pydata(all_vertices, [], faces); merged.update()
    obj_out = bpy.data.objects.new(name, merged); bpy.context.collection.objects.link(obj_out)
    for mat in materials_master: obj_out.data.materials.append(mat)
    for pidx, (mi, sm) in enumerate(zip(poly_material_indices, smooth_flags)):
        try:
            if mi >= 0: merged.polygons[pidx].material_index = mi
            merged.polygons[pidx].use_smooth = sm
        except: pass
    return obj_out

# ======================
#   Outils géométrie & formes
# ======================
def polygon_area(verts):
    a = 0.0
    for i in range(len(verts)):
        x1,y1 = verts[i]; x2,y2 = verts[(i+1)%len(verts)]
        a += x1*y2 - x2*y1
    return 0.5*a

def ensure_ccw(verts): return verts if polygon_area(verts) > 0 else list(reversed(verts))

def make_polygon_mesh(name, verts2d_ccw, z0=0.0, z1=1.0, mat=None):
    mesh = bpy.data.meshes.new(name)
    bm = bmesh.new()
    vtx_base = [bm.verts.new((x, y, z0)) for (x,y) in verts2d_ccw]
    bm.faces.new(vtx_base)
    geom = bmesh.ops.extrude_face_region(bm, geom=list(bm.faces))
    vs = [e for e in geom['geom'] if isinstance(e, bmesh.types.BMVert)]
    bmesh.ops.translate(bm, verts=vs, vec=Vector((0,0,(z1-z0))))
    bm.normal_update(); bm.to_mesh(mesh); bm.free()
    obj = bpy.data.objects.new(name, mesh); bpy.context.collection.objects.link(obj)
    if mat: obj.data.materials.append(mat)
    return obj

def rect_shape(w, d):
    hw, hd = w/2, d/2
    return [(-hw,-hd),( hw,-hd),( hw, hd),(-hw, hd)]

def L_shape(w, d, cut=(0.45,0.5)):
    w = max(4,w); d = max(4,d)
    hw, hd = w/2, d/2
    cwx, cwd = w*cut[0], d*cut[1]
    verts = [(-hw,-hd),( hw,-hd),( hw, hd-cwd),(-hw+cwx, hd-cwd),(-hw+cwx, hd),(-hw, hd)]
    return ensure_ccw(verts)

def U_shape(w, d, notch_w=0.5, notch_d=0.45):
    hw, hd = w/2, d/2
    nw = w*notch_w/2; nd = d*notch_d
    verts = [(-hw,-hd),( hw,-hd),( hw, hd),( nw, hd),( nw, hd-nd),(-nw, hd-nd),(-nw, hd),(-hw, hd)]
    return ensure_ccw(verts)

def T_shape(w, d, stem_w=0.35, bar_d=0.35):
    hw, hd = w/2, d/2
    sw = w*stem_w/2; bd = d*bar_d
    verts = [(-hw,-hd),( hw,-hd),( hw,-hd+bd),( sw,-hd+bd),( sw, hd),(-sw, hd),(-sw,-hd+bd),(-hw,-hd+bd)]
    return ensure_ccw(verts)

def trapezoid_shape(w, d, top_ratio=0.6):
    hw, hd = w/2, d/2; tr = max(0.2, min(0.95, top_ratio)); top = hw*tr
    return ensure_ccw([(-hw,-hd),( hw,-hd),( top, hd),(-top, hd)])

def triangle_shape(w, d):
    hw, hd = w/2, d/2
    return ensure_ccw([(-hw,-hd),( hw,-hd),( 0, hd)])

def regular_ngon(n, rx, ry=None):
    if ry is None: ry = rx
    return ensure_ccw([(rx*math.cos(2*math.pi*i/n), ry*math.sin(2*math.pi*i/n)) for i in range(n)])

def circle_shape(w, d, sides=18):
    r = min(w,d)*0.5
    return regular_ngon(sides, r, r)

def ellipse_shape(w, d, sides=22, ratio=0.7):
    rx = w*0.5; ry = d*0.5*ratio
    return regular_ngon(sides, rx, ry)

# ======================
#   Fenêtres & toits
# ======================
def _build_window_proto(win_w, win_h, lit=False):
    init_materials_if_needed()
    made=[]
    bpy.ops.mesh.primitive_cube_add(size=1); pane = bpy.context.active_object
    pane.scale = (win_w/2, 0.01, win_h/2); pane.data.materials.append(MAT_LIT if lit else MAT_GLASS); made.append(pane)
    bpy.ops.mesh.primitive_cube_add(size=1); frame = bpy.context.active_object
    frame.scale = (win_w/2+0.04, 0.02, win_h/2+0.04); mod = frame.modifiers.new("Solidify","SOLIDIFY"); mod.thickness=0.04; mod.offset=1
    made.append(frame)
    proto = join_objects(made, "CG_Window_ON_proto" if lit else "CG_Window_OFF_proto")
    proto.hide_viewport = True; proto.hide_render = True; proto.location = (9999,9999,9999)
    return proto

def window_prototypes(win_w, win_h):
    off = bpy.data.objects.get("CG_Window_OFF_proto"); on = bpy.data.objects.get("CG_Window_ON_proto")
    if off and on: return off, on
    return _build_window_proto(win_w, win_h, False), _build_window_proto(win_w, win_h, True)

def place_windows_along_edges(building_obj, verts2d_ccw, floors, z0, floor_h, win_w, win_h, win_sill, spacing, depth, lit_ratio, join=True):
    off_proto, on_proto = window_prototypes(win_w, win_h)
    made=[]
    for i in range(len(verts2d_ccw)):
        p1 = Vector((verts2d_ccw[i][0],  verts2d_ccw[i][1], 0))
        p2 = Vector((verts2d_ccw[(i+1)%len(verts2d_ccw)][0], verts2d_ccw[(i+1)%len(verts2d_ccw)][1], 0))
        edge = p2 - p1; length = edge.length
        if length < win_w*1.2: continue
        cols = max(1, int(length // spacing))
        dir_vec = edge.normalized(); normal = Vector((-dir_vec.y, dir_vec.x, 0)).normalized()
        start = (length - (cols-1)*spacing) * 0.5
        for c in range(cols):
            t = start + c*spacing; base_pt = p1 + dir_vec * t
            for f in range(floors):
                z = z0 + win_sill + win_h/2 + f*floor_h
                pos_local = base_pt + normal * (depth*0.5) + Vector((0,0,z))
                world_pos = building_obj.matrix_world @ pos_local
                lit = (random.random() < lit_ratio and f>0)
                src = on_proto if lit else off_proto
                inst = src.copy(); inst.data = src.data.copy()
                bpy.context.collection.objects.link(inst)
                rot_z = math.atan2(normal.y, normal.x); inst.rotation_euler = (0, 0, rot_z)
                inst.location = world_pos; inst.parent = building_obj
                made.append(inst)
    if join and made:
        j = join_objects(made, f"{building_obj.name}_Windows")
        if j: j.parent = building_obj
        return [j] if j else []
    return made

def add_flat_roof(building, top_z, verts2d_ccw, parapet_h=0.25):
    init_materials_if_needed()
    mesh = bpy.data.meshes.new(f"{building.name}_RoofFlat")
    bm = bmesh.new(); vtx = [bm.verts.new((x, y, top_z+0.03)) for (x,y) in verts2d_ccw]
    bm.faces.new(vtx); bm.normal_update(); bm.to_mesh(mesh); bm.free()
    obj = bpy.data.objects.new(mesh.name, mesh); bpy.context.collection.objects.link(obj)
    obj.data.materials.append(MAT_ROOF)
    solid = obj.modifiers.new("Solidify","SOLIDIFY"); solid.thickness = parapet_h; solid.offset = 1
    obj.parent = building; return [obj]

def add_hip_roof(building, top_z, verts2d_ccw):
    init_materials_if_needed()
    cx = sum([v[0] for v in verts2d_ccw])/len(verts2d_ccw); cy = sum([v[1] for v in verts2d_ccw])/len(verts2d_ccw)
    tip = Vector((cx, cy, top_z + 0.8))
    mesh = bpy.data.meshes.new(f"{building.name}_RoofHip")
    bm = bmesh.new(); vtx = [bm.verts.new((x, y, top_z)) for (x,y) in verts2d_ccw]; bm.faces.new(vtx)
    geom = bmesh.ops.extrude_face_region(bm, geom=list(bm.faces)); vs = [e for e in geom['geom'] if isinstance(e, bmesh.types.BMVert)]
    for v in vs: v.co = v.co.lerp(tip, 0.9)
    bm.normal_update(); bm.to_mesh(mesh); bm.free()
    obj = bpy.data.objects.new(mesh.name, mesh); bpy.context.collection.objects.link(obj)
    obj.data.materials.append(MAT_ROOF); obj.parent = building; return [obj]

# ======================
#   Textures
# ======================
def set_facade_tileable_texture(mat, image, scale=(1.0, 1.0)):
    mat.use_nodes = True
    nt = mat.node_tree
    for n in list(nt.nodes): nt.nodes.remove(n)
    out = nt.nodes.new("ShaderNodeOutputMaterial")
    bsdf = nt.nodes.new("ShaderNodeBsdfPrincipled"); nt.links.new(bsdf.outputs["BSDF"], out.inputs["Surface"])
    tex = nt.nodes.new("ShaderNodeTexImage"); tex.image = image
    try: tex.interpolation = 'Smart'
    except: tex.interpolation = 'Linear'
    tex.extension = 'REPEAT'; tex.projection = 'FLAT'
    mapn = nt.nodes.new("ShaderNodeMapping"); mapn.inputs["Scale"].default_value[0]=scale[0]; mapn.inputs["Scale"].default_value[1]=scale[1]
    tc = nt.nodes.new("ShaderNodeTexCoord"); nt.links.new(tc.outputs["Generated"], mapn.inputs["Vector"]); nt.links.new(mapn.outputs["Vector"], tex.inputs["Vector"])
    nt.links.new(tex.outputs["Color"], bsdf.inputs["Base Color"]); bsdf.inputs["Roughness"].default_value = 0.65

def get_texture_pool(dirpath):
    path = bpy.path.abspath(dirpath)
    if not os.path.isdir(path): return []
    files = []
    for ext in ("*.png","*.jpg","*.jpeg","*.webp","*.tif","*.tiff"): files += glob.glob(os.path.join(path, ext))
    imgs=[]
    for f in files:
        try: imgs.append(bpy.data.images.load(f, check_existing=True))
        except: pass
    return imgs

def pick_image_or_none(pool):
    return random.choice(pool) if pool else None

def ensure_tex_principled(mat, image, roughness=0.6, emission_strength=0.0, use_emission=False, scale=(1.0,1.0)):
    mat.use_nodes = True
    nt = mat.node_tree
    for n in list(nt.nodes): nt.nodes.remove(n)
    out = nt.nodes.new("ShaderNodeOutputMaterial"); out.location = (400, 0)
    principled = nt.nodes.new("ShaderNodeBsdfPrincipled"); principled.location = (160, 0)
    principled.inputs["Roughness"].default_value = roughness
    tex = nt.nodes.new("ShaderNodeTexImage"); tex.location = (-260, 0); tex.image = image
    try: tex.interpolation = 'Smart'
    except: tex.interpolation = 'Linear'
    tex.extension = 'REPEAT'
    mapn = nt.nodes.new("ShaderNodeMapping"); mapn.location = (-460, 0)
    mapn.inputs["Scale"].default_value[0] = scale[0]; mapn.inputs["Scale"].default_value[1] = scale[1]
    tc = nt.nodes.new("ShaderNodeTexCoord"); tc.location = (-660, 0)
    nt.links.new(tc.outputs["Generated"], mapn.inputs["Vector"])
    nt.links.new(mapn.outputs["Vector"], tex.inputs["Vector"])
    nt.links.new(tex.outputs["Color"], principled.inputs["Base Color"])
    if use_emission:
        emis = nt.nodes.new("ShaderNodeEmission"); emis.location = (160, -180)
        emis.inputs["Strength"].default_value = emission_strength
        add = nt.nodes.new("ShaderNodeAddShader"); add.location = (320, -60)
        nt.links.new(principled.outputs["BSDF"], add.inputs[0])
        nt.links.new(emis.outputs["Emission"], add.inputs[1])
        nt.links.new(add.outputs["Shader"], out.inputs["Surface"])
    else:
        nt.links.new(principled.outputs["BSDF"], out.inputs["Surface"])

def apply_window_textures_if_any(win_pool, scale=(1.0,1.0)):
    if not win_pool: return
    img = pick_image_or_none(win_pool)
    if img:
        ensure_tex_principled(MAT_GLASS, img, roughness=0.02, emission_strength=0.0, use_emission=False, scale=scale)
        ensure_tex_principled(MAT_LIT,   img, roughness=0.3,  emission_strength=3.0, use_emission=True,  scale=scale)

def make_mat_from_image(prefix, image, roughness=0.85, scale=(1.0,1.0)):
    mat = bpy.data.materials.new(f"{prefix}_{image.name}")
    ensure_tex_principled(mat, image, roughness=roughness, scale=scale)
    return mat

# ======================
#   Détails toit (tours)
# ======================
def add_rooftop_hvac_group(parent, base_z, count, area_bbox=8.0):
    init_materials_if_needed()
    objs=[]
    for i in range(count):
        sx = random.uniform(-area_bbox*0.4, area_bbox*0.4); sy = random.uniform(-area_bbox*0.4, area_bbox*0.4)
        w = random.uniform(0.8, 1.6); d = random.uniform(1.0, 2.0); h = random.uniform(0.4, 0.9)
        bpy.ops.mesh.primitive_cube_add(size=1); hv = bpy.context.active_object
        hv.scale = (w/2, d/2, h/2); hv.location = parent.location + Vector((sx, sy, base_z + h/2 + 0.05))
        hv.data.materials.append(MAT_METAL); hv.name = f"{parent.name}_HVAC_{i}"; hv.parent = parent; objs.append(hv)
    if objs: join_objects(objs, f"{parent.name}_HVAC_Joined")

def add_rooftop_antennas(parent, base_z, count, radius=6.0):
    init_materials_if_needed()
    objs=[]
    for i in range(count):
        angle = random.uniform(0, 2*math.pi); r = random.uniform(radius*0.3, radius)
        x = math.cos(angle)*r; y = math.sin(angle)*r; h = random.uniform(2.0, 6.0)
        bpy.ops.mesh.primitive_cylinder_add(vertices=16, radius=0.06, depth=h); mast = bpy.context.active_object
        mast.location = parent.location + Vector((x, y, base_z + h/2 + 0.05)); mast.data.materials.append(MAT_METAL)
        mast.name = f"{parent.name}_Antenna_{i}"; mast.parent = parent
        bpy.ops.mesh.primitive_uv_sphere_add(segments=16, ring_count=8, radius=0.12); head = bpy.context.active_object
        head.location = parent.location + Vector((x, y, base_z + h + 0.12)); head.data.materials.append(MAT_METAL); head.parent = parent
        objs.extend([mast, head])
    if objs: join_objects(objs, f"{parent.name}_Antennas_Joined")

def add_rooftop_tech_box(parent, base_z, size=(3.0, 2.2, 1.2)):
    init_materials_if_needed()
    w,d,h = size; bpy.ops.mesh.primitive_cube_add(size=1); box = bpy.context.active_object
    box.scale = (w/2, d/2, h/2); box.location = parent.location + Vector((0, 0, base_z + h/2 + 0.08))
    box.data.materials.append(MAT_ROOF); box.name = f"{parent.name}_TechBox"; box.parent = parent; return box

# ======================
#   Empreinte & construction des bâtiments
# ======================
def random_footprint(w, d, p, force_towers=False):
    w -= 2*p.setback; d -= 2*p.setback; w = max(4.0, w); d = max(4.0, d)
    choices=[]
    if force_towers: choices = ["hexagon","circle","ellipse"]
    else:
        if p.use_rect: choices.append("rectangle")
        if p.use_L:    choices.append("L")
        if p.use_U:    choices.append("U")
        if p.use_T:    choices.append("T")
        if p.use_tri:  choices.append("triangle")
        if p.use_trap: choices.append("trapezoid")
        if p.use_hex:  choices.append("hexagon")
        if p.use_circle: choices.append("circle")
        if p.use_ellipse:choices.append("ellipse")
        if not choices: choices=["rectangle"]
    shape = random.choice(choices)
    if shape == "rectangle":  verts = rect_shape(w,d)
    elif shape == "L":        verts = L_shape(w,d,(random.uniform(0.35,0.55), random.uniform(0.35,0.55)))
    elif shape == "U":        verts = U_shape(w,d, notch_w=random.uniform(0.35,0.6), notch_d=random.uniform(0.35,0.55))
    elif shape == "T":        verts = T_shape(w,d)
    elif shape == "triangle": verts = triangle_shape(w,d)
    elif shape == "trapezoid":verts = trapezoid_shape(w,d, top_ratio=random.uniform(0.5,0.9))
    elif shape == "hexagon":  verts = regular_ngon(6, w*0.45, d*0.45)
    elif shape == "circle":   verts = circle_shape(w,d, sides=18)
    elif shape == "ellipse":  verts = ellipse_shape(w,d, sides=22, ratio=random.uniform(0.6,1.0))
    else:                     verts = rect_shape(w,d)
    return ensure_ccw(verts), shape

def make_building_nonrect(name, lot_center, lot_size, p, tex_pool=None, force_towers=False):
    verts, shape = random_footprint(lot_size[0], lot_size[1], p, force_towers=force_towers)
    is_skyscraper = shape in {"circle", "ellipse", "hexagon"}
    floors = random.randint(p.skyscraper_min_floors, p.skyscraper_max_floors) if is_skyscraper else random.randint(p.min_floors, p.max_floors)
    # Variation douce
    noise = math.sin(lot_center[0]*0.05) * math.cos(lot_center[1]*0.05)
    floors = max(1, int(floors * (1.0 + 0.15*noise)))
    h = floors * p.floor_h
    init_materials_if_needed()

    # Façade + textures
    if is_skyscraper:
        if p.skyscraper_use_textures:
            img = pick_image_or_none(get_texture_pool(p.skyscraper_texture_dir))
            if img:
                mat_fac = bpy.data.materials.new(f"CG_Fac_Sky_{img.name}")
                set_facade_tileable_texture(mat_fac, img, scale=(p.tex_scale_x, p.tex_scale_y))
            else:
                mat_fac = MAT_GLASS if p.skyscraper_glass else facade_mat_random_color()
        else:
            mat_fac = MAT_GLASS if p.skyscraper_glass else facade_mat_random_color()
    else:
        img = pick_image_or_none(get_texture_pool(p.building_wall_tex_dir)) if p.use_textures else None
        if img:
            mat_fac = bpy.data.materials.new(f"CG_Fac_Wall_{img.name}")
            set_facade_tileable_texture(mat_fac, img, scale=(p.tex_scale_x, p.tex_scale_y))
        else:
            mat_fac = facade_mat_random_color()

    verts_world = [(x+lot_center[0], y+lot_center[1]) for (x,y) in verts]
    bld = make_polygon_mesh(name, verts_world, 0.0, h, mat_fac)

    if not (is_skyscraper and p.skyscraper_glass and not p.skyscraper_use_textures):
        place_windows_along_edges(bld, verts_world, floors, 0.0, p.floor_h, p.win_w, p.win_h, p.win_sill, p.win_spacing, p.win_depth, p.lit_ratio, p.join_windows)

    add_flat_roof(bld, h, verts_world, parapet_h=max(0.2, p.parapet_h)) if is_skyscraper else (
        add_flat_roof(bld, h, verts_world, parapet_h=p.parapet_h) if p.roof_type=='FLAT' else add_hip_roof(bld, h, verts_world)
    )
    if is_skyscraper and p.skyscraper_roof_details:
        base_radius = min(lot_size) * 0.35
        if p.skyscraper_add_techbox: add_rooftop_tech_box(bld, h, size=(p.techbox_w, p.techbox_d, p.techbox_h))
        add_rooftop_hvac_group(bld, h, count=random.randint(p.hvac_min, p.hvac_max), area_bbox=base_radius*2.0)
        add_rooftop_antennas(bld, h, count=random.randint(p.ant_min, p.ant_max), radius=base_radius)
    return bld

# ======================
#   Parcs
# ======================
def make_park(cx, cy, lot_size, tree_count=6):
    init_materials_if_needed()
    park = make_polygon_mesh("CG_Park", rect_shape(lot_size, lot_size), 0, 0.06, MAT_GRASS)
    park.location = (cx, cy, 0); trees=[]
    for i in range(tree_count):
        angle = random.uniform(0, 2*math.pi); r = random.uniform(0.8, lot_size*0.45)
        x = cx + math.cos(angle)*r; y = cy + math.sin(angle)*r
        bpy.ops.mesh.primitive_cylinder_add(vertices=12, radius=0.08, depth=0.6); trunk = bpy.context.active_object
        trunk.location = (x, y, 0.3); trunk.data.materials.append(MAT_ROOF)
        bpy.ops.mesh.primitive_ico_sphere_add(subdivisions=1, radius=0.5); crown = bpy.context.active_object
        crown.location = (x, y, 0.9); crown.data.materials.append(MAT_GRASS)
        trees.extend([trunk, crown])
    if trees:
        j = join_objects(trees, "CG_Park_Trees")
        if j: j.parent = park
    return park

# ======================
#   Routes & layout + diagonales
# ======================
def _make_strip(name, length, width, z=0.04, mat=None, loc=(0,0,0), angle_rad=0.0, z_offset=0.0):
    """Bande routière; z_offset pour éviter la coplanarité (z-fighting)."""
    bpy.ops.mesh.primitive_cube_add(size=1)
    r = bpy.context.active_object; r.name = name
    r.scale = (length*0.5, width*0.5, z)
    r.location = (loc[0], loc[1], (loc[2] if isinstance(loc, (tuple, list)) else 0.0) + z_offset)
    r.rotation_euler = (0, 0, angle_rad)
    if mat: r.data.materials.append(mat)
    return r

def _pick_width_and_mat(p):
    if random.random() < p.pedestrian_prob:
        return p.pedestrian_w, MAT_PEDESTRIAN
    w = random.uniform(p.road_w_min, p.road_w_max)
    mat = MAT_ALLEY if w <= (p.road_w_min + p.road_w_max)*0.5*0.65 else MAT_ROAD
    return w, mat

def _generate_axis_layout(count_lots, lot_size, road_picker, lot_var=0.15, jitter=1.0):
    # tailles de lots individuelles (±variation)
    lot_sizes = [lot_size * (1.0 + random.uniform(-lot_var, lot_var)) for _ in range(count_lots)]
    road_widths = [road_picker()[0] for _ in range(max(0, count_lots-1))]
    total_len = sum(lot_sizes) + sum(road_widths)
    x0 = -total_len * 0.5
    centers = []; cur = x0
    for i in range(count_lots):
        cur += lot_sizes[i] * 0.5
        jitter_i = random.uniform(-jitter, jitter)
        centers.append(cur + jitter_i)
        cur += lot_sizes[i] * 0.5
        if i < count_lots-1: cur += road_widths[i]
    return centers, road_widths, total_len, lot_sizes

# ======================
#   Booleans & nettoyage
# ======================
def add_boolean_diff(target_obj, cutter_obj, name="CG_Cut"):
    if not target_obj or not cutter_obj: return
    try:
        m = target_obj.modifiers.get(name) or target_obj.modifiers.new(name, 'BOOLEAN')
        m.operation = 'DIFFERENCE'; m.solver = 'EXACT'; m.object = cutter_obj
    except Exception: pass

def make_heighted_cutter(source_obj, name, half_height, hide=True, z_offset=0.0):
    if not source_obj: return None
    dup = source_obj.copy(); dup.data = source_obj.data.copy(); dup.name = name
    bpy.context.collection.objects.link(dup)
    if hide: dup.hide_viewport = True; dup.hide_render = True
    if dup.scale.z == 0: dup.scale.z = 1.0
    dup.scale.z *= max(half_height * 50.0, 10.0)
    dup.location.z = z_offset
    return dup

def clean_mesh_data(obj, merge_dist=0.0002):
    if not getattr(obj, "data", None) or obj.type != 'MESH': return
    me = obj.data; bm = bmesh.new(); bm.from_mesh(me)
    try:
        bmesh.ops.remove_doubles(bm, verts=bm.verts, dist=merge_dist)
        bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
    except Exception: pass
    bm.to_mesh(me); bm.free(); me.update()

def apply_boolean_modifiers(objs):
    view_layer = bpy.context.view_layer
    for o in objs:
        if not getattr(o, "modifiers", None): continue
        bool_mods = [m for m in list(o.modifiers) if m.type == 'BOOLEAN']
        if not bool_mods: continue
        try:
            for obj in view_layer.objects: obj.select_set(False)
            o.select_set(True); view_layer.objects.active = o
            for m in bool_mods:
                try: bpy.ops.object.modifier_apply(modifier=m.name)
                except Exception: pass
        except Exception: pass
        residual = [m for m in list(o.modifiers) if m.type == 'BOOLEAN']
        if residual:
            deps = bpy.context.evaluated_depsgraph_get()
            o_eval = o.evaluated_get(deps)
            try:
                new_me = bpy.data.meshes.new_from_object(o_eval, preserve_all_data_layers=False, depsgraph=deps)
                o.modifiers.clear(); o.data = new_me
            except Exception: pass
        clean_mesh_data(o, merge_dist=0.0002)

def delete_window_prototypes():
    for name in ("CG_Window_OFF_proto", "CG_Window_ON_proto"):
        obj = bpy.data.objects.get(name)
        if obj:
            try:
                for col in list(obj.users_collection):
                    try: col.objects.unlink(obj)
                    except: pass
                bpy.data.objects.remove(obj, do_unlink=True)
            except Exception: pass

def delete_cutters():
    for obj in list(bpy.data.objects):
        if "Cutter" in obj.name or obj.name.startswith("CG_Roads_All_Cutter"):
            try:
                for col in list(obj.users_collection):
                    try: col.objects.unlink(obj)
                    except: pass
                bpy.data.objects.remove(obj, do_unlink=True)
            except Exception: pass

# ======================
#   Construction de la scène
# ======================
# ==== Helpers Multi-bâtiments : Grille & Poisson ====
def _grid_for_count(n):
    import math
    ny = int(math.sqrt(n))
    nx = max(1, math.ceil(n / max(1, ny)))
    while (nx-1) * ny >= n and nx > 1: nx -= 1
    while nx * (ny-1) >= n and ny > 1: ny -= 1
    return nx, ny

def _sublot_centers_and_sizes(lot_w, lot_d, n, fill=0.7, jitter=0.6):
    import random
    nx, ny = _grid_for_count(n)
    cell_w = lot_w / nx
    cell_d = lot_d / ny
    used = []; k = 0
    for iy in range(ny):
        for ix in range(nx):
            if k >= n: break
            cx = (ix + 0.5) * cell_w - lot_w/2
            cy = (iy + 0.5) * cell_d - lot_d/2
            jx = random.uniform(-jitter, jitter)
            jy = random.uniform(-jitter, jitter)
            bw = cell_w * fill
            bd = cell_d * fill
            used.append((cx + jx, cy + jy, bw, bd)); k += 1
        if k >= n: break
    return used

def _poisson_in_rect(n_target, rect_w, rect_d, radius_min, max_tries=25, seed=None):
    import random
    if seed is not None: random.seed(seed)
    pts = [(0.0, 0.0)]
    def ok(p):
        x,y = p
        if not (-rect_w/2 <= x <= rect_w/2 and -rect_d/2 <= y <= rect_d/2):
            return False
        for (ax,ay) in pts:
            dx = x-ax; dy = y-ay
            if dx*dx + dy*dy < radius_min*radius_min:
                return False
        return True
    tries = 0
    while len(pts) < n_target and tries < n_target*max_tries:
        tries += 1
        x = random.uniform(-rect_w/2, rect_w/2)
        y = random.uniform(-rect_d/2, rect_d/2)
        if ok((x,y)): pts.append((x,y))
    return pts

def _sublots_poisson(lot_w, lot_d, n, setback, radius_min, tries):
    w = max(2.0, lot_w - 2*setback)
    d = max(2.0, lot_d - 2*setback)
    if w <= 2.0 or d <= 2.0:
        return [(0.0, 0.0, w, d)]
    pts = _poisson_in_rect(n, w, d, radius_min, max_tries=tries)
    k = 1.6
    bw = min(w, max(4.0, k * radius_min))
    bd = min(d, max(4.0, k * radius_min))
    return [(x, y, bw, bd) for (x,y) in pts]
# --- Simple proxy to override a few fields while falling back to the base PropertyGroup ---
class _PProxy:
    __slots__ = ("_base", "_over")
    def __init__(self, base, **over):
        self._base = base
        self._over = over
    def __getattr__(self, name):
        if name in self._over:
            return self._over[name]
        return getattr(self._base, name)
    def __setattr__(self, name, value):
        if name in ("_base","_over"):
            object.__setattr__(self, name, value)
        else:
            self._over[name] = value




def build_city(p, tex_pool=None, force_towers=False):
    init_materials_if_needed()
    if p.clear_scene: safe_clear_scene()
    random.seed(p.seed)

    # Pools textures
    win_pool  = get_texture_pool(p.window_tex_dir) if p.use_window_textures else None
    road_pool = get_texture_pool(p.road_tex_dir)
    sw_pool   = get_texture_pool(p.sidewalk_tex_dir)

    apply_window_textures_if_any(win_pool, scale=(p.tex_scale_x, p.tex_scale_y))

    # sol
    bpy.ops.mesh.primitive_plane_add(size=p.ground_size); g = bpy.context.active_object; g.name="CG_Ground"
    if not g.data.materials: g.data.materials.append(MAT_GROUND)
    city = bpy.data.objects.new("CG_City", None); bpy.context.collection.objects.link(city)

    # Layout H/V non uniformes
    x_centers, v_road_w, total_w, lot_sizes_x = _generate_axis_layout(
        p.count_x, p.lot_size, road_picker=lambda: _pick_width_and_mat(p),
        lot_var=p.lot_size_variation, jitter=p.row_col_jitter
    )
    y_centers, h_road_w, total_h, lot_sizes_y = _generate_axis_layout(
        p.count_y, p.lot_size, road_picker=lambda: _pick_width_and_mat(p),
        lot_var=p.lot_size_variation, jitter=p.row_col_jitter
    )
    g.scale = (max(total_w, p.ground_size)/2, max(total_h, p.ground_size)/2, 1)

    # Routes H & V (texture aléatoire par segment)
    roads=[]
    for j in range(p.count_y-1):
        y_mid  = (y_centers[j] + y_centers[j+1]) * 0.5
        width  = h_road_w[j]
        r = _make_strip("CG_Road_H", length=total_w, width=width, mat=None, loc=(0, y_mid, 0.04))
        img = pick_image_or_none(road_pool)
        if img:
            road_mat = make_mat_from_image("CG_RoadTex", img, roughness=0.9, scale=(p.road_tex_scale_x, p.road_tex_scale_y))
            r.data.materials.clear(); r.data.materials.append(road_mat)
        else:
            r.data.materials.append(MAT_ROAD)
        roads.append(r)

    for i in range(p.count_x-1):
        x_mid  = (x_centers[i] + x_centers[i+1]) * 0.5
        width  = v_road_w[i]
        r = _make_strip("CG_Road_V", length=total_h, width=width, mat=None, loc=(x_mid, 0, 0.04), angle_rad=math.radians(90))
        img = pick_image_or_none(road_pool)
        if img:
            road_mat = make_mat_from_image("CG_RoadTex", img, roughness=0.9, scale=(p.road_tex_scale_x, p.road_tex_scale_y))
            r.data.materials.clear(); r.data.materials.append(road_mat)
        else:
            r.data.materials.append(MAT_ROAD)
        roads.append(r)

    roads_union = join_objects(roads, "CG_Roads")
    if roads_union: roads_union.parent = city

    # Diagonales (+ z_offset) + cutter routes HV (élargi)
    diag_union = None
    roads_diag=[]; diag_cutter_road = None
    if p.diag_count > 0:
        L = math.sqrt(total_w**2 + total_h**2) * 1.15
        def add_family(angle_deg, count):
            ang = math.radians(angle_deg)
            # offsets espacés (simplement)
            span_guess = max(total_w, total_h)*0.55
            offs = []
            tries = 0
            while len(offs) < count and tries < 200:
                tries += 1
                cand = random.uniform(-span_guess, span_guess)
                ok = True
                for other in offs:
                    if abs(cand - other) < (p.diag_w + 0.6): ok=False; break
                if ok: offs.append(cand)
            if len(offs) < count:
                step = (2*span_guess)/(count+1)
                offs = [-span_guess + (k+1)*step for k in range(count)]
            return ang, offs

        nA, nB = (p.diag_count, p.diag_count) if p.diag_both_orient else (p.diag_count, 0)
        angA, offsA = add_family(+45, nA)
        angB, offsB = add_family(-45, nB)

        def make_diag(angle_rad, offset):
            nx = math.cos(angle_rad + math.pi/2.0); ny = math.sin(angle_rad + math.pi/2.0)
            cx = nx * offset; cy = ny * offset
            r = _make_strip(
                "CG_Road_D", length=L, width=p.diag_w, mat=None,
                loc=(cx, cy, 0.041), angle_rad=angle_rad, z_offset=p.diag_z_offset
            )
            img = pick_image_or_none(road_pool)
            if img:
                road_mat = make_mat_from_image("CG_RoadTex", img, roughness=0.9, scale=(p.road_tex_scale_x, p.road_tex_scale_y))
                r.data.materials.clear(); r.data.materials.append(road_mat)
            else:
                r.data.materials.append(MAT_ROAD)
            roads_diag.append(r)

        for off in offsA: make_diag(angA, off)
        for off in offsB: make_diag(angB, off)

        diag_union = join_objects(roads_diag, "CG_Roads_Diag")
        if diag_union:
            diag_union.parent = city
            # Cutter pour percer les routes HV
            diag_cutter_road = make_heighted_cutter(
                diag_union, "CG_Roads_Diag_Cutter_Road", half_height=3.0, hide=False, z_offset=0.0
            )
            diag_cutter_road.parent = city
            # Élargir le cutter avec Solidify (marge réglable)
            if p.diag_cut_expand > 0.0:
                try:
                    mod = diag_cutter_road.modifiers.new("CG_CutterExpand", "SOLIDIFY")
                    mod.thickness = p.diag_cut_expand
                    mod.offset = 0.0
                    for obj in bpy.context.view_layer.objects: obj.select_set(False)
                    diag_cutter_road.select_set(True)
                    bpy.context.view_layer.objects.active = diag_cutter_road
                    bpy.ops.object.modifier_apply(modifier=mod.name)
                except Exception: pass
            if roads_union and diag_cutter_road:
                add_boolean_diff(roads_union, diag_cutter_road, name="CG_Cut_Roads_Diag")

    # Cutters trottoirs & bâtiments
    hv_cutter_sidewalk = None
    if roads_union:
        hv_cutter_sidewalk = make_heighted_cutter(roads_union, "CG_Roads_HV_Cutter_Sidewalk", half_height=0.3, hide=True, z_offset=0.06)
        hv_cutter_sidewalk.parent = city
    diag_cutter_sidewalk = None
    diag_cutter_building = None
    if diag_union:
        diag_cutter_sidewalk = make_heighted_cutter(diag_union, "CG_Roads_Diag_Cutter_Sidewalk", half_height=0.3, hide=True, z_offset=0.06)
        diag_cutter_sidewalk.parent = city
        h_max = max(p.skyscraper_max_floors, p.max_floors) * p.floor_h + 5.0
        diag_cutter_building = make_heighted_cutter(diag_union, "CG_Roads_Diag_Cutter_Building", half_height=h_max, hide=True, z_offset=0.0)
        diag_cutter_building.parent = city

    sidewalk_total_cutter = None
    sw_parts = [c for c in (hv_cutter_sidewalk, diag_cutter_sidewalk) if c]
    if len(sw_parts) == 2:
        sidewalk_total_cutter = join_objects(sw_parts, "CG_Roads_All_Cutter_Sidewalk")
        sidewalk_total_cutter.hide_viewport = True; sidewalk_total_cutter.hide_render = True; sidewalk_total_cutter.parent = city
    elif len(sw_parts) == 1:
        sidewalk_total_cutter = sw_parts[0]

    # Lots : trottoirs & bâtiments avec variations + fusions + chanfreins
    all_buildings = []; all_sidewalks = []
    for ix, cx in enumerate(x_centers):
        for iy, cy in enumerate(y_centers):
            if random.random() > p.lot_density:
                park = make_park(cx, cy, min(lot_sizes_x[ix], lot_sizes_y[iy]), tree_count=random.randint(3,8))
                park.parent = city; continue

            lot_w = lot_sizes_x[ix]; lot_d = lot_sizes_y[iy]
            merged_w = 1; merged_d = 1
            # Fusion aléatoire de lots (2x1 ou 1x2)
            if random.random() < p.merge_lots_prob:
                if random.random() < 0.5 and ix < len(x_centers)-1:
                    merged_w = 2
                    lot_w = lot_sizes_x[ix] + v_road_w[ix] + lot_sizes_x[ix+1]
                elif iy < len(y_centers)-1:
                    merged_d = 2
                    lot_d = lot_sizes_y[iy] + h_road_w[iy] + lot_sizes_y[iy+1]

            # Trottoir
            sx = make_polygon_mesh("CG_Sidewalk", rect_shape(lot_w, lot_d), 0, 0.12, None)
            sx.location = (cx + (v_road_w[ix]*0.5 if merged_w==2 else 0.0),
                           cy + (h_road_w[iy]*0.5 if merged_d==2 else 0.0), 0)
            img_sw = pick_image_or_none(sw_pool)
            if img_sw:
                sw_mat = make_mat_from_image("CG_SideTex", img_sw, roughness=0.85, scale=(p.sidewalk_tex_scale_x, p.sidewalk_tex_scale_y))
                sx.data.materials.append(sw_mat)
            else:
                sx.data.materials.append(MAT_SIDE)

            # Chanfrein optionnel
            if random.random() < p.sidewalk_chamfer_prob and p.sidewalk_chamfer_size > 0.0:
                try:
                    bpy.context.view_layer.objects.active = sx
                    sx.select_set(True)
                    bpy.ops.object.mode_set(mode='EDIT')
                    bpy.ops.mesh.select_all(action='SELECT')
                    bpy.ops.mesh.bevel(offset=p.sidewalk_chamfer_size, offset_type='OFFSET', segments=1, profile=0.5, affect='VERTICES')
                    bpy.ops.object.mode_set(mode='OBJECT')
                    sx.select_set(False)
                except Exception:
                    try: bpy.ops.object.mode_set(mode='OBJECT')
                    except: pass

            # Bâtiment (setback variable local)
            local_setback = max(0.0, p.setback + random.uniform(-p.setback_var, p.setback_var))
            p_local = _PProxy(p, setback=local_setback)

            b = make_building_nonrect(
                f"CG_Bld_{ix}_{iy}", (sx.location.x, sx.location.y), (lot_w, lot_d), p_local,
                tex_pool, force_towers=force_towers
            )
            sx.parent = city; b.parent = city
            all_sidewalks.append(sx); all_buildings.append(b)

            # Découpes lots
            if p.cut_with_diagonals:
                if sidewalk_total_cutter:
                    add_boolean_diff(sx, sidewalk_total_cutter, name="CG_Cut_Sidewalk")
                if diag_cutter_building:
                    add_boolean_diff(b, diag_cutter_building, name="CG_Cut_Building_Diag")

    # Fusion finale
    merged_bld = merged_sw = None
    if all_buildings:
        merged_bld = join_objects(all_buildings, "CG_All_Buildings")
        if merged_bld: merged_bld.parent = city
    if all_sidewalks:
        merged_sw = join_objects(all_sidewalks, "CG_All_Sidewalks")
        if merged_sw: merged_sw.parent = city

    # Appliquer booléens + nettoyer (inclure routes pour appliquer la découpe des diagonales)
    targets_to_clean = []
    if roads_union: targets_to_clean.append(roads_union)
    if merged_bld:  targets_to_clean.append(merged_bld)
    if merged_sw:   targets_to_clean.append(merged_sw)
    apply_boolean_modifiers(targets_to_clean)

    # Nettoyage des objets temporaires
    delete_window_prototypes()
    delete_cutters()

    # Caméra / lumière si absentes
    if not any(isinstance(o.data, bpy.types.Camera) for o in bpy.data.objects if o.data):
        d = max(total_w,total_h)*0.6
        bpy.ops.object.camera_add(location=(d,-d,d), rotation=(math.radians(60),0,math.radians(45)))
    if not any(isinstance(o.data, bpy.types.Light) for o in bpy.data.objects if o.data):
        bpy.ops.object.light_add(type='SUN', location=(30,30,60)); bpy.context.active_object.data.energy = 3.0

    # Rotation globale
    if abs(p.grid_rotation_deg) > 1e-4:
        city.rotation_euler[2] = math.radians(p.grid_rotation_deg)

# ======================
#   Propriétés & UI
# ======================
class CG_Props(bpy.types.PropertyGroup):

    # === Multi-bâtiments par lot ===
    multibuild_enable: bpy.props.BoolProperty(
        name="Plusieurs bâtiments / lot", default=False
    )
    lot_buildings_min: bpy.props.IntProperty(
        name="Bâtiments / lot (min)", default=1, min=1, max=12
    )
    lot_buildings_max: bpy.props.IntProperty(
        name="Bâtiments / lot (max)", default=3, min=1, max=20
    )
    sublot_fill: bpy.props.FloatProperty(
        name="Taux d’occupation sous-lot", default=0.70, min=0.3, max=0.95, subtype='FACTOR'
    )
    sublot_jitter: bpy.props.FloatProperty(
        name="Jitter centre sous-lot (m)", default=0.6, min=0.0, max=4.0
    )
    # === Mode de placement (Grille vs Poisson) ===
    placement_mode: bpy.props.EnumProperty(
        name="Placement bâtiments",
        items=[('GRID',"Grille",""), ('POISSON',"Poisson","")],
        default='GRID'
    )
    poisson_min_radius: bpy.props.FloatProperty(
        name="Rayon min (m)", default=2.6, min=0.5, max=20.0
    )
    poisson_max_tries: bpy.props.IntProperty(
        name="Essais par point", default=25, min=5, max=200
    )
    # seed & nettoyage
    seed: bpy.props.IntProperty(name="Seed", default=1337)
    clear_scene: bpy.props.BoolProperty(name="Nettoyer la scène", default=True)

    # grille
    count_x: bpy.props.IntProperty(name="Lots X", default=4, min=1, max=40)
    count_y: bpy.props.IntProperty(name="Lots Y", default=3, min=1, max=40)
    lot_size: bpy.props.FloatProperty(name="Taille lot (m)", default=14.0, min=4.0)
    ground_size: bpy.props.FloatProperty(name="Taille sol (min)", default=220.0, min=10.0)
    grid_rotation_deg: bpy.props.FloatProperty(name="Rotation globale (°)", default=18.0, soft_min=-90.0, soft_max=90.0)
    setback: bpy.props.FloatProperty(name="Retrait (m)", default=0.8, min=0.0, max=5.0)
    lot_density: bpy.props.FloatProperty(name="Densité des lots", default=0.85, min=0.0, max=1.0, subtype='FACTOR')

    # variations blocs
    lot_size_variation: bpy.props.FloatProperty(name="Variation lot (±%)", default=0.15, min=0.0, max=0.6, subtype='FACTOR')
    row_col_jitter: bpy.props.FloatProperty(name="Jitter rangées/colonnes (m)", default=1.0, min=0.0, max=4.0)
    merge_lots_prob: bpy.props.FloatProperty(name="Proba fusion lots", default=0.12, min=0.0, max=0.5, subtype='FACTOR')
    setback_var: bpy.props.FloatProperty(name="Variation retrait (±m)", default=0.4, min=0.0, max=2.0)
    sidewalk_chamfer_prob: bpy.props.FloatProperty(name="Proba chanfrein trottoir", default=0.35, min=0.0, max=1.0, subtype='FACTOR')
    sidewalk_chamfer_size: bpy.props.FloatProperty(name="Taille chanfrein (m)", default=1.0, min=0.0, max=3.0)

    # routes & piétonnes
    road_w_min: bpy.props.FloatProperty(name="Route min (m)", default=3.0, min=1.0)
    road_w_max: bpy.props.FloatProperty(name="Route max (m)", default=8.0, min=1.0)
    pedestrian_prob: bpy.props.FloatProperty(name="Proba rue piétonne", default=0.18, min=0.0, max=1.0, subtype='FACTOR')
    pedestrian_w: bpy.props.FloatProperty(name="Piétonne (m)", default=3.2, min=1.0)

    # diagonales
    diag_count: bpy.props.IntProperty(name="Diagonales / sens", default=1, min=0, max=8)
    diag_w: bpy.props.FloatProperty(name="Largeur diagonale (m)", default=4.0, min=1.0)
    diag_both_orient: bpy.props.BoolProperty(name="Deux orientations (±45°)", default=True)
    diag_z_offset: bpy.props.FloatProperty(name="Décalage Z diagonales (m)", default=0.006, min=0.0, max=0.05, precision=4)
    diag_cut_expand: bpy.props.FloatProperty(name="Marge coupe diagonales (m)", default=0.12, min=0.0, max=0.6, precision=3)

    # découpe
    cut_with_diagonals: bpy.props.BoolProperty(name="Découper lots par diagonales", default=True)
    cut_targets: bpy.props.EnumProperty(name="Cibler", items=[('SIDEWALKS', "Trottoirs", ""), ('BUILDINGS', "Bâtiments", ""), ('BOTH', "Les deux", "")], default='BOTH')

    # étages / fenêtres
    floor_h: bpy.props.FloatProperty(name="Hauteur étage", default=3.0, min=2.2, max=6.0)
    min_floors: bpy.props.IntProperty(name="Min étages", default=3, min=1, max=200)
    max_floors: bpy.props.IntProperty(name="Max étages", default=10, min=1, max=400)
    win_w: bpy.props.FloatProperty(name="Fenêtre L", default=1.2, min=0.4)
    win_h: bpy.props.FloatProperty(name="Fenêtre H", default=1.6, min=0.4)
    win_sill: bpy.props.FloatProperty(name="Allège", default=0.9, min=0.0)
    win_spacing: bpy.props.FloatProperty(name="Espacement", default=2.4, min=0.6)
    win_depth: bpy.props.FloatProperty(name="Profondeur", default=0.06, min=-0.3, max=0.6)
    lit_ratio: bpy.props.FloatProperty(name="Ratio fenêtres allumées", default=0.22, min=0.0, max=1.0)
    join_windows: bpy.props.BoolProperty(name="Joindre fenêtres", default=True)

    # toits (non tours)
    roof_type: bpy.props.EnumProperty(name="Toit", items=[('FLAT',"Plat",""), ('HIP',"Pyramidal","")], default='FLAT')
    parapet_h: bpy.props.FloatProperty(name="Acrotère", default=0.25, min=0.0, max=1.0)

    # formes autorisées
    use_rect: bpy.props.BoolProperty(name="Rectangle", default=True)
    use_L: bpy.props.BoolProperty(name="L", default=True)
    use_U: bpy.props.BoolProperty(name="U", default=True)
    use_T: bpy.props.BoolProperty(name="T", default=True)
    use_tri: bpy.props.BoolProperty(name="Triangle", default=True)
    use_trap: bpy.props.BoolProperty(name="Trapèze", default=True)
    use_hex: bpy.props.BoolProperty(name="Hexagone", default=True)
    use_circle: bpy.props.BoolProperty(name="Cercle", default=True)
    use_ellipse: bpy.props.BoolProperty(name="Ellipse", default=True)

    # Échelle UV façades/fenêtres
    tex_scale_x: bpy.props.FloatProperty(name="Facade scale X", default=1.0, min=0.02, max=50.0)
    tex_scale_y: bpy.props.FloatProperty(name="Facade scale Y", default=1.0, min=0.02, max=50.0)

    # Textures bâtiments
    use_textures: bpy.props.BoolProperty(name="Textures murs (non tours)", default=False)
    building_wall_tex_dir: bpy.props.StringProperty(name="Dossier textures murs (non tours)", default="//textures_buildings/", subtype='DIR_PATH')
    use_window_textures: bpy.props.BoolProperty(name="Textures de fenêtres (non tours)", default=False)
    window_tex_dir: bpy.props.StringProperty(name="Dossier textures fenêtres", default="//textures_windows/", subtype='DIR_PATH')
    skyscraper_use_textures: bpy.props.BoolProperty(name="Textures pour gratte-ciels", default=False)
    skyscraper_texture_dir: bpy.props.StringProperty(name="Dossier textures gratte-ciels", default="//textures_skyscrapers/", subtype='DIR_PATH')

    # Textures routes & trottoirs (aléatoire par segment/lot)
    road_tex_dir: bpy.props.StringProperty(name="Dossier textures ROUTES", default="//textures_roads/", subtype='DIR_PATH')
    sidewalk_tex_dir: bpy.props.StringProperty(name="Dossier textures TROTTOIRS", default="//textures_sidewalks/", subtype='DIR_PATH')
    road_tex_scale_x: bpy.props.FloatProperty(name="Road scale X", default=1.0, min=0.02, max=50.0)
    road_tex_scale_y: bpy.props.FloatProperty(name="Road scale Y", default=1.0, min=0.02, max=50.0)
    sidewalk_tex_scale_x: bpy.props.FloatProperty(name="Sidewalk scale X", default=1.0, min=0.02, max=50.0)
    sidewalk_tex_scale_y: bpy.props.FloatProperty(name="Sidewalk scale Y", default=1.0, min=0.02, max=50.0)

    # export
    export_path: bpy.props.StringProperty(name="Fichier .glb", default="//citygen.glb", subtype='FILE_PATH')
    export_selection_only: bpy.props.BoolProperty(name="Exporter la sélection uniquement", default=False)
    export_triangulate: bpy.props.BoolProperty(name="Trianguler avant export", default=True)

    # gratte-ciel
    skyscraper_min_floors: bpy.props.IntProperty(name="Gratte-ciel min étages", default=18, min=8, max=200)
    skyscraper_max_floors: bpy.props.IntProperty(name="Gratte-ciel max étages", default=42, min=10, max=400)
    skyscraper_glass: bpy.props.BoolProperty(name="Façade vitrée (tours)", default=True)
    skyscraper_roof_details: bpy.props.BoolProperty(name="Détails toit (HVAC, antennes)", default=True)
    hvac_min: bpy.props.IntProperty(name="HVAC min", default=2, min=0, max=20)
    hvac_max: bpy.props.IntProperty(name="HVAC max", default=6, min=0, max=40)
    ant_min: bpy.props.IntProperty(name="Antennes min", default=1, min=0, max=20)
    ant_max: bpy.props.IntProperty(name="Antennes max", default=3, min=0, max=40)
    skyscraper_add_techbox: bpy.props.BoolProperty(name="Caisson technique", default=True)
    techbox_w: bpy.props.FloatProperty(name="TechBox L", default=3.0, min=0.5, max=20.0)
    techbox_d: bpy.props.FloatProperty(name="TechBox l", default=2.2, min=0.5, max=20.0)
    techbox_h: bpy.props.FloatProperty(name="TechBox h", default=1.2, min=0.3, max=10.0)

# ======================
#   Opérateurs
# ======================
class CITYGEN_OT_apply_profile(bpy.types.Operator):
    bl_idname = "citygen.apply_profile"
    bl_label = "Appliquer profil"
    bl_description = "Applique un profil de paramètres (Low-poly / HQ)"
    profile: bpy.props.EnumProperty(name="Profil", items=[('LOW',"Low-poly (mobile)",""), ('HQ',"HQ (bake normal)","")])
    def execute(self, context):
        init_materials_if_needed()
        p = context.scene.citygen
        if self.profile == 'LOW':
            p.floor_h = 3.0; p.min_floors = 2; p.max_floors = 6
            p.win_w = 1.4; p.win_h = 1.4; p.win_spacing = 3.0
            p.win_depth = 0.04; p.lit_ratio = 0.18; p.join_windows = True
            p.roof_type = 'FLAT'; p.parapet_h = 0.2
            p.use_rect = True; p.use_L = True; p.use_U = False; p.use_T = False
            p.use_tri = False; p.use_trap = True; p.use_hex = False; p.use_circle = True; p.use_ellipse = False
            p.use_textures = True; p.tex_scale_x = 2.0; p.tex_scale_y = 2.0
            p.lot_density = 0.9
            p.skyscraper_min_floors = 12; p.skyscraper_max_floors = 20
            p.skyscraper_glass = True; p.skyscraper_roof_details = True
            p.hvac_min = 1; p.hvac_max = 3; p.ant_min = 0; p.ant_max = 2
        else:
            p.floor_h = 3.2; p.min_floors = 4; p.max_floors = 14
            p.win_w = 1.2; p.win_h = 1.6; p.win_spacing = 2.0
            p.win_depth = 0.06; p.lit_ratio = 0.25; p.join_windows = True
            p.roof_type = 'HIP'; p.parapet_h = 0.3
            p.use_rect = True; p.use_L = True; p.use_U = True; p.use_T = True
            p.use_tri = True; p.use_trap = True; p.use_hex = True; p.use_circle = True; p.use_ellipse = True
            p.use_textures = True; p.tex_scale_x = 1.2; p.tex_scale_y = 1.2
            p.lot_density = 0.8
            p.skyscraper_min_floors = 24; p.skyscraper_max_floors = 48
            p.skyscraper_glass = True; p.skyscraper_roof_details = True
            p.hvac_min = 2; p.hvac_max = 6; p.ant_min = 1; p.ant_max = 4
        self.report({'INFO'}, f"Profil appliqué: {self.profile}"); return {'FINISHED'}

class CITYGEN_OT_generate(bpy.types.Operator):
    bl_idname = "citygen.generate"; bl_label = "Générer la ville"; bl_options = {'REGISTER', 'UNDO'}
    def execute(self, context):
        init_materials_if_needed()
        p = context.scene.citygen
        if p.min_floors > p.max_floors: p.min_floors, p.max_floors = p.max_floors, p.min_floors
        build_city(p, None, force_towers=False); self.report({'INFO'}, "Ville générée"); return {'FINISHED'}

class CITYGEN_OT_generate_skyline(bpy.types.Operator):
    bl_idname = "citygen.generate_skyline"; bl_label = "Générer uniquement des tours"
    bl_description = "Skyline de gratte-ciel (hexagon/circle/ellipse)"; bl_options = {'REGISTER', 'UNDO'}
    def execute(self, context):
        init_materials_if_needed()
        p = context.scene.citygen
        build_city(p, None, force_towers=True); self.report({'INFO'}, "Skyline (tours uniquement)"); return {'FINISHED'}

class CITYGEN_OT_export_glb(bpy.types.Operator):
    bl_idname = "citygen.export_glb"; bl_label = "Export .glb"; bl_description = "Export glTF binaire (.glb)"
    def execute(self, context):
        init_materials_if_needed()
        p = context.scene.citygen; path = bpy.path.abspath(p.export_path)
        if not path.lower().endswith(".glb"): path += ".glb"
        # Nettoyage + sécurité booleans
        try:
            delete_window_prototypes()
            delete_cutters()
            targets=[]
            for name in ("CG_Roads","CG_All_Buildings","CG_All_Sidewalks"):
                o = bpy.data.objects.get(name)
                if o: targets.append(o)
            if targets: apply_boolean_modifiers(targets)
        except Exception: pass
        try:
            if not hasattr(bpy.ops.export_scene, "gltf"): bpy.ops.preferences.addon_enable(module="io_scene_gltf2")
        except Exception: pass
        added_mods = []
        if p.export_triangulate:
            targets = [o for o in bpy.context.selected_objects] if p.export_selection_only else [o for o in bpy.context.scene.objects]
            for o in targets:
                if getattr(o.data, "polygons", None):
                    m = o.modifiers.new(name="CG_Tri_Export", type='TRIANGULATE'); added_mods.append((o, m))
        try:
            bpy.ops.export_scene.gltf(filepath=path, export_format='GLB', use_selection=p.export_selection_only,
                                      export_apply=True, export_texcoords=True, export_normals=True,
                                      export_materials='EXPORT', export_yup=True, export_cameras=False,
                                      export_lights=False, export_animations=False)
        except Exception as e:
            self.report({'ERROR'}, f"Echec export: {e}"); return {'CANCELLED'}
        finally:
            for o, m in added_mods:
                try: o.modifiers.remove(m)
                except: pass
        self.report({'INFO'}, f"Exporté : {path}"); return {'FINISHED'}

# ======================
#   UI
# ======================
class CITYGEN_PT_main(bpy.types.Panel):
    bl_label = "CityGen"
    bl_idname = "CITYGEN_PT_main"
    bl_space_type = 'VIEW_3D'; bl_region_type = 'UI'; bl_category = "CityGen"
    def draw(self, context):
        col = self.layout.column(align=True)
        row = col.row(align=True)
        op = row.operator("citygen.apply_profile", text="Low-poly", icon='DECORATE_ANIMATE'); op.profile='LOW'
        op = row.operator("citygen.apply_profile", text="HQ", icon='SHADING_RENDERED'); op.profile='HQ'
        col.separator()
        row = col.row(align=True)
        row.operator("citygen.generate", icon='MOD_BUILD')
        row.operator("citygen.generate_skyline", icon='SNAP_FACE_CENTER')

class CITYGEN_PT_layout(bpy.types.Panel):
    bl_label = "Grille"
    bl_idname = "CITYGEN_PT_layout"
    bl_space_type = 'VIEW_3D'; bl_region_type = 'UI'; bl_category = "CityGen"; bl_parent_id = "CITYGEN_PT_main"
    def draw(self, context):
        p = context.scene.citygen
        col = self.layout.column(align=True)
        col.prop(p, "seed"); col.prop(p, "clear_scene")
        box = col.box()
        box.prop(p, "count_x"); box.prop(p, "count_y")
        row = box.row(align=True); row.prop(p, "lot_size"); row.prop(p, "setback")
        row = box.row(align=True); row.prop(p, "ground_size"); row.prop(p, "grid_rotation_deg")
        col.separator(); col.prop(p, "lot_density")
        col.separator(); col.label(text="Variations blocs")
        row = col.row(align=True); row.prop(p, "lot_size_variation"); row.prop(p, "row_col_jitter")
        row = col.row(align=True); row.prop(p, "merge_lots_prob"); row.prop(p, "setback_var")
        row = col.row(align=True); row.prop(p, "sidewalk_chamfer_prob"); row.prop(p, "sidewalk_chamfer_size")

class CITYGEN_PT_roads(bpy.types.Panel):
    bl_label = "Routes & Diagonales"
    bl_idname = "CITYGEN_PT_roads"
    bl_space_type = 'VIEW_3D'; bl_region_type = 'UI'; bl_category = "CityGen"; bl_parent_id = "CITYGEN_PT_main"
    def draw(self, context):
        p = context.scene.citygen; col = self.layout.column(align=True)
        row = col.row(align=True); row.prop(p, "road_w_min"); row.prop(p, "road_w_max")
        row = col.row(align=True); row.prop(p, "pedestrian_prob"); row.prop(p, "pedestrian_w")
        col.separator(); col.label(text="Diagonales")
        row = col.row(align=True); row.prop(p, "diag_count"); row.prop(p, "diag_w")
        col.prop(p, "diag_both_orient")
        col.prop(p, "diag_z_offset")
        col.prop(p, "diag_cut_expand")

class CITYGEN_PT_cutting(bpy.types.Panel):
    bl_label = "Découpes (booléens)"
    bl_idname = "CITYGEN_PT_cutting"
    bl_space_type = 'VIEW_3D'; bl_region_type = 'UI'; bl_category = "CityGen"; bl_parent_id = "CITYGEN_PT_main"
    def draw(self, context):
        p = context.scene.citygen; col = self.layout.column(align=True)
        col.prop(p, "cut_with_diagonals")
        row = col.row(align=True); row.prop(p, "cut_targets", text="Cibler")

class CITYGEN_PT_buildings(bpy.types.Panel):
    bl_label = "Bâtiments"
    bl_idname = "CITYGEN_PT_buildings"
    bl_space_type = 'VIEW_3D'; bl_region_type = 'UI'; bl_category = "CityGen"; bl_parent_id = "CITYGEN_PT_main"
    def draw(self, context):
        p = context.scene.citygen; col = self.layout.column(align=True)
        col.prop(p, "floor_h")
        row = col.row(align=True); row.prop(p, "min_floors"); row.prop(p, "max_floors")
        col.separator()
        row = col.row(align=True); row.prop(p, "win_w"); row.prop(p, "win_h")
        row = col.row(align=True); row.prop(p, "win_spacing"); row.prop(p, "win_depth")
        row = col.row(align=True); row.prop(p, "win_sill"); row.prop(p, "lit_ratio")
        col.prop(p, "join_windows")
        col.separator(); col.label(text="Formes autorisées")
        grid = col.grid_flow(columns=3, align=True)
        for prop in ("use_rect","use_L","use_U","use_T","use_tri","use_trap","use_hex","use_circle","use_ellipse"):
            grid.prop(p, prop)
        col.separator(); col.label(text="Toits")
        col.prop(p, "roof_type"); col.prop(p, "parapet_h")
        col.separator(); col.label(text="Tours (gratte-ciel)")
        row = col.row(align=True); row.prop(p, "skyscraper_min_floors"); row.prop(p, "skyscraper_max_floors")
        col.prop(p, "skyscraper_glass"); col.prop(p, "skyscraper_roof_details")
        row = col.row(align=True); row.prop(p, "hvac_min"); row.prop(p, "hvac_max")
        row = col.row(align=True); row.prop(p, "ant_min"); row.prop(p, "ant_max")
        col.prop(p, "skyscraper_add_techbox")
        row = col.row(align=True); row.prop(p, "techbox_w"); row.prop(p, "techbox_d"); row.prop(p, "techbox_h")

        # === Multi-bâtiments ===
        col.separator(); col.label(text="Multi-bâtiments par lot")
        col.prop(p, "multibuild_enable")
        row = col.row(align=True); row.prop(p, "lot_buildings_min"); row.prop(p, "lot_buildings_max")

        # === Placement ===
        col.separator(); col.label(text="Placement")
        col.prop(p, "placement_mode", expand=True)
        if p.placement_mode == 'GRID':
            row = col.row(align=True); row.prop(p, "sublot_fill"); row.prop(p, "sublot_jitter")
        else:
            row = col.row(align=True); row.prop(p, "poisson_min_radius"); row.prop(p, "poisson_max_tries")

class CITYGEN_PT_textures(bpy.types.Panel):
    bl_label = "Textures"
    bl_idname = "CITYGEN_PT_textures"
    bl_space_type = 'VIEW_3D'; bl_region_type = 'UI'; bl_category = "CityGen"; bl_parent_id = "CITYGEN_PT_main"
    def draw(self, context):
        p = context.scene.citygen; col = self.layout.column(align=True)
        col.label(text="Échelle UV façades & fenêtres")
        row = col.row(align=True); row.prop(p, "tex_scale_x"); row.prop(p, "tex_scale_y")
        col.separator(); col.label(text="Routes (aléatoire par segment)")
        col.prop(p, "road_tex_dir")
        row = col.row(align=True); row.prop(p, "road_tex_scale_x"); row.prop(p, "road_tex_scale_y")
        col.separator(); col.label(text="Trottoirs (aléatoire par lot)")
        col.prop(p, "sidewalk_tex_dir")
        row = col.row(align=True); row.prop(p, "sidewalk_tex_scale_x"); row.prop(p, "sidewalk_tex_scale_y")
        col.separator(); col.label(text="Bâtiments non tours (murs)")
        col.prop(p, "use_textures"); col.prop(p, "building_wall_tex_dir")
        col.separator(); col.label(text="Fenêtres (non tours)")
        col.prop(p, "use_window_textures"); col.prop(p, "window_tex_dir")
        col.separator(); col.label(text="Gratte-ciels")
        col.prop(p, "skyscraper_use_textures"); col.prop(p, "skyscraper_texture_dir")

class CITYGEN_PT_export(bpy.types.Panel):
    bl_label = "Export .glb"
    bl_idname = "CITYGEN_PT_export"
    bl_space_type = 'VIEW_3D'; bl_region_type = 'UI'; bl_category = "CityGen"; bl_parent_id = "CITYGEN_PT_main"
    def draw(self, context):
        p = context.scene.citygen; col = self.layout.column(align=True)
        col.prop(p, "export_path")
        row = col.row(align=True); row.prop(p, "export_selection_only"); row.prop(p, "export_triangulate")
        col.operator("citygen.export_glb", icon='EXPORT')

# ======================
#   Register
# ======================
classes = (
    CG_Props,
    CITYGEN_OT_apply_profile,
    CITYGEN_OT_generate,
    CITYGEN_OT_generate_skyline,
    CITYGEN_OT_export_glb,
    CITYGEN_PT_main,
    CITYGEN_PT_layout,
    CITYGEN_PT_roads,
    CITYGEN_PT_cutting,
    CITYGEN_PT_buildings,
    CITYGEN_PT_textures,
    CITYGEN_PT_export,
)

def register():
    for c in classes: bpy.utils.register_class(c)
    bpy.types.Scene.citygen = bpy.props.PointerProperty(type=CG_Props)

def unregister():
    del bpy.types.Scene.citygen
    for c in reversed(classes): bpy.utils.unregister_class(c)

if __name__ == "__main__":
    register()

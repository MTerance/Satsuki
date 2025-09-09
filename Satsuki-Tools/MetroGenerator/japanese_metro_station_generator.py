bl_info = {
    "name": "Japanese Metro Station Generator",
    "author": "ChatGPT",
    "version": (1, 3, 0),
    "blender": (4, 0, 0),
    "location": "View3D > N Panel > Metro JP",
    "description": "Generate Japanese-style metro stations (elevated/underground) with corridors, exits, gates, machines, screen doors, escalators, elevator, signage, props, and multi-station lines.",
    "category": "Add Mesh"
}

import bpy
from math import radians
from mathutils import Vector
import os

# ----------------------------
# Materials
# ----------------------------
def ensure_material(name, base_color=(0.8,0.8,0.8,1.0), roughness=0.6, metallic=0.0):
    mat = bpy.data.materials.get(name)
    if mat is None:
        mat = bpy.data.materials.new(name=name)
        mat.use_nodes = True
        nt = mat.node_tree
        for n in list(nt.nodes):
            nt.nodes.remove(n)
        out = nt.nodes.new("ShaderNodeOutputMaterial")
        bsdf = nt.nodes.new("ShaderNodeBsdfPrincipled")
        nt.links.new(bsdf.outputs["BSDF"], out.inputs["Surface"])
        bsdf.inputs["Base Color"].default_value = base_color
        bsdf.inputs["Roughness"].default_value = roughness
        bsdf.inputs["Metallic"].default_value = metallic
    return mat

def assign_mat(obj, mat):
    if obj and obj.type == 'MESH':
        if obj.data.materials:
            obj.data.materials[0] = mat
        else:
            obj.data.materials.append(mat)

# ----------------------------
# Primitives
# ----------------------------
def add_box(size=(1,1,1), loc=(0,0,0), name="Box"):
    bpy.ops.mesh.primitive_cube_add(size=1, location=loc)
    o = bpy.context.active_object
    o.name = name
    o.scale = (size[0]/2, size[1]/2, size[2]/2)
    bpy.ops.object.transform_apply(scale=True)
    return o

def add_plane(size=(1,1), loc=(0,0,0), rot=(0,0,0), name="Plane"):
    bpy.ops.mesh.primitive_plane_add(size=1, location=loc, rotation=rot)
    o = bpy.context.active_object
    o.name = name
    o.scale = (size[0]/2, size[1]/2, 1)
    bpy.ops.object.transform_apply(scale=True, rotation=True)
    return o

def add_cylinder(radius=0.1, depth=2.0, loc=(0,0,0), name="Cylinder"):
    bpy.ops.mesh.primitive_cylinder_add(radius=radius, depth=depth, location=loc)
    o = bpy.context.active_object
    o.name = name
    return o

def make_collection(name):
    coll = bpy.data.collections.get(name)
    if coll is None:
        coll = bpy.data.collections.new(name)
        bpy.context.scene.collection.children.link(coll)
    return coll

def link_to_collection(obj, coll):
    # Ensure object is linked only to target collection
    for c in list(obj.users_collection):
        c.objects.unlink(obj)
    coll.objects.link(obj)

# ----------------------------
# Tracks
# ----------------------------
def build_track(collection, length=40.0, gauge=1.435, sleeper_step=0.6, z_base=0.0, elevated=False):
    rail_h = 0.12
    rail_w = 0.07
    sleeper_w = 2.2
    sleeper_d = 0.18
    sleeper_h = 0.08

    # rails
    left = add_box(size=(length, rail_w, rail_h), loc=(0, -gauge/2, z_base + rail_h/2), name="Rail_L")
    right = add_box(size=(length, rail_w, rail_h), loc=(0,  gauge/2, z_base + rail_h/2), name="Rail_R")
    assign_mat(left, ensure_material("RailMetal", (0.28,0.28,0.30,1), 0.25, 0.2))
    assign_mat(right, ensure_material("RailMetal", (0.28,0.28,0.30,1), 0.25, 0.2))
    link_to_collection(left, collection); link_to_collection(right, collection)

    # sleepers
    count = int(length / sleeper_step)
    for i in range(count):
        x = -length/2 + (i+0.5)*sleeper_step
        sl = add_box(size=(sleeper_d, sleeper_w, sleeper_h), loc=(x, 0, z_base + sleeper_h/2), name=f"Sleeper_{i:03d}")
        assign_mat(sl, ensure_material("SleeperWood", (0.40,0.32,0.22,1), 0.85, 0.0))
        link_to_collection(sl, collection)

    # base
    if elevated:
        slab = add_box(size=(length, 4.0, 0.35), loc=(0, 0, z_base - 0.1), name="ViaductSlab")
        assign_mat(slab, ensure_material("Concrete", (0.75,0.75,0.78,1), 0.9, 0.0))
        link_to_collection(slab, collection)
    else:
        ballast = add_box(size=(length, 4.5, 0.5), loc=(0, 0, z_base - 0.2), name="Ballast")
        assign_mat(ballast, ensure_material("Ballast", (0.42,0.42,0.44,1), 1.0, 0.0))
        link_to_collection(ballast, collection)

# ----------------------------
# Details / Props
# ----------------------------
def add_guardrails(collection, length, platform_w, z):
    # simple posts with rails on both sides
    post_step = 3.0
    n = int(length // post_step) + 1
    for side_y in (platform_w/2 - 0.05, -platform_w/2 + 0.05):
        for i in range(n):
            x = -length/2 + i*post_step
            post = add_cylinder(radius=0.03, depth=1.0, loc=(x, side_y, z+0.5), name=f"GuardPost_{'R' if side_y>0 else 'L'}_{i:02d}")
            assign_mat(post, ensure_material("RailPost", (0.75,0.75,0.78,1), 0.3, 0.0))
            link_to_collection(post, collection)
        # top rail
        rail = add_box(size=(length, 0.03, 0.05), loc=(0, side_y, z+1.0), name=f"GuardRail_{'R' if side_y>0 else 'L'}")
        assign_mat(rail, ensure_material("RailPost", (0.75,0.75,0.78,1), 0.3, 0.0))
        link_to_collection(rail, collection)

def add_screen_doors(collection, length, platform_w, z):
    # row of thin panels along platform edge (one side)
    panel_w = 1.5
    gap = 0.1
    count = int(length // (panel_w + gap))
    start_x = - (count * (panel_w + gap)) / 2
    for i in range(count):
        x = start_x + i * (panel_w + gap) + panel_w/2
        panel = add_box(size=(panel_w, 0.1, 1.4), loc=(x, platform_w/2 - 0.25, z+0.7), name=f"PSD_{i:03d}")
        assign_mat(panel, ensure_material("PSDPanel", (0.92,0.95,0.98,1), 0.2, 0.0))
        link_to_collection(panel, collection)

def add_bench(collection, x, y, z):
    seat = add_box(size=(1.6, 0.5, 0.08), loc=(x, y, z+0.45), name="BenchSeat")
    legs = []
    for dx in (-0.6, 0.6):
        legs.append(add_box(size=(0.08, 0.4, 0.45), loc=(x+dx, y, z+0.225), name=f"BenchLeg_{'L' if dx<0 else 'R'}"))
    for o in [seat]+legs:
        assign_mat(o, ensure_material("Bench", (0.82,0.78,0.70,1), 0.6, 0.0))
        link_to_collection(o, collection)

def add_light_pole(collection, x, y, z):
    pole = add_cylinder(radius=0.04, depth=3.2, loc=(x, y, z+1.6), name="LightPole")
    lamp = add_box(size=(0.3, 0.12, 0.12), loc=(x, y, z+2.8), name="Lamp")
    for o in (pole, lamp):
        assign_mat(o, ensure_material("LightMetal", (0.75,0.75,0.78,1), 0.3, 0.0))
        link_to_collection(o, collection)

def add_trash_bin(collection, x, y, z):
    b = add_box(size=(0.4, 0.4, 0.7), loc=(x, y, z+0.35), name="TrashBin")
    assign_mat(b, ensure_material("Bin", (0.75,0.80,0.90,1), 0.4, 0.0))
    link_to_collection(b, collection)

def add_signage(collection, x, y, z, text="Station"):
    panel = add_box(size=(2.4, 0.12, 0.6), loc=(x, y, z+2.0), name=f"Sign_{text}")
    assign_mat(panel, ensure_material("SignPanel", (0.85,0.90,0.98,1), 0.4, 0.0))
    link_to_collection(panel, collection)

def add_escalators(collection, x, y, z, up=True):
    # two inclined boxes approximating escalator
    length = 4.0; width = 1.2; height = 2.2
    base = add_box(size=(length, width, 0.3), loc=(x, y, z+0.15), name=f"EscalatorBase_{'Up' if up else 'Down'}")
    slope = add_box(size=(length, width*0.9, 0.3), loc=(x+length*0.1, y, z+1.0), name=f"EscalatorSlope_{'Up' if up else 'Down'}")
    slope.rotation_euler[1] = radians(30)
    for o in (base, slope):
        assign_mat(o, ensure_material("Escalator", (0.75,0.78,0.82,1), 0.4, 0.1))
        link_to_collection(o, collection)

def add_elevator(collection, x, y, z, height=3.0):
    shaft = add_box(size=(1.8, 1.8, height), loc=(x, y, z+height/2), name="ElevatorShaft")
    cabin = add_box(size=(1.4, 1.4, 2.2), loc=(x, y, z+1.1), name="ElevatorCabin")
    for o in (shaft, cabin):
        assign_mat(o, ensure_material("Glass", (0.75,0.85,0.95,0.4), 0.05, 0.0))
        link_to_collection(o, collection)

# Ticketing
def build_ticket_gate_row(collection, count=4, spacing=1.0, loc=(0,0,0)):
    x0, y0, z0 = loc
    for i in range(count):
        x = x0 + i*spacing
        lp = add_box(size=(0.2, 0.5, 1.1), loc=(x, y0-0.3, z0+0.55), name=f"GatePostL_{i:02d}")
        rp = add_box(size=(0.2, 0.5, 1.1), loc=(x, y0+0.3, z0+0.55), name=f"GatePostR_{i:02d}")
        arm = add_box(size=(0.2, 0.6, 0.1), loc=(x, y0, z0+1.0), name=f"GateArm_{i:02d}")
        for o, col in ((lp,(0.75,0.78,0.85,1)),(rp,(0.75,0.78,0.85,1)),(arm,(0.35,0.45,0.75,1))):
            assign_mat(o, ensure_material("Gate", col, 0.4, 0.0))
            link_to_collection(o, collection)

def build_ticket_machines(collection, count=2, spacing=1.0, loc=(0,0,0)):
    x0, y0, z0 = loc
    for i in range(count):
        x = x0 + i*spacing
        body = add_box(size=(0.6, 0.5, 1.5), loc=(x, y0, z0+0.75), name=f"TicketMachine_{i:02d}")
        screen = add_box(size=(0.4, 0.05, 0.25), loc=(x, y0+0.28, z0+1.1), name=f"MachineScreen_{i:02d}")
        for o, col in ((body,(0.80,0.82,0.90,1)),(screen,(0.1,0.2,0.5,1))):
            assign_mat(o, ensure_material("Machine", col, 0.4, 0.0))
            link_to_collection(o, collection)

# ----------------------------
# Station Builders
# ----------------------------
def build_elevated_station(name="MetroJP_Elevated", platform_len=40.0, platform_w=6.0, height=6.0, with_stairs=True, align_to_active=False, detail="BASIC", add_psd=False):
    coll = make_collection(name)

    # pylons
    span = 8.0
    n = max(2, int(platform_len // span) + 1)
    for i in range(n):
        x = -platform_len/2 + i*span
        p = add_box(size=(1.2, 3.5, height), loc=(x, -platform_w/2 + 1.2, height/2), name=f"Pylon_L_{i:02d}")
        q = add_box(size=(1.2, 3.5, height), loc=(x,  platform_w/2 - 1.2, height/2), name=f"Pylon_R_{i:02d}")
        assign_mat(p, ensure_material("Concrete", (0.72,0.72,0.75,1), 0.9, 0.0))
        assign_mat(q, ensure_material("Concrete", (0.72,0.72,0.75,1), 0.9, 0.0))
        link_to_collection(p, coll); link_to_collection(q, coll)

    # deck + platform
    deck = add_box(size=(platform_len, platform_w+2.0, 0.6), loc=(0,0,height+0.3), name="Deck")
    assign_mat(deck, ensure_material("Concrete", (0.72,0.72,0.75,1), 0.9, 0.0))
    link_to_collection(deck, coll)

    platform = add_box(size=(platform_len, platform_w, 0.22), loc=(0,0,height+0.61), name="Platform")
    assign_mat(platform, ensure_material("PlatformTile", (0.92,0.92,0.95,1), 0.8, 0.0))
    link_to_collection(platform, coll)

    # tactile strips
    for side_y in (platform_w/2 - 0.3, -platform_w/2 + 0.3):
        strip = add_box(size=(platform_len, 0.4, 0.04), loc=(0, side_y, height+0.72), name=f"TactileStrip_{'R' if side_y>0 else 'L'}")
        assign_mat(strip, ensure_material("TactileYellow", (0.96,0.82,0.20,1), 0.6, 0.0))
        link_to_collection(strip, coll)

    # canopy
    roof = add_box(size=(platform_len, platform_w+1.0, 0.15), loc=(0,0,height+3.0), name="Roof")
    assign_mat(roof, ensure_material("RoofMetal", (0.70,0.75,0.80,1), 0.4, 0.1))
    link_to_collection(roof, coll)

    # tracks on deck
    build_track(coll, length=platform_len, elevated=True, z_base=height+0.4)

    # stairs block
    if with_stairs:
        stair_len = 6.0
        stair_w = 2.2
        stair_h = height
        stairs = add_box(size=(stair_len, stair_w, stair_h), loc=(platform_len/2 - 4.0, -platform_w/2 - stair_w/2 - 0.2, stair_h/2), name="StairBlock")
        assign_mat(stairs, ensure_material("Concrete", (0.72,0.72,0.75,1), 0.9, 0.0))
        link_to_collection(stairs, coll)

    # details
    if detail == "ENRICHED":
        add_guardrails(coll, platform_len, platform_w, height+0.6)
        add_signage(coll, 0, platform_w/2 + 0.8, height+0.6, text="Station")
        # benches, lights, bins every ~10m
        step = 10.0
        k = int(platform_len//step)
        for i in range(k):
            x = -platform_len/2 + (i+0.5)*step
            add_bench(coll, x, 0, height+0.61)
            add_light_pole(coll, x, -platform_w/2 - 0.6, height+0.61)
            add_trash_bin(coll, x, 0.9-platform_w/2, height+0.61)
        if add_psd:
            add_screen_doors(coll, platform_len, platform_w, height+0.61)

    if align_to_active and bpy.context.active_object:
        origin = bpy.context.active_object.location.copy()
        for obj in list(coll.objects):
            obj.location += origin

    return coll

def build_underground_station(name="MetroJP_Underground", platform_len=40.0, platform_w=6.0, depth=6.0, corridor_len=12.0, align_to_active=False, corridor_layout='I', detail="BASIC", add_psd=False):
    coll = make_collection(name)

    z0 = -depth
    # tunnel
    tunnel = add_box(size=(platform_len, platform_w+4.0, 4.5), loc=(0,0,z0-1.5), name="TunnelVolume")
    assign_mat(tunnel, ensure_material("TunnelWall", (0.42,0.42,0.45,1), 1.0, 0.0))
    link_to_collection(tunnel, coll)

    # platform
    platform = add_box(size=(platform_len, platform_w, 0.25), loc=(0,0,z0+0.125), name="Platform")
    assign_mat(platform, ensure_material("PlatformTile", (0.92,0.92,0.95,1), 0.8, 0.0))
    link_to_collection(platform, coll)

    # tactile strip
    strip = add_box(size=(platform_len, 0.4, 0.04), loc=(0, platform_w/2 - 0.3, z0+0.25), name="TactileStrip")
    assign_mat(strip, ensure_material("TactileYellow", (0.96,0.82,0.20,1), 0.6, 0.0))
    link_to_collection(strip, coll)

    # tracks
    build_track(coll, length=platform_len, elevated=False, z_base=z0-0.1)

    # Corridors layouts
    def corridor_block(x_offset, y_offset, name_prefix):
        cor = add_box(size=(corridor_len, 3.0, 2.6), loc=(x_offset, y_offset, z0+1.3), name=f"{name_prefix}_Corridor")
        assign_mat(cor, ensure_material("CorridorTile", (0.88,0.88,0.91,1), 0.9, 0.0))
        link_to_collection(cor, coll)
        shaft = add_box(size=(3.0, 3.0, depth), loc=(x_offset + corridor_len/2, y_offset, -depth/2), name=f"{name_prefix}_Shaft")
        assign_mat(shaft, ensure_material("Concrete", (0.72,0.72,0.75,1), 0.9, 0.0))
        link_to_collection(shaft, coll)
        kiosk = add_box(size=(3.2, 3.2, 2.4), loc=(x_offset + corridor_len/2, y_offset, 1.2), name=f"{name_prefix}_Entrance")
        assign_mat(kiosk, ensure_material("Kiosk", (0.78,0.82,0.90,1), 0.5, 0.0))
        link_to_collection(kiosk, coll)
        canopy = add_box(size=(3.6, 3.6, 0.12), loc=(x_offset + corridor_len/2, y_offset, 2.5), name=f"{name_prefix}_Canopy")
        assign_mat(canopy, ensure_material("RoofMetal", (0.70,0.75,0.80,1), 0.4, 0.1))
        link_to_collection(canopy, coll)
        return cor

    y_base = platform_w/2 + 1.8
    if corridor_layout == 'I':
        corridor_block(0.0, y_base, "I")
    elif corridor_layout == 'L':
        corridor_block(-platform_len*0.2, y_base, "L_Main")
        corridor_block(-platform_len*0.2 + corridor_len/2, y_base + 4.0, "L_Branch")
    elif corridor_layout == 'T':
        corridor_block(-platform_len*0.25, y_base, "T_Left")
        corridor_block( platform_len*0.25, y_base, "T_Right")

    # details
    if detail == "ENRICHED":
        add_signage(coll, 0, -platform_w/2 - 0.8, z0+0.25, text="Station")
        step = 10.0
        k = int(platform_len//step)
        for i in range(k):
            x = -platform_len/2 + (i+0.5)*step
            add_bench(coll, x, -0.8, z0+0.25)
            add_trash_bin(coll, x, -1.4, z0+0.25)
        if add_psd:
            add_screen_doors(coll, platform_len, platform_w, z0+0.25)

    if align_to_active and bpy.context.active_object:
        origin = bpy.context.active_object.location.copy()
        for obj in list(coll.objects):
            obj.location += origin

    return coll

# ----------------------------
# UI / Operators
# ----------------------------
class METROJP_Props(bpy.types.PropertyGroup):
    align_to_active: bpy.props.BoolProperty(
        name="Align to Selected",
        description="Place generated station at active object's origin (use a block from your city generator).",
        default=True
    )
    mode: bpy.props.EnumProperty(
        name="Mode",
        items=(('ELEVATED', "Elevated (Aérien)", ""), ('UNDERGROUND', "Underground (Souterrain)", "")),
        default='UNDERGROUND'
    )
    platform_len: bpy.props.FloatProperty(name="Platform Length", default=40.0, min=16.0, max=240.0)
    platform_w:   bpy.props.FloatProperty(name="Platform Width",  default=6.0,  min=4.0,  max=16.0)
    # Elevated
    viaduct_h:    bpy.props.FloatProperty(name="Viaduct Height", default=6.0,  min=3.0,  max=24.0)
    with_stairs:  bpy.props.BoolProperty(name="Add Stairs Block", default=True)
    # Underground
    depth:        bpy.props.FloatProperty(name="Depth",          default=6.0,  min=3.0,  max=30.0)
    corridor_len: bpy.props.FloatProperty(name="Corridor Length",default=12.0, min=6.0,  max=80.0)
    corridor_layout: bpy.props.EnumProperty(
        name="Corridor Layout",
        items=(('I', "I (droit)", ""), ('L', "L (branche latérale)", ""), ('T', "T (deux branches)", "")),
        default='I'
    )
    # Detail
    detail: bpy.props.EnumProperty(
        name="Detail Level",
        items=(('BASIC', "Basic", ""), ('ENRICHED', "Enriched", "")),
        default='ENRICHED'
    )
    add_psd: bpy.props.BoolProperty(name="Add Screen Doors", default=False)

    # Ticketing
    add_gates: bpy.props.BoolProperty(name="Add Ticket Gates", default=True)
    gates_count: bpy.props.IntProperty(name="Gates Count", default=4, min=1, max=12)
    add_machines: bpy.props.BoolProperty(name="Add Ticket Machines", default=True)
    machines_count: bpy.props.IntProperty(name="Machines Count", default=2, min=1, max=10)

    # Multi-station
    stations_count: bpy.props.IntProperty(name="Stations Count", default=1, min=1, max=12)
    station_spacing: bpy.props.FloatProperty(name="Station Spacing", default=120.0, min=20.0, max=1000.0)

class METROJP_OT_generate(bpy.types.Operator):
    bl_idname = "metrojp.generate"
    bl_label = "Generate Metro Station (v1.3)"
    bl_options = {'REGISTER','UNDO'}
    def execute(self, context):
        p = context.scene.metrojp
        for idx in range(p.stations_count):
            offset_x = idx * p.station_spacing
            # empty to offset origin
            empty = bpy.data.objects.new(f"StationOffset_{idx}", None)
            bpy.context.scene.collection.objects.link(empty)
            empty.location = (offset_x, 0, 0)
            bpy.context.view_layer.objects.active = empty
            if p.mode == 'ELEVATED':
                coll = build_elevated_station(platform_len=p.platform_len, platform_w=p.platform_w, height=p.viaduct_h, with_stairs=p.with_stairs, align_to_active=True, detail=p.detail, add_psd=p.add_psd)
                base_z = p.viaduct_h + 0.7
                if p.add_gates:
                    build_ticket_gate_row(coll, count=p.gates_count, spacing=1.0, loc=(0, -p.platform_w/2 - 1.0, base_z))
                if p.add_machines:
                    build_ticket_machines(coll, count=p.machines_count, spacing=1.2, loc=(-p.platform_len/4, -p.platform_w/2 - 2.0, base_z))
                # Escalators & elevator near stair block
                if p.detail == 'ENRICHED':
                    add_escalators(coll, p.platform_len/2 - 6.0, -p.platform_w/2 - 1.5, p.viaduct_h+0.2, up=True)
                    add_elevator(coll, p.platform_len/2 - 8.5, -p.platform_w/2 - 1.5, 0.0, height=p.viaduct_h+2.0)
            else:
                coll = build_underground_station(platform_len=p.platform_len, platform_w=p.platform_w, depth=p.depth, corridor_len=p.corridor_len, align_to_active=True, corridor_layout=p.corridor_layout, detail=p.detail, add_psd=p.add_psd)
                base_z = -p.depth + 1.0
                if p.add_gates:
                    build_ticket_gate_row(coll, count=p.gates_count, spacing=1.0, loc=(-p.platform_len*0.1, p.platform_w/2 + 1.2, base_z))
                if p.add_machines:
                    build_ticket_machines(coll, count=p.machines_count, spacing=1.2, loc=(-p.platform_len*0.1 - 3.0, p.platform_w/2 + 2.8, base_z))
                if p.detail == 'ENRICHED':
                    add_escalators(coll, -p.platform_len/2 + 6.0, p.platform_w/2 + 1.2, -p.depth+0.1, up=True)
                    add_elevator(coll, -p.platform_len/2 + 9.0, p.platform_w/2 + 3.6, -p.depth, height=p.depth+3.0)
        return {'FINISHED'}

class METROJP_OT_cleanup(bpy.types.Operator):
    bl_idname = "metrojp.cleanup"
    bl_label = "Cleanup Generated Stations"
    bl_options = {'REGISTER','UNDO'}
    def execute(self, context):
        for name in ("MetroJP_Elevated", "MetroJP_Underground"):
            coll = bpy.data.collections.get(name)
            if coll:
                for obj in list(coll.objects):
                    bpy.data.objects.remove(obj, do_unlink=True)
                bpy.data.collections.remove(coll, do_unlink=True)
        # also remove StationOffset empties
        for obj in list(bpy.data.objects):
            if obj.type == 'EMPTY' and obj.name.startswith("StationOffset_"):
                bpy.data.objects.remove(obj, do_unlink=True)
        self.report({'INFO'}, "Removed generated metro station collections and offsets.")
        return {'FINISHED'}

class METROJP_PT_panel(bpy.types.Panel):
    bl_label = "Japanese Metro Generator"
    bl_idname = "METROJP_PT_panel"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Metro JP"
    def draw(self, context):
        p = context.scene.metrojp
        layout = self.layout
        layout.prop(p, "align_to_active")
        layout.prop(p, "mode")
        layout.separator()
        col = layout.column(align=True)
        col.label(text="Platform")
        col.prop(p, "platform_len")
        col.prop(p, "platform_w")
        if p.mode == 'ELEVATED':
            col = layout.column(align=True); col.label(text="Elevated"); col.prop(p, "viaduct_h"); col.prop(p, "with_stairs")
        else:
            col = layout.column(align=True); col.label(text="Underground"); col.prop(p, "depth"); col.prop(p, "corridor_len"); col.prop(p, "corridor_layout")
        layout.separator()
        box = layout.box()
        box.label(text="Detailing")
        row = box.row(align=True); row.prop(p, "detail"); row.prop(p, "add_psd")
        layout.separator()
        box = layout.box()
        box.label(text="Ticketing")
        row = box.row(align=True); row.prop(p, "add_gates"); row.prop(p, "gates_count")
        row = box.row(align=True); row.prop(p, "add_machines"); row.prop(p, "machines_count")
        layout.separator()
        box = layout.box()
        box.label(text="Multi-Station")
        row = box.row(align=True); row.prop(p, "stations_count"); row.prop(p, "station_spacing")
        layout.separator()
        row = layout.row(align=True)
        row.operator("metrojp.generate", icon="OUTLINER_OB_MESH")
        row.operator("metrojp.cleanup", icon="TRASH")

classes = (METROJP_Props, METROJP_OT_generate, METROJP_OT_cleanup, METROJP_PT_panel)

def register():
    for c in classes:
        bpy.utils.register_class(c)
    bpy.types.Scene.metrojp = bpy.props.PointerProperty(type=METROJP_Props)

def unregister():
    for c in reversed(classes):
        bpy.utils.unregister_class(c)
    del bpy.types.Scene.metrojp

if __name__ == "__main__":
    register()

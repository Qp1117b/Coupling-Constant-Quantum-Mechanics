extends MeshInstance3D
class_name Bond3D

@export var atom_a: Atom3D
@export var atom_b: Atom3D
@export var bond_order: int = 1

var bond_length: float = 0.0
var coupling_strength: float = 0.0

var _flow_offset: float = 0.0
var _material: ShaderMaterial

const FLOW_SPEED: float = 1.8
const DASH_SIZE: float = 0.07
const GAP_SIZE: float = 0.05
const BOND_RADIUS: float = 0.025

func _ready():
    _setup_mesh()

func _setup_mesh():
    var cyl_mesh = CylinderMesh.new()
    cyl_mesh.top_radius = BOND_RADIUS
    cyl_mesh.bottom_radius = BOND_RADIUS
    cyl_mesh.height = 1.0
    cyl_mesh.radial_segments = 10
    self.mesh = cyl_mesh

    _material = ShaderMaterial.new()
    _material.shader = _create_shader()
    _material.set_shader_parameter("dash_size", DASH_SIZE)
    _material.set_shader_parameter("gap_size", GAP_SIZE)
    material_override = _material

func _create_shader() -> Shader:
    var s = Shader.new()
    s.code = """
shader_type spatial;

uniform vec4 albedo_color : source_color = vec4(0.7, 0.7, 0.85, 1.0);
uniform vec4 emission_color : source_color = vec4(0.3, 0.3, 0.5, 1.0);
uniform float dash_size = 0.07;
uniform float gap_size = 0.05;
uniform float flow_offset = 0.0;
uniform float emission_strength = 0.6;
uniform float bond_length = 1.0;
uniform float pulse = 0.0;

varying float v_local_y;

void vertex() {
    v_local_y = VERTEX.y;
}

void fragment() {
    float bl = max(bond_length, 0.001);
    float world_y = v_local_y * bl;
    float period = dash_size + gap_size;
    float pos = mod(world_y + flow_offset, period);

    if (pos > dash_size) {
        discard;
    }

    float t = (world_y + bl * 0.5) / bl;
    float fade = smoothstep(0.0, 0.08, t) * smoothstep(1.0, 0.92, t);

    float pulse_factor = 1.0 + pulse * 0.25 * sin(flow_offset * 6.28318);

    ALBEDO = albedo_color.rgb * fade * pulse_factor;
    EMISSION = emission_color.rgb * emission_strength * fade * pulse_factor;
}
"""
    return s

func _process(_delta):
    if is_instance_valid(atom_a) and is_instance_valid(atom_b):
        _update_geometry()

func _update_geometry():
    var pos_a = atom_a.global_position
    var pos_b = atom_b.global_position
    var midpoint = (pos_a + pos_b) / 2.0
    bond_length = pos_a.distance_to(pos_b)

    if bond_length > 0.01:
        var direction = (pos_b - pos_a) / bond_length
        var up_vec = Vector3.UP if abs(direction.y) < 0.99 else Vector3.FORWARD
        var x_axis = direction.cross(up_vec).normalized()
        var z_axis = x_axis.cross(direction).normalized()
        var bond_basis = Basis(x_axis, direction * bond_length, z_axis)
        global_transform = Transform3D(bond_basis, midpoint)

    coupling_strength = _compute_coupling()
    _update_uniforms()

func _update_uniforms():
    _material.set_shader_parameter("flow_offset", _flow_offset)
    _material.set_shader_parameter("bond_length", bond_length)
    _material.set_shader_parameter("emission_strength", 0.4 + coupling_strength * 0.6)
    _material.set_shader_parameter("pulse", coupling_strength)

    var ideal = ChemValidator.ideal_bond_length(atom_a.element_symbol, atom_b.element_symbol)
    var dev = abs(bond_length - ideal) / ideal if ideal > 0.0 else 1.0
    var quality_color = ChemValidator.get_bond_color(dev)

    match bond_order:
        2:
            _material.set_shader_parameter("albedo_color", Color(0.85, 0.65, 0.95, 1.0).lerp(quality_color, 0.5))
            _material.set_shader_parameter("emission_color", Color(0.5, 0.3, 0.8, 1.0).lerp(quality_color, 0.4))
        3:
            _material.set_shader_parameter("albedo_color", Color(0.95, 0.55, 0.75, 1.0).lerp(quality_color, 0.5))
            _material.set_shader_parameter("emission_color", Color(0.7, 0.2, 0.5, 1.0).lerp(quality_color, 0.4))
        _:
            _material.set_shader_parameter("albedo_color", quality_color)
            _material.set_shader_parameter("emission_color", quality_color * 0.5)

func _compute_coupling() -> float:
    if bond_length <= 0:
        return 0.0
    var data_a = ElementDB.get_element(atom_a.element_symbol)
    var data_b = ElementDB.get_element(atom_b.element_symbol)
    var r_a = float(data_a.get("covalent_radius_pm", 50)) / 100.0
    var r_b = float(data_b.get("covalent_radius_pm", 50)) / 100.0
    var r0 = r_a + r_b
    var t0 = 1.0
    var decay = 1.5
    return t0 * bond_order * exp(-decay * abs(bond_length - r0))

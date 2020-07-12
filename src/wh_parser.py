from typing import BinaryIO, List, Any, Callable

from wh_binary_objects import Particle, Prop
from reader import bool1, string, int2, int4, float4, read_list, assert_version, int8


def mod_vector(vector: List):
    return sum([x * x for x in vector]) ** 0.5


def parse_file(file: BinaryIO):
    file.read(8)  # FASTBIN0
    root_version = int2(file)
    if root_version != 23 and root_version != 24:
        raise Exception('Only versions 23 and 24 of root are supported')

    buildings = read_building_list(file)
    read_building_list_far(file)
    read_capture_location_set(file)
    read_ef_line_list(file)
    read_go_outlines(file)
    read_non_terrain_outlines(file)
    read_zones_template_list(file)
    read_prefab_instance_list(file)
    read_bmd_outline_list(file)
    read_terrain_outlines(file)
    read_lite_building_outlines(file)
    read_camera_zones(file)
    read_civilian_deployment_list(file)
    read_civilian_shelter_list(file)
    props = read_prop_list(file)
    particles = read_particle_list(file)

    # rest of file

    return buildings


def read_building_list(file: BinaryIO):
    assert_version('BATTLEFIELD_BUILDING_LIST', 1, int2(file))
    return read_list(file, read_building_instance)


def read_building_instance(file: BinaryIO):
    instance = {}
    assert_version('BUILDING', 8, int2(file))
    file.read(4)
    instance["model_name"] = string(file)
    instance["object_relation1"] = string(file)

    coordinates = read_coordinates(file)
    translation = read_translation(file)

    scales = get_scale(coordinates)
    unscale(coordinates, scales)

    instance["position"] = translation
    instance["scale"] = scales
    instance["coordinates"] = coordinates

    file.read(18)
    instance["object_relation2"] = string(file)

    return instance


def read_building_list_far(file: BinaryIO):
    int2(file)  # version
    assert int4(file) == 0, "BATTLEFIELD_BUILDING_LIST_FAR has items"


def read_capture_location_set(file: BinaryIO):
    int2(file)  # version
    assert int4(file) == 0, "CAPTURE_LOCATION_SET has items"


def read_ef_line_list(file: BinaryIO):
    assert int4(file) == 0, "EF_LINE_LIST has items"


def read_go_outlines(file: BinaryIO):
    assert int4(file) == 0, "GO_OUTLINES has items"


def read_non_terrain_outlines(file: BinaryIO):
    assert int4(file) == 0, "NON_TERRAIN_OUTLINES has items"


def read_zones_template_list(file: BinaryIO):
    int2(file)  # version
    assert int4(file) == 0, "ZONES_TEMPLATE_LIST has items"


def read_prefab_instance_list(file: BinaryIO):
    int2(file)  # version
    assert int4(file) == 0, "PREFAB_INSTANCE_LIST has items"


def read_bmd_outline_list(file: BinaryIO):
    int2(file)  # version
    assert int4(file) == 0, "BMD_OUTLINE_LIST has items"


def read_particle_list(file: BinaryIO):
    assert_version('PARTICLE_EMITTER_LIST', 1, int2(file))
    return read_list(file, read_particle_instance)


def read_terrain_outlines(file: BinaryIO):
    assert int4(file) == 0, "TERRAIN_OUTLINES has items"


def read_lite_building_outlines(file: BinaryIO):
    assert int4(file) == 0, "LITE_BUILDING_OUTLINES has items"


def read_camera_zones(file: BinaryIO):
    int2(file)  # version
    assert int4(file) == 0, "CAMERA_ZONES has items"


def read_civilian_deployment_list(file: BinaryIO):
    assert int4(file) == 0, "CIVILIAN_DEPLOYMENT_LIST has items"


def read_civilian_shelter_list(file: BinaryIO):
    assert int4(file) == 0, "CIVILIAN_SHELTER_LIST has items"


def read_prop_list(file: BinaryIO):
    assert_version('PROP_LIST', 2, int2(file))
    keys = read_list(file, read_prop_key_instance)
    props = read_list(file, read_prop_prop_instance)
    result = {}
    for key in keys:
        result[key] = []
    for prop in props:
        key = keys[prop.key_index]
        result[key].append(prop)
    return result


def read_prop_key_instance(file: BinaryIO):
    return string(file)


def read_prop_prop_instance(file: BinaryIO):
    assert_version('PROP', 15, int2(file))

    prop = Prop()
    prop.key_index = int2(file)
    file.read(2)  # TODO

    prop.coordinates = read_coordinates(file)
    prop.translation = read_translation(file)

    prop.scale = get_scale(prop.coordinates)
    unscale(prop.coordinates, prop.scale)

    prop.decal = bool1(file)
    file.read(7)  # flags from logic_decal to animated
    prop.decal_parallax_scale = float4(file)
    prop.decal_tiling = float4(file)
    bool1(file)

    prop.flags = read_flags(file)

    bool1(file)
    bool1(file)
    bool1(file)
    bool1(file)
    prop.height_mode = string(file)
    print(int8(file))
    bool1(file)
    bool1(file)

    return prop


def read_particle_instance(file: BinaryIO):
    particle = Particle()
    version = int2(file)
    assert_version('PARTICLE_EMITTER', 5, version)
    particle.model_name = string(file)

    particle.coordinates = read_coordinates(file)
    particle.position = read_translation(file)

    file.read(6)  # to be translated

    particle.flags = read_flags(file)
    particle.object_relation = string(file)
    file.read(4)
    particle.autoplay = bool1(file)
    particle.visible_in_shroud = bool1(file)
    return particle


def read_flags(file: BinaryIO):
    assert_version('PARTICLE_EMITTER->flags', 2, int2(file))
    return {
        'allow_in_outfield': bool1(file),
        'clamp_to_surface': bool1(file),
        'clamp_to_water_surface': bool1(file),
        'spring': bool1(file),
        'summer': bool1(file),
        'autumn': bool1(file),
        'winter': bool1(file)
    }


def read_coordinates(file: BinaryIO):
    coordinates = [[None] * 3 for i in range(3)]
    for i in range(9):
        coordinates[i // 3][i % 3] = float4(file)
    return coordinates


def read_translation(file: BinaryIO):
    translation = [None] * 3
    for i in range(3):
        translation[i] = float4(file)
    return translation


def get_scale(coordinates):
    return list(map(mod_vector, coordinates))


def unscale(coordinates, scales):
    for i in range(3):
        for j in range(3):
            coordinates[i][j] /= scales[i]

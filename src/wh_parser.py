from typing import BinaryIO, List, Any, Callable

from wh_binary_objects import Particle
from reader import bool1, string, int2, int4, float4, read_list, assert_version


def mod_vector(vector: List):
    return sum([x * x for x in vector]) ** 0.5


def parse_file(file: BinaryIO):
    file.read(8)    # FASTBIN0
    assert_version('Root serializer', 23, int2(file))

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
    read_prop_list(file)
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

    coordinates = [[None] * 3 for i in range(3)]
    for i in range(9):
        coordinates[i // 3][i % 3] = float4(file)

    translation = [None] * 3
    for i in range(3):
        translation[i] = float4(file)

    scales = list(map(mod_vector, coordinates))
    for i in range(3):
        scale = scales[i]
        for j in range(3):
            coordinates[i][j] /= scale

    instance["position"] = translation
    instance["scale"] = scales
    instance["coordinates"] = coordinates

    file.read(18)
    instance["object_relation2"] = string(file)

    return instance


def read_building_list_far(file: BinaryIO):
    int2(file) # version
    assert int4(file) == 0, "BATTLEFIELD_BUILDING_LIST_FAR has items"


def read_capture_location_set(file: BinaryIO):
    int2(file) # version
    assert int4(file) == 0, "CAPTURE_LOCATION_SET has items"


def read_ef_line_list(file: BinaryIO):
    assert int4(file) == 0, "EF_LINE_LIST has items"


def read_go_outlines(file: BinaryIO):
    assert int4(file) == 0, "GO_OUTLINES has items"


def read_non_terrain_outlines(file: BinaryIO):
    assert int4(file) == 0, "NON_TERRAIN_OUTLINES has items"


def read_zones_template_list(file: BinaryIO):
    int2(file) # version
    assert int4(file) == 0, "ZONES_TEMPLATE_LIST has items"


def read_prefab_instance_list(file: BinaryIO):
    int2(file) # version
    assert int4(file) == 0, "PREFAB_INSTANCE_LIST has items"


def read_bmd_outline_list(file: BinaryIO):
    int2(file) # version
    assert int4(file) == 0, "BMD_OUTLINE_LIST has items"


def read_particle_list(file: BinaryIO):
    assert_version('PARTICLE_EMITTER_LIST', 1, int2(file))
    return read_list(file, read_particle_instance)


def read_terrain_outlines(file: BinaryIO):
    assert int4(file) == 0, "TERRAIN_OUTLINES has items"


def read_lite_building_outlines(file: BinaryIO):
    assert int4(file) == 0, "LITE_BUILDING_OUTLINES has items"


def read_camera_zones(file: BinaryIO):
    int2(file) # version
    assert int4(file) == 0, "CAMERA_ZONES has items"


def read_civilian_deployment_list(file: BinaryIO):
    assert int4(file) == 0, "CIVILIAN_DEPLOYMENT_LIST has items"


def read_civilian_shelter_list(file: BinaryIO):
    assert int4(file) == 0, "CIVILIAN_SHELTER_LIST has items"


def read_prop_list(file: BinaryIO):
    assert_version('PROP_LIST', 2, int2(file))
    keys = read_list(file, read_prop_key_instance)
    props = read_list(file, read_prop_prop_instance)


def read_prop_key_instance(file: BinaryIO):
    pass


def read_prop_prop_instance(file: BinaryIO):
    pass


def read_particle_instance(file: BinaryIO):
    particle = Particle()
    version = int2(file)
    assert_version('PARTICLE_EMITTER', 5, version)
    particle.model_name = string(file)

    coordinates = [[None] * 3 for i in range(3)]
    for i in range(9):
        coordinates[i // 3][i % 3] = float4(file)

    particle.coordinates = coordinates
    particle.position = list(map(lambda i: float4(file), range(3)))

    file.read(6)  # to be translated

    version = int2(file)
    assert_version('PARTICLE_EMITTER->flags', 2, version)
    particle.flags = {
        'allow_in_outfield': bool1(file),
        'clamp_to_surface': bool1(file),
        'clamp_to_water_surface': bool1(file),
        'spring': bool1(file),
        'summer': bool1(file),
        'autumn': bool1(file),
        'winter': bool1(file)
    }
    particle.object_relation = string(file)
    file.read(4)
    particle.autoplay = bool1(file)
    particle.visible_in_shroud = bool1(file)
    return particle

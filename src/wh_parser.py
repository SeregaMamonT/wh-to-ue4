import struct
from typing import BinaryIO, List

from wh_binary_objects import Particle


def bool1(file: BinaryIO):
    return struct.unpack('?', file.read(1))[0]


def int2(file: BinaryIO):
    return struct.unpack('h', file.read(2))[0]


def int4(file: BinaryIO):
    return struct.unpack('i', file.read(4))[0]


def int8(file: BinaryIO):
    return struct.unpack('Q', file.read(8))[0]


def float4(file: BinaryIO):
    return struct.unpack('f', file.read(4))[0]


def string(file: BinaryIO):
    length = int2(file)
    return file.read(length).decode()


def mod_vector(vector: List):
    return sum([x * x for x in vector]) ** 0.5


def parse_file(file: BinaryIO):
    # FASTBIN0
    buf = file.read(8)
    version = int2(file)
    assert version == 23, "Root serializer version should be 23 but found " + str(version)

    # READ PREFABS
    version = int2(file)
    assert version == 1, "PREFAB_INSTANCE_LIST serializer version should be 1 but found " + str(version)

    mesh_count = int4(file)
    # file.read(2)

    mesh_instances = list(map(lambda _: read_mesh_instance(file), range(mesh_count)))

    file.read(74)

    # READ PARTICLES
    version = int2(file)
    assert_version('PARTICLE_EMITTER_LIST', 1, version)

    particle_count = int4(file)
    particle_instances = list(map(lambda _: read_particle_instance(file), range(particle_count)))
    print(particle_instances)

    return mesh_instances


def read_mesh_instance(file: BinaryIO):
    instance = {}
    version = int2(file)
    assert version == 8, "PREFAB_INSTANCE serializer version should be 1 but found " + str(version)
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
    flags = {
        'allow_in_outfield': bool1(file),
        'clamp_to_surface': bool1(file),
        'clamp_to_water_surface': bool1(file),
        'spring': bool1(file),
        'summer': bool1(file),
        'autumn': bool1(file),
        'winter': bool1(file)
    }
    particle.flags = flags
    particle.object_relation = string(file)
    file.read(4)
    particle.autoplay = bool1(file)
    particle.visible_in_shroud = bool1(file)
    return particle


def assert_version(name, expected, actual):
    assert actual == expected, "{0} serializer version should be {1} but found {2}".format(name, expected, actual)

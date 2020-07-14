from typing import BinaryIO

from reader import bool1, string, int1, int2, int4, float4, read_list, assert_version, int8, read_coordinates, \
    read_translation, get_scale, unscale, read_flags

from wh_binary_objects import Particle

def read_particle_list(file: BinaryIO):
    assert_version('PARTICLE_EMITTER_LIST', 1, int2(file))
    return read_list(file, read_particle_instance)


def read_particle_instance(file: BinaryIO):
    particle = Particle()
    version = int2(file)
    # print('Version: ', version)
    # assert_version('PARTICLE_EMITTER', 5, version)
    particle.model_name = string(file)
    # print('Particle name: ', particle.model_name)

    particle.coordinates = read_coordinates(file)
    # print(particle.coordinates)
    particle.position = read_translation(file)
    # print(particle.position)
    file.read(6)  # to be translated

    particle.flags = read_flags(file)
    # print(particle.flags)
    particle.object_relation = string(file)
    # print(particle.object_relation)
    if (version == 5):
        file.read(4)
        particle.autoplay = bool1(file)
        # print('Autoplay: ', particle.autoplay)
        particle.visible_in_shroud = bool1(file)
    elif (version == 6):
        file.read(8)
        particle.autoplay = bool1(file)
        # print('Autoplay: ', particle.autoplay)
        particle.visible_in_shroud = bool1(file)
    return particle
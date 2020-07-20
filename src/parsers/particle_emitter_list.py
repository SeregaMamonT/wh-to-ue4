from typing import BinaryIO

from reader import bool1, string, int1, int2, int4, float4, read_list, assert_version, int8, read_transform_4_x_3, read_flags

from wh_binary_objects import Particle


def read_particle_instance_v5(file):
    particle = Particle()
    particle.model_name = string(file)
    particle.transform = read_transform_4_x_3(file)
    file.read(6)  # to be translated
    particle.flags = read_flags(file)
    particle.object_relation = string(file)

    file.read(4)
    particle.autoplay = bool1(file)
    particle.visible_in_shroud = bool1(file)

    return particle


def read_particle_instance_v6(file):
    particle = Particle()
    particle.model_name = string(file)
    particle.transform = [[None] * 3 for i in range(4)]
    for i in range(12):
        particle.transform[i // 3][i % 3] = float4(file)
    file.read(6)  # to be translated
    particle.flags = read_flags(file)
    particle.object_relation = string(file)
    file.read(8)
    particle.autoplay = bool1(file)
    particle.visible_in_shroud = bool1(file)

    return particle

version_readers = {
    5: read_particle_instance_v5,
    6: read_particle_instance_v6,
}


def get_version_reader(version):
    if version in version_readers:
        return version_readers[version]
    else:
        raise Exception('Unsupported particle version: ' + str(version))



def read_particle_list(file: BinaryIO):
    version = int2(file)  # version
    amount = int4(file)
    particle_list = []
    for i in range(amount):
        particle_version = int2(file)
        particle_list.append(get_version_reader(particle_version)(file))

    return particle_list
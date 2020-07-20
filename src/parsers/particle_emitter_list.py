from typing import BinaryIO

from reader import bool1, string, int1, int2, int4, float4, read_list, assert_version, int8, read_transform_n_x_m

from wh_binary_objects import Particle

from version_holder import VersionHolder


def read_particle_list(file: BinaryIO):
    assert_version('PARTICLE_EMITTER_LIST', 1, int2(file))
    return read_list(file, read_particle)


def read_particle(file):
    particle_version = int2(file)
    return particle_versions.get_reader(particle_version)(file)


def read_particle_instance_v5(file):
    particle = read_particle_instnace_common(file)
    particle.pdlc_mask = int4(file)
    particle.autoplay = bool1(file)
    particle.visible_in_shroud = bool1(file)

    return particle


def read_particle_instance_v6(file):
    particle = read_particle_instnace_common(file)
    particle.pdlc_mask = int8(file)
    particle.autoplay = bool1(file)
    particle.visible_in_shroud = bool1(file)

    return particle


def read_particle_instnace_common(file):
    particle = Particle()
    particle.model_name = string(file)
    particle.transform = read_transform_n_x_m(file, 4, 3)
    # not 100 sure about order if particle crash it would be probably here
    particle.emission_rate = float4(file)
    particle.instance_name = string(file)
    particle.flags = read_particle_flags(file)
    particle.object_relation = string(file)

    return particle


def read_particle_flags(file):
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


particle_versions = VersionHolder('Particle', {
    5: read_particle_instance_v5,
    6: read_particle_instance_v6,
})

from typing import BinaryIO

from reader import bool1, string, int1, int2, int4, float4, read_list, assert_version, int8, read_coordinates, \
    read_translation, get_scale, unscale


def read_point_light_v5(file):
    position = (float4(file), float4(file), float4(file))
    radius = float4(file)
    colour = (float4(file), float4(file), float4(file))
    colour_scale = float4(file)
    animation_type = int1(file)
    params = (float4(file), float4(file))
    # animation_type = float4(file)
    colour_min = float4(file)
    random_offset = float4(file)
    falloff_type = string(file)
    lf_relative = bool1(file)
    height_mode = string(file)
    light_probes_only = bool1(file)
    pdlc_mask = int4(file)

def read_point_light_v6(file):
    position = (float4(file), float4(file), float4(file))
    radius = float4(file)
    colour = (float4(file), float4(file), float4(file))
    colour_scale = float4(file)
    animation_type = int1(file)
    params = (float4(file), float4(file))
    # animation_type = float4(file)
    colour_min = float4(file)
    random_offset = float4(file)
    falloff_type = string(file)
    lf_relative = bool1(file)
    height_mode = string(file)
    light_probes_only = bool1(file)
    pdlc_mask = int8(file)


version_readers = {
    5: read_point_light_v5,
    6: read_point_light_v6,
}


def get_version_reader(version):
    if version in version_readers:
        return version_readers[version]
    else:
        raise Exception('Unsupported point light version: ' + str(version))


def read_point_light_list(file: BinaryIO):
    version = int2(file)  # version
    point_lights = int4(file)
    # print("Point lights: ", version, point_lights)
    for i in range(point_lights):
        point_light_version = int2(file)
        get_version_reader(point_light_version)(file)
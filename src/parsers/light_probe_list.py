from typing import BinaryIO

from reader import bool1, string, int1, int2, int4, float4, read_list, assert_version, int8, read_coordinates, \
    read_translation, get_scale, unscale

from wh_binary_objects import LightProbe



def read_light_probe(file):
    light_probe = LightProbe()
    light_probe.position = (float4(file), float4(file), float4(file))
    light_probe.radius = float4(file)
    light_probe.is_primary = bool1(file)
    light_probe.height_mode = string(file)

    return light_probe


def read_light_probe_list(file: BinaryIO):
    version = int2(file)  # version
    amount = int4(file)
    light_probe_list = []
    for i in range(amount):
        point_light_version = int2(file)
        light_probe_list.append(read_light_probe(file))

    return light_probe_list

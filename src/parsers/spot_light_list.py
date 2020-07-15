from typing import BinaryIO

from reader import bool1, string, int1, int2, int4, float4, read_list, assert_version, int8, read_coordinates, \
    read_translation, get_scale, unscale

from wh_binary_objects import SpotLight


def read_spot_light_v5(file):
    spot_light = SpotLight()
    spot_light.position = (float4(file), float4(file), float4(file))
    spot_light.end = (float4(file), float4(file), float4(file), float4(file))
    spot_light.length = float4(file)
    spot_light.inner_angle = float4(file)
    spot_light.outer_angle = float4(file)
    spot_light.colour = (float4(file), float4(file), float4(file))
    spot_light.falloff = float4(file)
    spot_light.gobo = string(file)
    spot_light.flags = {}
    spot_light.flags["volumetric"] = bool1(file)
    spot_light.height_mode = string(file)
    spot_light.pdlc_mask = int4(file)

    return spot_light


def read_spot_light_v6(file):
    spot_light = SpotLight()
    spot_light.position = (float4(file), float4(file), float4(file))
    spot_light.end = (float4(file), float4(file), float4(file), float4(file))
    spot_light.length = float4(file)
    spot_light.inner_angle = float4(file)
    spot_light.outer_angle = float4(file)
    spot_light.colour = (float4(file), float4(file), float4(file))
    spot_light.falloff = float4(file)
    spot_light.gobo = string(file)
    spot_light.flags = {}
    spot_light.flags["volumetric"] = bool1(file)
    spot_light.height_mode = string(file)
    spot_light.pdlc_mask = int8(file)

    return spot_light


version_readers = {
    5: read_spot_light_v5,
    6: read_spot_light_v6,
}


def get_version_reader(version):
    if version in version_readers:
        return version_readers[version]
    else:
        raise Exception('Unsupported spot light version: ' + str(version))


def read_spot_light_list(file: BinaryIO):
    version = int2(file)  # version
    spot_lights = int4(file)
    spot_lights_list = []
    # print("Spot lights: ", version, spot_lights)
    for i in range(spot_lights):
        spot_light_version = int2(file)
        spot_lights_list.append(get_version_reader(spot_light_version)(file))

    return spot_lights_list

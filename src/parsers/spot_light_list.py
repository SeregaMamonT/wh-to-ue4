from typing import BinaryIO

from reader import bool1, string, int1, int2, int4, float4, read_list, assert_version, int8, read_coordinates, \
    read_translation, get_scale, unscale


def read_spot_light_v5(file):
    position = (float4(file), float4(file), float4(file))
    end = (float4(file), float4(file), float4(file), float4(file))
    length = float4(file)
    inner_angle = float4(file)
    outer_angle = float4(file)
    colour = (float4(file), float4(file), float4(file))
    falloff = float4(file)
    gobo = string(file)
    volumetric = bool1(file)
    height_mode = string(file)
    pdlc_mask = int4(file)
    # print(position, gobo, pdlc_mask)


def read_spot_light_v6(file):
    position = (float4(file), float4(file), float4(file))
    end = (float4(file), float4(file), float4(file), float4(file))
    length = float4(file)
    inner_angle = float4(file)
    outer_angle = float4(file)
    colour = (float4(file), float4(file), float4(file))
    falloff = float4(file)
    gobo = string(file)
    volumetric = bool1(file)
    height_mode = string(file)
    pdlc_mask = int8(file)
    # print(position, gobo, pdlc_mask)



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
    # print("Spot lights: ", version, spot_lights)
    for i in range(spot_lights):
        spot_light_version = int2(file)
        get_version_reader(spot_light_version)(file)

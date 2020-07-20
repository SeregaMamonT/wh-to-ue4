from typing import BinaryIO

from reader import bool1, string, int1, int2, int4, float4, read_list, assert_version, int8

from wh_binary_objects import SpotLight, ColourRGB

from wh_common_objects import Point3D

from version_holder import VersionHolder


def read_spot_light_list(file: BinaryIO):
    assert_version('SPOT_LIGHT_LIST', 1, int2(file))
    return read_list(file, read_spot_light)


def read_spot_light(file):
    spot_light_version = int2(file)
    return spot_light_versions.get_reader(spot_light_version)(file)


def read_spot_light_v5(file):
    spot_light = read_spot_light_common(file)
    spot_light.pdlc_mask = int4(file)

    return spot_light


def read_spot_light_v6(file):
    spot_light = read_spot_light_common(file)

    return spot_light


def read_spot_light_common(file):
    spot_light = SpotLight()
    spot_light.position = Point3D(float4(file), float4(file), float4(file))
    spot_light.end = (float4(file), float4(file), float4(file), float4(file))
    spot_light.length = float4(file)
    spot_light.inner_angle = float4(file)
    spot_light.outer_angle = float4(file)
    spot_light.colour = ColourRGB(float4(file), float4(file), float4(file))
    spot_light.falloff = float4(file)
    spot_light.gobo = string(file)
    spot_light.flags = {"volumetric": bool1(file)}
    spot_light.height_mode = string(file)

    return spot_light


spot_light_versions = VersionHolder('Spot light', {
    5: read_spot_light_v5,
    6: read_spot_light_v6,
})
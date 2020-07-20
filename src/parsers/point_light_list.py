from typing import BinaryIO

from reader import bool1, string, int1, int2, int4, float4, read_list, assert_version, int8

from wh_binary_objects import PointLight, ColourRGB

from wh_common_objects import Point3D

from version_holder import VersionHolder


def read_point_light_list(file: BinaryIO):
    assert_version('POINT_LIGHT_LIST', 1, int2(file))
    return read_list(file, read_point_light)


def read_point_light(file):
    point_light_version = int2(file)
    return point_light_versions.get_reader(point_light_version)(file)


def read_point_light_v4(file):
    point_light = read_point_light_common(file)
    # in all files it is in1 -4
    file.read(1)
    point_light.height_mode = string(file)
    # in all files it is 0
    file.read(1)
    point_light.pdlc_mask = int4(file)

    return point_light


def read_point_light_v5(file):
    point_light = read_point_light_common(file)
    point_light.flags = {"lf_relative": bool1(file)}
    point_light.height_mode = string(file)
    point_light.flags["light_probes_only"] = bool1(file)
    point_light.pdlc_mask = int4(file)

    return point_light


def read_point_light_v6(file):
    point_light = read_point_light_common(file)
    point_light.flags = {"lf_relative": bool1(file)}
    point_light.height_mode = string(file)
    point_light.flags["light_probes_only"] = bool1(file)
    point_light.pdlc_mask = int8(file)

    return point_light


def read_point_light_common(file):
    point_light = PointLight()
    point_light.position = Point3D(float4(file), float4(file), float4(file))
    point_light.radius = float4(file)
    point_light.colour = ColourRGB(float4(file), float4(file), float4(file))
    point_light.colour_scale = float4(file)
    point_light.animation_type = int1(file)
    point_light.params = (float4(file), float4(file))
    point_light.colour_min = float4(file)
    point_light.random_offset = float4(file)
    point_light.falloff_type = string(file)

    return point_light


point_light_versions = VersionHolder('Point light', {
    4: read_point_light_v4,
    5: read_point_light_v5,
    6: read_point_light_v6,
})




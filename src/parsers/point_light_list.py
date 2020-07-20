from typing import BinaryIO

from reader import bool1, string, int1, int2, int4, float4, read_list, assert_version, int8

from wh_binary_objects import PointLight, ColourRGB

from wh_common_objects import Point3D

def read_point_light_v4(file):
    point_light = PointLight()
    point_light.position = (float4(file), float4(file), float4(file))
    point_light.radius = float4(file)
    point_light.colour = (float4(file), float4(file), float4(file))
    point_light.colour_scale = float4(file)
    point_light.animation_type = int1(file)
    point_light.params = (float4(file), float4(file))
    point_light.colour_min = float4(file)
    point_light.random_offset = float4(file)
    point_light.falloff_type = string(file)

    # in all files it is in1 -4
    file.read(1)
    point_light.height_mode = string(file)

    # in all files it is 0
    file.read(1)
    point_light.pdlc_mask = int4(file)

    return point_light


def read_point_light_v5(file):
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
    point_light.flags = {}
    point_light.flags["lf_relative"] = bool1(file)
    point_light.height_mode = string(file)
    point_light.flags["light_probes_only"] = bool1(file)
    point_light.pdlc_mask = int4(file)
    return point_light


def read_point_light_v6(file):
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
    point_light.flags = {}
    point_light.flags["lf_relative"] = bool1(file)
    point_light.height_mode = string(file)
    point_light.flags["light_probes_only"] = bool1(file)
    point_light.pdlc_mask = int8(file)
    return point_light


version_readers = {
    4: read_point_light_v4,
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
    point_lights_list = []
    # print("Point lights: ", version, point_lights)
    for i in range(point_lights):
        point_light_version = int2(file)
        point_lights_list.append(get_version_reader(point_light_version)(file))
    return point_lights_list

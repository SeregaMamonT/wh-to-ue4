from typing import BinaryIO

from reader import bool1, string, int1, int2, int4, float4, read_list, assert_version, int8

from wh_binary_objects import LightProbe

from wh_common_objects import Point3D

from version_holder import VersionHolder


def read_light_probe_list(file: BinaryIO):
    assert_version('LIGHT_PROBE_LIST', 1, int2(file))
    return read_list(file, read_light_probe)


def read_light_probe(file):
    light_probe_version = int2(file)
    return light_probe_versions.get_reader(light_probe_version)(file)


def read_light_probe_v2(file):
    light_probe = LightProbe()
    light_probe.position = Point3D(float4(file), float4(file), float4(file))
    light_probe.radius = float4(file)
    light_probe.is_primary = bool1(file)
    light_probe.height_mode = string(file)

    return light_probe


light_probe_versions = VersionHolder('Light probe', {
    2: read_light_probe_v2,
})

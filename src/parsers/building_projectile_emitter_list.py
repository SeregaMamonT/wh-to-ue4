from typing import BinaryIO

from reader import bool1, string, int1, int2, int4, float4, read_list, assert_version, int8

from wh_binary_objects import BuildingProjectileEmitter
from wh_common_objects import Point3D

from version_holder import VersionHolder


def read_building_projectile_emitter_list(file: BinaryIO):
    assert_version('BUILDING_PROJECTILE_EMITTER_LIST', 1, int2(file))
    return read_list(file, read_building_projectile_emitter)


def read_building_projectile_emitter(file):
    building_projectile_emitter_version = int2(file)
    return building_projectile_emitter_versions.get_reader(building_projectile_emitter_version)(file)


def read_building_projectile_emitter_v2(file):
    building_projectile_emitter = BuildingProjectileEmitter()
    building_projectile_emitter.position = Point3D(float4(file), float4(file), float4(file))
    building_projectile_emitter.direction = (float4(file), float4(file), float4(file))
    # print(building_projectile_emitter.direction)
    building_projectile_emitter.building_index = int4(file)
    building_projectile_emitter.height_mode = string(file)

    return building_projectile_emitter


building_projectile_emitter_versions = VersionHolder('Building projectile emitter', {
    2: read_building_projectile_emitter_v2,
})



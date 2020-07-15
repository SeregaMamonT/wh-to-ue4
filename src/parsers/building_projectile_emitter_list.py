from typing import BinaryIO

from reader import bool1, string, int1, int2, int4, float4, read_list, assert_version, int8, read_coordinates, \
    read_translation, get_scale, unscale


from wh_binary_objects import BuildingProjectileEmitter


def read_building_projectile_emitter(file):
    building_projectile_emitter = BuildingProjectileEmitter()
    building_projectile_emitter.position = (float4(file), float4(file), float4(file))
    building_projectile_emitter.direction = (float4(file), float4(file), float4(file))
    building_projectile_emitter.building_index = int4(file)
    building_projectile_emitter.height_mode = string(file)

    return building_projectile_emitter


def read_building_projectile_emitter_list(file: BinaryIO):
    version = int2(file)  # version
    amount = int4(file)
    building_projectile_emitter_list = []
    for i in range(amount):
        building_projectile_emitter_version = int2(file)
        building_projectile_emitter_list.append(read_building_projectile_emitter(file))

    return building_projectile_emitter_list
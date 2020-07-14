from typing import BinaryIO

from reader import bool1, string, int1, int2, int4, float4, read_list, assert_version, int8, read_coordinates, \
    read_translation, get_scale, unscale


def read_building_projectile_emitter_list(file: BinaryIO):
    version = int2(file)  # version
    amount = int4(file)
    # print('projectile emitter: ', version, amount)
    for i in range(amount):
        building_projectile_emitter_version = int2(file)
        position = (float4(file), float4(file), float4(file))
        direction = (float4(file), float4(file), float4(file))
        building_index = int4(file)
        height_mode = string(file)
        # print(building_projectile_emitter_version, position, direction,building_index,height_mode)
    # assert int4(file) == 0, "BUILDING_PROJECTILE_EMITTER_LIST has items"
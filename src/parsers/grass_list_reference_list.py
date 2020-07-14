from typing import BinaryIO

from reader import bool1, string, int1, int2, int4, float4, read_list, assert_version, int8, read_coordinates, \
    read_translation, get_scale, unscale


def read_grass_list_reference_list(file: BinaryIO):
    # assert_version('Vegetation', 2, int2(file))
    tree_list = int4(file)
    print('Amount: ', tree_list)
    for i in range(tree_list):
        another_serializer = int2(file)
        key = string(file)
        print('Name:', key)
        amount = int4(file)
        print('Amount: ', amount)
        for j in range(amount):
            x = float4(file)
            y = float4(file)
            z = float4(file)
            scale = float4(file)
            is_freeform = bool1(file)
            # print(x, y, z, scale, is_freeform)
    vegetation = []

    # int2(file)  # version
    # assert int4(file) == 0, "GRASS_LIST_REFERENCE_LIST has items"
from typing import BinaryIO

from reader import bool1, string, int1, int2, int4, float4, read_list, assert_version, int8, get_scale, \
    read_transform_n_x_m

from wh_binary_objects import PrefabInstance, Point2D


def read_prefab_instance(file):
    prefab_instance = PrefabInstance()
    prefab_version = int2(file)
    prefab_instance.name = string(file)
    prefab_instance.transformation = read_transform_n_x_m(file, 4, 4)
    # print(prefab_instance.transform)
    property_overrides = int4(file)
    # print('Property overrides: ', property_overrides)
    for j in range(property_overrides):
        file.read(2)
        property_value = string(file)
        # print(property_value)
        file.read(14)
    file.read(7)
    prefab_instance.height_mode = string(file)

    return prefab_instance


def read_prefab_instance_list(file: BinaryIO):
    version = int2(file)  # version
    prefab_amount = int4(file)
    prefab_instance_list = []
    for i in range(prefab_amount):
        prefab_instance_list.append(read_prefab_instance(file))

    return prefab_instance_list

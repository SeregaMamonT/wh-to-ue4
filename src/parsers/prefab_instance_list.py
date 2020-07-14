from typing import BinaryIO

from reader import bool1, string, int1, int2, int4, float4, read_list, assert_version, int8, read_coordinates, \
    read_translation, get_scale, unscale

def read_prefab_instance_list(file: BinaryIO):
    version = int2(file)  # version
    # print('Serrializer Version: ', version)
    prefab_amount = int4(file)
    # print('Prefabs amount: ', prefab_amount)
    for i in range(prefab_amount):
        prefab_version = int2(file)
        # print('Prefab serrializer Version: ', prefab_version)
        name = string(file)
        # print('Prefab name: ', name)
        # file.read(75)
        transformation_matrix = []
        i = 16
        while i > 0:
            matrix_element = float4(file)
            transformation_matrix.append(matrix_element)
            i = i - 1
        # print(transformation_matrix)
        property_overrides = int4(file)
        # print('Property overrides: ', property_overrides)
        for j in range(property_overrides):
            file.read(2)
            property_value = string(file)
            # print(property_value)
            file.read(14)
        file.read(7)
        height_mode = string(file)
        # print('Height mode: ', height_mode)
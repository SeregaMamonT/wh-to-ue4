from typing import BinaryIO

from reader import bool1, string, int1, int2, int4, float4, read_list, assert_version, int8, read_coordinates, \
    read_translation, get_scale, unscale, read_flags

from wh_binary_objects import Prop

def read_prop_list(file: BinaryIO):
    assert_version('PROP_LIST', 2, int2(file))
    keys = read_list(file, read_prop_key_instance)
    props = read_list(file, read_prop_prop_instance)
    result = {}
    for key in keys:
        result[key] = []
    for prop in props:
        key = keys[prop.key_index]
        result[key].append(prop)
    return result


def read_prop_key_instance(file: BinaryIO):
    return string(file)


def read_prop_prop_instance(file: BinaryIO):
    # assert_version('PROP', 15, int2(file))

    version = int2(file)
    # print('Prop version: ', version)

    prop = Prop()
    prop.key_index = int2(file)
    file.read(2)  # TODO

    prop.coordinates = read_coordinates(file)
    # print(prop.coordinates)
    prop.translation = read_translation(file)
    # print(prop.translation)
    prop.scale = get_scale(prop.coordinates)
    # print(prop.scale)
    unscale(prop.coordinates, prop.scale)

    prop.decal = bool1(file)
    # print('Decal: ', prop.decal)
    file.read(7)  # flags from logic_decal to animated
    prop.decal_parallax_scale = float4(file)
    # print('Decal parallax: ', prop.decal_parallax_scale)
    prop.decal_tiling = float4(file)
    # print('Decal tiling: ', prop.decal_tiling)
    bool1(file)

    prop.flags = read_flags(file)

    bool1(file)
    bool1(file)
    bool1(file)
    bool1(file)
    prop.height_mode = string(file)
    # print('Height mode: ', prop.height_mode)
    if version == 15:
        strange_number = int8(file)
        # print('Strange number: ', strange_number)
        bool1(file)
        bool1(file)
    elif version == 14:
        strange_number = int4(file)
        # print('Strange number: ', strange_number)
        bool1(file)
        bool1(file)
    # print(int8(file))

    return prop
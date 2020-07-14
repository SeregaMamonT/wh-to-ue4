from typing import BinaryIO

from reader import bool1, string, int1, int2, int4, float4, read_list, assert_version, int8, read_coordinates, \
    read_translation, get_scale, unscale


def read_sound_shape_list(file: BinaryIO):
    version = int2(file)  # version
    sound_shapes = int4(file)
    # print('Sound shapes: ', version, sound_shapes)
    for i in range(sound_shapes):
        sound_shape_version = int2(file)
        key = string(file)
        type = string(file)
        # print(key, type)
        points = int4(file)
        # print('Points: ', points)
        point_list = []
        for j in range(points):
            point = (float4(file), float4(file), float4(file))
            point_list.append(point)
        inner_radius = float4(file)
        outer_radius = float4(file)

        # probably campaign_type_mask int4
        file.read(4)

        inner_cube = (float4(file), float4(file), float4(file), float4(file), float4(file), float4(file))
        outer_cube = (float4(file), float4(file), float4(file), float4(file), float4(file), float4(file))
        # print(point_list)
        # print(inner_radius, outer_radius, inner_cube, outer_cube)
        clamp_to_surface = bool1(file)
        height_mode = string(file)

        # there is tag <river_nodes/> in xml, byt i dont know what it has inside, i will find, will try  to parse

        file.read(4)
        pdlc_mask = int8(file)
        # print(height_mode, pdlc_mask, clamp_to_surface)
    # assert int4(file) == 0, "SOUND_SHAPE_LIST has items"
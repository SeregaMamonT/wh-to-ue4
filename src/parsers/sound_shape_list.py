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
        # print(sound_shape_version, key, type, point_list, inner_radius, outer_radius)

        inner_cube = (float4(file), float4(file), float4(file), float4(file), float4(file), float4(file))
        outer_cube = (float4(file), float4(file), float4(file), float4(file), float4(file), float4(file))
        river_nodes_amount = int4(file)
        # print(inner_radius, outer_radius, inner_cube, outer_cube, river_nodes_amount)
        river_nodes_list = []
        for i in range(river_nodes_amount):
            river_node_version = int2(file)
            rive_nodes_points = (float4(file), float4(file), float4(file), float4(file),float4(file))
            river_nodes_list.append(rive_nodes_points)
        # print(river_nodes_list)
        clamp_to_surface = bool1(file)
        height_mode = string(file)

        campaign_type_mask = int4(file)
        if sound_shape_version == 6:
            pdlc_mask = int4(file)
        elif sound_shape_version == 7:
            pdlc_mask = int8(file)
    # assert int4(file) == 0, "SOUND_SHAPE_LIST has items"
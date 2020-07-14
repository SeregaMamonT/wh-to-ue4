from typing import BinaryIO

from reader import bool1, string, int1, int2, int4, float4, read_list, assert_version, int8, read_coordinates, \
    read_translation, get_scale, unscale


def read_point_light_list(file: BinaryIO):
    version = int2(file)  # version
    point_lights = int4(file)
    # print("Point lights: ", version, point_lights)
    # print('Current file position: ' + hex(input_file.tell()).upper())
    for i in range(point_lights):
        point_ligh_version = int2(file)
        position = (float4(file), float4(file), float4(file))
        radius = float4(file)
        colour = (float4(file), float4(file), float4(file))
        colour_scale = float4(file)
        # file.read(9)
        animation_type = int1(file)
        params = (float4(file), float4(file))
        # animation_type = float4(file)
        colour_min = float4(file)
        random_offset = float4(file)
        falloff_type = string(file)
        lf_relative = bool1(file)
        height_mode = string(file)
        light_probes_only = bool1(file)
        if point_ligh_version == 5:
            pdlc_mask = int4(file)
        elif point_ligh_version == 6:
            pdlc_mask = int8(file)
        # print(point_ligh_version, position, radius, colour, colour_scale, animation_type, params, colour_min, random_offset, falloff_type, height_mode, pdlc_mask)
    # assert int4(file) == 0, "POINT_LIGHT_LIST has items"
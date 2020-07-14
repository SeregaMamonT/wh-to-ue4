from typing import BinaryIO

from reader import bool1, string, int1, int2, int4, float4, read_list, assert_version, int8, read_coordinates, \
    read_translation, get_scale, unscale


def read_spot_light_list(file: BinaryIO):
    version = int2(file)  # version
    spot_lights = int4(file)
    # print("Spot lights: ", version, spot_lights)
    for i in range(spot_lights):
        spot_light_version = int2(file)
        position = (float4(file), float4(file), float4(file))
        end = (float4(file), float4(file), float4(file), float4(file))
        length = float4(file)
        inner_angle = float4(file)
        outer_angle = float4(file)
        colour = (float4(file), float4(file), float4(file))
        falloff = float4(file)

        gobo = string(file)
        volumetric = bool1(file)

        height_mode = string(file)
        if spot_light_version == 5:
            pdlc_mask = int4(file)
        elif spot_light_version == 6:
            pdlc_mask = int8(file)
        # print(spot_light_version, position, end, length, inner_angle, outer_angle, colour, falloff, height_mode,
        #       pdlc_mask, gobo, volumetric)

    # assert int4(file) == 0, "SPOT_LIGHT_LIST has items"

from typing import BinaryIO

from reader import bool1, string, int1, int2, int4, float4, read_list, assert_version, int8, read_coordinates, \
    read_translation, get_scale, unscale


def read_composite_scene_list(file: BinaryIO):
    version = int2(file)  # version
    composite_scenes = int4(file)
    # print('Composite scenes: ', version, composite_scenes)
    for i in range(composite_scenes):
        composite_scene_version = int2(file)
        file.read(48)
        composite_scene_name = string(file)
        height_mode = string(file)
        if composite_scene_version == 6:
            pdlc_mask = int4(file)
        elif composite_scene_version == 7:
            pdlc_mask = int8(file)
        file.read(3)
        # print(composite_scene_version, composite_scene_name, height_mode, pdlc_mask)
    # assert int4(file) == 0, "COMPOSITE_SCENE_LIST has items"
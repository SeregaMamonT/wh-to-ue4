from typing import BinaryIO

from reader import bool1, string, int1, int2, int4, float4, read_list, assert_version, int8, read_coordinates, \
    read_translation, get_scale, unscale

from wh_binary_objects import CompositeScene


def read_composite_scene_v6(file):
    composite_scene = CompositeScene()
    composite_scene.coordinates = [[None] * 3 for i in range(3)]
    for i in range(9):
        composite_scene.coordinates[i // 3][i % 3] = float4(file)
    composite_scene.transform = [None] * 3
    for i in range(3):
        composite_scene.transform[i] = float4(file)
    composite_scene.scene_file = string(file)
    composite_scene.height_mode = string(file)
    composite_scene.pdlc_mask = int4(file)
    composite_scene.flags = {}
    composite_scene.flags["autoplay"] = bool1(file)
    composite_scene.flags["visible_in_shroud"] = bool1(file)
    composite_scene.flags["no_culling"] = bool1(file)

    return composite_scene


def read_composite_scene_v7(file):
    composite_scene = CompositeScene()
    composite_scene.coordinates = [[None] * 3 for i in range(3)]
    for i in range(9):
        composite_scene.coordinates[i // 3][i % 3] = float4(file)
    composite_scene.transform = [None] * 3
    for i in range(3):
        composite_scene.transform[i] = float4(file)
    composite_scene.scene_file = string(file)
    composite_scene.height_mode = string(file)
    composite_scene.pdlc_mask = int8(file)
    composite_scene.flags = {}
    composite_scene.flags["autoplay"] = bool1(file)
    composite_scene.flags["visible_in_shroud"] = bool1(file)
    composite_scene.flags["no_culling"] = bool1(file)

    return composite_scene


version_readers = {
    6: read_composite_scene_v6,
    7: read_composite_scene_v7,
}


def get_version_reader(version):
    if version in version_readers:
        return version_readers[version]
    else:
        raise Exception('Unsupported composite scene version: ' + str(version))


def read_composite_scene_list(file: BinaryIO):
    version = int2(file)  # version
    amount = int4(file)
    composite_scenes_list = []
    for i in range(amount):
        composite_scenes_version = int2(file)
        composite_scenes_list.append(get_version_reader(composite_scenes_version)(file))

    return composite_scenes_list

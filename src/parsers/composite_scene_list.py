from typing import BinaryIO

from reader import bool1, string, int1, int2, int4, float4, read_list, assert_version, int8, read_transform_n_x_m

from wh_binary_objects import CompositeScene

from version_holder import VersionHolder


def read_composite_scene_list(file: BinaryIO):
    assert_version('COMPOSITE_SCENE_LIST', 1, int2(file))
    return read_list(file, read_composite_scene)


def read_composite_scene(file):
    composite_scene_version = int2(file)
    return composite_scene_versions.get_reader(composite_scene_version)(file)


def read_composite_scene_v6(file):
    composite_scene = read_composite_scene_common(file)
    composite_scene.pdlc_mask = int4(file)
    composite_scene.flags = {}
    composite_scene.flags["autoplay"] = bool1(file)
    composite_scene.flags["visible_in_shroud"] = bool1(file)
    composite_scene.flags["no_culling"] = bool1(file)

    return composite_scene


def read_composite_scene_v7(file):
    composite_scene = read_composite_scene_common(file)
    composite_scene.pdlc_mask = int8(file)
    composite_scene.flags = {}
    composite_scene.flags["autoplay"] = bool1(file)
    composite_scene.flags["visible_in_shroud"] = bool1(file)
    composite_scene.flags["no_culling"] = bool1(file)

    return composite_scene


def read_composite_scene_common(file):
    composite_scene = CompositeScene()
    composite_scene.transform = read_transform_n_x_m(file, 4, 3)
    composite_scene.scene_file = string(file)
    composite_scene.height_mode = string(file)

    return composite_scene


composite_scene_versions = VersionHolder('Composite scene', {
    6: read_composite_scene_v6,
    7: read_composite_scene_v7,
})

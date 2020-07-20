from typing import BinaryIO

from reader import bool1, string, int1, int2, int4, float4, read_list, assert_version, int8, read_flags, \
    read_transform_n_x_m

from wh_binary_objects import Prop

from version_holder import VersionHolder


def read_prop_list(file: BinaryIO):
    assert_version('PROP_LIST', 2, int2(file))
    keys = read_list(file, read_prop_key_instance)
    props = read_list(file, read_prop_instance)
    result = {}
    for key in keys:
        result[key] = []
    for prop in props:
        key = keys[prop.key_index]
        prop.key = key
        result[key].append(prop)

    return result


def read_prop_key_instance(file: BinaryIO):
    return string(file)


def read_prop_instance(file):
    prop_instance_version = int2(file)
    return prop_instance_versions.get_reader(prop_instance_version)(file)


def read_prop_instance_v14(file):
    prop = read_prop_instance_common(file)
    strange_number = int4(file)
    bool1(file)
    bool1(file)

    return prop


def read_prop_instance_v15(file):
    prop = read_prop_instance_common(file)
    strange_number = int8(file)
    bool1(file)
    bool1(file)

    return prop


def read_prop_instance_common(file):
    prop = Prop()
    prop.key_index = int2(file)
    file.read(2)  # TODO
    prop.transform = read_transform_n_x_m(file, 4, 3)
    prop.decal = bool1(file)
    file.read(7)  # flags from logic_decal to animated
    prop.decal_parallax_scale = float4(file)
    # print('Decal parallax: ', prop.decal_parallax_scale)
    prop.decal_tiling = float4(file)
    # print('Decal tiling: ', prop.decal_tiling)
    decal_override_gbuffer_normal = bool1(file)
    prop.flags = read_flags(file)
    prop.flags["decal_override_gbuffer_normal"] = decal_override_gbuffer_normal
    prop.flags["visible_in_shroud"] = bool1(file)
    prop.flags["decal_apply_to_terrain"] = bool1(file)
    prop.flags["decal_apply_to_gbuffer_objects"] = bool1(file)
    prop.flags["decal_render_above_snow"] = bool1(file)
    prop.height_mode = string(file)

    return prop


prop_instance_versions = VersionHolder('Prop', {
    14: read_prop_instance_v14,
    15: read_prop_instance_v15,
})

from typing import BinaryIO

from reader import bool1, string, int1, int2, int4, float4, read_list, assert_version, int8, read_coordinates, \
    read_translation, get_scale, unscale

from wh_binary_objects import PrefabTree, PrefabTreeProps


def read_prefab_tree(file):
    tree = PrefabTree()
    tree.key = string(file)
    amount = int4(file)
    tree.props = []
    for i in range(amount):
        props = PrefabTreeProps()
        props.position = (float4(file), float4(file), float4(file))
        props.scale = float4(file)
        props.is_freeform = bool1(file)
        tree.props.append(props)
    return tree



def read_prefab_tree_list_v1(file):
    version = int2(file)  # version
    file.read(6)
    amount = int4(file)
    prefab_tree_list = []
    for i in range(amount):
       prefab_tree_list.append(read_prefab_tree(file))

    return prefab_tree_list


def read_prefab_tree_list_v2(file):
    version = int2(file)
    amount = int4(file)
    prefab_tree_list = []
    for i in range(amount):
       prefab_tree_list.append(read_prefab_tree(file))

    return prefab_tree_list


version_readers = {
    1: read_prefab_tree_list_v1,
    2: read_prefab_tree_list_v2,
}


def get_version_reader(version):
    if version in version_readers:
        return version_readers[version]
    else:
        raise Exception('Unsupported vegetatation version: ' + str(version))


def read_prefab_vegetation_list(file: BinaryIO):
    version = int2(file)  # version
    prefab_vegetation = get_version_reader(version)(file)
    return prefab_vegetation
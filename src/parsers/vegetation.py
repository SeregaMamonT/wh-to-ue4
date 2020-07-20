from typing import BinaryIO

from reader import bool1, string, int1, int2, int4, float4, read_list, assert_version, int8, read_coordinates, \
    read_translation, get_scale, unscale

from wh_binary_objects import Tree, PrefabTreeProps

from wh_common_objects import Point3D

def read_tree(file):
    tree = Tree()
    tree.key = string(file)
    amount = int4(file)
    tree.props = []
    # print(tree.key)
    for i in range(amount):
        props = PrefabTreeProps()
        props.position = Point3D(float4(file), float4(file), float4(file))
        props.scale = float4(file)
        props.is_freeform = bool1(file)
        # print(props.__dict__)
        tree.props.append(props)
    return tree



def read_prefab_tree_list_v1(file):
    version = int2(file)  # version
    file.read(6)
    amount = int4(file)
    prefab_tree_list = []
    for i in range(amount):
       prefab_tree_list.append(read_tree(file))

    return prefab_tree_list


def read_prefab_tree_list_v2(file):
    version = int2(file)
    amount = int4(file)
    prefab_tree_list = []
    for i in range(amount):
       prefab_tree_list.append(read_tree(file))

    return prefab_tree_list


def read_map_tree_list_v1(file):
    version = int2(file)  # version
    file.read(6)
    amount = int4(file)
    prefab_tree_list = []
    for i in range(amount):
       prefab_tree_list.append(read_tree(file))

    return prefab_tree_list


def read_map_tree_list_v2(file):
    amount = int4(file)
    # print(amount)
    map_tree_list = []
    for i in range(amount):
       map_tree_list.append(read_tree(file))
    return map_tree_list


version_readers = {
    1: read_prefab_tree_list_v1,
    2: read_prefab_tree_list_v2,
}


map_version_readers = {
    1: read_map_tree_list_v1,
    2: read_map_tree_list_v2,
}


def get_version_reader(version):
    if version in version_readers:
        return version_readers[version]
    else:
        raise Exception('Unsupported vegetatation version: ' + str(version))


def get_map_version_reader(version):
    if version in map_version_readers:
        return map_version_readers[version]
    else:
        raise Exception('Unsupported map vegetatation version: ' + str(version))


def read_prefab_vegetation_list(file: BinaryIO):
    version = int2(file)  # version
    prefab_vegetation = get_version_reader(version)(file)
    return prefab_vegetation


def read_map_vegetation_list(file: BinaryIO):
    version = int2(file)  # version
    map_vegetation = get_map_version_reader(version)(file)
    return map_vegetation
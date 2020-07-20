from typing import BinaryIO

from reader import bool1, string, int1, int2, int4, float4, read_list, assert_version, int8

from wh_binary_objects import Tree, PrefabTreeProps

from wh_common_objects import Point3D

from version_holder import VersionHolder


def read_tree(file):
    tree = Tree()
    tree.key = string(file)
    trees_amount = int4(file)
    tree.props = []
    # print(tree.key)
    for tree_property in range(trees_amount):
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
    return read_list(file, read_tree)


def read_map_tree_list_v1(file):
    version = int2(file)  # version
    file.read(6)
    return read_list(file, read_tree)


def read_map_tree_list_v2(file):
    return read_list(file, read_tree)



def read_prefab_vegetation_list(file: BinaryIO):
    version = int2(file)  # version
    prefab_vegetation = preab_vegetation_versions.get_reader(version)(file)

    return prefab_vegetation


def read_map_vegetation_list(file: BinaryIO):
    version = int2(file)  # version
    map_vegetation = map_vegetation_versions.get_reader(version)(file)

    return map_vegetation


preab_vegetation_versions = VersionHolder('Prefab vegetation', {
    1: read_prefab_tree_list_v1,
    2: read_prefab_tree_list_v2,
})


map_vegetation_versions = VersionHolder('Map vegetation', {
    1: read_map_tree_list_v1,
    2: read_map_tree_list_v2,
})


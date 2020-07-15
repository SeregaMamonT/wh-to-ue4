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

def read_prefab_tree_list(file: BinaryIO):
    version = int2(file)  # version
    amount = int4(file)
    prefab_tree_list = []
    for i in range(amount):
       prefab_tree_list.append(read_prefab_tree(file))

    return prefab_tree_list
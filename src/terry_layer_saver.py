from wh_binary_objects import Prefab, MapData


def terry_layer_saver(object, type: int):
    get_type_saver(type)(object)


def prefab_saver(prefab: Prefab):
    return


def map_saver(map: MapData):
    return


def get_type_saver(type):
    if type in terry_savers:
        return terry_savers[type]
    else:
        raise Exception('Unsupported save type: ' + str(type))


terry_savers = {
    1: prefab_saver,
    2: map_saver,
}


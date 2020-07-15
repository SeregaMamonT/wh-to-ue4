from typing import BinaryIO

from reader import bool1, string, int1, int2, int4, float4, read_list, assert_version, int8, read_coordinates, \
    read_translation, get_scale, unscale

from wh_binary_objects import PlayableArea


def read_playable_area_v2(file):
    playable_area = PlayableArea()
    playable_area.min_x = float4(file)
    playable_area.min_y = float4(file)
    playable_area.max_x = float4(file)
    playable_area.max_y = float4(file)

    # dont know exact flags
    file.read(5)


    return playable_area


def read_playable_area_v3(file):
    playable_area = PlayableArea()
    playable_area.min_x = float4(file)
    playable_area.min_y = float4(file)
    playable_area.max_x = float4(file)
    playable_area.max_y = float4(file)
    playable_area.has_been_set = bool1(file)
    valid_location_flags_version = int2(file)
    playable_area.flags = {}
    playable_area.flags["valid_north"] = bool1(file)
    playable_area.flags["valid_south"] = bool1(file)
    playable_area.flags["valid_east"] = bool1(file)
    playable_area.flags["valid_west"] = bool1(file)

    return playable_area

version_readers = {
    2: read_playable_area_v2,
    3: read_playable_area_v3,
}


def get_version_reader(version):
    if version in version_readers:
        return version_readers[version]
    else:
        raise Exception('Unsupported point light version: ' + str(version))


def read_playable_area(file: BinaryIO):
    version = int2(file)  # version
    playable_area = get_version_reader(version)(file)

    return playable_area
from typing import BinaryIO

from reader import bool1, string, int1, int2, int4, float4, read_list, assert_version, int8
from wh_binary_objects import PlayableArea

from version_holder import VersionHolder


def read_playable_area(file: BinaryIO):
    version = int2(file)  # version
    return playable_area_versions.get_reader(version)(file)


def read_playable_area_v2(file):
    playable_area = PlayableArea()
    playable_area.min_x = float4(file)
    playable_area.min_y = float4(file)
    playable_area.max_x = float4(file)
    playable_area.max_y = float4(file)
    playable_area.flags = {}
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


playable_area_versions = VersionHolder('Playable area', {
    2: read_playable_area_v2,
    3: read_playable_area_v3,
})







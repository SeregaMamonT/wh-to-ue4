from typing import BinaryIO

from reader import bool1, string, int1, int2, int4, float4, read_list, assert_version, int8, read_coordinates, \
    read_translation, get_scale, unscale

from wh_binary_objects import CaptureLocation, CaptureLocationBuildingLink


def read_capture_location(file):
    capture_location = CaptureLocation()
    capture_location.location = (float4(file), float4(file))
    capture_location.radius = float4(file)
    capture_location.valid_for_min_num_players = int4(file)
    capture_location.valid_for_max_num_players = int4(file)
    capture_location.capture_point_type = string(file)
    location_points = int4(file)
    capture_location.location_points_list = []
    for l in range(location_points):
        t = (float4(file), float4(file))
        capture_location.location_points_list.append(t)
    capture_location.database_key = string(file)
    capture_location.flag_facing = (float4(file), float4(file))
    building_links_amount = int4(file)
    capture_location.building_links = []
    for l in range(building_links_amount):
        building_link = CaptureLocationBuildingLink()
        building_link.version = int2(file)
        building_link.building_index = int4(file)
        building_link.prefab_index = int4(file)
        building_link.link = string(file)
        capture_location.building_links.append(building_link)

    return capture_location


def read_capture_location_list(file):
    capture_locations = int4(file)
    capture_locations_list = []
    for i in range(capture_locations):
        capture_locations_list.append(read_capture_location(file))

    return capture_locations_list

def read_capture_location_set(file: BinaryIO):
    version = int2(file)  # version
    capture_locations_lists = int4(file)
    capture_locations_set = []
    for i in range(capture_locations_lists):
        capture_locations_set.append(read_capture_location_list(file))

    return capture_locations_set
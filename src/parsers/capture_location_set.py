from typing import BinaryIO

from reader import bool1, string, int1, int2, int4, float4, read_list, assert_version, int8, read_coordinates, \
    read_translation, get_scale, unscale

def read_capture_location_set(file: BinaryIO):
    version = int2(file)  # version
    # print('Version: ', version)
    list_amount = int4(file)
    for i in range(list_amount):
        location_amount = int4(file)
        # print('Locations: ', location_amount)
        for j in range(location_amount):
            location = (float4(file), float4(file))
            # print(location)
            radius = float4(file)
            valid_for_min_num_players = int4(file)
            valid_for_max_num_players = int4(file)
            # print(radius, valid_for_min_num_players, valid_for_max_num_players)
            capture_point_type = string(file)
            # print(capture_point_type)
            location_points = int4(file)
            location_points_list = []
            for l in range(location_points):
                t = (float4(file), float4(file))
                location_points_list.append(t)
            # print(location_points_list)
            database_key = string(file)
            # print(database_key)
            flag_facing = (float4(file), float4(file))
            building_links = int4(file)
            # print(building_links)
            for l in range(building_links):
                bilding_links_version = int2(file)
                bilding_links_building_index = int4(file)
                bilding_links_prefab_index = int4(file)
                building_link = string(file)
                # print(bilding_links_version, bilding_links_building_index, bilding_links_prefab_index, building_link)
    # assert int4(file) == 0, "CAPTURE_LOCATION_SET has items"
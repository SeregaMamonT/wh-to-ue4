from typing import BinaryIO

from reader import bool1, string, int1, int2, int4, float4, read_list, assert_version, int8, read_coordinates, \
    read_translation, get_scale, unscale


def read_deployment_list(file: BinaryIO):
    version = int2(file)  # version
    amount = int4(file)
    # print('deployment_list: ', version, amount)
    for i in range(amount):
        deployment_area_version = int2(file)
        deployment_area_category = string(file)
        # print(deployment_area_version, deployment_area_category)
        deployment_zones_amount = int4(file)
        for j in range(deployment_zones_amount):
            deployment_zone_version = int2(file)
            deployment_zone_regions_amount = int4(file)
            for l in range(deployment_zone_regions_amount):
                deployment_zone_region_version = int2(file)
                boundary_list_amount = int4(file)
                for k in range(boundary_list_amount):
                    boundary_version = int2(file)
                    deployment_area_boundary_type = string(file)
                    # print(deployment_area_boundary_type)
                    boundary_amount = int4(file)
                    boundary_positions = []
                    for m in range(boundary_amount):
                        position = (float4(file), float4(file))
                        boundary_positions.append(position)
                    # print(boundary_positions)

                # not sure about order, and palces in cycle
                orientation = float4(file)
                snap_facing = bool1(file)
                id = int4(file)
                # print(orientation, snap_facing, id)
    # assert int4(file) == 0, "DEPLOYMENT_LIST has items"
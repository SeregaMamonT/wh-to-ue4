from typing import BinaryIO

from reader import bool1, string, int1, int2, int4, float4, read_list, assert_version, int8, read_coordinates, \
    read_translation, get_scale, unscale

from wh_binary_objects import Deployment, DeploymentArea, DeploymentZoneRegion, Boundary, Point2D


def read_boundary(file):
    boundary = Boundary()
    boundary.type = string(file)
    positions = int4(file)
    boundary.positions = []
    for i in range(positions):
        position = Point2D(float4(file), float4(file))
        boundary.positions.append(position)

    return boundary


def read_boundary_list(file):
    boundary_list = []
    amount = int4(file)
    for i in range(amount):
        boundary_version = int2(file)
        boundary_list.append(read_boundary(file))

    return boundary_list

def read_deployment_zone_region(file):
    deployment_zone_region = DeploymentZoneRegion()

    boundary_list_amount = int4(file)
    deployment_zone_region.boundary_list = []
    for i in range(boundary_list_amount):
        boundary_version = int2(file)
        deployment_zone_region.boundary_list.append(read_boundary_list(file))
    deployment_zone_region.orientation = float4(file)
    deployment_zone_region.snap_facing = bool1(file)
    deployment_zone_region.id = int4(file)

    return deployment_zone_region


def read_deployment_area(file):
    deployment_area = DeploymentArea()
    deployment_area.category = string(file)
    deployment_zones_amount = int4(file)
    deployment_area.deployment_zone_regions = []
    for i in range(deployment_zones_amount):
        deployment_zone_region_version = int2(file)
        deployment_area.deployment_zone_regions.append(read_deployment_zone_region(file))

    return deployment_area


def read_deployment_list(file: BinaryIO):
    version = int2(file)  # version
    amount = int4(file)
    deployment_list = []
    for i in range(amount):
        deployment_area_version = int2(file)
        deployment_list.append(read_deployment_area(file))

    return deployment_list
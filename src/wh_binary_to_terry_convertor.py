from wh_terry_objects import TerryBuilding, ECTransform
from typing import BinaryIO, List
from wh_binary_objects import Building

from matrix import get_angles_deg, transpose, get_angles_deg_XYZ, get_angles_deg_XZY, get_angles_XYZ, get_angles_XZY, \
    degrees_tuple


def mod_vector(vector: List):
    return sum([x * x for x in vector]) ** 0.5


def convert_building(building: Building):
    terry_building = TerryBuilding()
    terry_building.ectransform = ECTransform()
    terry_building.key = building.building_key
    terry_building.damage = int(building.starting_damage_unary * 100)
    terry_building.ectransform.position = []

    for i in range(3):
        terry_building.ectransform.position.append(building.transform[i])

    coordinates = building.coordinates
    terry_building.ectransform.scale = list(map(mod_vector, coordinates))
    for i in range(3):
        scale = terry_building.ectransform.scale[i]
        for j in range(3):
            coordinates[i][j] /= scale
    terry_building.ectransform.rotation = degrees_tuple(get_angles_XYZ(transpose(coordinates)))

    # print(terry_building.ectransform.__dict__)
    return terry_building

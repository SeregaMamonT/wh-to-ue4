from wh_terry_objects import TerryBuilding
from typing import BinaryIO, List
from wh_binary_objects import Building


def mod_vector(vector: List):
    return sum([x * x for x in vector]) ** 0.5


def convert_building(building: Building):
    terry_building = TerryBuilding
    terry_building.key = building.building_key
    terry_building.damage = int(building.starting_damage_unary*100)
    terry_building.ectransform.position = []

    for i in range(3):
        terry_building.ectransform.position.append(building.transform[i])

    coordinates = building.coordinates
    terry_building.scales = list(map(mod_vector, coordinates))
    for i in range(3):
        scale = terry_building.scales[i]
        for j in range(3):
            coordinates[i][j] /= scale

    return terry_building
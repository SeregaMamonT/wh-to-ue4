from xml.etree.ElementTree import Element, SubElement
from typing import List

from terry_savers.xml_saver_utils import ectransform_to_xml, ecmeshrendersettings_to_xml, ecterrainclamp_to_xml, s_bool, \
    create_entity_node, s_float

from wh_terry_objects import TerrySoundShape


def save_sound_shape_sphere(sound_shape: TerrySoundShape, entity):
    ectransform_to_xml(entity, sound_shape.ectransform)
    ECSphere = SubElement(entity, "ECSphere", {
        "radius": s_float(sound_shape.radius),
    })


def save_sound_shape_point_cloud(sound_shape: TerrySoundShape, entity):
    ectransform_to_xml(entity, sound_shape.ectransform)
    ECPointCloud = SubElement(entity, "ECSphere", {
    })
    point_cloud = SubElement(ECPointCloud, "point_cloud", {
    })
    for i in sound_shape.points_cloud:
        point = SubElement(point_cloud, "point", {
            "x": s_float(i.x),
            "y": s_float(i.y),
            "z": s_float(i.z),
        })


def save_sound_shape_point(sound_shape: TerrySoundShape, entity):
    ectransform_to_xml(entity, sound_shape.ectransform)


def save_sound_shape_polyline(sound_shape: TerrySoundShape, entity):
    ectransform_to_xml(entity, sound_shape.ectransform)
    ECPolyline = SubElement(entity, "ECPolyline", {
    })
    polyline = SubElement(ECPolyline, "polyline", {
        "closed": "true"
    })
    for i in sound_shape.points:
        point = SubElement(polyline, "point", {
            "x": s_float(i.x),
            "y": s_float(i.y),
        })
    ECTransform2D = SubElement(entity, "ECTransform2D", {
    })


def save_sound_shape_river(sound_shape: TerrySoundShape, entity):
    return


type_savers = {
    "SST_RIVER": save_sound_shape_river,
    "SST_POINT": save_sound_shape_point,
    "SST_SPHERE": save_sound_shape_sphere,
    "SST_MULTI_POINT": save_sound_shape_point_cloud,
    "SST_LINE_LIST": save_sound_shape_polyline,
}


def get_type_saver(type):
    if type in type_savers:
        return type_savers[type]
    else:
        raise Exception('Unsupported sound shape type: ' + str(type))


def save_sound_shape_list(sound_shapes: List[TerrySoundShape], entities: Element):
    for sound_shape in sound_shapes:
        entity = create_entity_node(entities)
        ECSoundMarker = SubElement(entity, "ECSoundMarker", {
            "key": sound_shape.key,
        })
        get_type_saver(sound_shape.type)(sound_shape, entity)


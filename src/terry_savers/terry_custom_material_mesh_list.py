from xml.etree.ElementTree import Element, SubElement
from typing import List

from terry_savers.xml_saver_utils import ectransform_to_xml, ecmeshrendersettings_to_xml, ecterrainclamp_to_xml, s_bool, \
    create_entity_node

from wh_terry_objects import TerryCustomMaterialMesh

def save_custom_material_mesh_list(custom_material_meshes: List[TerryCustomMaterialMesh], entities: Element):
    for mesh in custom_material_meshes:
        entity = create_entity_node(entities)

        ECPolygonMesh = SubElement(entity, "ECPolygonMesh", {
            "material": mesh.material,
            "affects_protection_map": "false",
        })
        ectransform_to_xml(entity, mesh.ectransform)
        ECPolyline = SubElement(entity, "ECPolyline", {
        })
        polyline = SubElement(ECPolyline, "polyline", {
            "closed": "true"
        })
        for i in mesh.polyline:
            point = SubElement(polyline, "point", {
                "x": str(i.x),
                "y": str(i.y),
            })


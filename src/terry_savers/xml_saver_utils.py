from xml.etree.ElementTree import Element, SubElement, tostring
from typing import Dict, List
from wh_terry_objects import ECTransform, ECMeshRenderSettings, ECBattleProperties


def format_float(x):
    return "{:.5f}".format(x).rstrip("0").strip(".")


def ectransform_to_xml(entity: Element, ectransform: ECTransform):
    ECTransform = SubElement(entity, "ECTransform", {
        "position": " ".join(map(format_float, ectransform.position)),
        "rotation": " ".join(map(format_float, ectransform.rotation)),
        "scale": " ".join(map(format_float, ectransform.scale)),
    })

    return entity


def ecmeshrendersettings_to_xml(entity: Element, ecmeshrendersettings: ECMeshRenderSettings):
    ECMeshRenderSettings = SubElement(entity, "ECMeshRenderSettings", {
        "cast_shadow": str(ecmeshrendersettings.cast_shadow)
    })

    return entity
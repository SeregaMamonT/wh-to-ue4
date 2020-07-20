from typing import Dict, List

from app_typing import Matrix, Vector

from wh_binary_objects import Point2D, Point3D, ColourRGBA


class ECTransform:
    position: List[float]
    rotation: List[float]
    scale: List[float]


class ECMeshRenderSettings:
    def __init__(self, cast_shadow: bool):
        self.cast_shadow = cast_shadow


class ECTerrainClamp:
    terrain_clamp_active: bool
    clamp_to_sea_level: bool
    terrain_oriented: bool


class ECBattleProperties:
    allow_in_outfield: bool


class TerryBuilding:
    key: str
    damage: int
    capture_location: str
    flags: Dict[str, bool]
    ectransform: ECTransform
    ecterrainclamp: ECTerrainClamp
    ecmeshrendersettings: ECMeshRenderSettings


class TerryParticle:
    vfx: str
    scale: int
    instance_name: str
    flags: Dict[str, bool]
    ectransform: ECTransform
    ecterrainclamp: ECTerrainClamp
    ecbattleproperties: ECBattleProperties


class TerryDecal:
    model_path: str
    parallax_scale: float
    tiling: int
    normal_mode: str
    flags: Dict[str, bool]
    ectransform: ECTransform
    ecterrainclamp: ECTerrainClamp
    ecbattleproperties: ECBattleProperties


class TerryPropBuilding:
    model_path: str
    animation_path: str
    opacity: int
    ectransform: ECTransform
    ecterrainclamp: ECTerrainClamp
    ecbattleproperties: ECBattleProperties
    ecmeshrendersettings: ECMeshRenderSettings


class TerryPrefabInstance:
    key: str
    ectransform: ECTransform
    ecterrainclamp: ECTerrainClamp


class TerryTree:
    key: str
    ectransform: ECTransform
    ecterrainclamp: ECTerrainClamp


class TerryCustomMaterialMesh:
    material: str
    affects_protection_map: bool
    polyline: List[Point2D]
    ectransform: ECTransform


class TerryTerrainHole:
    procedural_exclusion_zone: bool
    procedural_exclusion_zone_margin: int
    ectransform: ECTransform
    polyline: List[Point2D]


class TerryLightProbe:
    radius: int
    is_primary: bool
    ectransform: ECTransform


class TerryPlayableArea:
    width: float
    height: float
    deployment_locations: List[str]
    ectransform: ECTransform


class TerryPointLight:
    colour: ColourRGBA
    colour_scale: float
    radius: float
    animation_type: str
    animation_speed_scale: tuple
    colour_min: float
    random_offset: float
    falloff_type: str
    for_light_probes_only: bool
    ectransform: ECTransform


class TerrySpotLight:
    colour: ColourRGBA
    intensity: float
    length: float
    inner_angle: float
    outer_angle: float
    falloff: float
    volumetric: bool
    gobo: str
    ectransform: ECTransform


class TerrySoundShape:
    key: str
    type: str
    radius: float
    points: List[Point2D]
    points_cloud: List[Point3D]
    ectransform: ECTransform


class TerryCompositeSecne:
    path: str
    autoplay: bool
    ectransform: ECTransform

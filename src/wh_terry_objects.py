from typing import Dict, List

from app_typing import Matrix, Vector

from wh_common_objects import Point2D, Point3D, ColourRGBA, ColourRGB, Cube, Scale3D, Rotation3D




class ECTransform:

    def __init__(self, position: Point3D, rotation: Rotation3D, scale: Scale3D):
        self.position = position
        self.rotation = rotation
        self.scale = scale


class ECMeshRenderSettings:
    def __init__(self, cast_shadow: bool):
        self.cast_shadow = cast_shadow


class ECTerrainClamp:
    terrain_clamp_active: bool
    clamp_to_sea_level: bool
    terrain_oriented: bool


class ECTransformable:
    ectransform: ECTransform


class ECTerrainClampable:
    ecterrainclamp: ECTerrainClamp


class ECBattleProperties:
    allow_in_outfield: bool


class ECPolyline:
    closed: bool
    polyline: List[Point2D]


class TerryBuilding(ECTransformable, ECTerrainClampable):
    key: str
    damage: int
    capture_location: str
    flags: Dict[str, bool]
    ecmeshrendersettings: ECMeshRenderSettings


class TerryParticle(ECTransformable, ECTerrainClampable):
    vfx: str
    scale: int
    instance_name: str
    flags: Dict[str, bool]
    ecbattleproperties: ECBattleProperties


class TerryDecal(ECTransformable, ECTerrainClampable):
    model_path: str
    parallax_scale: float
    tiling: int
    normal_mode: str
    flags: Dict[str, bool]
    ecbattleproperties: ECBattleProperties


class TerryPropBuilding(ECTransformable, ECTerrainClampable):
    model_path: str
    animation_path: str
    opacity: int
    ecbattleproperties: ECBattleProperties
    ecmeshrendersettings: ECMeshRenderSettings


class TerryPrefabInstance(ECTransformable, ECTerrainClampable):
    key: str


class TerryBuildingProjectileEmitter(ECTransformable):
    building_index: int


class TerryZoneTemplate(ECTransformable):
    locked: bool
    rank_distance: float
    zone_skirt_distance: float
    polyline: ECPolyline


class TerryRegion(ECTransformable):
    polyline: ECPolyline


class TerryTree(ECTransformable, ECTerrainClampable):
    key: str


class TerryCustomMaterialMesh(ECTransformable):
    material: str
    affects_protection_map: bool
    polyline: List[Point2D]


class TerryTerrainHole(ECTransformable):
    procedural_exclusion_zone: bool
    procedural_exclusion_zone_margin: int
    polyline: List[Point2D]


class TerryLightProbe(ECTransformable):
    radius: int
    is_primary: bool


class TerryPlayableArea(ECTransformable):
    width: float
    height: float
    deployment_locations: List[str]


class TerryPointLight(ECTransformable):
    colour: ColourRGBA
    colour_scale: float
    radius: float
    animation_type: str
    animation_speed_scale: tuple
    colour_min: float
    random_offset: float
    falloff_type: str
    for_light_probes_only: bool


class TerrySpotLight(ECTransformable):
    colour: ColourRGBA
    intensity: float
    length: float
    inner_angle: float
    outer_angle: float
    falloff: float
    volumetric: bool
    gobo: str


class TerrySoundShape(ECTransformable):
    key: str
    type: str
    radius: float
    points: List[Point2D]
    points_cloud: List[Point3D]


class TerryCompositeSecne(ECTransformable):
    path: str
    autoplay: bool

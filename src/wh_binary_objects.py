from typing import Dict, List

from app_typing import Matrix, Vector


class Point3D:

    def __init__(self, x: float, y: float, z: float):
        self.x = x
        self.y = y
        self.z = z


class Point2D:

    def __init__(self, x: float, y: float):
        self.x = x
        self.y = y


class ColourRGB:

    def __init__(self, r: float, g: float, b: float):
        self.red = r
        self.green = g
        self.blue = b


class Building:
    model_name: str
    object_relation1: str
    object_relation2: str
    position: Vector
    coordinates: Matrix
    scale: Vector


class Particle:
    model_name: str
    object_relation: str
    position: Vector
    coordinates: Matrix
    flags: Dict[str, bool]
    autoplay: bool
    visible_in_shroud: bool


class Prop:
    key_index: int
    position: Vector
    coordinates: Matrix
    scale: Vector
    decal: bool
    flags: Dict[str, bool]
    decal_parallax_scale: float
    decal_tiling: float
    height_mode: str


class PointLight:
    position: Point3D
    radius: float
    colour_scale: float
    colour: ColourRGB
    animation_type: int
    params: tuple
    colour_min: float
    random_offset: float
    falloff_type: str
    height_mode: str
    light_probes_only: str
    pdlc_mask: int
    flags: Dict[str, bool]


class SpotLight:
    position: Point3D
    end: Vector
    length: float
    inner_angle: float
    outer_angle: float
    colour: ColourRGB
    falloff: float
    gobo: str
    flags: Dict[str, bool]
    height_mode: str
    pdlc_mask: int


class CaptureLocationBuildingLink:
    version: int
    building_index: int
    prefab_index: int
    link: str


class CaptureLocation:
    location: Point2D
    radius: float
    valid_for_min_num_players: float
    valid_for_max_num_players = float
    capture_point_type: str
    location_points_list: List[Point2D]
    database_key: str
    flag_facing: Point2D
    building_links: List[CaptureLocationBuildingLink]


class Outline:
    points: List[Point2D]


class ZoneTemplate:
    name: str
    points: List[Point2D]
    transformation: Matrix


class PrefabInstance:
    name: str
    transformation: Matrix
    property_overrides = []
    height_mode: str


class PolyLine:
    type: str
    points: List[Point2D]


class Polygone:
    points_amount: int
    points: List[Point2D]


class PolyLineList:
    type: str
    polygones: List[Polygone]


class AiHint:
    separators: List[PolyLine]
    directed_points: []
    polylines: List[PolyLine]
    polylines_list: List[PolyLineList]


class LightProbe:
    position: Point3D
    radius: float
    is_primary: bool
    height_mode: str


class TerrainStencilTriangle:
    position1: Point3D
    position2: Point3D
    position3: Point3D
    height_mode: str


class BuildingProjectileEmitter:
    position: Point3D
    direction = Point3D
    building_index: int
    height_mode = str


class PlayableArea:
    min_x: float
    min_y: float
    max_x: float
    max_y: float
    has_been_set: bool
    flags: Dict[str, bool]


class Prefab:
    buildings: List[Building]
    capture_locations: List[CaptureLocation]
    go_outlines: List[Outline]
    non_terrain_outlines: List[Outline]
    zones_templates: List[ZoneTemplate]
    prefab_instances: List[PrefabInstance]
    props: Dict[str, List[Prop]]
    particles: List[Particle]
    ai_hints: AiHint
    light_probes: List[LightProbe]
    terrain_stencil_triangle: List[TerrainStencilTriangle]
    point_lights: List[PointLight]
    building_projectile_emitters: List[BuildingProjectileEmitter]
    playable_area = PlayableArea
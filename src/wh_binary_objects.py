from typing import Dict, List

from app_typing import Matrix, Vector

from wh_common_objects import Point2D, Point3D, ColourRGBA, ColourRGB, Cube, Scale3D, Rotation3D


class BuildingProperty:
    starting_damage_unary: float
    building_id: str
    flags: Dict[str, bool]


class Building:
    building_key: str
    position_type: str
    building_id: str
    parent_id: int
    height_mode: str
    transform: Matrix
    properties: BuildingProperty



class Particle:
    model_name: str
    object_relation: str
    transform: Matrix
    emission_rate: float
    instance_name: str
    flags: Dict[str, bool]
    autoplay: bool
    pdlc_mask: int
    visible_in_shroud: bool


class Prop:
    key_index: int
    key: str
    transform: Matrix
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
    outline: Outline
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
    direction: Vector
    building_index: int
    height_mode: str


class PlayableArea:
    min_x: float
    min_y: float
    max_x: float
    max_y: float
    has_been_set: bool
    flags: Dict[str, bool]


class PrefabTreeProps:
    position: Point3D
    scale: float
    is_freeform: bool


class Tree:
    key: str
    props: List[PrefabTreeProps]


class CustomMaterialMesh:
    vertices: List[Point3D]
    indices: List[int]
    material: str
    height_mode = str


class RiverNode:
    width: float
    flow_speed: float
    vertex: Point3D

class SoundShape:
    key: str
    type: str
    points: List[Point3D]
    inner_radius: float
    outer_radius: float
    inner_cube: Cube
    outer_cube: Cube
    river_nodes: List[RiverNode]
    clamp_to_surface: bool
    height_mode: str
    campaign_type_mask: int
    pdlc_mask: int


class Boundary:
    positions: List[Point2D]
    type: str


class DeploymentZoneRegion:
    orientation: float
    snap_facing: bool
    id: int
    boundary_list: List[Boundary]


class DeploymentArea:
    category: str
    deployment_zone_regions: List


class Deployment:
    deployment_areas: List[DeploymentArea]


class CompositeScene:
    scene_file: str
    height_mode: str
    pdlc_mask: int
    flags: Dict[str, bool]
    transform: Matrix


class BMDData:
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


class Vegetation:
    trees: List[Tree]


class Prefab(BMDData):
    def __init__(self):
        super().__init__()


class MapData(BMDData):
    custom_material_meshes: List[CustomMaterialMesh]
    spot_lights: List[SpotLight]
    sound_shapes: List[SoundShape]
    deployment: List[Deployment]
    composite_scenes: List[CompositeScene]

from typing import Dict, List

from app_typing import Matrix, Vector


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


class Prefab:
    buildings: List[Building]
    props: Dict[str, List[Prop]]
    particles: List[Particle]
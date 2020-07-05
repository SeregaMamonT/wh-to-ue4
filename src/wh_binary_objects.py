from typing import Dict, List

from app_typing import Matrix, Vector


class Mesh:
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


class Prefab:
    meshes: List[Mesh]
    particles: List[Particle]
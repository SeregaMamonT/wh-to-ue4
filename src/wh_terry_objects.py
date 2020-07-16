from typing import Dict, List

from app_typing import Matrix, Vector


class ECTransform:
    position: List[float]
    rotation: List[float]
    scale: List[float]


class ECMeshRenderSettings:
    cast_shadow: bool


class ECTerrainClamp:
    terrain_clamp_active: bool
    clamp_to_sea_level: bool
    terrain_oriented: bool


class ECBattleProperties:
    allow_in_outfield: bool


class TerryBuilding:
    key: str
    damage: int
    indestructible: bool
    toggleable: bool
    capture_location: str
    export_as_prop: bool
    allow_in_outfield_as_prop: bool
    ectransform: ECTransform
    ecterrainclamp: ECTerrainClamp
    ecmeshrendersettings: ECMeshRenderSettings

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
from fastapi import APIRouter

from src.app.api.v1.endpoints import (
    dynamic_map_data,
    map_war_report,
    static_map_data,
    war_state,
    shards,
    hexes,
)

router = APIRouter()

router.include_router(hexes.router)
router.include_router(shards.router)
router.include_router(war_state.router)
router.include_router(map_war_report.router)
router.include_router(dynamic_map_data.router)
router.include_router(static_map_data.router)

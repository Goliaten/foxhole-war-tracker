from datetime import datetime
import logging
from typing import Any, Dict
from src.app.database.models import REV, Shard, WarState
from src.app.services import war_api_client
from src.app.database import crud
from src.app.database.session import AsyncSessionLocal

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


async def fetch_and_store_war_data(base_url: str):
    """
    High-level service function to orchestrate fetching and storing data.
    """
    logger.info("Starting data ingestion...")
    try:
        # 1. Fetch data from external API
        war_data = await war_api_client.get_current_war_data(base_url)

        if not war_data:
            logger.warning("No data received from War API.")
            return

        # 2. Get a new DB session
        async with AsyncSessionLocal() as db:
            rev = await crud.create_rev_and_get_id(db)

            shard = await crud.get_shard_by_url(db, base_url)

            # 3. Pass data to CRUD function to create or update
            await insert_scraped_data(db, war_data, rev, shard)
            logger.info(
                f"Successfully upserted War {war_data.get('war_state', {}).get('warNumber')}. "
                f"Shard {shard.name}"
            )

    except Exception as e:
        logger.error(f"Error during data ingestion: {e}", exc_info=True)


async def insert_scraped_data(db, war_data: Dict[str, Any], rev, shard) -> Any:
    logger.debug(f"war_data keys: {war_data.keys()}")

    for key, value in war_data.items():
        match key:
            case "war_state":
                print(f"{key} {value}")
                value = parse_war_state(value, rev, shard)
                await crud.upsert_warstate(db, value)
                print("inserted")
            case "map_list":
                ...
            case "map_war_report":
                ...
            case "static_map_data":
                ...
            case "dynamic_map_data":
                ...
            case _:
                logger.warning(f"Unknown key {key}")


def parse_war_state(data: WarState, rev: REV, shard: Shard) -> WarState:
    """
    Ensured date fields are of datetime format
    """
    fields = [
        "conquestStartTime",
        "conquestEndTime",
        "resistanceStartTime",
        "scheduledConquestEndTime",
    ]
    for field in fields:
        if field not in data:
            continue
        if not data[field]:
            continue
        data[field] = datetime.fromtimestamp(int(data[field] / 1000))

    data["REV"] = rev.REV
    data["shard_id"] = shard.id

    return data

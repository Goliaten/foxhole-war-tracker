from datetime import datetime
import logging
from typing import Any, Dict, List, Tuple
from src.app.database.models import REV, Hex, Shard
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
        mock = False
        if not mock:
            war_data = await war_api_client.get_current_war_data(base_url)
        else:
            with open("war_data.json", "r") as file:
                import json

                war_data = json.load(file)
                del json

        if not war_data:
            logger.warning("No data received from War API.")
            return

        # 2. Get a new DB session
        async with AsyncSessionLocal() as db:
            rev = await crud.create_rev_and_get_id(db)

            shard = await crud.get_shard(db, url=base_url)

            logger.info(
                f"Inserting data for shard {shard.name if shard else '_unknown_'}."
            )
            # 3. Pass data to CRUD function to create or update
            await insert_scraped_data(db, war_data, rev, shard)
            logger.info(
                f"Successfully upserted War {war_data.get('war_state', {}).get('warNumber')}. "
                f"Shard {shard.name if shard else '_unkown_'}"
            )

    except Exception as e:
        logger.error(f"Error during data ingestion: {e}", exc_info=True)


async def insert_scraped_data(
    db, war_data: Dict[str, Any], rev: REV, shard: Shard
) -> Any:
    hexes: List[Hex] = []

    for key, value in war_data.items():
        match key:
            case "war_state":
                logger.info("Inserting war state.")
                value = parse_war_state(value, rev, shard)
                await crud.upsert_warstate(db, value)

            case "map_list":
                logger.info("Inserting map list.")
                value = parse_map_list(value, rev)
                for hex in value:
                    try:
                        out_hex = await crud.upsert_hex(
                            db, hex, key_fields=["name"], strict_insert=True
                        )
                    except ValueError:
                        logger.debug(f"Hex {hex} is already in DB.")
                        out_hex = await crud.get_hex(db, name=hex["name"])
                    hexes.append(out_hex)

            case "map_war_report":
                logger.info("Inserting map war report.")
                value = parse_map_war_report(value, rev, shard, hexes)
                for mapwardata in value:
                    await crud.upsert_map_war_report(db, mapwardata)

            case "static_map_data":
                logger.info("Inserting static map data.")
                value = parse_static_map_data(value, rev, shard, hexes)
                for static_map_data in value:
                    out_static_data = await crud.upsert_static_map_data(
                        db, static_map_data[0], strict_insert=True
                    )
                    upsert_items = [
                        x | {"StaticMapData_id": out_static_data.id}
                        for x in static_map_data[1]
                    ]
                    for item in upsert_items:
                        await crud.upsert_static_map_data_item(
                            db, item, strict_insert=True
                        )

            case "dynamic_map_data":
                logger.info("Inserting dynamic map data.")
                value = parse_dynamic_map_data(value, rev, shard, hexes)
                for dynamic_map_data in value:
                    out_dynamic_data = await crud.upsert_dynamic_map_data(
                        db, dynamic_map_data[0], strict_insert=True
                    )
                    upsert_items = [
                        x | {"DynamicMapData_id": out_dynamic_data.id}
                        for x in dynamic_map_data[1]
                    ]
                    for item in upsert_items:
                        await crud.upsert_dynamic_map_data_item(
                            db, item, strict_insert=True
                        )

            case _:
                logger.warning(f"Unknown key {key}")


def parse_war_state(data: Dict[str, Any], rev: REV, shard: Shard) -> Dict[str, Any]:
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


def parse_map_list(data: List[Dict[str, Any]], rev: REV) -> List[Dict[str, Any]]:
    data = [{"id": None, "name": x, "REV": rev.REV} for x in data]
    return data


def parse_map_war_report(
    data: Dict[str, Dict[str, Any]], rev: REV, shard: Shard, hexes: List[Hex]
) -> List[Dict[str, Any]]:
    out = []
    for key, value in data.items():
        hex = [x for x in hexes if x.name == key][0]
        item = {
            "REV": rev.REV,
            "hex_id": hex.id,
            "shard_id": shard.id,
        } | value
        out.append(item)
    return out


def parse_static_map_data(
    data: Dict[str, Dict[str, Any]], rev: REV, shard: Shard, hexes: List[Hex]
) -> List[Tuple[Dict[str, Any], List[Dict[str, Any]]]]:
    out: List[Tuple[Dict[str, Any], List[Dict[str, Any]]]] = []

    for key, value in data.items():
        hex = [x for x in hexes if x.name == key][0]

        # adding id from other tables
        item: Dict[str, Any] = {
            "REV": rev.REV,
            "hex_id": hex.id,
            "shard_id": shard.id,
        } | value

        # removing unused data
        to_pop = ["mapItemsW", "mapItems", "lastUpdated", "mapItemsC"]
        for x in to_pop:
            item.pop(x)

        # separating sub-items
        try:
            data_items: List[Dict[str, Any]] = item.pop("mapTextItems")
        except (ValueError, IndexError):
            data_items = []

        for data_item in data_items:
            data_item |= {"REV": rev.REV}

        out.append((item, data_items))

    return out


def parse_dynamic_map_data(
    data: Dict[str, Dict[str, Any]], rev: REV, shard: Shard, hexes: List[Hex]
) -> List[Tuple[Dict[str, Any], List[Dict[str, Any]]]]:
    out: List[Tuple[Dict[str, Any], List[Dict[str, Any]]]] = []

    for key, value in data.items():
        hex = [x for x in hexes if x.name == key][0]

        # adding id from other tables
        item: Dict[str, Any] = {
            "REV": rev.REV,
            "hex_id": hex.id,
            "shard_id": shard.id,
        } | value

        # removing unused data
        to_pop = ["mapItemsW", "mapTextItems", "lastUpdated", "mapItemsC"]
        for x in to_pop:
            item.pop(x)

        # separating sub-items
        try:
            data_items: List[Dict[str, Any]] = item.pop("mapItems")
        except (ValueError, IndexError):
            data_items = []

        for data_item in data_items:
            data_item |= {"REV": rev.REV}

        out.append((item, data_items))

    return out

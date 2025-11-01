from asyncio import create_task
import asyncio
from typing import Any, Dict, List
import httpx

from src.app.schemas.warapiEndpointEnum import warapiEndpoints


async def get_current_war_data(base_url: str) -> dict:
    """
    Fetches the main /war endpoint from the external API.
    """
    async with httpx.AsyncClient() as client:
        try:
            if not touch_base_url(client, base_url):
                print(f"Server not available. {base_url}")
                raise
            out_json = {}
            out_json[warapiEndpoints.war_state.name] = await get_war_state(
                client, base_url
            )
            out_json[warapiEndpoints.map_list.name] = await get_map_list(
                client, base_url
            )

            out_json[warapiEndpoints.map_war_report.name] = await get_map_war_reports(
                client, base_url, out_json[warapiEndpoints.map_list.name]
            )
            out_json[warapiEndpoints.static_map_data.name] = await get_static_map_datas(
                client, base_url, out_json[warapiEndpoints.map_list.name]
            )
            out_json[
                warapiEndpoints.dynamic_map_data.name
            ] = await get_dynamic_map_datas(
                client, base_url, out_json[warapiEndpoints.map_list.name]
            )
            out_json[warapiEndpoints.map_data_schema.name] = await get_map_data_schemas(
                client, base_url, out_json[warapiEndpoints.map_list.name]
            )

            return out_json

        except httpx.HTTPStatusError as e:
            print(f"HTTP error occurred: {e}")
            raise
        except httpx.RequestError as e:
            print(f"An error occurred while requesting {e.request.url!r}: {e}")
            raise


def flatten_dict(dict_: List[Dict[Any, Any]]) -> Dict[Any, Any]:
    return {x: y for dct in dict_ for x, y in dct.items()}


async def touch_base_url(client: httpx.AsyncClient, base_url: str) -> Any:
    """
    Checks if `base_url` server is available
    """
    response = await client.get(f"{base_url}")
    if response.is_server_error:
        return False
    else:
        return True


async def get_war_state(client: httpx.AsyncClient, base_url: str) -> Any:
    """
    Gets state of the war
    """
    return await get_from_endpoint(client, base_url, warapiEndpoints.war_state.value)


async def get_map_list(client: httpx.AsyncClient, base_url: str) -> Any:
    """
    Gets list of maps
    """
    return await get_from_endpoint(client, base_url, warapiEndpoints.map_list.value)


async def get_map_war_reports(
    client: httpx.AsyncClient, base_url: str, maps: List[str]
) -> Any:
    """
    Gets static map data for all provided maps
    """

    tasks = [
        create_task(
            get_from_map_endpoint(
                client,
                base_url,
                warapiEndpoints.map_war_report.value.format(map_name=map_),
                map_,
            )
        )
        for map_ in maps
    ]
    return flatten_dict(await asyncio.gather(*tasks))


async def get_static_map_datas(
    client: httpx.AsyncClient, base_url: str, maps: List[str]
) -> Any:
    """
    Gets static map data for all provided maps
    """

    tasks = [
        create_task(
            get_from_map_endpoint(
                client,
                base_url,
                warapiEndpoints.static_map_data.value.format(map_name=map_),
                map_,
            )
        )
        for map_ in maps
    ]
    return flatten_dict(await asyncio.gather(*tasks))


async def get_dynamic_map_datas(
    client: httpx.AsyncClient, base_url: str, maps: List[str]
) -> Any:
    """
    Gets static map data for all provided maps
    """

    tasks = [
        create_task(
            get_from_map_endpoint(
                client,
                base_url,
                warapiEndpoints.dynamic_map_data.value.format(map_name=map_),
                map_,
            )
        )
        for map_ in maps
    ]
    return flatten_dict(await asyncio.gather(*tasks))


async def get_map_data_schemas(
    client: httpx.AsyncClient, base_url: str, maps: List[str]
) -> Any:
    """
    Gets static map data for all provided maps
    """

    tasks = [
        create_task(
            get_from_map_endpoint(
                client,
                base_url,
                warapiEndpoints.map_data_schema.value.format(map_name=map_),
                map_,
            )
        )
        for map_ in maps
    ]
    return flatten_dict(await asyncio.gather(*tasks))


async def get_from_endpoint(
    client: httpx.AsyncClient, base_url: str, endpoint: str
) -> Any:
    response = await client.get(f"{base_url}{endpoint}")
    response.raise_for_status()
    return response.json()


async def get_from_map_endpoint(
    client: httpx.AsyncClient, base_url: str, endpoint: str, map_: str
) -> Dict[str, Any]:
    response = await client.get(f"{base_url}{endpoint}")
    response.raise_for_status()
    return {map_: response.json()}

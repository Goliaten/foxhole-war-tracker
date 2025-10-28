import httpx
from src.app.core.config import settings

BASE_URL = settings.WAR_API_BASE_URL


async def get_current_war_data() -> dict:
    """
    Fetches the main /war endpoint from the external API.
    """
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(f"{BASE_URL}/worldconquest/war")

            # Raise an exception for bad status codes (4xx or 5xx)
            response.raise_for_status()

            return response.json()

        except httpx.HTTPStatusError as e:
            print(f"HTTP error occurred: {e}")
            raise
        except httpx.RequestError as e:
            print(f"An error occurred while requesting {e.request.url!r}: {e}")
            raise

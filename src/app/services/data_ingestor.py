import logging
from src.app.services import war_api_client
from src.app.database import crud
from src.app.database.session import AsyncSessionLocal

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


async def fetch_and_store_war_data():
    """
    High-level service function to orchestrate fetching and storing data.
    """
    logger.info("Starting data ingestion...")
    try:
        # 1. Fetch data from external API
        war_data = await war_api_client.get_current_war_data()

        if not war_data:
            logger.warning("No data received from War API.")
            return

        # 2. Get a new DB session
        async with AsyncSessionLocal() as db:
            # 3. Pass data to CRUD function to create or update
            war = await crud.create_or_update_war(db, war_data)
            logger.info(
                f"Successfully upserted War {war.war_number}. Winner: {war.winner}"
            )

    except Exception as e:
        logger.error(f"Error during data ingestion: {e}", exc_info=True)

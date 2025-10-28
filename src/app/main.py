import asyncio
import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI
from src.app.services.data_ingestor import fetch_and_store_war_data
from src.app.api.v1.endpoints import wars

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Polling interval (in seconds)
POLL_INTERVAL = 300  # 5 minutes


async def background_poller():
    """
    A simple background task that runs forever, polling the API.
    """
    logger.info("Background poller started.")
    while True:
        try:
            await fetch_and_store_war_data()
        except Exception as e:
            logger.error(f"Error in background poller: {e}", exc_info=True)

        logger.info(f"Polling complete. Sleeping for {POLL_INTERVAL} seconds.")
        await asyncio.sleep(POLL_INTERVAL)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    FastAPI lifespan manager. Runs on startup and shutdown.
    """
    # On startup
    logger.info("Application startup...")
    # Start the background task
    task = asyncio.create_task(background_poller())

    yield  # The application is now running

    # On shutdown
    logger.info("Application shutdown...")
    task.cancel()
    try:
        await task
    except asyncio.CancelledError:
        logger.info("Background poller successfully cancelled.")


# Initialize the FastAPI app
app = FastAPI(
    title="Foxhole War Tracker API",
    description="Tracks Foxhole war data and provides it via a local API.",
    version="0.1.0",
    lifespan=lifespan,
)

# Include the API router
app.include_router(wars.router, prefix="/api/v1/wars", tags=["Wars"])


@app.get("/health", tags=["Health"])
async def health_check():
    """
    Simple health check endpoint.
    """
    return {"status": "ok"}

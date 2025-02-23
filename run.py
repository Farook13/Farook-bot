import logging
from info import app

# Configure logging
logger = logging.getLogger(__name__)

if __name__ == "__main__":
    logger.info("Bot starting...")
    try:
        app.run()  # Start the bot defined in info.py
    except Exception as e:
        logger.error(f"Failed to start bot: {str(e)}")
    logger.info("Bot stopped.")
​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​
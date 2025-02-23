import os
import logging
from pyrogram import Client
from dotenv import load_dotenv

# Configure logging
logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

# Telegram API credentials
API_ID = os.getenv('12618934')
API_HASH = os.getenv('49aacd0bc2f8924add29fb02e20c8a16')
BOT_TOKEN = os.getenv('7857321740:AAEtcoE9BbLGCaF5TlkeGvhLZpXU36vco8E')

# MongoDB and OMDb credentials (passed to utils if needed)
MONGO_URI = os.getenv('mongodb+srv://saidalimuhamed88:iladias2025@cluster0.qt4dv.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0')
OMDB_API_KEY = os.getenv('OMDB_API_KEY')

# Initialize Pyrogram client
app = Client(
    "movie_bot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN
)

# Log startup info
logger.info("Initializing bot...")
logger.info(f"API_ID: {API_ID[:4]}... (masked)")
logger.info(f"API_HASH: {API_HASH[:4]}... (masked)")
logger.info(f"BOT_TOKEN: {BOT_TOKEN[:4]}... (masked)")
logger.info(f"MONGO_URI: {MONGO_URI[:10]}... (masked)")
logger.info(f"OMDB_API_KEY: {OMDB_API_KEY[:4]}... (masked)")

# Import bot handlers after app is defined
from bot import *

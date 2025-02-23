import logging
from pyrogram import Client, filters
from pyrogram.types import Message
from utils import get_movie_details, get_movie_file

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize Pyrogram client
app = Client(
    "movie_bot",
    api_id=os.getenv('API_ID'),
    api_hash=os.getenv('API_HASH'),
    bot_token=os.getenv('BOT_TOKEN')
)

# Start command
@app.on_message(filters.command("start") & filters.private)
async def start(client, message: Message):
    await message.reply_text("Welcome to the Movie Filter Bot! Send me a movie name to get details and a file (if available).")


​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​
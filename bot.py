import logging
from pyrogram import Client, filters
from pyrogram.types import Message
from utils import get_movie_details, get_movie_file

# Minimal logging for performance
logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s', level=logging.WARNING)
logger = logging.getLogger(__name__)

# Initialize Pyrogram client
app = Client(
    "movie_bot",
    api_id=os.getenv('API_ID'),
    api_hash=os.getenv('API_HASH'),
    bot_token=os.getenv('BOT_TOKEN')
)

# Start command - lightweight response
@app.on_message(filters.command("start") & filters.private)
async def start(client, message: Message):
    await message.reply_text("Welcome! Send a movie name for details and file.")

# Handle movie search with fast response
@app.on_message(filters.text & filters.private & ~filters.command)
async def filter_movie(client, message: Message):
    movie_name = message.text.lower().strip()

    # Fetch IMDb details (cached in MongoDB)
    imdb_info = await get_movie_details(movie_name)
    response_text = (
        f"**{imdb_info['title']} ({imdb_info['year']})**\n{imdb_info['plot']}"
        if imdb_info else f"No IMDb data for '{movie_name}'."
    )

    # Fetch movie file (async MongoDB query)
    file_stream, file_name = await get_movie_file(movie_name)
    
    if file_stream:
        try:
            await message.reply_text(response_text, parse_mode="markdown")
            await message.reply_document(document=file_stream, caption=f"Movie: {file_name}")
            file_stream.close()
        except Exception as e:
            await message.reply_text(f"{response_text}\nFile error: {str(e)}", parse_mode="markdown")
    else:
        await message.reply_text(f"{response_text}\nNo file found.", parse_mode="markdown")

# Minimal error handler
@app.on_message(filters.private)
async def error_handler(client, message: Message):
    logger.warning(f"Message error: {message.text}")
​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​
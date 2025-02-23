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

# Handle movie search, IMDb details, and file sending
@app.on_message(filters.text & filters.private & ~filters.command)
async def filter_movie(client, message: Message):
    movie_name = message.text.lower().strip()

    # Fetch IMDb details
    imdb_info = get_movie_details(movie_name)
    if imdb_info:
        response_text = f"**{imdb_info['title']} ({imdb_info['year']})**\n{imdb_info['plot']}"
    else:
        response_text = f"Couldn’t find IMDb details for '{movie_name}'."

    # Fetch movie file from MongoDB
    file_stream, file_name = get_movie_file(movie_name)
    
    if file_stream:
        try:
            # Send IMDb details first
            await message.reply_text(response_text, parse_mode="markdown")
            # Send the file
            await message.reply_document(
                document=file_stream,
                caption=f"Here’s your movie: {file_name}"
            )
            file_stream.close()
        except Exception as e:
            await message.reply_text(f"{response_text}\nError sending file: {str(e)}", parse_mode="markdown")
    else:
        await message.reply_text(f"{response_text}\nNo file available for this movie.", parse_mode="markdown")

# Error handler
@app.on_message(filters.private)
async def error_handler(client, message: Message):
    logger.warning(f"Error processing message: {message.text}")
​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​
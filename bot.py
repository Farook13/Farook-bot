import logging
from pyrogram import filters
from pyrogram.types import Message
from info import app  # Import app from info.py
from utils import get_movie_details, get_movie_file

# Minimal logging for performance
logger = logging.getLogger(__name__)

@app.on_message(filters.command("start") & filters.private)
async def start(client, message: Message):
    logger.info(f"Received /start from {message.from_user.id}")
    await message.reply_text("Welcome! Send a movie name for details and file.")

@app.on_message(filters.text & filters.private & ~filters.command("start"))
async def filter_movie(client, message: Message):
    movie_name = message.text.lower().strip()
    logger.info(f"Processing movie request: {movie_name}")
    imdb_info = await get_movie_details(movie_name)
    response_text = (
        f"**{imdb_info['title']} ({imdb_info['year']})**\n{imdb_info['plot']}"
        if imdb_info else f"No IMDb data for '{movie_name}'."
    )
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

@app.on_message(filters.private)
async def error_handler(client, message: Message):
    logger.warning(f"Message error: {message.text}")
​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​
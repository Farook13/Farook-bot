​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​import logging
from pyrogram import Client, filters
from pyrogram.types import Message
import pymongo
from pymongo import MongoClient
import gridfs
from io import BytesIO
import requests

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# Telegram API credentials
API_ID = 'YOUR_API_ID'        # Replace with your API ID
API_HASH = 'YOUR_API_HASH'    # Replace with your API Hash
BOT_TOKEN = 'YOUR_BOT_TOKEN'  # Replace with your Bot Token

# MongoDB connection
MONGO_URI = 'YOUR_MONGODB_URI'  # e.g., 'mongodb://localhost:27017'
client = MongoClient(MONGO_URI)
db = client['movie_bot']
fs = gridfs.GridFS(db)
movies_collection = db['movies']

# OMDb API key
OMDB_API_KEY = 'YOUR_OMDB_API_KEY'
OMDB_URL = 'http://www.omdbapi.com/'

# Initialize Pyrogram client
app = Client("movie_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

# Fetch movie details from OMDb API
def get_movie_details(movie_name):
    params = {
        't': movie_name,
        'apikey': OMDB_API_KEY
    }
    response = requests.get(OMDB_URL, params=params)
    data = response.json()
    
    if data.get('Response') == 'True':
        return {
            'title': data.get('Title'),
            'year': data.get('Year'),
            'plot': data.get('Plot'),
            'poster': data.get('Poster')
        }
    return None

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

    # Search MongoDB for the movie file
    movie = movies_collection.find_one({"title": {"$regex": movie_name, "$options": "i"}})
    
    if movie and 'file_id' in movie:
        try:
            # Retrieve file from GridFS
            file_data = fs.get(movie['file_id']).read()
            file_stream = BytesIO(file_data)
            file_stream.name = movie.get('filename', f"{movie['title']}.mp4")

            # Send IMDb details first
            await message.reply_text(response_text, parse_mode="markdown")
            
            # Send the file
            await message.reply_document(
                document=file_stream,
                caption=f"Here’s your movie: {movie['title']}"
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

# Run the bot
if __name__ == '__main__':
    print("Bot is running...")
    app.run()
​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​
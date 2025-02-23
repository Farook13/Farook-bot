import telegram
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import logging
import pymongo
from pymongo import MongoClient
import gridfs
from io import BytesIO

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# Bot token from BotFather
TOKEN = 'YOUR_BOT_TOKEN'

# MongoDB connection
MONGO_URI = 'YOUR_MONGODB_URI'  # e.g., 'mongodb://localhost:27017'
client = MongoClient(MONGO_URI)
db = client['movie_bot']  # Database name
fs = gridfs.GridFS(db)    # GridFS for handling large files
movies_collection = db['movies']  # Collection for metadata

# Start command
def start(update, context):
    update.message.reply_text("Welcome to the Movie Filter Bot! Send me a movie name to get its file.")

# Handle movie search and file sending
def filter_movie(update, context):
    movie_name = update.message.text.lower().strip()

    # Search MongoDB for the movie
    movie = movies_collection.find_one({"title": {"$regex": movie_name, "$options": "i"}})
    
    if movie:
        # Check if there's a file associated
        if 'file_id' in movie:
            try:
                # Retrieve file from GridFS
                file_data = fs.get(movie['file_id']).read()
                file_stream = BytesIO(file_data)
                file_stream.name = movie.get('filename', f"{movie['title']}.mp4")  # Default to .mp4 if no filename

                # Send the file to the user
                update.message.reply_document(document=file_stream, caption=f"Here’s your movie: {movie['title']}")
                file_stream.close()
            except Exception as e:
                update.message.reply_text(f"Error sending file: {str(e)}")
        else:
            update.message.reply_text(f"Found {movie['title']}, but no file is available.")
    else:
        update.message.reply_text(f"Sorry, I couldn’t find '{movie_name}' in the database. Try another!")

# Error handler
def error(update, context):
    logger.warning('Update "%s" caused error "%s"', update, context.error)

def main():
    # Create the Updater and pass it your bot's token
    updater = Updater(TOKEN, use_context=True)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # Add command and message handlers
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, filter_movie))

    # Log errors
    dp.add_error_handler(error)

    # Start the Bot
    updater.start_polling()
    print("Bot is running...")
    updater.idle()

if __name__ == '__main__':
    main()
​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​

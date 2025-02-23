import asyncio
import pymongo
from pymongo import MongoClient
import gridfs
from io import BytesIO
import requests
import os

# Persistent MongoDB client with connection pooling
client = MongoClient(os.getenv('MONGO_URI'), maxPoolSize=50)
db = client['movie_bot']
fs = gridfs.GridFS(db)
movies_collection = db['movies']
cache_collection = db['imdb_cache']  # Cache for IMDb data

# OMDb API settings
OMDB_API_KEY = os.getenv('OMDB_API_KEY')
OMDB_URL = 'http://www.omdbapi.com/'

# Async HTTP client for IMDb API
async def fetch_imdb_data(movie_name):
    params = {'t': movie_name, 'apikey': OMDB_API_KEY}
    loop = asyncio.get_event_loop()
    response = await loop.run_in_executor(None, lambda: requests.get(OMDB_URL, params=params))
    data = response.json()
    return data if data.get('Response') == 'True' else None

# Cached movie details with MongoDB
async def get_movie_details(movie_name):
    cached = cache_collection.find_one({"movie_name": movie_name})
    if cached and 'data' in cached:
        return cached['data']

    data = await fetch_imdb_data(movie_name)
    if data:
        result = {
            'title': data.get('Title'),
            'year': data.get('Year'),
            'plot': data.get('Plot'),
            'poster': data.get('Poster')
        }
        cache_collection.update_one(
            {"movie_name": movie_name},
            {"$set": {"data": result}},
            upsert=True
        )
        return result
    return None

# Async MongoDB file retrieval
async def get_movie_file(movie_name):
    movie = await movies_collection.find_one({"title": {"$regex": movie_name, "$options": "i"}})
    if movie and 'file_id' in movie:
        file_data = await asyncio.get_event_loop().run_in_executor(None, lambda: fs.get(movie['file_id']).read())
        file_stream = BytesIO(file_data)
        file_stream.name = movie.get('filename', f"{movie['title']}.mp4")
        return file_stream, movie['title']
    return None, None
​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​
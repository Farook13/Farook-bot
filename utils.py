import pymongo
from pymongo import MongoClient
import gridfs
from io import BytesIO
import requests
import os

# MongoDB connection
client = MongoClient(os.getenv('MONGO_URI'))
db = client['movie_bot']
fs = gridfs.GridFS(db)
movies_collection = db['movies']

# OMDb API settings
OMDB_API_KEY = os.getenv('OMDB_API_KEY')
OMDB_URL = 'http://www.omdbapi.com/'

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

# Fetch movie file from MongoDB
def get_movie_file(movie_name):
    movie = movies_collection.find_one({"title": {"$regex": movie_name, "$options": "i"}})
    if movie and 'file_id' in movie:
        file_data = fs.get(movie['file_id']).read()
        file_stream = BytesIO(file_data)
        file_stream.name = movie.get('filename', f"{movie['title']}.mp4")
        return file_stream, movie['title']
    return None, None
​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​

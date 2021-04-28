from LVL import get_data_file #  Pylint in vsc doesn't like this for some reason... pylint: disable=import-error
import os
import shutil
import requests
import json

OMDB_API_KEY = 'e945ee0b' # Should we really be hardcoding this?
POSTER_STORAGE_PATH = get_data_file('posters')

if not os.path.exists(POSTER_STORAGE_PATH):
    os.makedirs(POSTER_STORAGE_PATH)

def get_poster_file(imdb_id):
    return os.path.join(POSTER_STORAGE_PATH, imdb_id)

def update_poster_file(imdb_id, new_file):
    # Copy the new file to the existing path
    return shutil.copy(new_file, get_poster_file(imdb_id))

def download_poster(imdb_id):
    # This should be delegated to an OMDB API Helper class
    omdb_api_url = f"https://www.omdbapi.com/?apikey={OMDB_API_KEY}&i={imdb_id}"
    with requests.get(omdb_api_url) as resp:
        raw_json = resp.content.decode('utf-8')
        media = json.loads(raw_json)
    poster_url = media['Poster']
    print(f"Downloading poster from {poster_url}")
    with requests.get(poster_url) as req:
        with open(get_poster_file(imdb_id), 'wb') as f:
            f.write(req.content)
    print(f"Downloaded poster for {imdb_id} to {get_poster_file(imdb_id)}")

if __name__ == "__main__":
    download_poster("tt0368226")

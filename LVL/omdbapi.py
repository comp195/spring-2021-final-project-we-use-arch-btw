from LVL.Media.state import State
from LVL.Media.media import Media
import requests
import json

_API_KEY = 'e945ee0b'
_OMDB_API_URL = f"https://www.omdbapi.com/?apiKey={_API_KEY}"

def make_omdb_request(request: dict) -> str:
    params = ''
    for k, v in request.items():
        params += f"&{k}={v}"
    with requests.get(f"{_OMDB_API_URL}{params}") as resp:
        raw_resp = resp.content.decode('utf-8')
        if resp.status_code != 200:
            raise Exception(f"Exception querying OMDB. Code: {resp.status_code}, {raw_resp}")
        resp_json = json.loads(raw_resp)
        return resp_json

def omdb_search(title: str, year: str = None):
    return make_omdb_request({
        't': title,
        'y': year
    } if year is not None else {
        't': title
    })

def omdb_get(imdb_id: str):
    return make_omdb_request({
        'i': imdb_id
    })

def parse_result(result: dict) -> Media:
    return Media(
        result['imdbID'], 
        result['Title'], 
        result['Year'], 
        result['Rated'], 
        result['Genre'], 
        result['Plot'], 
        get_rotten_tomatoes(result['Ratings']),
        None, 
        result['Runtime'], 
        State.UNWATCHED, 
        0)

def get_rotten_tomatoes(ratings):
    for i in ratings:
        if i['Source'] == 'Rotten Tomatoes':
            return(i['Value'])
    return "-"

def search_by_title(title):
    # For Searching. returns tuple of [title, id] if hits, otherwise None
    results = make_omdb_request({'s': title})
    if results["Response"] == "False":
        return None
    movie_list = []
    for i in results['Search']:
        if i["Type"] == "movie":
            movie_list.append([i["Title"], i["imdbID"], i["Year"]])
    return(movie_list)

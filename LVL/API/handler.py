import requests
import json

OMDB_API_KEY = 'e945ee0b' # Should we really be hardcoding this? No, but yes

def search_by_title(title):
    # For Searching. returns tuple of [title, id] if hits, otherwise None
    omdb_api_url = f"https://www.omdbapi.com/?apikey={OMDB_API_KEY}&s=\"{title}\""
    # print(omdb_api_url)
    with requests.get(omdb_api_url) as resp:
        raw_json = resp.content.decode('utf-8')
        results = json.loads(raw_json)
    if results["Response"] == "False":
        return None
    movie_list = []
    for i in results['Search']:
        if i["Type"] == "movie":
            movie_list.append([i["Title"], i["imdbID"]])
    return(movie_list)


if __name__ == "__main__":
    print(search_by_title("WWWWWWWWWWWWWWWWW"))
    print(search_by_title("Wall E"))
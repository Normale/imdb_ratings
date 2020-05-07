from requests import get, post
from typing import Tuple, List
import json


key = ""
data = []
question = "Friends"

def search_title(title: str) -> Tuple[str, int]:
    response_search = get('http://www.omdbapi.com/', params={
        't': f"{title}",
        'ApiKey': key
    })
    parsed = json.loads(response_search.text)
    try:
        id: str = parsed["imdbID"]
        no_seasons: int = int(parsed["totalSeasons"])
    except:
        print(parsed)
    return id, no_seasons



def get_episodes_data(id: str, no_seasons: int):
    for season_nr in range(1, no_seasons + 1):
        response = get('http://www.omdbapi.com/', params={
            'i': id,
            'Season': season_nr,
            'ApiKey': key
        })
        parsed = json.loads(response.text)
        print(f"SEZON {season_nr}")
        data.append(parsed["Episodes"])
    for season in data:
        for element in season:
            # print(element["Episode"], element["imdbRating"], element["Title"])
            print(element)
    return data

def get_series_data(title: str, api_key: str) -> List[List[dict]]:
    try:
        id, no_seasons = search_title(title)
    except:
        print("Not Found")
        return None
    try:
        get_episodes_data(id, no_seasons)
    except:
        print("Internal server error")
        return None



if __name__ == "__main__":
    key = "" #omdb key, private
    data = []
    question = "Friends"
    id, no_seasons = search_title(question)
    data = get_episodes_data(id, no_seasons)
    

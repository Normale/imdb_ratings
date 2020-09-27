from requests import get, post
from typing import Tuple, List
import json

DEFAULTKEY = "fd10716c"

def get_json(*args, **kwargs):
    response = get(*args, **kwargs)
    parsed = json.loads(response.text)
    return parsed


def search_title(title: str, key: str) -> Tuple[str, int]:
    parsed = get_json('http://www.omdbapi.com/', params={
        't': f"{title}",
        'ApiKey': key
    })
    try:
        id: str = parsed["imdbID"]
        no_seasons: int = int(parsed["totalSeasons"])
    except:
        print("spadłem z rowerka")
        print(parsed)
    return id, no_seasons


def get_episodes_data(id: str, no_seasons: int, key: str=DEFAULTKEY):
    data = []
    for season_nr in range(1, no_seasons + 1):
        parsed = get_json('http://www.omdbapi.com/', params={
                'i': id,
                'Season': season_nr,
                'ApiKey': key
            })
        data.append(parsed["Episodes"])
    return data


def get_series_data(title: str, api_key: str=DEFAULTKEY) -> List[List[dict]]:
    try:
        id, no_seasons = search_title(title, api_key)
        print(id, no_seasons)
    except:
        print("Not Found")
        return None
    try:
        result = get_episodes_data(id, no_seasons, api_key)
    except:
        print("Internal server error")
        return None
    return result



if __name__ == "__main__":
    key = "fd10716c"
    data = []
    question = "Friends"
    id, no_seasons = search_title(question,key)
    data = get_episodes_data(id, no_seasons, key)
    print(data)
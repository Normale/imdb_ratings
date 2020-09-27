from requests import get, post
from typing import Tuple, List
import json

DEFAULTKEY = "fd10716c"

def get_json(**kwargs) -> dict:
    response = get('http://www.omdbapi.com/', **kwargs)
    parsed = json.loads(response.text)
    return parsed


def exception_returns_none(func):
    def wrapper(*args, **kwargs):
        try:
          return func(*args, **kwargs)
        except:
          return None
    return wrapper

@exception_returns_none
def search_title(title: str, key: str) -> Tuple[str, int]:
    parsed = get_json(params={
        't': f"{title}",
        'ApiKey': key
    })
    id: str = parsed["imdbID"]
    no_seasons: int = int(parsed["totalSeasons"])
    
    return id, no_seasons


@exception_returns_none
def get_episodes_data(id: str, no_seasons: int, key: str=DEFAULTKEY):
    data = []
    for season_nr in range(1, no_seasons + 1):
        parsed = get_json(params={
                'i': id,
                'Season': season_nr,
                'ApiKey': key
            })
        data.append(parsed["Episodes"])
    return data


@exception_returns_none
def get_series_data(title: str, api_key: str=DEFAULTKEY) -> List[List[dict]]:
    id, no_seasons = search_title(title, api_key)
    print(title, id, no_seasons)

    result = get_episodes_data(id, no_seasons, api_key)
    return result


if __name__ == "__main__":
    key = "fd10716c"
    data = []
    question = "Friends"
    id, no_seasons = search_title(question,key)
    data = get_episodes_data(id, no_seasons, key)
    # print(data)

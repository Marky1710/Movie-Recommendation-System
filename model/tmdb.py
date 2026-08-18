import os
import requests
from dotenv import load_dotenv

load_dotenv()

TMDB_API_KEY = os.getenv("TMDB_API_KEY")

BASE_URL = "https://api.themoviedb.org/3"
IMAGE_URL = "https://image.tmdb.org/t/p/w500"


def get_movie_details(movie_title):

    url = f"{BASE_URL}/search/movie"

    params = {
        "api_key": TMDB_API_KEY,
        "query": movie_title
    }

    response = requests.get(url, params=params)

    if response.status_code != 200:
        return None

    data = response.json()

    if not data["results"]:
        return None

    movie = data["results"][0]

    return {
        "title": movie.get("title"),
        "rating": movie.get("vote_average", 0),
        "overview": movie.get("overview", ""),
        "poster": (
            IMAGE_URL + movie["poster_path"]
            if movie.get("poster_path")
            else None
        )
    }

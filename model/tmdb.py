import os
import time
import socket
import requests
from dotenv import load_dotenv
import urllib3.util.connection as urllib3_connection

load_dotenv()

TMDB_API_KEY = os.getenv("TMDB_API_KEY")

BASE_URL = "https://api.themoviedb.org/3"
IMAGE_URL = "https://image.tmdb.org/t/p/w500"


# Force urllib3 to use IPv4
urllib3_connection.allowed_gai_family = lambda: socket.AF_INET


def get_movie_details(movie_title):

    url = f"{BASE_URL}/search/movie"

    params = {
        "api_key": TMDB_API_KEY,
        "query": movie_title
    }

    for attempt in range(3):

        try:
            response = requests.get(
                url,
                params=params,
                timeout=10
            )

            if response.status_code == 200:

                data = response.json()
                results = data.get("results", [])

                if not results:
                    return None

                # Find exact title match first
                selected_movie = None

                for movie in results:
                    title = movie.get("title", "")

                    if title.lower() == movie_title.lower():
                        selected_movie = movie
                        break

                # If exact match is unavailable,
                # use the first result
                if selected_movie is None:
                    selected_movie = results[0]

                return {
                    "title": selected_movie.get("title"),
                    "rating": selected_movie.get("vote_average", 0),
                    "release_date": selected_movie.get("release_date", ""),
                    "overview": selected_movie.get("overview", ""),
                    "poster": (
                        IMAGE_URL + selected_movie["poster_path"]
                        if selected_movie.get("poster_path")
                        else None
                    )
                }

            print(
                f"TMDB request failed for {movie_title} "
                f"(Attempt {attempt + 1}/3)"
            )

        except requests.exceptions.RequestException as e:

            print(
                f"TMDB API Error for {movie_title} "
                f"(Attempt {attempt + 1}/3): {e}"
            )

        if attempt < 2:
            time.sleep(2 ** attempt)

    return None
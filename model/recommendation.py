import ast
import pandas as pd

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


# -----------------------------
# Load Dataset
# -----------------------------

movies = pd.read_csv("data/tmdb_5000_movies.csv")
credits = pd.read_csv("data/tmdb_5000_credits.csv")


# -----------------------------
# Merge Movies and Credits
# -----------------------------

movies = movies.merge(
    credits,
    left_on="id",
    right_on="movie_id"
)


# -----------------------------
# Select Required Columns
# -----------------------------

movies = movies[
    [
        "movie_id",
        "title_x",
        "overview",
        "genres",
        "keywords",
        "cast",
        "crew"
    ]
]

movies.rename(columns={"title_x": "title"}, inplace=True)


# -----------------------------
# Convert Genres / Keywords
# -----------------------------

def convert_features(text):
    result = []

    for item in ast.literal_eval(text):
        result.append(item["name"])

    return result


movies["genres"] = movies["genres"].apply(convert_features)
movies["keywords"] = movies["keywords"].apply(convert_features)


# -----------------------------
# Convert Cast
# -----------------------------

def convert_cast(text):
    result = []

    for item in ast.literal_eval(text):
        result.append(item["name"])

    return result[:3]


movies["cast"] = movies["cast"].apply(convert_cast)


# -----------------------------
# Get Director
# -----------------------------

def get_director(text):

    for item in ast.literal_eval(text):

        if item["job"] == "Director":
            return item["name"]

    return ""


movies["crew"] = movies["crew"].apply(get_director)

movies.rename(columns={"crew": "director"}, inplace=True)


# -----------------------------
# Handle Missing Overview
# -----------------------------

movies["overview"] = movies["overview"].fillna("")


# -----------------------------
# Create Combined Tags
# -----------------------------

def create_tags(row):

    return (
        row["overview"]
        + " "
        + " ".join(row["genres"])
        + " "
        + " ".join(row["keywords"])
        + " "
        + " ".join(row["cast"])
        + " "
        + row["director"]
    )


movies["tags"] = movies.apply(create_tags, axis=1)

movies["tags"] = movies["tags"].str.lower()


# -----------------------------
# TF-IDF
# -----------------------------

tfidf = TfidfVectorizer(
    max_features=5000,
    stop_words="english"
)

tfidf_matrix = tfidf.fit_transform(movies["tags"])


# -----------------------------
# Cosine Similarity
# -----------------------------

similarity = cosine_similarity(tfidf_matrix)


# -----------------------------
# Recommendation Function
# -----------------------------

def recommend(movie_title):

    movie_title = movie_title.strip().lower()
    movie_matches = movies[
        movies["title"].str.lower().str.strip() == movie_title
    ]

    if movie_matches.empty:
        return []

    movie_index = movie_matches.index[0]

    similarity_scores = list(
        enumerate(similarity[movie_index])
    )

    similarity_scores = sorted(
        similarity_scores,
        key=lambda x: x[1],
        reverse=True
    )

    recommendations = []

    for i, score in similarity_scores[1:11]:

        recommendations.append(
            movies.iloc[i]["title"]
        )

    return recommendations
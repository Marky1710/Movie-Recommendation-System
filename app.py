from flask import Flask, render_template, request

from model.recommendation import recommend
from model.tmdb import get_movie_details


app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])
def home():

    recommendations = []
    movie_title = ""

    if request.method == "POST":

        movie_title = request.form.get("movie_title")

        if movie_title:

            movie_names = recommend(movie_title)

            print("Movie:", movie_title)
            print("Recommended movie names:", movie_names)

            for movie in movie_names:

                details = get_movie_details(movie)

                if details:
                    recommendations.append(details)

            print("Movie details:", recommendations)

    return render_template(
        "index.html",
        recommendations=recommendations,
        movie_title=movie_title
    )


if __name__ == "__main__":
    app.run(debug=True)

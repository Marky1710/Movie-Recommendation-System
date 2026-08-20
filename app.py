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

            for movie in movie_names:

                details = get_movie_details(movie)

                if details:
                    recommendations.append(details)

                if len(recommendations) == 10:
                    break

    return render_template(
        "index.html",
        recommendations=recommendations,
        movie_title=movie_title
    )


if __name__ == "__main__":
    app.run(debug=True)
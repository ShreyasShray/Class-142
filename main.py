from flask import Flask, jsonify, request
import csv
from demographic_filtering import output
from content_based_filtering import get_recommendation

all_movies = []

with open("final.csv") as f:
    reader = csv.reader(f)
    data = list(reader)
    all_movies = data[1:]

liked_movies = []
unliked_movies = []
not_watch = []

app = Flask(__name__)

@app.route("/get-movies")
def get_movies():
    return jsonify({
        "data":all_movies[0],
        "status":"success"
    })

@app.route("/liked-movies", methods = ["POST"])
def liked_movies():
    movie = all_movies[0]
    all_movies = all_movies[1:]
    liked_movies.append(movie)
    return jsonify({
        "status":"success"
    }), 201

@app.route("/unliked-movies", methods = ["POST"])
def unliked_movies():
    movie = all_movies[0]
    all_movies = all_movies[1:]
    unliked_movies.append(movie)
    return jsonify({
        "status":"success"
    }), 201

@app.route("/not-watch-movies", methods = ["POST"])
def not_watch_movies():
    movie = all_movies[0]
    all_movies = all_movies[1:]
    not_watch.append(movie)
    return jsonify({
        "status":"success"
    }), 201

@app.route("/popular-movies")
def popular_movies():
    movie_data = []
    for movie in output:
        _d = {
            "title":movie[0],
            "poster_link":movie[3],
            "release_date":movie[4] or "N/A",
            "duration":movie[6],
            "rating":movie[2],
            "over_view":movie[5]
        }
        movie_data.append(_d)

    return jsonify({
        "data":movie_data,
        "status":"success"
    }), 200

@app.route("/recommended-movies")
def recommended_movies():
    all_recommended = []
    for liked_movie in liked_movies:
        output = get_recommendation(liked_movie[19])
        for data in output:
            all_recommended.append(data)
    import itertools
    all_recommended.sort()
    all_recommended = list(all_recommended for all_recommended,_ in itertools.groupby(all_recommended))
    movie_data = []
    for recommended in all_recommended:
        _d = {
            "title":recommended[0],
            "poster_link":recommended[3],
            "release_date":recommended[4] or "N/A",
            "duration":recommended[6],
            "rating":recommended[2],
            "over_view":recommended[5]
        }
        movie_data.append(_d)
    return jsonify({
        "data":movie_data,
        "status":"success"
    }), 200

if(__name__ == "__main__"):
    app.run()
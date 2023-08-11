from pymongo import MongoClient, DESCENDING, ASCENDING
from flask import Flask, render_template, jsonify, request
app = Flask(__name__)
client = MongoClient('mongodb://lurgi:doubleu!2@52.79.132.116/', 27017)
db = client.jungle


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/movies/like", methods=["GET"])
def listingLike():
    movies = list(db.movies.find({"is_deleted": False}, {
                  "_id": False}).sort("likes", DESCENDING))
    return jsonify({"ok": True, "movies": movies})


@app.route("/movies/view", methods=["GET"])
def listingView():
    movies = list(db.movies.find({"is_deleted": False}, {"_id": False}
                                 ).sort("views_num", DESCENDING))
    return jsonify({"ok": True, "movies": movies})


@app.route("/movies/open", methods=["GET"])
def listingOpen():
    movies = list(db.movies.find({"is_deleted": False}, {"_id": False}).sort(
        [("open_year", ASCENDING), ("open_month", ASCENDING), ("open_day", ASCENDING)]))
    return jsonify({"ok": True, "movies": movies})


@app.route("/movies/delete", methods=["GET"])
def listingDelete():
    movies = list(db.movies.find({"is_deleted": True}, {
                  "_id": False}).sort("likes", DESCENDING))
    return jsonify({"ok": True, "movies": movies})


@app.route("/like", methods=["POST"])
def likeMovie():
    request_title = request.form["title"]
    db.movies.update_one({"title": request_title}, {'$inc': {'likes': 1}})
    return jsonify({"ok": True})


@app.route("/delete", methods=["POST"])
def deleteMovie():
    request_title = request.form["title"]
    bol = db.movies.find_one({"title": request_title})['is_deleted']
    db.movies.update_one({"title": request_title}, {
                         '$set': {'is_deleted': not bol}})
    return jsonify({"ok": True})


if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)

from flask import Flask, render_template
from flask_cors import CORS

from routes.game import add_game, get_games, move_game, remove_game, search
from routes.user import auth, create, login

# Sets up flask app and routes
app = Flask(__name__)
CORS(app)
app.add_url_rule("/api/login", view_func=login, methods=["POST"])
app.add_url_rule("/api/create", view_func=create, methods=["POST"])
app.add_url_rule("/api/auth", view_func=auth, methods=["POST"])
app.add_url_rule("/api/search", view_func=search, methods=["POST"])
app.add_url_rule("/api/add", view_func=add_game, methods=["POST"])
app.add_url_rule("/api/remove", view_func=remove_game, methods=["POST"])
app.add_url_rule("/api/games", view_func=get_games, methods=["POST"])
app.add_url_rule("/api/move", view_func=move_game, methods=["POST"])


@app.route("/")
def index_page():
    return render_template("index.html")


@app.route("/games")
def games():
    return render_template("games.html")


@app.route("/search")
def search_page():
    return render_template("search.html")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="9001")

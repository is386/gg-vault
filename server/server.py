from flask import Flask

from routes.game import add_game, search
from routes.user import auth, create, login

# Sets up flask app and routes
app = Flask(__name__)
app.add_url_rule("/login", view_func=login, methods=["POST"])
app.add_url_rule("/create", view_func=create, methods=["POST"])
app.add_url_rule("/auth", view_func=auth, methods=["POST"])
app.add_url_rule("/search", view_func=search, methods=["POST"])
app.add_url_rule("/add", view_func=add_game, methods=["POST"])
# TODO: Get games endpoint   - in: user id     out: multiple games and data
# TODO: Add game endpoint    - in: game id
# TODO: Remove game endpoint - in: game id
# TODO: Move game endpoint   - in: game id


@app.route("/")
def index():
    return "Index Page"


if __name__ == "__main__":
    app.run(host="localhost", port=8080, debug=True)

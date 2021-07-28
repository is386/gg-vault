import bcrypt
from flask import Flask, Response, g, request
from markupsafe import escape

from db import Database

app = Flask(__name__)

user_min: int = 1
user_max: int = 20
pass_min: int = 5
pass_max: int = 36
db: Database = Database("data/games.db")


def validAcctBody() -> bool:
    return ("username" in request.form.keys() and
            "password" in request.form.keys() and
            len(request.form["username"]) >= user_min and
            len(request.form["username"]) <= user_max and
            len(request.form["password"]) >= pass_min and
            len(request.form["password"]) <= pass_max)


@app.route("/")
def index():
    return "Index Page"


@app.route("/create", methods=["POST"])
def create_account():
    # Returns 401 if the body does not contain valid data
    if not validAcctBody():
        return Response("{'error': 'invalid body'}", status=401)

    # Returns 401 if the user name is taken
    user: str = str(request.form["username"])
    if db.user_exists(user):
        return Response("{'error': 'username taken'}", status=401)

    # Hashes the given password and inserts it into the db
    pw: bytes = request.form["password"].encode("utf-8")
    hashed: bytes = bcrypt.hashpw(pw, bcrypt.gensalt())
    db.insert_user(user, hashed)

    return Response(status=200)


@app.route("/login", methods=["POST"])
def login():
    # Returns 401 if the body does not contain valid data
    if not validAcctBody():
        return Response("{'error': 'invalid body'}", status=401)

    # Returns 401 if the user name does not exist
    user: str = str(request.form["username"])
    if not db.user_exists(user):
        return Response("{'error': 'username does not exist'}", status=401)

    # Check if the given password matches whats in the DB
    pw: bytes = request.form["password"].encode("utf-8")
    hashed: bytes = db.get_pass(user)
    if not bcrypt.checkpw(pw, hashed):
        return Response("{'error': 'wrong password'}", status=403)

    return Response(status=200)


@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, "_database", None)
    if db is not None:
        db.close()


if __name__ == "__main__":
    app.run(host="localhost", port=8080, debug=True)

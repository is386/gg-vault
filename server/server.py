import json

import bcrypt
import jwt
from flask import Flask, Response, g, request

from db import Database

app = Flask(__name__)

user_min: int = 1
user_max: int = 20
pass_min: int = 5
pass_max: int = 36
db: Database = Database("data/games.db")

# Gets the environment variables from env.json
with open("env.json") as f:
    env_data: dict = json.load(f)


# Checks if the body contains a valid username and password
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

    # Sign a user token for auth
    token: bytes = jwt.encode(
        payload={"username": user}, key=env_data["access_token_secret"])
    return Response("{'token': %s}" % token.decode("utf-8"), status=200)


@app.route("/auth", methods=["POST"])
def auth():
    # TODO: Check if header exists
    auth_header = request.headers.get("authorization")

    # TODO: Check if auth header has proper format
    token: str = auth_header.split(" ")[1]
    payload: dict = jwt.decode(token, key=env_data["access_token_secret"])

    # TODO Check if payload has username
    user: str = payload["username"]
    if not db.user_exists(user):
        return Response("{'error': 'username does not exist'}", status=401)

    return Response(status=200)


@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, "_database", None)
    if db is not None:
        db.close()


if __name__ == "__main__":
    app.run(host="localhost", port=8080, debug=True)

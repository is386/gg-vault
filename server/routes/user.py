import json

import bcrypt
import jwt
from flask import Response, request
from utils.db import Database

user_min: int = 1
user_max: int = 20
pass_min: int = 5
pass_max: int = 36

# Gets the environment variables from env.json
with open("env.json") as f:
    env: dict = json.load(f)

path: str = env["db_path"]
secret: str = env["access_token_secret"]


# Checks if the body contains a valid username and password
def validAcctBody() -> bool:
    return ("username" in request.form.keys() and
            "password" in request.form.keys() and
            len(request.form["username"]) >= user_min and
            len(request.form["username"]) <= user_max and
            len(request.form["password"]) >= pass_min and
            len(request.form["password"]) <= pass_max)


def create() -> Response:
    # Returns 401 if the body does not contain valid data
    if not validAcctBody():
        return Response("{'error': 'invalid body'}", status=400)

    # Returns 401 if the user name is taken
    user: str = str(request.form["username"])
    db: Database = Database(path)
    if db.user_exists(user):
        return Response("{'error': 'username taken'}", status=400)

    # Hashes the given password and inserts it into the db
    pw: bytes = request.form["password"].encode("utf-8")
    hashed: bytes = bcrypt.hashpw(pw, bcrypt.gensalt())
    db.insert_user(user, hashed)

    db.close()
    return Response(status=200)


def login() -> Response:
    # Returns 401 if the body does not contain valid data
    if not validAcctBody():
        return Response("{'error': 'invalid body'}", status=400)

    # Returns 401 if the user name does not exist
    user: str = str(request.form["username"])
    db: Database = Database(path)
    if not db.user_exists(user):
        return Response("{'error': 'username does not exist'}", status=400)

    # Check if the given password matches whats in the DB
    pw: bytes = request.form["password"].encode("utf-8")
    hashed: bytes = db.get_pass(user)
    if not bcrypt.checkpw(pw, hashed):
        return Response("{'error': 'wrong password'}", status=403)

    # Sign a user token for auth
    token: bytes = jwt.encode(
        payload={"username": user}, key=secret)

    db.close()
    return Response("{'token': %s}" % token.decode("utf-8"), status=200)


def auth() -> Response:
    if not authenticate():
        return Response("{'error': 'not authorized'}", status=401)
    return Response(status=200)


def authenticate() -> str:
    # TODO: Check if header exists
    auth_header = request.headers.get("authorization")

    # TODO: Check if auth header has proper format
    token: str = auth_header.split(" ")[1]
    payload: dict = jwt.decode(token, key=secret)

    # TODO Check if payload has username
    user: str = payload["username"]
    db: Database = Database(path)
    if not db.user_exists(user):
        return None

    db.close()
    return user

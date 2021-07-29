import json

import requests
from flask import Response, request
from utils.db import Database

from routes.user import authenticate

with open("env.json") as f:
    env: dict = json.load(f)

path: str = env["db_path"]
client_id: str = env["client_id"]
bearer: str = "Bearer {}".format(env["bearer"])
headers: dict = {"Client-ID": client_id, "Authorization": bearer}
url: str = "https://api.igdb.com/v4/games"
search_body: str = "fields name,genres.name,rating,cover.url; search \"{}\"; limit 10;"
get_body: str = "where id = {}; fields name,genres.name,rating,cover.url;"


def search() -> Response:
    # Checks if the request has the proper form
    if "query" not in request.form.keys():
        return Response("{'error': 'invalid body'}", status=400)

    # Sends the search query to the IGDB API
    query: str = str(request.form["query"])
    body: str = search_body.format(query)
    resp: requests.Response = requests.post(url, data=body, headers=headers)

    # Respond with error if the IGDB request fails
    if (resp.status_code != 200):
        return Response("{'error': 'IGDB error'}", status=500)

    # Respond with error if there were no search results
    if not len(resp.json()):
        return Response("{'error': 'no results'}", status=400)

    return Response(json.dumps(resp.json()), status=resp.status_code)


def add_game() -> Response:
    wishlist: bool = False

    # Gets the user name based on the access token
    user: str = authenticate()
    if not user:
        return Response("{'error': 'not authorized'}", status=403)

    # Checks if the request has the proper form
    if "game_id" not in request.form.keys():
        return Response("{'error': 'invalid body'}", status=400)

    # Checks if the given game id is an integer
    try:
        game_id: int = int(request.form["game_id"])
    except ValueError:
        return Response("{'error': 'game_id not integer'}", status=400)

    # Checks if the given game id exists in the IGDB
    body: str = get_body.format(game_id)
    resp: requests.Response = requests.post(url, data=body, headers=headers)

    # Respond with error if the IGDB request fails
    if (resp.status_code != 200):
        return Response("{'error': 'IGDB error'}", status=500)

    # Respond with error if the game id does not exist
    if not len(resp.json()):
        return Response("{'error': 'game id doesn't exist'}", status=400)

    # Checks if the request is for a wishlist game
    if "wishlist" in request.form.keys():
        wishlist = True

    # Inserts the game into the db for the given user
    db: Database = Database(path)
    user_id: int = db.get_user_id(user)
    db.insert_game(user_id, game_id, wishlist)

    return Response(status=200)


def remove_game() -> Response:
    # Gets the user name based on the access token
    user: str = authenticate()
    if not user:
        return Response("{'error': 'not authorized'}", status=403)

    # Checks if the request has the proper form
    if "game_id" not in request.form.keys():
        return Response("{'error': 'invalid body'}", status=400)

    # Checks if the given game id is an integer
    try:
        game_id: int = int(request.form["game_id"])
    except ValueError:
        return Response("{'error': 'game_id not integer'}", status=400)

    # Inserts the game into the db for the given user
    db: Database = Database(path)
    user_id: int = db.get_user_id(user)
    db.delete_game(user_id, game_id)

    return Response(status=200)

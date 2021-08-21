import json
from os import environ as env

import requests
from flask import Response, request
from utils.db import Database

from routes.user import authenticate

path: str = env["DB_PATH"]
client_id: str = env["CLIENT"]
bearer: str = "Bearer {}".format(env["BEARER"])
headers: dict = {"Client-ID": client_id, "Authorization": bearer}
url: str = "https://api.igdb.com/v4/games"
search_body: str = "fields name,genres.name,rating,cover.url; search \"{}\"; limit 100;"
get_body: str = "where id = {}; fields name,genres.name,rating,cover.url;"


def search() -> Response:
    # Checks if the request has the proper form
    if "query" not in request.form.keys():
        return Response("{'error': 'invalid body'}", status=400, content_type="application/json")

    # Sends the search query to the IGDB API
    query: str = str(request.form["query"])
    body: str = search_body.format(query)
    resp: requests.Response = requests.post(url, data=body, headers=headers)

    # Respond with error if the IGDB request fails
    if (resp.status_code != 200):
        return Response("{'error': 'IGDB error'}", status=500, content_type="application/json")

    # Respond with error if there were no search results
    if not len(resp.json()):
        return Response("{'error': 'no results'}", status=400, content_type="application/json")

    return Response(json.dumps(resp.json()), status=resp.status_code, content_type="application/json")


def add_game() -> Response:
    wishlist: bool = False

    # Gets the user name based on the access token
    user: str = authenticate()
    if not user:
        return Response("{'error': 'not authorized'}", status=403, content_type="application/json")

    # Check game id
    resp: Response = check_game_id()
    if resp:
        return resp
    game_id: int = int(request.form["game_id"])

    # Gets the game's data from IGDB
    body: str = get_body.format(game_id)
    resp: requests.Response = requests.post(url, data=body, headers=headers)
    game: dict = resp.json()[0]
    name: str = game["name"]
    rating: str = game["rating"] if "rating" in game else None
    genre: str = game["genres"][0]["name"]
    cover: str = game["cover"]["url"]

    # Checks if the request is for a wishlist game
    if "wishlist" in request.form.keys():
        wishlist = True

    # Inserts the game into the db for the given user
    db: Database = Database(path)
    user_id: int = db.get_user_id(user)
    db.insert_game(user_id, game_id, name, genre, rating, cover, wishlist)
    db.close()

    return Response(status=200, content_type="application/json")


def remove_game() -> Response:
    # Gets the user name based on the access token
    user: str = authenticate()
    if not user:
        return Response("{'error': 'not authorized'}", status=403, content_type="application/json")

    # Check game id
    resp: Response = check_game_id()
    if resp:
        return resp
    game_id: int = int(request.form["game_id"])

    # Deletes the game from the db for the given user
    db: Database = Database(path)
    user_id: int = db.get_user_id(user)
    db.delete_game(user_id, game_id)
    db.close()

    return Response(status=200, content_type="application/json")


def move_game() -> Response:
    wishlist: bool = False

    # Gets the user name based on the access token
    user: str = authenticate()
    if not user:
        return Response("{'error': 'not authorized'}", status=403, content_type="application/json")

    # Check game id
    resp: Response = check_game_id()
    if resp:
        return resp
    game_id: int = int(request.form["game_id"])

    # Checks if the request is for a wishlist game
    if "wishlist" in request.form.keys():
        wishlist = True

    # Moves the game between my_games and wishlist
    db: Database = Database(path)
    user_id: int = db.get_user_id(user)
    db.move_game(user_id, game_id, wishlist)
    db.close()

    return Response(status=200, content_type="application/json")


def get_games() -> Response:
    # Gets the user name based on the access token
    user: str = authenticate()
    if not user:
        return Response("{'error': 'not authorized'}", status=403, content_type="application/json")

    # Gets all the games the user has
    db: Database = Database(path)
    user_id: int = db.get_user_id(user)
    games: dict = db.get_games(user_id)
    db.close()

    # Responds with error if the user has no games
    if not len(games["my_games"]) and not len(games["wishlist"]):
        return Response("{'error': 'no games'}", status=400, content_type="application/json")

    return Response(json.dumps(games), status=200, content_type="application/json")


# Returns a response based on if the game_id exists or is valid
def check_game_id() -> Response:
    # Checks if the request has the proper form
    if "game_id" not in request.form.keys():
        return Response("{'error': 'invalid body'}", status=400, content_type="application/json")

    # Checks if the given game id is an integer
    try:
        game_id: int = int(request.form["game_id"])
    except ValueError:
        return Response("{'error': 'game_id not integer'}", status=400, content_type="application/json")

    # Checks if the given game id exists in the IGDB
    body: str = get_body.format(game_id)
    resp: requests.Response = requests.post(url, data=body, headers=headers)

    # Respond with error if the IGDB request fails
    if (resp.status_code != 200):
        return Response("{'error': 'IGDB error'}", status=500, content_type="application/json")

    # Respond with error if the game id does not exist
    if not len(resp.json()):
        return Response("{'error': 'game id doesn't exist'}", status=400, content_type="application/json")

    return None

import json

import requests
from db import Database
from flask import Response, request

with open("env.json") as f:
    env: dict = json.load(f)

path: str = env["db_path"]
client_id: str = env["client_id"]
bearer: str = "Bearer {}".format(env["bearer"])
headers: dict = {"Client-ID": client_id, "Authorization": bearer}
url: str = "https://api.igdb.com/v4/games"
search_query: str = "fields name,genres.name,rating,cover.url; search \"{}\"; limit 10;"


def search() -> Response:
    # Checks if the request has the proper form
    if "query" not in request.form.keys():
        return Response("{'error': 'invalid body'}", status=403)

    # Sends the search query to the IGDB API
    query: str = str(request.form["query"])
    raw: str = search_query.format(query)
    resp: requests.Response = requests.post(url, data=raw, headers=headers)

    # Respond with error if the IGDB request fails
    if (resp.status_code != 200):
        return Response("{'error': 'IGDB error'}", status=500)

    # Respond with error if there were no search results
    if not len(resp.json()):
        return Response("{'error': 'no results'}", status=403)

    return Response(json.dumps(resp.json()), status=resp.status_code)

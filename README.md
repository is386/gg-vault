# GGVault

## About GGVault

This website lets you track the video games you own and the video games you wish to own in the future. It lets you search for games using the Internet Games Databse API.

## Python Dependencies

To run the server, you will need to install the following modules:

- `flask`

- `flask_cors`

## Setup env.json

Create a file named `env.json` in the `server` directory. Add the following code to the file. This file is ignored by `.gitignore` so no need to worry about accidentally pushing your information. `db_path` is used to house the database created by the server to store user information. `client_id` is the client id that you can get from the IGDB API. `bearer` is the bearer token provided to you by the IGDB API. `access_token_secret` is used to generate a JWT key, and it can be any random string of characters. I reccomend using an encryption library to generate it.

```json
{
  "db_path": "data/games.db",
  "client_id": "IGDB_CLIENT_ID_HERE",
  "bearer": "IGDB_BEARER_TOKEN_HERE",
  "access_token_secret": "ACCESS_TOKEN_HERE"
}
```

## Run the Server

Navigate to the `server` directory, then run the command `python server.py`. By default it runs on port `8080`. You can run the client application using any method of rendering HTML files.

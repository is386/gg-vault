# GGVault

## About GGVault

This website lets you track the video games you own and the video games you wish to own in the future. It lets you search for games using the Internet Games Databse API.

## Python Dependencies

This application was developed on Python version `3.8.5`.

To run the server, you will need to install the following modules:

- `Flask`

- `Flask_Cors`

- `gunicorn`

- `requests`

- `PyJWT`

- `bcrypt`

To use the `requirements.txt` file, just run `pip3 install -r requirements.txt`.

## Setup environment variables

You will need the following environment variables set for this application:

- `CLIENT`: the client id that you can get from the IGDB API

- `BEARER`: the bearer token provided to you by the IGDB API

- `SECRET`: used to generate a JWT key, and it can be any random string of characters. I reccomend using an encryption library to generate it.

## Run the Server

Navigate to the `server` directory, then run the command `python server.py`.

from os import mkdir, path
from sqlite3 import Connection, Cursor, connect

db_path: str = "data/games.db"


class Database:

    def __init__(self):
        self.__conn = self.__connect()

    # Returns a connection to the DB at the given path
    # Creates the DB if it does not exist
    def __connect(self) -> Connection:
        if not path.exists("./data"):
            mkdir("./data")
        if not path.exists(db_path):
            open(db_path, "w+").close()
        return self.__init_db()

    # Returns a connection to the DB
    # Creates the tables if they do not exist
    def __init_db(self) -> Connection:
        conn: Connection = connect(db_path, check_same_thread=False)
        conn.execute("""
            CREATE TABLE IF NOT EXISTS "users" (
                    "id"        INTEGER NOT NULL UNIQUE,
                    "username"  TEXT UNIQUE,
                    "password"  TEXT,
                    PRIMARY KEY("id")
            );""")
        conn.execute("""
            CREATE TABLE IF NOT EXISTS "games" (
                    "user_id"   INTEGER,
                    "game_id"   INTEGER,
                    "name"      TEXT,
                    "genre"     TEXT,
                    "rating"    TEXT,
                    "cover"     TEXT,
                    "wishlist"  INTEGER
            );""")
        return conn

    # Closes the connection to the database
    def close(self):
        self.__conn.close()

    # Returns True if the username is available, false otherwise
    def user_exists(self, user: str) -> bool:
        c: Cursor = self.__conn.cursor()
        c = self.__conn.execute(
            "SELECT username FROM users WHERE username=?", (user,))
        rows: list = c.fetchall()
        return len(rows) == 1

    # Returns the given user's hashed password
    def get_pass(self, user: str) -> bytes:
        c: Cursor = self.__conn.cursor()
        c = self.__conn.execute(
            "SELECT password FROM users WHERE username=?", (user,))
        rows: list = c.fetchall()
        return rows[0][0]

    # Returns the user's id
    def get_user_id(self, user: str) -> int:
        c: Cursor = self.__conn.cursor()
        c = self.__conn.execute(
            "SELECT id FROM users WHERE username=?", (user,))
        rows: list = c.fetchall()
        return rows[0][0]

    # Inserts the given username and password into the DB
    def insert_user(self, user: str, pw: bytes):
        self.__conn.execute("""
            INSERT INTO
                users(username, password)
            VALUES
                (?, ?)
            """, (user, pw))
        self.__conn.commit()

    # Inserts the given game id into the DB
    def insert_game(self, user_id: int, game_id: int, name: str, genre: str, rating: str, cover: str, wishlist: bool):
        if self.entry_exists(user_id, game_id):
            return
        self.__conn.execute("""
            INSERT INTO
                games(user_id, game_id, name, genre, rating, cover, wishlist)
            VALUES
                (?, ?, ?, ?, ?, ?, ?)
            """, (user_id, game_id, name, genre, rating, cover, int(wishlist)))
        self.__conn.commit()

    # Deletes the given game id from the DB
    def delete_game(self, user_id: int, game_id: int):
        self.__conn.execute("""
            DELETE FROM
                games
            WHERE
                user_id=? AND game_id=?;
            """, (user_id, game_id))
        self.__conn.commit()

    # Moves the given game id to/from wishlist
    def move_game(self, user_id: int, game_id: int, wishlist: bool):
        self.__conn.execute("""
            UPDATE
                games
            SET
                wishlist=?
            WHERE
                user_id=? AND game_id=?;
            """, (int(wishlist), user_id, game_id))
        self.__conn.commit()

    # Returns a dict of the games the user has in their lists
    def get_games(self, user_id: int) -> dict:
        c: Cursor = self.__conn.cursor()
        c = self.__conn.execute(
            "SELECT * FROM games WHERE user_id=?", (user_id,))
        games: list = c.fetchall()
        my_games: list = []
        wishlist: list = []

        for g in games:
            game: dict = {"id": g[1], "name": g[2],
                          "genre": g[3], "rating": g[4], "cover": g[5]}
            wishlist.append(game) if g[-1] else my_games.append(game)

        return {"my_games": my_games, "wishlist": wishlist}

    # Check if the game already exists for the user
    def entry_exists(self, user_id: int, game_id: int) -> bool:
        c: Cursor = self.__conn.cursor()
        c = self.__conn.execute(
            "SELECT * FROM games WHERE user_id=? AND game_id=?", (user_id, game_id))
        return len(c.fetchall()) > 0

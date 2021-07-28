import bcrypt
from flask import Flask, Response, request
from markupsafe import escape

app = Flask(__name__)

user_min: int = 1
user_max: int = 20
pass_min: int = 5
pass_max: int = 36


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
    if not validAcctBody():
        return Response(status=401)

    user: str = str(request.form["username"])
    # TODO: SQLite DB with table for users
    # TODO: DB module to handle select users by name and insert user
    # TODO: Check if user name already exists in DB with select
    pw: bytes = request.form["password"].encode("utf-8")
    hashed: bytes = bcrypt.hashpw(pw, bcrypt.gensalt())
    # TODO: Insert user and hashed password into DB

    return Response(status=200)


if __name__ == "__main__":
    app.run(host="localhost", port=8080, debug=True)

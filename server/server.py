from flask import Flask

from routes.user import auth, create, login

# Sets up flask app and routes
app = Flask(__name__)
app.add_url_rule("/login", view_func=login, methods=["POST"])
app.add_url_rule("/create", view_func=create, methods=["POST"])
app.add_url_rule("/auth", view_func=auth, methods=["POST"])


@app.route("/")
def index():
    return "Index Page"


if __name__ == "__main__":
    app.run(host="localhost", port=8080, debug=True)

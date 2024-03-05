from flask import Flask, request
import json
import time
import sqlite3

from test import ExampleObject

ExampleObject.makeExampleTable()

app = Flask(__name__)
app.config["SERVER_NAME"] = "localhost:5000"
app.config["CLIENT_NAME"] = "http://localhost:5173"


def jsonResponse(jsonData):
    """
    Create a standard JSON response with the provided data, only including the client side URL in the ACAO.

    Parameters
    ----------
    jsonData: dict
        A Python dict representing the JSON data to include

    Returns
    -------
    Flask.response_class
        The response containing the provided data
    """
    resp = Flask.response_class(
        response=json.dumps(jsonData, indent=2), status=200, mimetype="application/json"
    )
    resp.headers["Access-Control-Allow-Origin"] = app.config["CLIENT_NAME"]
    return resp


# Get example data from all APIs
@app.route("/exampleAPICalls", methods=["GET", "POST"])
def exampleAPICalls():
    steamResp = None
    chatGPTResp = None
    spotifyResp = None
    return jsonResponse(
        {"steam": steamResp, "chatgpt": chatGPTResp, "spotify": spotifyResp}
    )

# Get all users
@app.route("/allUsers", methods=["GET", "POST"])
def allUsers():
    connection = sqlite3.connect("test.db")
    cursor = connection.cursor()

    cursor.execute("SELECT id FROM users")
    rows = cursor.fetchall()

    jsonData = []
    for row in rows:
        user = ExampleObject()
        user.load_season(row[0])
        jsonData += [user.toJSON()]

    connection.commit()
    connection.close()

    return jsonResponse({"total": len(rows), "users": jsonData})


# Insert and return data for new user in database
@app.route("/insertUser", methods=["GET", "POST"])
def insertUser():
    user = ExampleObject("Bob", "Minecraft")
    user.insert_user()
    return jsonResponse({"name": user.name, "favGame": user.favGame})


if __name__ == "__main__":
    app.run(debug=True)

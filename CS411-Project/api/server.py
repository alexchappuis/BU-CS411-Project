from flask import Flask, request, session
import json
import time
import datetime
import sqlite3
import requests
import base64
from openai import OpenAI
import apikeys
import routes
import jsonify

from test import ExampleObject

ExampleObject.makeExampleTable()

app = Flask(__name__)
app.config["SERVER_NAME"] = "localhost:5000"
app.config["CLIENT_NAME"] = "http://localhost:5173"
chatGptClient = OpenAI(api_key = apikeys.CHATGPT_KEY)


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
    steamData = getSteamData()
    chatGptData = getChatGptData()
    spotifyData = getSpotifyData()
    return jsonResponse(
        {"steam": steamData, "chatgpt": chatGptData, "spotify": spotifyData}
    )

@app.route("/login")
def login():
    scope = "user-read-private user-read-email"
    params = {
        "client_id": apikeys.SPOTIFY_CLIENTID,
        "response_type": "code",
        "scope": scope,
        "redirect_uri": app["SERVER_NAME"] + "/callback",
        "show_dialog": True
    }

@app.route("/callback")
def callback():
    if "error" in request.args:
        return jsonify({"error": request.args["error"]})
    if "code" in request.args:
        reqBody = {
            "code": request.args["code"],
            "grant_type": "authorization_code",
            "redirect_uri": app["SERVER_NAME"] + "/callback",
            "client_id": apikeys.SPOTIFY_CLIENTID,
            "client_secret": apikeys.SPOTIFY_CLIENTSECRET
        }
        response = requests.post(routes.SPOTIFY_TOKEN_URL, data=reqBody)
        tokenInfo = response.json()
        session["access_token"] = tokenInfo["access_token"]
        session["refresh_token"] = tokenInfo["refresh_token"]
        session["expires_at"] = datetime.now().timestamp() + tokenInfo["expires_in"]

def getSteamData():
    steamURL = "http://api.steampowered.com/IPlayerService/GetOwnedGames/v0001/?key=%s&steamid=%s&include_appinfo=%s&include_played_free_games=%s&format=%s" % (apikeys.ISTEAMUSER_KEY, "76561198322874928", "false", "false", "json")
    steamResponse = requests.get(steamURL)
    return steamResponse.json()

@app.route("/steamData", methods=["POST"])
def getSteamUserData():
    print("TEST===================")
    data = request.get_json(force=True)
    id = data["id"]
    steamURL = "http://api.steampowered.com/IPlayerService/GetOwnedGames/v0001/?key=%s&steamid=%s&include_appinfo=%s&include_played_free_games=%s&format=%s" % (apikeys.ISTEAMUSER_KEY, id, "false", "false", "json")
    steamResponse = requests.get(steamURL)
    print(steamResponse.json())
    return jsonResponse({"data": steamResponse.json()})

def getChatGptData():
    MODEL = "gpt-3.5-turbo"
    chatGptResp = chatGptClient.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "user", "content": "Write a poem about penguins"},
        ],
        temperature=0,
        max_tokens=100,
    )
    return json.loads(chatGptResp.model_dump_json())

def getSpotifyData():
    token = getSpotifyToken()
    headers = {
        "Authorization": "Bearer " + token
    }
    url = "https://api.spotify.com/v1/tracks/4a1ptzo1GXEjGDuhXd5ybn"
    response = requests.get(url=url, headers=headers, data={})
    return response.json()

def getSpotifyToken():
    auth = "%s:%s" % (apikeys.SPOTIFY_CLIENTID, apikeys.SPOTIFY_CLIENTSECRET)
    authBytes = auth.encode("utf-8")
    auth64 = str(base64.b64encode(authBytes), "utf-8")
    url = "https://accounts.spotify.com/api/token"
    headers = {
        "Authorization": "Basic " + auth64,
        "Content-Type": "application/x-www-form-urlencoded"
    }
    data = {
        "grant_type": "client_credentials"
    }
    response = requests.post(url, headers=headers, data=data)
    jsonData = json.loads(response.content)
    return jsonData["access_token"]

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

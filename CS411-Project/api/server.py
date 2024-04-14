import urllib.parse
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
import math
import urllib

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
    chatGptData = [] #getChatGptData()
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

@app.route("/generatePlaylist", methods=["POST"])
def generatePlaylist():
    #get user ID and spotify token
    data = request.get_json(force=True)
    id = data["id"]
    token = data["spotify_token"]
    top5 = getTopGames(id, 5)
    imageUrls = getGameBanners(top5)
    numSongs = calculateNumSongs(top5)
    songInfos = getSpotifySongs(top5, numSongs, token)
    return jsonResponse({"games": top5, "img_urls": imageUrls, "num_songs": numSongs, "songs": songInfos})


#get top 5 games by playtime of the associated user
def getTopGames(id, length):
    steamURL = "http://api.steampowered.com/IPlayerService/GetOwnedGames/v0001/?key=%s&steamid=%s&include_appinfo=%s&include_played_free_games=%s&format=%s" % (apikeys.ISTEAMUSER_KEY, id, "true", "true", "json")
    steamResponse = requests.get(steamURL)
    games = steamResponse.json()["response"]["games"]
    #sort games owned by playtime
    sortedGames = sorted(games, key=lambda game: -game["playtime_forever"])
    return sortedGames[:length]

#get banners of each game in top 5 most played
def getGameBanners(games):
    imageUrls = [""] * len(games)
    for i in range(len(games)):
        id = games[i]["appid"]
        infoUrl = "https://store.steampowered.com/api/appdetails?appids=%s" % (id)
        gameInfo = requests.get(infoUrl)
        imageUrls[i] = gameInfo.json()[str(id)]["data"]["header_image"]
    return imageUrls

#calculate number of songs from each game to put in playlist based on playtime
def calculateNumSongs(games):
    totalTime = 0
    for game in games:
        totalTime += game["playtime_forever"]
    numSongs = [0] * len(games)
    total = 0
    for i in range(len(games)):
        percent = games[i]["playtime_forever"] / totalTime
        numSongs[i] = math.floor(20 * percent)
        total += numSongs[i]
    #rounding will probably mean we won't have exactly 20 songs total,
    #so just give #1 game the remaining spots
    if total < 20:
        numSongs[0] += 20 - total
    return numSongs

def getSpotifySongs(games, numSongs, token):
    songInfos = []
    for game in range(len(games)):
        #curl --request GET \
        #--url 'https://api.spotify.com/v1/search?q=Terraria&type=track&limit=7&offset=0' \
        #--header 'Authorization: Bearer 1POdFZRZbvb...qqillRxMr2z'
        endpoint = "https://api.spotify.com/v1/search?"
        gameName = games[game]["name"]
        params = {"q": gameName, "type": "track", "limit": numSongs[game], "offset": 0}
        url = endpoint + urllib.parse.urlencode(params)
        headers = {
            "Authorization": "Bearer " + token
        }
        response = requests.get(url=url, headers=headers, data={})
        respJson = response.json()
        for i in range(numSongs[game]):
            song = respJson["tracks"]["items"][i]
            id = song["id"]
            name = song["name"]
            duration = song["duration_ms"]
            coverUrl = song["album"]["images"][0]["url"]
            previewUrl = song["preview_url"]
            info = {
                "id": id,
                "name": name,
                "duration": duration,
                "cover_url": coverUrl,
                "preview_url": previewUrl,
            }
            songInfos += [info]
    return songInfos
    


@app.route("/steamData", methods=["POST"])
def getSteamUserData():
    #get user ID
    data = request.get_json(force=True)
    id = data["id"]
    steamURL = "http://api.steampowered.com/IPlayerService/GetOwnedGames/v0001/?key=%s&steamid=%s&include_appinfo=%s&include_played_free_games=%s&format=%s" % (apikeys.ISTEAMUSER_KEY, id, "true", "true", "json")
    steamResponse = requests.get(steamURL)
    games = steamResponse.json()["response"]["games"]
    #sort games owned by playtime
    sortedGames = sorted(games, key=lambda game: -game["playtime_forever"])
    imageUrls = [""] * 5
    totalTime = 0
    #get banners of each game in top 5 most played
    for i in range(5):
        id = sortedGames[i]["appid"]
        infoUrl = "https://store.steampowered.com/api/appdetails?appids=%s" % (id)
        gameInfo = requests.get(infoUrl)
        imageUrls[i] = gameInfo.json()[str(id)]["data"]["header_image"]
        totalTime += sortedGames[i]["playtime_forever"]
    #calculate number of songs to put in playlist based on playtime
    numSongs = [0] * 5
    total = 0
    for i in range(5):
        percent = sortedGames[i]["playtime_forever"] / totalTime
        numSongs[i] = math.floor(20 * percent)
        total += numSongs[i]
    #rounding will probably mean we won't have exactly 20 songs total,
    #so just give #1 game the remaining spots
    if total < 20:
        numSongs[0] += 20 - total
    return jsonResponse({"games": sortedGames[:5], "img_urls": imageUrls, "num_songs": numSongs})

@app.route("/chatGptRecs", methods=["POST"])
def getChatGptRecs():
    data = request.get_json(force=True)
    games = data["games"]


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

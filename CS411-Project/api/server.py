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
    scope = "user-read-private user-read-email user-library-read"
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
    steamData = steamResponse.json()

    connection = sqlite3.connect("test.db")
    cursor = connection.cursor()

    for game in steamData["response"]["games"]:
        cursor.execute("SELECT play_count FROM steam_games WHERE app_id=?", (game["appid"],))
        result = cursor.fetchone()
        if result:
            play_count = result[1] + 1
            cursor.execute("UPDATE steam_games SET play_count=?, play_time=? WHERE app_id=?", (play_count, game["playtime_forever"], game["appid"]))
        else:
            cursor.execute("INSERT INTO steam_games (app_id, name, play_count, play_time) VALUES (?, ?, 1, ?)", (game["appid"], game["name"], game["playtime_forever"]))

    connection.commit()
    connection.close()

    return steamData

def updateDatabase(user_id, steamData):
    connection = sqlite3.connect("test.db")
    cursor = connection.cursor()

    cursor.execute("SELECT * FROM users WHERE user_id=?", (user_id,))
    result = cursor.fetchone()
    if result is None:
        cursor.execute("INSERT INTO users (user_id) VALUES (?)", (user_id,))
        for game in steamData["response"]["games"]:
            cursor.execute("SELECT play_count, play_time FROM steam_games WHERE app_id=?", (game["appid"],))
            result = cursor.fetchone()
            if result:
                play_count = result[0] + 1
                play_time = result[1] + game["playtime_forever"]
                cursor.execute("UPDATE steam_games SET play_count=?, play_time=? WHERE app_id=?", (play_count, play_time, game["appid"]))
            else:
                cursor.execute("INSERT INTO steam_games (app_id, name, play_count, play_time) VALUES (?, ?, 1, ?)", (game["appid"], game["name"], game["playtime_forever"]))

    connection.commit()
    connection.close()

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


#get top (length) games by playtime of the associated user
def getTopGames(id, length):
    steamURL = "http://api.steampowered.com/IPlayerService/GetOwnedGames/v0001/?key=%s&steamid=%s&include_appinfo=%s&include_played_free_games=%s&format=%s" % (apikeys.ISTEAMUSER_KEY, id, "true", "true", "json")
    steamResponse = requests.get(steamURL)
    updateDatabase(id, steamResponse.json())
    games = steamResponse.json()["response"]["games"]
    #sort games owned by playtime
    sortedGames = sorted(games, key=lambda game: -game["playtime_forever"])
    return sortedGames[:length]

#get banner of singular game
def getGameBanner(id):
    infoUrl = "https://store.steampowered.com/api/appdetails?appids=%s" % (id)
    gameInfo = requests.get(infoUrl)
    return gameInfo.json()[str(id)]["data"]["header_image"]

#get banners of each game in top 5 most played
def getGameBanners(games):
    imageUrls = [""] * len(games)
    for i in range(len(games)):
        id = games[i]["appid"]
        imageUrls[i] = getGameBanner(id)
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
    
#initialize table for steam game play count
def createTables():
    connection = sqlite3.connect("test.db")
    cursor = connection.cursor()
    sql = """CREATE TABLE IF NOT EXISTS steam_games (
        app_id INTEGER PRIMARY KEY,
        name TEXT NOT NULL,
        play_count INTEGER NOT NULL,
        play_time INTEGER NOT NULL
    );"""
    cursor.execute(sql)
    sql = """CREATE TABLE IF NOT EXISTS users (
        user_id INTEGER PRIMARY KEY
    );"""
    cursor.execute(sql)
    connection.commit()
    connection.close()

#get top 10 most played games across all users
@app.route("/mostPlayedGames", methods=["GET"])
def mostPlayedGames():
    connection = sqlite3.connect("test.db")
    cursor = connection.cursor()

    cursor.execute("SELECT * FROM steam_games")
    rows = cursor.fetchall()

    connection.commit()
    connection.close()

    sortedGames = sorted(rows, key=lambda game: -game[3])
    gamesJson = []
    for i in range(10):
        game = sortedGames[i]
        gamesJson += [{
            "app_id": game[0],
            "name": game[1],
            "play_count": game[2],
            "play_time": game[3],
            "rank": i+1,
            "banner_url": getGameBanner(game[0])
        }]
    return jsonResponse(gamesJson)

@app.route("/addPlaylist", methods=["POST"])
def addPlaylist():
    #get user ID and spotify token
    data = request.get_json(force=True)
    user_id = "31x6jp2buqjwabztxvxeugfzfnue" #data["spotify_id"]
    token = data["spotify_token"]
    song_ids = data["song_ids"]
    song_uris = []
    for id in song_ids:
        song_uris += ["spotify:track:" + id]
    endpoint_url = f"https://api.spotify.com/v1/users/{user_id}/playlists"
    request_body = json.dumps({
        "name": "My Top Games",
        "description": "Playlist generated by good ol\' fashioned code.",
        "public": False
    })
    response = requests.post(
        url = endpoint_url,
        data = request_body,
        headers = {
            "Content-Type": "application/json",
            "Authorization": "Bearer " + token
        }
    )
    print("playlist json", response.json())
    playlistId = response.json()["id"]
    endpoint_url = f"https://api.spotify.com/v1/playlists/{playlistId}/tracks"

    request_body = json.dumps({
        "uris" : song_uris
    })
    response = requests.post(
        url = endpoint_url,
        data = request_body,
        headers = {
            "Content-Type": "application/json",
            "Authorization": "Bearer " + token
        }
    )
    print(response.json())
    return jsonResponse({"status_code": 200})

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


createTables()

if __name__ == "__main__":
    app.run(debug=True)

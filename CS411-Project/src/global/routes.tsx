import * as KEYS from "./apikeys";

// CLIENT SIDE
const CLIENT_URL = "http://localhost:5173"
export const HOME = "/";

// CLIENT SIDE - 3RD PARTY APIS
const SPOTIFY_AUTH_URL = "https://accounts.spotify.com/authorize"
const SPOTIFY_TOKEN_URL = "https://accounts.spotify.com/api/token"
const SPOTIFY_API_BASE_URL = "https://api.spotify.com/v1"
const RESPONSE_TYPE = "token"
export const LOGIN = `${SPOTIFY_AUTH_URL}?client_id=${KEYS.SPOTIFY_CLIENTID}&redirect_uri=${CLIENT_URL + HOME}&response_type=${RESPONSE_TYPE}`;
export const STEAM_USER_URL = (id: string) =>
    `http://api.steampowered.com/IPlayerService/GetOwnedGames/v0001/?key=${KEYS.ISTEAMUSER_KEY}&steamid=${id}&include_appinfo=${"false"}&include_played_free_games=${"false"}&format=${"json"}`

// SERVER SIDE
const SERVER_URL = "http://localhost:5000";
export const SERVER_GET_STEAM_USER = SERVER_URL + "/steamData";

// OTHER
export const GITHUB = "https://github.com/alexchappuis/BU-CS411-Project/tree/main";
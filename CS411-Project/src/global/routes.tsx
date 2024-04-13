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

// SERVER SIDE
const SERVER_URL = "http://localhost:5000";

// OTHER
export const GITHUB = "https://github.com/alexchappuis/BU-CS411-Project/tree/main";
# CS411 Project: Alex Chappuis, Noah Barnes, Richard Lin

This project lets users log in to Spotify's OAuth, enter their Steam user ID, then generate a Spotify playlist based on their most played games.

# Set up

## Dependencies and Keys

To set up this project, do the usual `npm install` to install necessary dependencies. Then, create a file called `apikeys.tsx` in `CS411-Project/src/global` and paste in your API keys for ISteamUser, ChatGPT, and Spotify like this:

```
export const ISTEAMUSER_KEY = "KEY"
export const CHATGPT_KEY = "KEY"
export const SPOTIFY_CLIENTID = "KEY"
export const SPOTIFY_CLIENTSECRET = "KEY"
```

Now, create a file called `apikeys.py` in `CS411-Project/api` and paste in your API keys again like this:

```
ISTEAMUSER_KEY = "KEY"
CHATGPT_KEY = "KEY"
SPOTIFY_CLIENTID = "KEY"
SPOTIFY_CLIENTSECRET = "KEY"
```

## Client and Server URLs

Next, run the server using `python3 server.py` in the appropriate directory and see where the server is running (e.g. `http://localhost:5000`). Paste this URL into the `SERVER_URL` variable in `CS411-Project/src/global/routes.tsx`. After that, run `npm run dev` to start up the client-side web app and see where that is running (e.g. `http://localhost:5173`). Paste this url into the `app.config["CLIENT_NAME"]` variable in `CS411-Project/api/server.py` to allow the front-end to communicate with the back-end.

# Running

With everything in place, terminate the current instances of the client and server, then start the server with `python3 server.py` and start the client with `npm run dev` in their respective directories. Visit the client URL, and everything should be working.
import { useState, useEffect, useContext } from 'react';
import { Row } from 'react-bootstrap';

import * as ROUTES from "../global/routes";
import * as CONTEXTS from "../global/contexts";

import "../styles/spotifyLogin.css";

const SpotifyLogin = () => {
  const [username, setUsername] = useState("");
  const tokenCon = useContext(CONTEXTS.TokenContext);
  const spotifyCon = useContext(CONTEXTS.SpotifyContext)

  useEffect(() => {
    const hash = window.location.hash;
    let localToken = window.localStorage.getItem("token");
    let localRefresh = window.localStorage.getItem("refresh_token")
    let localExpiration = window.localStorage.getItem("expiration")
    if(localToken && localRefresh && localExpiration) {
      tokenCon.setToken(localToken);
      spotifyCon.setLogin({token: localToken, refreshToken: localRefresh, expiration: parseInt(localExpiration)})
    }
    else if(hash) {
        console.log(hash)
        let atString = hash.substring(1).split("&").find(elem => elem.startsWith("access_token"));
        if(atString) {
            let tokenString = atString.split("=")[1];
            window.location.hash = "";
            window.localStorage.setItem("token", tokenString)
            tokenCon.setToken(tokenString);
        } else {
            console.error("Could not get Spotify OAuth access token.");
        }
    }
  }, [])

  useEffect(() => {
    let accessToken = localStorage.getItem("token");
    fetch('https://api.spotify.com/v1/me', {
      headers: {
        Authorization: 'Bearer ' + accessToken
      }
    })
    .then((res) => res.json())
    .then((data) => {
      setUsername(data["display_name"]);
    })
  }, [spotifyCon.login])

  const logout = () => {
    spotifyCon.setLogin({token: "", refreshToken: "", expiration: 0});
    window.localStorage.removeItem("token");
    window.localStorage.removeItem("refresh_token");
    window.localStorage.removeItem("expiration");
  }
  return (
    <div id="spotifyLogin">
      <Row id="spotifyLabel">
        {username && <small>Currently signed in as <br/> <b>{username}</b></small>}
        {!username && <small>Not logged in</small>}
      </Row>
      <Row>
        {username && <a className="spotifyBtn" onClick={logout} href="">Logout</a>}
        {!username && <a className="spotifyBtn" href={ROUTES.LOGIN}>Spotify Login</a>}
      </Row>
    </div>
  )
}

export default SpotifyLogin
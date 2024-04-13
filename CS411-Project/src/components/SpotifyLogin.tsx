import { useState, useEffect, useContext } from 'react';
import { Row } from 'react-bootstrap';

import * as ROUTES from "../global/routes";
import * as CONTEXTS from "../global/contexts";

const SpotifyLogin = () => {
  const [username, setUsername] = useState("");
  const tokenCon = useContext(CONTEXTS.TokenContext);
  

  useEffect(() => {
    const hash = window.location.hash;
    let localToken = window.localStorage.getItem("token");
    if(localToken) tokenCon.setToken(localToken);
    else if(hash) {
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
      console.log(data["display_name"]);
      setUsername(data["display_name"]);
    })
  }, [tokenCon.token])

  const logout = () => {
    tokenCon.setToken("");
    window.localStorage.removeItem("token");
  }
  return (
    <div id="spotifyLogin">
      <Row id="spotifyLabel">
          {username && <small>Currently signed in as <br/> <b>{username}</b></small>}
          {!username && <small>Not logged in</small>}
      </Row>
      <Row>
        {tokenCon.token && <a className="spotifyBtn" onClick={logout} href="">Logout</a>}
        {!tokenCon.token && <a className="spotifyBtn" href={ROUTES.LOGIN}>Spotify Login</a>}
      </Row>
    </div>
  )
}

export default SpotifyLogin
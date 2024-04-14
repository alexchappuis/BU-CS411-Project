import { useContext, useEffect, useRef, useState } from 'react';
import { Row } from 'react-bootstrap'

import * as ROUTES from "../global/routes";
import * as CONTEXTS from "../global/contexts";

import { Game, User } from '../global/contexts';

import "../styles/steamSearch.css";

const UsernameSearch = () => {
  const tokenCon = useContext(CONTEXTS.TokenContext);
  const userCon = useContext(CONTEXTS.SteamContext);
  const [id, setId] = useState("");

  const search = () => {
    console.log("Searching");
    fetch(ROUTES.SERVER_GET_STEAM_USER, {
      method: "POST",
      body: JSON.stringify({
        id: id,
      }),
    })
    .then(resp => resp.json())
    .then(data => {
      console.log(data)
      let games = data["games"];
      let u: User = {name: "Bob", id: parseInt(id), games: []}
      for(let i = 0; i < games.length; i++) {
        let g = games[i];
        let game: Game = {
          id: g["appid"],
          name: g["name"],
          playtime: Math.floor(g["playtime_forever"] / 60),
          iconUrl: g["img_icon_url"],
          logoUrl: data["img_urls"][i],
          rank: i+1
        };
        u["games"].push(game);
      }
      userCon.setUser(u);
    });
    fetch(ROUTES.SERVER_GENERATE_PLAYLIST, {
      method: "POST",
      body: JSON.stringify({
        id: id,
        spotify_token: tokenCon.token,
      }),
    })
    .then(resp => resp.json())
    .then(data => console.log(data));
  }

  return (
    <div id="steamSearch">
      <Row id="searchLabel">
        <p>Steam User ID Search</p>
      </Row>
      <Row id="idSearch">
      <input
        type="text"
        id="idSearchEntry"
        onChange={(e) => {
          setId(e.target.value);
        }}
      />
      </Row>
      <Row>
        <button className="searchBtn" onClick={search} disabled={id === ""}>Search</button>
      </Row>
    </div>
  )
}

export default UsernameSearch
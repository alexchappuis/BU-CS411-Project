import { useContext, useEffect, useRef, useState } from 'react';
import { Row } from 'react-bootstrap'

import * as ROUTES from "../global/routes";
import * as CONTEXTS from "../global/contexts";

import { Game, Song } from '../global/contexts';

import "../styles/steamSearch.css";

const UsernameSearch = () => {
  const tokenCon = useContext(CONTEXTS.TokenContext);
  const spotifyCon = useContext(CONTEXTS.SpotifyContext);
  const gamesCon = useContext(CONTEXTS.SteamContext);
  const playlistCon = useContext(CONTEXTS.PlaylistContext);
  const [id, setId] = useState("");

  const search = () => {
    console.log("Searching");
    fetch(ROUTES.SERVER_GENERATE_PLAYLIST, {
      method: "POST",
      body: JSON.stringify({
        id: id,
        spotify_token: tokenCon.token,
      }),
    })
    .then(resp => resp.json())
    .then(data => {
      console.log(data)
      // create list of all games
      let games = data["games"];
      let gs: Game[] = [];
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
        gs.push(game);
      }
      gamesCon.setGames(gs);
      //create list of all songs
      let songs = data["songs"];
      let pl: Song[] = [];
      for(let i = 0; i < songs.length; i++) {
        let s = songs[i];
        let song: Song = {
          name: s["name"],
          id: s["id"],
          duration: s["duration"],
          coverUrl: s["cover_url"],
          previewUrl: s["preview_url"]
        }
        pl.push(song);
      }
      playlistCon.setPlaylist(pl);
    });
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
import { useContext, useState } from "react";
import { Button, Col, Row } from "react-bootstrap";

import SpotifyLogin from "../components/SpotifyLogin";
import UsernameSearch from "../components/UsernameSearch";

import * as ROUTES from "../global/routes";
import * as CONTEXTS from "../global/contexts";

import { Game, Song } from "../global/contexts";

import "../styles/home.css";
import GameRecord from "../components/GameRecord";
import SongItem from "../components/SongItem";

function Home() {
  const [games, setGames] = useState<Game[]>([]);
  const [playlist, setPlaylist] = useState<Song[]>([]);
  const [addSuccess, setAddSuccess] = useState<Boolean>(false);
  const tokenCon = useContext(CONTEXTS.TokenContext);

  const createPlaylist = () => {
    let song_ids: string[] = [];
    for(let i = 0; i < playlist.length; i++) {
      song_ids.push(playlist[i].id);
    }
    fetch(ROUTES.SERVER_CREATE_PLAYLIST, {
      method: "POST",
      body: JSON.stringify({
        song_ids: song_ids,
        spotify_token: tokenCon.token,
      }),
    })
    .then(resp => resp.json())
    .then(data => {
      console.log(data);
      if(data["status_code"] === 200) {
        setAddSuccess(true);
      }
    })
  }

  return (
    <div className="page">
      <CONTEXTS.SteamContext.Provider value={{games, setGames}}>
        <CONTEXTS.PlaylistContext.Provider value={{playlist, setPlaylist}}>
          <Row>
            <Col sm={{span: 4, offset: 1}}>
              <SpotifyLogin />
            </Col>
            <Col sm={{span: 5, offset: 1}}>
              <UsernameSearch />
            </Col>
          </Row>
          {games.length > 0 && <Row className="gamesList">
            <Col sm={{span: 10, offset: 1}} className="gameDesc">
              {games.map((game) => (
                <GameRecord
                  key={game["id"]}
                  name={game["name"]}
                  id={game["id"]}
                  hoursPlayed={game["playtime"]}
                  rank={game["rank"]}
                  coverUrl={game["logoUrl"]}
                />
              ))}
            </Col>
          </Row>}
          {playlist.length > 0 && <Row id="playlist">
              <Col sm={{span: 10, offset: 1}} id="songsContainer">
                {playlist.map((song) => (
                  <SongItem
                    key={song["id"]}
                    name={song["name"]}
                    id={song["id"]}
                    duration={song["duration"]}
                    coverUrl={song["coverUrl"]}
                    previewUrl={song["previewUrl"]}
                  />
                ))}
              </Col>
          </Row>}
          {/* {playlist.length > 0 && <Row id="generateContainer">
            <button className="spotifyBtn" onClick={createPlaylist}>Create Spotify Playlist</button>
            {addSuccess && <h1>Successfully added playlist</h1>}
          </Row>} */}
        </CONTEXTS.PlaylistContext.Provider>
      </CONTEXTS.SteamContext.Provider>
    </div>
  );
}

export default Home;

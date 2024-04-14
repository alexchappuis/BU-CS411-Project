import { useState } from "react";
import { Col, Row } from "react-bootstrap";

import SpotifyLogin from "../components/SpotifyLogin";
import UsernameSearch from "../components/UsernameSearch";

import * as CONTEXTS from "../global/contexts";

import { Game, Song } from "../global/contexts";

import "../styles/home.css";
import GameRecord from "../components/GameRecord";
import SongItem from "../components/SongItem";

function Home() {
  const [games, setGames] = useState<Game[]>([]);
  const [playlist, setPlaylist] = useState<Song[]>([])
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
          {games.length > 0 && <Row id="gamesList">
            <Col sm={{span: 10, offset: 1}} id="gameDesc">
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
        </CONTEXTS.PlaylistContext.Provider>
      </CONTEXTS.SteamContext.Provider>
    </div>
  );
}

export default Home;

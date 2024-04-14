import { useState } from "react";
import { Col, Row } from "react-bootstrap";

import SpotifyLogin from "../components/SpotifyLogin";
import UsernameSearch from "../components/UsernameSearch";

import * as ROUTES from "../global/routes";
import * as CONTEXTS from "../global/contexts";

import { User } from "../global/contexts";

import "../styles/home.css";
import GameRecord from "../components/GameRecord";

function Home() {
  const [user, setUser] = useState<User>({name: "", id: -1, games: []});
  return (
    <div className="page">
      <CONTEXTS.SteamContext.Provider value={{user, setUser}}>
        <Row>
          <Col sm={{span: 4, offset: 1}}>
            <SpotifyLogin />
          </Col>
          <Col sm={{span: 5, offset: 1}}>
            <UsernameSearch />
          </Col>
        </Row>
        <Row id="gamesList">
          <div >
            <Col sm={{span: 10, offset: 1}} id="gameDesc">
              {user["games"].map((game) => (
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
          </div>
        </Row>
      </CONTEXTS.SteamContext.Provider>
    </div>
  );
}

export default Home;

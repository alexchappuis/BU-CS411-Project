import React, { useState, useEffect } from 'react';
import { Col } from 'react-bootstrap';

import "../styles/mostPlayed.css"
import GameRecord from '../components/GameRecord';

const MostPlayedGames: React.FC = () => {
  const [mostPlayedGames, setMostPlayedGames] = useState([]);

  useEffect(() => {
    fetch('http://localhost:5000/mostPlayedGames')
      .then(resp => resp.json())
      .then(data => {
        console.log(data);
        setMostPlayedGames(data);
      })
      .catch(error => {
        console.error('Error fetching most played games:', error);
      });
  }, []);

  return (
    <div className="gamesList">
      <Col sm={{span: 10, offset: 1}} className="gameDesc">
        <h1>Most Played Games</h1>
        {mostPlayedGames.map((game: any) => (
          <GameRecord
            name={game["name"]}
            id={game["app_id"]}
            hoursPlayed={Math.floor(game["play_time"] / 60)}
            usersPlayed={game["play_count"]}
            rank={game["rank"]}
            coverUrl={game["banner_url"]}
          />
        ))}
      </Col>
    </div>
  );
}

export default MostPlayedGames;

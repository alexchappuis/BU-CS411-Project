import React, { useState, useEffect } from 'react';
import axios from 'axios';

const MostPlayedGames: React.FC = () => {
  const [mostPlayedGames, setMostPlayedGames] = useState([]);

  useEffect(() => {
    axios.get('http://localhost:5000/mostPlayedGames')
      .then(response => {
        setMostPlayedGames(response.data);
      })
      .catch(error => {
        console.error('Error fetching most played games:', error);
      });
  }, []);

  return (
    <div>
      <h1>Most Played Games</h1>
      <ul>
        {mostPlayedGames.map((game: any) => (
          <li key={game.app_id}>
            {game.name} - {game.play_count} plays
          </li>
        ))}
      </ul>
    </div>
  );
}

export default MostPlayedGames;

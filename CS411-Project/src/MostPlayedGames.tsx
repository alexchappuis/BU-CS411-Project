import React, { useState, useEffect } from 'react';

const MostPlayedGames: React.FC = () => {
  const [mostPlayedGames, setMostPlayedGames] = useState([]);

  useEffect(() => {
    fetch('http://localhost:5000/mostPlayedGames')
      .then(resp => resp.json())
      .then(data => {
        setMostPlayedGames(data);
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

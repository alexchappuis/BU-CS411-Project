
  //CBB3957503CCD086D43F77928C001F4C
  // 76561197960434622
  const steamId = document.getElementById("steamId").value;
const submitBtn = document.getElementById("submit-btn");
  const gameList = document.getElementById("game-list");

  
    // Logic for retrieving Steam User ID (not included)
    // You'll need to implement a way to get the Steam User ID from the username 
    // (explained earlier, consider user input or alternative methods)
  
    submitBtn.addEventListener("click", () => {
        const steamId = document.getElementById("steamId").value.trim(); // Remove leading/trailing whitespace
      
        if (steamId) { // Check for non-empty Steam ID
          const url = `https://api.steampowered.com/ISteamUsers/GetOwnedGames/v1/?key=CBB3957503CCD086D43F77928C001F4C&steamids=${steamId}`;
          fetch(url)
            .then(response => response.json())
            .then(data => {
              if (data.response && data.response.players) {
                // Process valid response...
              } else {
                alert("Error: No games found for this Steam ID. Please check the ID and try again.");
              }
            })
            .catch(error => {
              console.error(error);
              alert("Error fetching games. Please try again.");
            });
        } else {
          alert("Please enter your Steam ID.");
        }
      });
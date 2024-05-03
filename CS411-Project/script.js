async function fetchSteamInfo() {
    const username = document.getElementById("steamUsername").value;
    const response = await fetch(`https://api.steampowered.com/ISteamUser/ResolveVanityURL/v0001/?key=YOUR_API_KEY&vanityurl=${username}`);
    const data = await response.json();
    if (data.response.success === 1) {
      const steamId = data.response.steamid;
      const summaryResponse = await fetch(`https://api.steampowered.com/ISteamUser/GetPlayerSummaries/v0002/?key=YOUR_API_KEY&steamids=${steamId}`);
      const summaryData = await summaryResponse.json();
      const player = summaryData.response.players[0];
      document.getElementById("steamInfo").innerHTML = `
        <img src="${player.avatar}" alt="Avatar" style="float: left; margin-right: 10px;">
        <div>
          <p><strong>Username:</strong> ${player.personaname}</p>
          <p><strong>Real Name:</strong> ${player.realname || "Not provided"}</p>
          <p><strong>Country:</strong> ${player.loccountrycode || "Not provided"}</p>
        </div>
      `;
    } else {
      document.getElementById("steamInfo").innerHTML = "<p>User not found</p>";
    }
  }
  
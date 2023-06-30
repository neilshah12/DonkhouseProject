import React, { useState } from "react";
import { Link, useLoaderData } from "react-router-dom";

export default function Leaderboard() {
    const players = useLoaderData()

    const [leaderboardOption, setLeaderboardOption] = useState("biggest winners");

    const handleLeaderboardToggle = (option) => {
        setLeaderboardOption(option);
    };

    const filteredPlayerList = () => {
        if (leaderboardOption === "biggest winners") {
            return players
                .filter((player) => JSON.parse(player.stats).net > 0)
                .sort((a, b) => JSON.parse(b.stats).net - JSON.parse(a.stats).net)
                .slice(0, 10);
        }
        else if (leaderboardOption === "biggest losers") {
            return players
                .filter((player) => JSON.parse(player.stats).net < 0)
                .sort((a, b) => JSON.parse(a.stats).net - JSON.parse(b.stats).net)
                .slice(0, 10);
        } 
        else if (leaderboardOption === "donk betting board of shame") {
            return players
                .filter((player) => JSON.parse(player.stats).donk[1] > 0)
                .sort((a, b) => JSON.parse(b.stats).donk[0]/JSON.parse(b.stats).donk[1]
                 - JSON.parse(a.stats).donk[0]/JSON.parse(a.stats).donk[1])
                .slice(0, 10);
        } else {
            return players;
        }
    };

    return (
        <div className="leaderboard-container">
          <div className="leaderboard-toggler">
                <button
                    className={leaderboardOption === "biggest winners" ? "active" : ""}
                    onClick={() => handleLeaderboardToggle("biggest winners")}
                >
                    Winningest
                </button>
                <button
                    className={leaderboardOption === "biggest losers" ? "active" : ""}
                    onClick={() => handleLeaderboardToggle("biggest losers")}
                >
                    Losingest
                </button>
                <button
                    className={leaderboardOption === "donk betting board of shame" ? "active" : ""}
                    onClick={() => handleLeaderboardToggle("donk betting board of shame")}
                >
                    Donk Betting Board of Shame
                </button>
            </div>
          <table className="leaderboard-table">
            <thead>
              <tr>
                <th>Player Name</th>
                <th>Player Data</th>
              </tr>
            </thead>
            <tbody>
              {filteredPlayerList().map(player => (
                <tr key={player.id}>
                  <td>
                    <Link to={player.username.toString()}>{player.username}</Link>
                  </td>
                  <td>
                    {leaderboardOption === "donk betting board of shame"
                      ? `${JSON.parse(player.stats).donk[0]} / ${JSON.parse(player.stats).donk[1]}`
                      : JSON.parse(player.stats).net}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      );
}

export const playerLoader = async () => {
    const res = await fetch('http://localhost:3001/api/get')

    return res.json()
}
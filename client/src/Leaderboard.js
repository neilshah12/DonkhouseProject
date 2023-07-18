import React, { useState } from "react";
import { Link, useLoaderData, useNavigate } from "react-router-dom";
import Select from 'react-select';

export default function Leaderboard() {
    const players = useLoaderData()
    const [selectedOption, setSelectedOption] = useState("hello");
    const [leaderboardOption, setLeaderboardOption] = useState("biggest winners");
    const navigate = useNavigate();

    const handleLeaderboardToggle = (option) => {
        setLeaderboardOption(option);
    };

    const extractPlayers = () => {
      const result = [];

      for (let i = 0; i < players.length; i++) {
        const obj = players[i];
        const username = obj.username;
        const newObj = { value: username, label: username };
        result.push(newObj);
      }
      return result;
    }
    const options = extractPlayers(players);

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
        else if (leaderboardOption === "most aggressive") {
          return players
              .filter((player) => JSON.parse(player.stats).vpip[1] > 0)
              .sort((a, b) => JSON.parse(b.stats).vpip[0]/JSON.parse(b.stats).vpip[1]
                 - JSON.parse(a.stats).vpip[0]/JSON.parse(a.stats).vpip[1])
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

    const handleOptionChange = e => {
      setSelectedOption(e.value);
      const link = e.value.toString();
      navigate(link)
    };

    return (
        <div className="board">
          <Select 
            options={options} 
            onChange={handleOptionChange}
            value={options.filter(function(option) {
              return option.value === selectedOption;
            })} 
          />
          <div className="duration">
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
                <button
                    className={leaderboardOption === "most aggressive" ? "active" : ""}
                    onClick={() => handleLeaderboardToggle("most aggressive")}
                >
                    Most Aggressive
                </button>
            </div>
            <div className="leaderboard-table">
              {filteredPlayerList().map((player, index) => (
                <Link
                  key={player.username.toString()}
                  to={player.username.toString()}
                  className="leaderboard-entry"
                >
                  <div className="flex">
                    <div className="item">
                      {player.username}
                    </div>
                    <div className="item">
                      <span>
                        {leaderboardOption === "most aggressive" && `${JSON.parse(player.stats).vpip[0]} / ${JSON.parse(player.stats).vpip[1]}`}
                        {leaderboardOption === "donk betting board of shame" && `${JSON.parse(player.stats).donk[0]} / ${JSON.parse(player.stats).donk[1]}`}
                        {leaderboardOption === "biggest winners" && `${JSON.parse(player.stats).net}`}
                        {leaderboardOption === "biggest losers" && `${JSON.parse(player.stats).net}`}
                      </span>
                    </div>
                  </div>
                </Link>
              ))}
            </div>
        </div>
      );
}

export const playerLoader = async () => {
    const res = await fetch('http://localhost:3001/api/get')

    return res.json()
}
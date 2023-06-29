import React, { useState, useEffect } from "react";
import { Link, useLoaderData } from "react-router-dom";

export default function Leaderboard() {
    const players = useLoaderData()
    const [leaderboardOption, setLeaderboardOption] = useState("biggest winners");

    const handleLeaderboardToggle = (option) => {
        setLeaderboardOption(option);
    };

    const filteredPlayerList = () => {
        if (leaderboardOption === "biggest winners") {
        return players.filter((player) => player.net > 0).sort((a, b) => b.net - a.net);
        } else if (leaderboardOption === "biggest losers") {
        return players.filter((player) => player.net < 0).sort((a, b) => a.net - b.net);
        } else {
        return players;
        }
    };
    
    return (
        <div className="leaderboard">
            <div className="leaderboard-toggler">
                <button
                    className={leaderboardOption === "biggest winners" ? "active" : ""}
                    onClick={() => handleLeaderboardToggle("biggest winners")}
                >
                    Biggest Winners
                </button>
                <button
                    className={leaderboardOption === "biggest losers" ? "active" : ""}
                    onClick={() => handleLeaderboardToggle("biggest losers")}
                >
                    Biggest Losers
                </button>
            </div>
            {filteredPlayerList().map(player => (
                <Link to={player.username.toString()} key={player.id}>
                    <p>{player.username} | {player.net}</p>
                </Link>
            ))}
      </div>
    );
}

export const playerLoader = async () => {
    const res = await fetch('http://localhost:3001/api/get')

    return res.json()
}
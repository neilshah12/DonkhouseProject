import React, { useState, useEffect } from "react";
import Axios from 'axios';
import { useHistory } from 'react-router-dom';

const Leaderboard = () => {
    const [playerList, setPlayerList] = useState([]);
    const [leaderboardOption, setLeaderboardOption] = useState("biggest winners");
    const history = useHistory();

    useEffect(() => {
        Axios.get('http://localhost:3001/api/get').then((response) => {
        setPlayerList(response.data);
        });
    }, []);

    const handleLeaderboardToggle = (option) => {
        setLeaderboardOption(option);
    };

    const filteredPlayerList = () => {
        if (leaderboardOption === "biggest winners") {
        return playerList.filter((player) => player.net > 0).sort((a, b) => b.net - a.net);
        } else if (leaderboardOption === "biggest losers") {
        return playerList.filter((player) => player.net < 0).sort((a, b) => a.net - b.net);
        } else {
        return playerList;
        }
    };

    const handlePlayerClick = (username) => {
        // Redirect the user to a new page with player statistics
        history.push(`/player/${username}`);
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
            
            <div className="leaderboard">
                {filteredPlayerList().map((val) => (
                    <h4 key={val.username} onClick={() => handlePlayerClick(val.username)}>
                    Username: {val.username} | Net: {val.net} 
                    </h4>
                ))}
            </div>
      </div>
    );
}
 
export default Leaderboard;
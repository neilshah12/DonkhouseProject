import { Link, useLoaderData, useParams } from "react-router-dom";

export default function PlayerInfo() {
    const { username } = useParams()
    const player_info = useLoaderData()
    const statistics = JSON.parse(player_info[0].stats);
    const statistics_entries = Object.entries(statistics).filter(([key]) => !["username", "net", "raised"].includes(key));
    return (
        <div className="playerinfo">
          <div className="leaderboard-table">
            <div className="flex">
              <h3>{username}</h3>
              <div className="item">{(JSON.parse(player_info[0].stats).net >= 0 ? "+$" : "-$") + Math.abs(JSON.parse(player_info[0].stats).net)}</div>
            </div>
            {player_info.map(game => (
              <Link to={`/game/${game.id}`} key={game.id} className="leaderboard-entry">
                <div className="flex">
                <div className="item">
                  {game.name.replace("logs/", "")}
                </div>
                <div className="item">
                  {new Date(game.date).toLocaleDateString()}
                </div>
                </div>
              </Link>
            ))}
          </div>

          <table className="leaderboard-table">
            <tbody>
                {statistics_entries.map(([name, data]) => (
                <tr key={name}>
                    <td>{name}</td>
                    <td>{data[0]} / {data[1]}</td>
                </tr>
                ))}
            </tbody>
            </table>
        </div>
      );
}

export const playerInfoLoader = async ({ params }) => {
    const { username } = params
    const res = await fetch('http://localhost:3001/api/get/' + username)

    
    return res.json()
}
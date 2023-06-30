import { Link, useLoaderData, useParams } from "react-router-dom";

export default function PlayerInfo() {
    const { username } = useParams()
    const player_info = useLoaderData()
    const statistics = JSON.parse(player_info[0].stats);
    const statistics_entries = Object.entries(statistics).filter(([key]) => !["username", "net", "raised"].includes(key));
    return (
        <div className="playerinfo">
          <table className="leaderboard-table">
            <thead>
              <tr>
                <th>{username}</th>
                <th>{(JSON.parse(player_info[0].stats).net >= 0 ? "+$" : "-$") + Math.abs(JSON.parse(player_info[0].stats).net)}</th>
              </tr>
            </thead>
            <tbody>
              {player_info.map(game => (
                <tr key={game.id}>
                  <td>
                    <Link to={`/game/${game.id}`}>{game.name.replace("logs/", "")}</Link>
                  </td>
                  <td>{new Date(game.date).toLocaleDateString()}</td>
                </tr>
              ))}
            </tbody>
          </table>

          <table>
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
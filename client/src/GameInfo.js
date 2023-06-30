import { Link, useLoaderData, useParams } from "react-router-dom"

export default function GameInfo() {
    const { id } = useParams()
    const [players] = useLoaderData()

    const playerNets = JSON.parse(players.playerNets).player_nets;
    const sortedEntries = Object.entries(playerNets).sort((a, b) => b[1] - a[1]);
    console.log(sortedEntries)
    return (
        <div className="playerinfo">
          <table className="leaderboard-table">
            <thead>
              <tr>
                <th>Username</th>
                <th>Net</th>
              </tr>
            </thead>
            <tbody>
              {sortedEntries.map(([username, net]) => (
                <tr key={username}>
                  <td>
                    <Link to={`/${username}`}>{username}</Link>
                  </td>
                  <td>{net}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      );
}

export const gameInfoLoader = async ({ params }) => {
    const { id } = params
    const res = await fetch('http://localhost:3001/api/get/game/' + id)

    const a = res.json()
    console.log(a)
    return a
}
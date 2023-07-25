import { Link, useLoaderData } from "react-router-dom"

export default function GameInfo() {
    const [players] = useLoaderData()

    const playerNets = JSON.parse(players.playerNets).player_nets;
    const sortedEntries = Object.entries(playerNets).sort((a, b) => b[1] - a[1]);
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
                    <Link to={`/${username}`} className="table-link">{username}</Link>
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
    const res = await fetch('http://devalshah-001-site7.ctempurl.com/api/get/game/' + id)

    if (!res.ok) {
      throw Error('Database is down, please come back another time and let Neil know')
    }
    
    return res.json()
}
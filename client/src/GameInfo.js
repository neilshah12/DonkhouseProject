import { Link, useLoaderData, useParams } from "react-router-dom"

export default function GameInfo() {
    const { id } = useParams()
    const [players] = useLoaderData()

    const playerNets = JSON.parse(players.playerNets).player_nets;
    const sortedEntries = Object.entries(playerNets).sort((a, b) => b[1] - a[1]);
    console.log(sortedEntries)
    return (
        <div className="playerinfo">
            {sortedEntries.map(([username, net]) => (
                <Link to={`/${username}`} key={username}>
                    <p>{username} | {net}</p>
                </Link>
            ))}
        </div>
    )
}

export const gameInfoLoader = async ({ params }) => {
    const { id } = params
    const res = await fetch('http://localhost:3001/api/get/game/' + id)

    const a = res.json()
    console.log(a)
    return a
}
import { Link, useLoaderData, useParams } from "react-router-dom";

export default function PlayerInfo() {
    const { username } = useParams()
    const games = useLoaderData()
    console.log(games)

    return (
        <div className="playerinfo">
            {games.map(game => (
                <Link to={`/game/${game.id}`} key={game.id}>
                    <p>{game.name} | {game.date}</p>
                </Link>
            ))}
        </div>
    )
}

export const playerInfoLoader = async ({ params }) => {
    const { username } = params
    const res = await fetch('http://localhost:3001/api/get/' + username)

    
    return res.json()
}
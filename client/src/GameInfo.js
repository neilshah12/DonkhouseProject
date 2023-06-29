import { useParams } from "react-router-dom"

export default function GameInfo() {
    const { id } = useParams()
    return (
        <div className="gameinfo">
            { id }
        </div>
    )
}
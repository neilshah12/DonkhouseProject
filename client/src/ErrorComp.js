import { Link, useRouteError } from "react-router-dom";

export default function ErrorComp() {
    const error = useRouteError()
    return (
        <div className="error">
            <h2>Error</h2>
            <p>Tell Neil that this is broken</p>
            <p>{error.message}</p>
            <Link to="/">Back to Homepage</Link>
        </div>
    )
}
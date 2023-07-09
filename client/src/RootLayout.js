import { Outlet, Link } from "react-router-dom"

export default function RootLayout() {
    return (
        <div className="rootlayout">
            <Link to="/" className="home-link">
                <h1 className="title">DonkHouse Live Tracker</h1>
            </Link>
            <main>
                <Outlet />
            </main> 
        </div>
    )
}
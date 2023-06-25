import { Outlet } from "react-router-dom"

export default function RootLayout() {
    return (
        <div className="rootlayout">
            <h1 className="title">DonkHouse Live Tracker</h1>

            <main>
                <Outlet />
            </main>
        </div>
    )
}
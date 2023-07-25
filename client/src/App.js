import {createBrowserRouter, Route, createRoutesFromElements, RouterProvider} from 'react-router-dom';
import Leaderboard, { playerLoader } from "./Leaderboard";
import './App.css';
import './style.css';
import RootLayout from "./RootLayout";
import PlayerInfo, { playerInfoLoader } from "./PlayerInfo";
import GameInfo, { gameInfoLoader } from "./GameInfo";
import ErrorComp from './ErrorComp';

const router = createBrowserRouter(
  createRoutesFromElements(
    <Route path="/" element={<RootLayout />} errorElement={<ErrorComp />}>
        <Route index element={<Leaderboard />} loader={playerLoader}/>
        <Route path=":username" element={<PlayerInfo />} loader={playerInfoLoader}/>
        <Route path="game/:id" element={<GameInfo />} loader={gameInfoLoader}/>
    </Route>
  )
)

function App() {
  return (
    <div className="App">
      <RouterProvider router={router} />
    </div>
  );
}

export default App;
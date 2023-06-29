import React, { useState, useEffect } from "react";
import {createBrowserRouter, Route, createRoutesFromElements, RouterProvider} from 'react-router-dom';
import Leaderboard, { playerLoader } from "./Leaderboard";
import './App.css';
import RootLayout from "./RootLayout";
import PlayerInfo, { playerInfoLoader } from "./PlayerInfo";
import GameInfo from "./GameInfo";

const router = createBrowserRouter(
  createRoutesFromElements(
    <Route path="/" element={<RootLayout />}>
        <Route index element={<Leaderboard />} loader={playerLoader} />
        <Route path=":username" element={<PlayerInfo />} loader={playerInfoLoader}/>
        <Route path="game/:id" element={<GameInfo />}/>
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
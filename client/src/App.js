import React, { useState, useEffect } from "react";
import Leaderboard from "./Leaderboard";
import './App.css';

function App() {

  return (
    <div className="App">
      <h1 className="title">DonkHouse Live Tracker</h1>
      <Leaderboard />
    </div>
  );
}

export default App;
const mysql = require('mysql');
const bodyParser = require('body-parser');
const cors = require('cors');
const express = require('express');
const app = express();

// Create a connection pool
const pool = mysql.createPool({
  connectionLimit: 10,
  host: 'MYSQL5048.site4now.net',
  user: 'a53d6c_donktrk',
  password: 'donkhouse72',
  database: 'db_a53d6c_donktrk'
});

app.use(cors());
app.use(bodyParser.urlencoded({ extended: true }))
// Define a route to handle the query
app.get('/api/get', (req, res) => {
    // Perform the query using pool.query
    pool.query('SELECT * FROM players', (error, results, fields) => {
      if (error) {
        console.error('Error executing query:', error);
        res.status(500).json({ error: 'An error occurred' });
        return;
      }
      
      // Send the query results as the response
      res.json(results);
    });
});

app.get('/api/get/:username', (req, res) => {
    const username = req.params.username;
    // Perform the query using pool.query
    const query = `
      SELECT games.id, games.date, games.name, players.stats
      FROM games
      JOIN association ON games.id = association.game_id
      JOIN players ON association.player_id = players.id
      WHERE players.username = ?;
    `;
    
    pool.query(query, [username], (error, results, fields) => {
      if (error) {
        console.error('Error executing query:', error);
        res.status(500).json({ error: 'An error occurred' });
        return;
      }
    
      // Send the query results as the response
      res.json(results);
    });
});

app.get('/api/get/game/:id', (req, res) => {
  const game_id = parseInt(req.params.id)
  const query = `
  SELECT games.playerNets
  FROM games
  WHERE games.id = ?
  `;

  pool.query(query, [game_id], (error, results, fields) => {
    if (error) {
      console.error('Error executing query:', error);
      res.status(500).json({ error: 'An error occurred' });
      return
    }
    res.json(results)
  });
});

app.listen(3001, () => {
    console.log("running on port 3001");
})
require('dotenv').config();
const express = require('express');
const redis = require('redis');
const cookieParser = require('cookie-parser');
const authRoutes = require('./routes/authRoutes');
const { login } = require('./controllers/authController'); // Import login function
const bodyParser = require('body-parser');
const pool = require('./config/database');

const app = express();
const client = redis.createClient();

client.on('error', (err) => {
  console.error('Redis error:', err);
});

app.use(express.json());
app.use(cookieParser());
app.use(bodyParser.json());

// Use authentication routes
app.use('/auth', authRoutes);

// User registration route
app.post('/register', async (req, res) => {
  const { username, email, password } = req.body;
  try {
    const result = await pool.query(
      'INSERT INTO users (username, email, password) VALUES ($1, $2, $3) RETURNING *',
      [username, email, password]
    );
    res.status(201).json({ message: 'User registered successfully', user: result.rows[0] });
  } catch (error) {
    res.status(500).json({ error: 'Error registering user' });
  }
});

// User login route
app.post('/login', async (req, res) => {
  const { email, password } = req.body;
  try {
    const result = await pool.query('SELECT * FROM users WHERE email = $1 AND password = $2', [email, password]);
    if (result.rows.length > 0) {
      res.status(200).json({ message: 'Login successful', token: 'fake-jwt-token' });
    } else {
      res.status(401).json({ error: 'Invalid credentials' });
    }
  } catch (error) {
    res.status(500).json({ error: 'Error logging in' });
  }
});
module.exports = app;

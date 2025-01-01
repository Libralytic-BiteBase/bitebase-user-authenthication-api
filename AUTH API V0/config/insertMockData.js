const { Pool } = require('pg');
const bcrypt = require('bcrypt');
require('dotenv').config();

const pool = new Pool({
  host: process.env.DB_HOST,
  port: process.env.DB_PORT,
  user: process.env.DB_USER,
  password: process.env.DB_PASSWORD,
  database: 'postgres', // Connect to the default 'postgres' database to create the new database
});

const createDatabaseAndInsertMockData = async () => {
  // Use a separate client for creating the database
  const createDbClient = await pool.connect();
  try {
    // Create the database if it doesn't exist
    await createDbClient.query(`CREATE DATABASE ${process.env.DB_NAME}`);
    console.log(`Database ${process.env.DB_NAME} created successfully`);
  } catch (error) {
    if (error.code === '42P04') {
      console.log(`Database ${process.env.DB_NAME} already exists`);
    } else {
      console.error('Error creating database:', error);
      return;
    }
  } finally {
    createDbClient.release();
  }

  // Connect to the newly created database
  const newPool = new Pool({
    host: process.env.DB_HOST,
    port: process.env.DB_PORT,
    user: process.env.DB_USER,
    password: process.env.DB_PASSWORD,
    database: process.env.DB_NAME,
  });

  const newClient = await newPool.connect();
  try {
    await newClient.query('BEGIN');

    // Create the users table
    await newClient.query(`
      CREATE TABLE IF NOT EXISTS users (
        id SERIAL PRIMARY KEY,
        username VARCHAR(50) UNIQUE NOT NULL,
        email VARCHAR(100) UNIQUE NOT NULL,
        password VARCHAR(255) NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
      );
    `);

    // Insert mock data into the users table
    const hashedPassword1 = await bcrypt.hash('password1', 10);
    const hashedPassword2 = await bcrypt.hash('password2', 10);
    const hashedPassword3 = await bcrypt.hash('password3', 10);
    
    await newClient.query(`
      INSERT INTO users (username, email, password) VALUES
      ('john_doe_updated', 'john.doe@example.com', $1),
      ('jane_smith_updated', 'jane.smith@example.com', $2),
      ('alice_jones_updated', 'alice.jones@example.com', $3)
      ON CONFLICT (username) DO NOTHING;
    `, [hashedPassword1, hashedPassword2, hashedPassword3]);

    await newClient.query('COMMIT');
    console.log('Mock data inserted successfully');
  } catch (error) {
    await newClient.query('ROLLBACK');
    console.error('Error inserting mock data:', error);
  } finally {
    newClient.release();
  }
};

createDatabaseAndInsertMockData().catch((err) => console.error('Unexpected error:', err));

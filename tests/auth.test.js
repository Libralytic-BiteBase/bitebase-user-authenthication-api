const { app, server } = require('../server');
const pool = require('../config/database');
const request = require('supertest');
const bcrypt = require('bcrypt');

async function resetDatabase() {
  const client = await pool.connect();
  try {
    await client.query('TRUNCATE users CASCADE');
    const hashedPassword = await bcrypt.hash('hashedpassword', 10);
    await client.query(
      'INSERT INTO users (username, email, password) VALUES ($1, $2, $3)',
      ['testuser', 'test@example.com', hashedPassword]
    );
  } finally {
    client.release();
  }
}

describe('Auth API', () => {
  beforeAll(async () => {
    // Ensure the database is connected
    await pool.query('SELECT 1');
  });

  beforeEach(async () => {
    await resetDatabase();
  });

  it('should register a new user', async () => {
    const res = await request(app)
      .post('/api/auth/register')
      .send({
        username: 'newuser',
        email: 'newuser@example.com',
        password: 'password123',
      });

    expect(res.statusCode).toBe(201);
    expect(res.body).toHaveProperty('message', 'User registered successfully');
  });

  it('should login an existing user', async () => {
    const res = await request(app)
      .post('/api/auth/login')
      .send({
        username: 'testuser',
        password: 'hashedpassword',
      });

    expect(res.statusCode).toBe(200);
    expect(res.body).toHaveProperty('token');
  });

  it('should not login with invalid credentials', async () => {
    const res = await request(app)
      .post('/api/auth/login')
      .send({
        username: 'testuser',
        password: 'wrongpassword',
      });

    expect(res.statusCode).toBe(401);
  });

  it('should have mock data in the database', async () => {
    const client = await pool.connect();
    try {
      const result = await client.query(
        'SELECT * FROM users WHERE username = $1',
        ['testuser']
      );
      expect(result.rows.length).toBe(1);
      expect(result.rows[0].email).toBe('test@example.com');
    } finally {
      client.release();
    }
  });

  afterEach(async () => {
    // Close the server after each test
    if (server && server.close) {
      await new Promise((resolve) => server.close(resolve));
    }
  });

  afterAll(async () => {
    // Close the database pool
    await pool.end();

    // Close the server
    if (server && server.close) {
      await new Promise((resolve) => server.close(resolve));
    }
  });
});

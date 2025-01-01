const db = require('../config/database');
const fs = require('fs');
const path = require('path');

async function initializeDatabase() {
  try {
    const sql = fs.readFileSync(
      path.join(__dirname, '../migrations/init.sql'),
      'utf8'
    );
    await db.query(sql);
    console.log('Database schema initialized successfully');
  } catch (error) {
    console.error('Error initializing database:', error);
  } finally {
    db.end();
  }
}

initializeDatabase();

const crypto = require('crypto');
const fs = require('fs');
const path = require('path');

// Generate a random 256-bit (32-byte) secret
const secret = crypto.randomBytes(32).toString('hex');

// Path to the .env file
const envPath = path.join(__dirname, '.env');

// Read the existing .env file
let envContent = '';
if (fs.existsSync(envPath)) {
  envContent = fs.readFileSync(envPath, 'utf8');
}

// Add or update the JWT_SECRET in the .env file
const newEnvContent = envContent.replace(/JWT_SECRET=.*/g, '') + `\nJWT_SECRET=${secret}\n`;

// Write the updated content back to the .env file
fs.writeFileSync(envPath, newEnvContent.trim() + '\n');

console.log('JWT secret generated and stored in .env file');
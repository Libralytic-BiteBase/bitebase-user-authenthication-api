DROP TABLE IF EXISTS users;

-- Create the users table
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Insert mock data into the users table
INSERT INTO users (username, email, password) VALUES
('john_doe', 'john.doe@example.com', 'hashed_password_1'),
('jane_smith', 'jane.smith@example.com', 'hashed_password_2'),
('alice_jones', 'alice.jones@example.com', 'hashed_password_3');

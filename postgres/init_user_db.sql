CREATE DATABASE user_db;

\c user_db;

-- Création de la table User
CREATE TABLE "user" (
    uid SERIAL PRIMARY KEY,
    first_name VARCHAR(100) NOT NULL,
    last_name VARCHAR(100) NOT NULL,
    password VARCHAR(255) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL
);

-- Création de la table user_preference
CREATE TABLE user_preference (
    id SERIAL PRIMARY KEY,
    id_user INTEGER NOT NULL,
    genre_id INTEGER NOT NULL
);

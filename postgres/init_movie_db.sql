CREATE DATABASE movie_db;

\c movie_db;

-- Création de la table Genre
CREATE TABLE genre (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) UNIQUE NOT NULL
);

-- Création de la table Movie
CREATE TABLE movie (
    id SERIAL PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    genre INTEGER NOT NULL,
    director VARCHAR(100),
    release_date DATE,
    duration INTEGER,
    synopsis TEXT,
    movie_cast TEXT,
    rating DECIMAL(3, 1)
);

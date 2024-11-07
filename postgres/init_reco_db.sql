CREATE DATABASE reco_db;

\c reco_db;

-- Création de la table recommendations
CREATE TABLE recommendations (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL,
    movie_id INTEGER NOT NULL
);

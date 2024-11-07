CREATE DATABASE list_db;

\c list_db;

-- Création de la table List
CREATE TABLE list (
    id SERIAL PRIMARY KEY,
    listType VARCHAR(50) NOT NULL
);

-- Création de la table List_User
CREATE TABLE list_user (
    id SERIAL PRIMARY KEY,
    list_id INTEGER NOT NULL,
    movie_id INTEGER NOT NULL,
    user_id INTEGER NOT NULL
);

-- Création de la base de données
CREATE DATABASE list_db;

-- Se connecter à la base de données
\c list_db;

-- Modification de la table list (ou création si elle n'existe pas)
DROP TABLE IF EXISTS list_type;
CREATE TABLE list_type (
    id SERIAL PRIMARY KEY,
    name_list VARCHAR(50) UNIQUE NOT NULL  -- favoris, a_voir, deja_vu, en_cours
);

-- Modification de la table list_user (ou création si elle n'existe pas)
DROP TABLE IF EXISTS user_list;
CREATE TABLE user_list (
    id SERIAL PRIMARY KEY,
    list_id INTEGER NOT NULL REFERENCES list(id) ON DELETE CASCADE,
    movie_id INTEGER NOT NULL,
    user_id INTEGER NOT NULL,
    first_name VARCHAR(100) NOT NULL,      -- Prénom de l'utilisateur
    last_name VARCHAR(100) NOT NULL,       -- Nom de l'utilisateur
    email VARCHAR(100) NOT NULL,           -- Email de l'utilisateur
    name_movie VARCHAR(100) NOT NULL,      -- Nom du film
    UNIQUE (list_id, movie_id, user_id)    -- Empêche les doublons pour un même film dans une même liste pour un utilisateur
);

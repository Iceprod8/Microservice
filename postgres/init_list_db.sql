-- Création de la base de données
CREATE DATABASE list_db;

-- Se connecter à la base de données
\c list_db;

-- Création de la table list_type
DROP TABLE IF EXISTS list_type;
CREATE TABLE list_type (
    id SERIAL PRIMARY KEY,
    name_list VARCHAR(50) UNIQUE NOT NULL  -- favoris, a_voir, deja_vu, en_cours
);

-- Création de la table user_list
DROP TABLE IF EXISTS user_list;
CREATE TABLE user_list (
    uid SERIAL PRIMARY KEY,
    id_list_type INTEGER NOT NULL REFERENCES list_type(id) ON DELETE CASCADE,  -- clé étrangère vers list_type
    id_movie INTEGER NOT NULL,
    id_user INTEGER NOT NULL,
    first_name VARCHAR(100) NOT NULL,      -- Prénom de l'utilisateur
    last_name VARCHAR(100) NOT NULL,       -- Nom de l'utilisateur
    email VARCHAR(100) NOT NULL,           -- Email de l'utilisateur
    name_movie VARCHAR(100) NOT NULL,      -- Nom du film
    UNIQUE (id_list_type, id_movie, id_user)  -- Empêche les doublons pour un même film dans une même liste pour un utilisateur
);

--
--      MOVIE SERVICE BDD
--

-- Création de la table Genre pour les genres de films (à créer en premier pour être référencée dans d'autres tables)
CREATE TABLE genre (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) UNIQUE NOT NULL
);

-- Création de la table Movie pour le service Movies Service
CREATE TABLE movie (
    id SERIAL PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    genre INTEGER REFERENCES genre(id) ON DELETE CASCADE,
    director VARCHAR(100),
    release_date DATE,
    duration INTEGER,
    synopsis TEXT,
    cast TEXT,
    rating DECIMAL(3, 1)
);

-- Création de la table rating pour les évaluations des films
CREATE TABLE rating (
    id SERIAL PRIMARY KEY,
    id_movie INTEGER REFERENCES movie(id) ON DELETE CASCADE,
    id_user INTEGER REFERENCES "user"(uid) ON DELETE CASCADE
);



--
--      USER SERVICE BDD
--

-- Création de la table User pour le service User Service
CREATE TABLE "user" (
    uid SERIAL PRIMARY KEY,
    first_name VARCHAR(100) NOT NULL,
    last_name VARCHAR(100) NOT NULL,
    password VARCHAR(255) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL
);

-- Création de la table user_preference pour les préférences de l'utilisateur
CREATE TABLE user_preference (
    id SERIAL PRIMARY KEY,
    id_user INTEGER REFERENCES "user"(uid) ON DELETE CASCADE,
    id_genre INTEGER REFERENCES genre(id) ON DELETE CASCADE
);



--
--      RECOMMENDATION SERVICE BDD
--

-- Création de la table recommendations pour le service Recommendation Service
CREATE TABLE recommendations (
    id SERIAL PRIMARY KEY,
    id_user INTEGER REFERENCES "user"(uid) ON DELETE CASCADE,
    id_movie INTEGER REFERENCES movie(id) ON DELETE CASCADE
);



--
--      LIST SERVICE BDD
--

-- Création de la table List pour le service Lists Service
CREATE TABLE list (
    id SERIAL PRIMARY KEY,
    listType VARCHAR(50) NOT NULL
);

-- Création de la table List_User pour associer des utilisateurs à des listes et des films
CREATE TABLE list_user (
    id SERIAL PRIMARY KEY,
    id_listType INTEGER REFERENCES list(id) ON DELETE CASCADE,
    id_movie INTEGER REFERENCES movie(id) ON DELETE CASCADE
);

import requests
import os
from flask import Flask, request, jsonify
from database import db  # Importer db depuis database.py
from models import Movie  # Importer le modèle Movie après avoir défini db

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('SQLALCHEMY_DATABASE_URI')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

port = int(os.environ.get('PORT', 5000))

@app.route("/")
def home():
    return "movie microservice"

# Toutes les routes CRUD ici (ajout de film, récupération, mise à jour, suppression)

@app.route("/movies", methods=["POST"])
def add_movie():
    data = request.get_json()
    new_movie = Movie(
        title=data.get('title'),
        genre=data.get('genre'),
        director=data.get('director'),
        release_date=data.get('release_date'),
        synopsis=data.get('synopsis')
    )
    db.session.add(new_movie)
    db.session.commit()
    return jsonify({"message": "Movie added successfully!"}), 201

@app.route("/movies", methods=["GET"])
def get_movies():
    movies = Movie.query.all()
    movies_list = [
        {"id": movie.id, "title": movie.title, "genre": movie.genre, "director": movie.director,
         "release_date": movie.release_date, "synopsis": movie.synopsis}
        for movie in movies
    ]
    return jsonify(movies_list)

@app.route("/movies/<int:id>", methods=["GET"])
def get_movie(id):
    movie = Movie.query.get(id)
    if movie:
        return jsonify({"id": movie.id, "title": movie.title, "genre": movie.genre,
                        "director": movie.director, "release_date": movie.release_date,
                        "synopsis": movie.synopsis})
    else:
        return jsonify({"error": "Movie not found"}), 404

@app.route("/movies/<int:id>", methods=["PUT"])
def update_movie(id):
    data = request.get_json()
    movie = Movie.query.get(id)
    if movie:
        movie.title = data.get('title', movie.title)
        movie.genre = data.get('genre', movie.genre)
        movie.director = data.get('director', movie.director)
        movie.release_date = data.get('release_date', movie.release_date)
        movie.synopsis = data.get('synopsis', movie.synopsis)
        db.session.commit()
        return jsonify({"message": "Movie updated successfully!"})
    else:
        return jsonify({"error": "Movie not found"}), 404

@app.route("/movies/<int:id>", methods=["DELETE"])
def delete_movie(id):
    movie = Movie.query.get(id)
    if movie:
        db.session.delete(movie)
        db.session.commit()
        return jsonify({"message": "Movie deleted successfully!"})
    else:
        return jsonify({"error": "Movie not found"}), 404

# Démarrage de l'application après la définition des routes
if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True, host="0.0.0.0", port=port)

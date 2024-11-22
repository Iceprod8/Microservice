from flask import Flask
from .publisher import start_rabbitmq_consumers
from .database import db, init_db
from .router.movies import movie_blueprint
from .router.ratings import rating_blueprint
from .router.genres import genre_blueprint
from .models import Genre
import os
import json
import sys

sys.stdout.reconfigure(line_buffering=True)
sys.stderr.reconfigure(line_buffering=True)

def create_app():
    app = Flask(__name__)
    app.config.from_prefixed_env()

    init_db(app)

    app.register_blueprint(movie_blueprint, url_prefix="/movies")
    app.register_blueprint(rating_blueprint, url_prefix="/movies")
    app.register_blueprint(genre_blueprint, url_prefix="/movies")

    with app.app_context():
        db.create_all()
        populate_default_genres()
        start_rabbitmq_consumers()
    
    return app

def populate_default_genres():
    genres_file_path = os.path.join(os.path.dirname(__file__), 'genres.json')

    try:
        with open(genres_file_path, 'r') as file:
            genres_data = json.load(file)
    except FileNotFoundError:
        print(f"Error: {genres_file_path} not found.")
        return

    if Genre.query.count() == 0:
        for genre_data in genres_data:
            genre_name = genre_data.get("name")
            if genre_name:
                genre = Genre(name=genre_name)
                db.session.add(genre)
        db.session.commit()
        print("Default genres added to the database.")

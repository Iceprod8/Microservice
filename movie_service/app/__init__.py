from flask import Flask
from .publisher import start_rabbitmq_consumers
from .database import db, init_db
from .router.movies import movie_blueprint
from .router.ratings import rating_blueprint
from .router.genres import genre_blueprint
from .models import Genre, Movie
from datetime import datetime
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
        populate_default_data()
        start_rabbitmq_consumers()
    
    return app

def populate_default_data():
    data_file_path = os.path.join(os.path.dirname(__file__), 'init_data.json')
    try:
        with open(data_file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
    except FileNotFoundError:
        print(f"Error: {data_file_path} not found.")
        return
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON: {e}")
        return

    # Populate genres
    genres = data.get("genres", [])
    if Genre.query.count() == 0:
        print("Populating genres...")
        genre_map = {}
        for genre_data in genres:
            genre_name = genre_data.get("name")
            if genre_name:
                genre = Genre(name=genre_name[:50])
                db.session.add(genre)
                db.session.flush()
                genre_map[genre_name] = genre.id
        db.session.commit()
        print(f"{len(genres)} genres added to the database.")

    # Populate movies
    movies = data.get("movies", [])
    if Movie.query.count() == 0:
        print("Populating movies...")
        for movie_data in movies:
            genre_id = movie_data.get("genre_ids", [])[0] if movie_data.get("genre_ids") else None
            if not genre_id:
                print(f"Warning: Skipping movie '{movie_data.get('title')}' because it has no valid genre.")
                continue

            raw_release_date = movie_data.get("release_date")
            release_date = None
            if raw_release_date:
                try:
                    release_date = datetime.strptime(raw_release_date, "%Y-%m-%d").date()
                except ValueError:
                    print(f"Warning: Skipping movie '{movie_data.get('title')}' due to invalid date: {raw_release_date}")
                    continue

            cast = ", ".join(movie_data.get("cast", [])) if isinstance(movie_data.get("cast"), list) else movie_data.get("cast")
            director = ", ".join(movie_data.get("director", [])) if isinstance(movie_data.get("director"), list) else movie_data.get("director")

            movie = Movie(
                title=movie_data.get("title", "Unknown Title")[:100],
                genre_id=genre_id,
                director=director[:50] if director else "Unknown Director",
                release_date=release_date,
                duration=movie_data.get("duration", 0),
                synopsis=movie_data.get("synopsis", "")[:255],
                cast=cast[:255] if cast else ""
            )
            db.session.add(movie)
        db.session.commit()
        print(f"{len(movies)} movies added to the database.")
from flask import Flask
from .database import init_db
from .router.movies import movie_blueprint

def create_app():
    app = Flask(__name__)
    app.config.from_prefixed_env()

    init_db(app)

    app.register_blueprint(movie_blueprint, url_prefix="/movies")

    return app

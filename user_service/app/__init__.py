from flask import Flask
from .database import init_db, db
from .router.users import user_blueprint
from .router.preferences import preferences_blueprint
import os

def create_app():
    app = Flask(__name__)
    app.config.from_prefixed_env()

    init_db(app)

    app.register_blueprint(user_blueprint, url_prefix="/users")
    app.register_blueprint(preferences_blueprint, url_prefix="/users")

    app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY", "fallback_secret_key")

    with app.app_context():
        db.create_all()
        
    return app

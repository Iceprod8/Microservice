from flask import Flask
from .database import init_db
from .router.users import user_blueprint
from .router.preferences import preferences_blueprint

def create_app():
    app = Flask(__name__)
    app.config.from_prefixed_env()

    init_db(app)

    app.register_blueprint(user_blueprint, url_prefix="/users")
    app.register_blueprint(preferences_blueprint, url_prefix="/preferences")

    return app

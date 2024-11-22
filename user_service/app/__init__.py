from flask import Flask
from .publisher import start_rabbitmq_consumers
from .database import init_db, db
from .router.users import user_blueprint
from .router.preferences import preferences_blueprint
from flask_jwt_extended import JWTManager
import os
import sys

sys.stdout.reconfigure(line_buffering=True)
sys.stderr.reconfigure(line_buffering=True)

revoked_tokens = set()

def configure_jwt(app):
    jwt = JWTManager(app)

    @jwt.token_in_blocklist_loader
    def check_if_token_in_blocklist(jwt_header, jwt_payload):
        jti = jwt_payload["jti"]  # Identifiant unique du token
        return jti in revoked_tokens
    
def create_app():
    app = Flask(__name__)
    app.config.from_prefixed_env()

    init_db(app)

        # Initialiser JWTManager ici
    jwt = JWTManager(app)

    # Appliquer la configuration de blocage des tokens
    configure_jwt(app)

    app.register_blueprint(user_blueprint, url_prefix="/users")
    app.register_blueprint(preferences_blueprint, url_prefix="/users")

    app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY", "fallback_secret_key")

    with app.app_context():
        db.create_all()
        start_rabbitmq_consumers(app)
        
    return app

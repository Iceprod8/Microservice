from flask import Flask
from .database import init_db, db
from .router.recommendations import recommendations_blueprint
import sys

sys.stdout.reconfigure(line_buffering=True)
sys.stderr.reconfigure(line_buffering=True)

def create_app():
    app = Flask(__name__)
    app.config.from_prefixed_env()

    init_db(app)
    with app.app_context():
        db.create_all()

    app.register_blueprint(recommendations_blueprint, url_prefix="/reco")

    return app
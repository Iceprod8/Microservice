from flask import Flask
from .database import init_db, db
from .models import ListType
from .router.lists import list_blueprint

def create_app():
    app = Flask(__name__)
    app.config.from_prefixed_env()

    # Initialisation de la base de données
    init_db(app)

    # Enregistrement du blueprint
    app.register_blueprint(list_blueprint, url_prefix="/lists")

    # Initialisation des types de listes au démarrage de l'application
    with app.app_context():
        db.create_all()
        initialize_list_types()

    return app

def initialize_list_types():
    # Vérifie si la table ListType est déjà remplie
    if ListType.query.count() > 0:
        print("Les types de listes sont déjà initialisés.")
        return

    # Si la table est vide, on ajoute les types de listes
    list_types = ["favoris", "a_voir", "deja_vu", "en_cours"]
    for list_type in list_types:
        new_type = ListType(name_list=list_type)
        db.session.add(new_type)
    db.session.commit()
    print("Types de listes initialisés dans la base de données.")

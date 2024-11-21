from flask import Blueprint, request,jsonify
from ..database import db
from ..models import UserList,ListType
from ..schemas import UserListSchema,ListTypeSchema
from ..validators import validate_movie, validate_user

list_blueprint = Blueprint("lists", __name__)
user_list_schema = UserListSchema()
user_lists_schema = UserListSchema(many=True)

@list_blueprint.route("/add", methods=["POST"])
def add_movie_list():
    data = request.get_json()
    # Valider l'existence de l'utilisateur
    is_valid_user, user_data = validate_user(data["id_user"])
    if not is_valid_user:
        return jsonify(user_data), 404
    
    # Valider l'existence du film
    is_valid_movie, movie_data = validate_movie(data["id_movie"])
    if not is_valid_movie:
        return jsonify(movie_data), 404

    # Vérifier si le type de liste existe
    list_type = ListType.query.get(data["id_list_type"])
    if not list_type:
        return jsonify({"message": "type list not exist"}), 400

    # Vérifier si l'utilisateur a déjà ajouté ce film dans cette liste
    existing_entry = UserList.query.filter_by(id_user=data["id_user"], id_movie=data["id_movie"], id_list_type=data["id_list_type"]).first()
    if existing_entry:
        return jsonify({"message": "the movie has already been added"}), 400
    
    # Créer une nouvelle entrée dans la liste
    new_list = UserList(
        id_user=data['id_user'],
        first_name=data['first_name'],
        last_name=data['last_name'],
        email=data['email'],
        id_list_type=data['id_list_type'],
        id_movie=data['id_movie'],
        name_movie=data['name_movie']
    )

    db.session.add(new_list)
    db.session.commit()

    user_list_data = user_list_schema.dump(new_list)
    return jsonify(user_list_data), 201

@list_blueprint.route("/feed-list/<int:user_id>/<int:list_id>", methods=["GET"])
def get_user_movies_in_list(user_id, list_id):
    """
    Récupérer les films ajoutés par un utilisateur dans une liste spécifique.
    """
    movies = UserList.query.filter_by(id_user=user_id, id_list_type=list_id).all()
    if not movies:
        return jsonify({"message": "No movies found for the user in the specified list"}), 404

    result = user_lists_schema.dump(movies)
    return jsonify(result), 200

@list_blueprint.route("/users/<int:user_id>", methods=["GET"])
def get_user_lists_with_movies(user_id):
    """
    Récupérer toutes les listes d'un utilisateur avec les films associés.
    """
    lists = UserList.query.filter_by(id_user=user_id).all()
    if not lists:
        return jsonify({"message": "No lists found for the user"}), 404

    # Grouper les films par type de liste
    lists_with_movies = {}
    for entry in lists:
        list_type = entry.id_list_type
        if list_type not in lists_with_movies:
            lists_with_movies[list_type] = {
                "list_type": list_type,
                "movies": []
            }
        lists_with_movies[list_type]["movies"].append(user_list_schema.dump(entry))

    return jsonify(lists_with_movies), 200

# Route pour obtenir tous les films d'une liste
@list_blueprint.route("/<int:id_list>/movies", methods=["GET"])
def get_list_movies(id_list):
    # Récupérer les films dans la liste donnée
    movies = UserList.query.filter_by(id_list_type=id_list).all()
    if not movies:
        return jsonify({"message": "List not found"}), 404
    # Utilisez l'instance du schéma pour sérialiser une liste d'objets
    result = user_lists_schema.dump(movies)
    return jsonify(result), 200

# Route pour supprimer un film d'une liste
@list_blueprint.route("/<int:list_id>/movies/<int:id_movie>", methods=["DELETE"])
def delete_movie_from_list(list_id, id_movie):
    movie = UserList.query.filter_by(id_list_type=list_id, id_movie=id_movie).first()
    if not movie:
        return jsonify({"message": "Movie not found in list"}), 404

    db.session.delete(movie)
    db.session.commit()
    return jsonify({"message": "Movie removed from list"}), 200

# Route pour supprimer une liste d'un utilisateur
@list_blueprint.route("/<int:list_id>/users/<int:user_id>", methods=["DELETE"])
def delete_list(user_id, list_id):
    user_list = UserList.query.filter_by(id_list_type=list_id, id_user=user_id).first()
    if not user_list:
        return jsonify({"message": "List not found"}), 404

    db.session.delete(user_list)
    db.session.commit()

    return jsonify({"message": "List deleted successfully"}), 200

# Schéma pour sérialiser les types de liste
list_type_schema = ListTypeSchema(many=True)

# Route pour obtenir tous les types de liste
@list_blueprint.route("/list-types", methods=["GET"])
def get_all_list_types():
    list_types = ListType.query.all()
    result = list_type_schema.dump(list_types)
    return jsonify(result), 200

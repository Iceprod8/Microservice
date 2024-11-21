from flask import Blueprint, request, jsonify
from ..publisher import publish_user_deleted, publish_user_updated
from werkzeug.security import generate_password_hash, check_password_hash
from ..database import db
from ..models import User
from ..schemas import UserSchema
from flask_jwt_extended import create_access_token, jwt_required, get_jwt, JWTManager

user_blueprint = Blueprint("user", __name__)
user_schema = UserSchema() 
users_schema = UserSchema(many=True)

# Gestion des tokens révoqués
revoked_tokens = set()

# Route pour enregistrer un utilisateur
@user_blueprint.route("/register", methods=["POST"])
def register_user():
    data = request.get_json()
    hashed_password = generate_password_hash(data["password"])
    new_user = User(
        first_name=data["first_name"],
        last_name=data["last_name"],
        password=hashed_password,
        email=data["email"]
    )
    db.session.add(new_user)
    db.session.commit()
    user_data = user_schema.dump(new_user)
    access_token = create_access_token(identity=str(new_user.uid))

    return jsonify({
        "user": user_data,
        "access_token": access_token
    }), 201

# Route pour connecter un utilisateur
@user_blueprint.route("/login", methods=["POST"])
def login_user():
    data = request.get_json()
    user = User.query.filter_by(email=data["email"]).first()
    if user and check_password_hash(user.password, data["password"]):
        access_token = create_access_token(identity=str(user.uid))
        return jsonify({
            "message": "Login successful",
            "access_token": access_token
        }), 200
    return jsonify({"message": "Invalid credentials"}), 401

# Route pour obtenir tous les utilisateurs
@user_blueprint.route("/all", methods=["GET"])
def get_all_users():
    all_users = User.query.all()
    result = users_schema.dump(all_users)
    return jsonify(result), 200

# Route pour obtenir un utilisateur par ID
@user_blueprint.route("/<int:id>", methods=["GET"])
def get_single_user(id):
    user = User.query.get(id)
    if not user:
        return jsonify({"message": "User not found"}), 404
    user_data = user_schema.dump(user)
    return jsonify(user_data), 200

# Route pour mettre à jour un utilisateur
@user_blueprint.route("/<int:id>", methods=["PUT"])
def update_user(id):
    data = request.get_json()
    user = User.query.get(id)
    if not user:
        return jsonify({"message": "User not found"}), 404

    user.first_name = data.get("first_name", user.first_name)
    user.last_name = data.get("last_name", user.last_name)
    if "password" in data:
        user.password = generate_password_hash(data["password"])
    user.email = data.get("email", user.email)

    db.session.commit()

    publish_user_updated(user)

    updated_user = user_schema.dump(user)
    return jsonify(updated_user), 200

# Route pour supprimer un utilisateur
@user_blueprint.route("/<int:id>", methods=["DELETE"])
def delete_user(id):
    user = User.query.get(id)
    if not user:
        return jsonify({"message": "User not found"}), 404

    db.session.delete(user)
    db.session.commit()
    publish_user_deleted(id)
    return jsonify({"message": "User deleted successfully"}), 200

@user_blueprint.route("/logout", methods=["POST"])
@jwt_required()
def logout_user():
    jti = get_jwt()["jti"]  # Récupérer le JWT ID unique
    revoked_tokens.add(jti)  # Ajouter le token à la liste des tokens révoqués
    return jsonify({"message": "Logout successful"}), 200

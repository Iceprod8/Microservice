from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from ..database import db
from ..models import User
from ..schemas import UserSchema

user_blueprint = Blueprint("user", __name__)
user_schema = UserSchema() 
users_schema = UserSchema(many=True)

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
    return jsonify(user_data), 201

# Route pour connecter un utilisateur
@user_blueprint.route("/login", methods=["POST"])
def login_user():
    data = request.get_json()
    user = User.query.filter_by(email=data["email"]).first()
    if user and check_password_hash(user.password, data["password"]):
        return jsonify({"message": "Login successful"}), 200
    return jsonify({"message": "Invalid credentials"}), 401

# Route pour obtenir tous les utilisateurs
@user_blueprint.route("/users", methods=["GET"])
def get_all_users():
    all_users = User.query.all()
    result = users_schema.dump(all_users)
    return jsonify(result), 200

# Route pour obtenir un utilisateur par ID
@user_blueprint.route("/users/<int:id>", methods=["GET"])
def get_single_user(id):
    user = User.query.get(id)
    if not user:
        return jsonify({"message": "User not found"}), 404
    user_data = user_schema.dump(user)
    return jsonify(user_data), 200

# Route pour mettre à jour un utilisateur
@user_blueprint.route("/users/<int:id>", methods=["PUT"])
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
    updated_user = user_schema.dump(user)
    return jsonify(updated_user), 200

# Route pour supprimer un utilisateur
@user_blueprint.route("/users/<int:id>", methods=["DELETE"])
def delete_user(id):
    user = User.query.get(id)
    if not user:
        return jsonify({"message": "User not found"}), 404
    
    db.session.delete(user)
    db.session.commit()
    return jsonify({"message": "User deleted successfully"}), 200

from flask_jwt_extended import create_access_token, jwt_required, get_jwt, JWTManager
from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from ..database import db
from ..models import User
from ..schemas import UserSchema
from ..publisher import publish_user_created, publish_user_deleted, publish_user_updated

user_blueprint = Blueprint("user", __name__)
user_schema = UserSchema() 
users_schema = UserSchema(many=True)

# Gestion des tokens révoqués
revoked_tokens = set()

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
    access_token = create_access_token(identity=new_user.id)
    user_data = user_schema.dump(new_user)
    publish_user_created(new_user)

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
        access_token = create_access_token(identity=user.id)
        return jsonify({
            "message": "Login successful",
            "access_token": access_token
        }), 200
    return jsonify({"message": "Invalid credentials"}), 401

# Route pour déconnexion
@user_blueprint.route("/logout", methods=["POST"])
@jwt_required()
def logout_user():
    jti = get_jwt()["jti"]  # Récupérer le JWT ID unique
    revoked_tokens.add(jti)  # Ajouter le token à la liste des tokens révoqués
    return jsonify({"message": "Logout successful"}), 200

# Gestionnaire global pour vérifier si le token est révoqué
def check_if_token_in_blocklist(jwt_header, jwt_payload):
    jti = jwt_payload["jti"]
    return jti in revoked_tokens

# Ajouter à l'application principale
def configure_jwt(app):
    jwt = JWTManager(app)
    jwt.token_in_blocklist_loader(check_if_token_in_blocklist)
from flask import Blueprint, request, jsonify
from ..database import db
from ..models import UserPreference
from ..schemas import UserPreferenceSchema

preferences_blueprint = Blueprint("preferences", __name__)
preference_schema = UserPreferenceSchema()
preferences_schema = UserPreferenceSchema(many=True)

@preferences_blueprint.route("/<int:uid>/preferences", methods=["POST"])
def add_user_preference(uid):
    data = request.get_json()
    new_preference = UserPreference(id_user=uid, id_genre=data["id_genre"])
    db.session.add(new_preference)
    db.session.commit()
    result = preference_schema.dump(new_preference)
    return jsonify(result), 201

@preferences_blueprint.route("/<int:uid>/preferences", methods=["GET"])
def get_user_preferences(uid):

    preferences = UserPreference.query.filter_by(id_user=uid).all()
    if not preferences:
        return jsonify({"message": "No preferences found for this user."}), 404

    genre_ids = [preference.id_genre for preference in preferences]
    return jsonify({"user_id": uid, "preferred_genres": genre_ids})

@preferences_blueprint.route("/<int:uid>/preferences/<int:preference_id>", methods=["DELETE"])
def delete_user_preference(uid, preference_id):
    preference = UserPreference.query.filter_by(id_user=uid, id=preference_id).first()

    if not preference:
        return jsonify({"message": "Preference not found."}), 404

    db.session.delete(preference)
    db.session.commit()

    return jsonify({"message": "Preference deleted successfully."}), 200

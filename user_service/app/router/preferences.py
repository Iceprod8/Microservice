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
    return preference_schema.jsonify(new_preference), 201

from marshmallow import Schema, fields

class ListTypeSchema(Schema):
    id = fields.Int()
    name_list = fields.Str(required=True)  # favoris, a_voir, deja_vu, en_cours


class UserListSchema(Schema):
    uid = fields.Int()
    id_user = fields.Int(required=True)  # Identifiant de l'utilisateur, récupéré via l'API du service d'utilisateurs
    first_name = fields.Str(required=True)  # récupéré via l'API du service d'utilisateurs
    last_name = fields.Str(required=True)  # récupéré via l'API du service d'utilisateurs
    email = fields.Email(required=True)  # récupéré via l'API du service d'utilisateurs
    id_list_type = fields.Nested(ListTypeSchema, only=("id", "name_list"))  # Inclut id et name_list de ListType
    id_movie = fields.Int(required=True)  # Identifiant du film, récupéré via l'API du service de films
    name_movie = fields.Str(required=True)  # Nom du film

from marshmallow import Schema, fields

class ListTypeSchema(Schema):
    id = fields.Int()
    name = fields.Str(required=True)  # favoris, a_voir, deja_vu, en_cours
    


class UserListSchema(Schema):
    id = fields.Int()
    id_user = fields.Int(required=True)
    id_list_type = fields.Int(required=True)
    list_type = fields.Nested(ListTypeSchema, only=("id", "name"))  # Récupère seulement l'id et le nom du type
    movies = fields.List(fields.Nested("ListMovieSchema"))  # Récupère les films de la liste


class ListMovieSchema(Schema):
    id = fields.Int()
    id_user_list = fields.Int(required=True)
    id_movie = fields.Int(required=True)  # Référence à l'ID d'un film dans la base Movie


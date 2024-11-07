from marshmallow import Schema, fields

class UserSchema(Schema):
    uid = fields.Int()
    first_name = fields.Str(required=True)
    last_name = fields.Str(required=True)
    email = fields.Email(required=True)
    password = fields.Str(load_only=True, required=True)

class UserPreferenceSchema(Schema):
    id = fields.Int()
    id_user = fields.Int(required=True)
    id_genre = fields.Int(required=True)

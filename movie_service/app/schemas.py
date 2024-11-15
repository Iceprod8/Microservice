from marshmallow import Schema, fields

class MovieSchema(Schema):
    uid = fields.Int()
    first_name = fields.Str(required=True)
    last_name = fields.Str(required=True)
    email = fields.Email(required=True)
    password = fields.Str(load_only=True, required=True)

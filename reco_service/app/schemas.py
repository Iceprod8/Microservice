from marshmallow import Schema, fields

class RecommendationSchema(Schema):
    id = fields.Int()
    user_id = fields.Int(required=True)
    movie_id = fields.Int(required=True)



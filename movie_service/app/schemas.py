from marshmallow import Schema, fields, validate

class MovieSchema(Schema):
    id = fields.Int(dump_only=True)
    title = fields.Str(required=True)
    genre_id = fields.Int()
    genre = fields.Nested("GenreSchema", only=("id", "name"), dump_only=True)
    director = fields.Str()
    release_date = fields.Date()
    duration = fields.Int()
    synopsis = fields.Str()
    cast = fields.Str()
    rating = fields.Float(dump_only=True)
    
class GenreSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True, validate=validate.Length(min=1))

class RatingSchema(Schema):
    id = fields.Int(dump_only=True)
    movie_id = fields.Int(required=True)
    user_id = fields.Int(required=True)
    score = fields.Float(required=True, validate=validate.Range(min=1, max=5))

    movie = fields.Nested("MovieSchema", only=("id", "title", "rating"), dump_only=True)

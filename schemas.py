from marshmallow import Schema, fields


class MovieSchema(Schema):
    id = fields.Int()
    title = fields.Str()
    description = fields.Str()
    trailer = fields.Str()
    year = fields.Int()
    rating = fields.Float()
    genre = fields.Int()
    director = fields.Int()


movie_schema = MovieSchema()
movies_schema = MovieSchema(many=True)

# app.py

from flask import Flask, request
from flask_restx import Api, Resource
from flask_sqlalchemy import SQLAlchemy
from marshmallow import Schema, fields

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
api = Api(app)
api.app.config['RESTX_JSON'] = {'ensure_ascii': False, 'indent': 4}
movies_ns = api.namespace('movies')
directors_ns = api.namespace('directors')
genres_ns = api.namespace('genres')

###___________________________________________________________________________________________


class Movie(db.Model):
    __tablename__ = 'movie'
    """Модель класса фильмы."""
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255))
    description = db.Column(db.String(255))
    trailer = db.Column(db.String(255))
    year = db.Column(db.Integer)
    rating = db.Column(db.Float)
    genre_id = db.Column(db.Integer, db.ForeignKey("genre.id"))
    genre = db.relationship("Genre")
    director_id = db.Column(db.Integer, db.ForeignKey("director.id"))
    director = db.relationship("Director")


class MovieSchema(Schema):
    """Схема для сериализации класса фильмы."""
    id = fields.Int()
    title = fields.Str()
    description = fields.Str()
    trailer = fields.Str()
    year = fields.Int()
    rating = fields.Float()
    genre_id = fields.Int()
    director_id = fields.Int()

###_________________________________________________________________________________


class Director(db.Model):
    __tablename__ = 'director'
    """Модель класса режиссеров."""
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))


class DirectorSchema(Schema):
    """Схема для сериализации класса режиссеров."""
    id = fields.Int()
    name = fields.Str()

###____________________________________________________________________________________


class Genre(db.Model):
    __tablename__ = 'genre'
    """Модель класса жанров."""
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))


class GenreSchema(Schema):
    """Схема для сериализации класса жанров."""
    id = fields.Int()
    name = fields.Str()

###____________________________________________________________________________


"""Здесь регистрируем класс (Class-Based View) по пути /movies/ (эндпоинту)."""
@movies_ns.route('/')
class MovieView(Resource):
    def get(self):
        """Получение списка фильмов."""
        director_id = request.args.get('director_id')
        genre_id = request.args.get('genre_id')

        movies = Movie.query
        if director_id:
            movies = movies.filter(Movie.director_id == director_id)
        if genre_id:
            movies = movies.filter(Movie.genre_id == genre_id)

        movies = movies.all()
        return MovieSchema(many=True).dump(movies), 200

    def post(self):
        """Создание фильма, здесь мы получаем данные из запроса и создаем новую сущность в БД."""
        data = request.get_json()
        new_movie = Movie(**data)
        db.session.add(new_movie)
        db.session.commit()
        db.session.close()
        return "", 201


@movies_ns.route('/<int:mid>')
class MovieView(Resource):
    def get(self, mid):
        """Получение конкретного фильма по идентификатору."""
        movie = Movie.query.get(mid)
        return MovieSchema().dump(movie), 200

    def put(self, mid):
        """Обновление фильма по идентификатору."""
        movie = db.session.query(Movie).get(mid)
        req_json = request.json
        movie.title = req_json.get('title')
        movie.description = req_json.get('description')
        movie.trailer = req_json.get('trailer')
        movie.year = req_json.get('year')
        movie.rating = req_json.get('rating')
        movie.genre_id = req_json.get('genre_id')
        movie.director_id = req_json.get('director_id')
        db.session.add(movie)
        db.session.commit()
        return "", 204


    def patch(self, mid):
        """Частичное обновление фильма."""
        movie = Movie.query.get(mid)
        req_json = request.json
        if "title" in req_json:
            movie.title = req_json.get("title")
        if "description" in req_json:
            movie.description = req_json.get("description")
        if "trailer" in req_json:
            movie.trailer = req_json.get("trailer")
        if "year" in req_json:
            movie.year = req_json.get("year")
        if "rating" in req_json:
            movie.rating = req_json.get("rating")
        if "genre_id" in req_json:
            movie.genre_id = req_json.get("genre_id")
        if "director_id" in req_json:
            movie.director_id = req_json.get("director_id")
        db.session.add(movie)
        db.session.commit()
        return "", 204

    def delete(self, mid):
        """Удаление фильма"""
        movie = Movie.query.get(mid)
        db.session.delete(movie)
        db.session.commit()
        return "", 204

###____________________________________________________________________________


"""Здесь регистрируем класс (Class-Based View) по пути /directors/ (эндпоинту)."""
@directors_ns.route('/')
class DirectorsView(Resource):
    def get(self):
        """Получение списка режиссеров."""
        directors = Director.query.all()
        return DirectorSchema(many=True).dump(directors), 200

    def post(self):
        """Создание режиссера, здесь мы получаем данные из запроса и создаем новую сущность в БД."""
        data = request.get_json()
        new_director = Director(**data)
        db.session.add(new_director)
        db.session.commit()
        db.session.close()
        return "", 201


@directors_ns.route('/<int:rid>')
class DirectorView(Resource):
    def get(self, rid):
        """Получение конкретного режиссера по идентификатору."""
        director = Director.query.get(rid)
        return DirectorSchema().dump(director), 200

    def put(self, rid):
        """Обновление режиссера по идентификатору."""
        director = db.session.query(Director).get(rid)
        req_json = request.json
        director.name = req_json.get('name')
        db.session.add(director)
        db.session.commit()
        return "", 204


    def delete(self, rid):
        """Удаление режиссера"""
        director = Director.query.get(rid)
        db.session.delete(director)
        db.session.commit()
        return "", 204

###____________________________________________________________________________


"""Здесь регистрируем класс (Class-Based View) по пути /genres/ (эндпоинту)."""
@genres_ns.route('/')
class GenresView(Resource):
    def get(self):
        """Получение списка жанров."""
        genres = Genre.query.all()
        return GenreSchema(many=True).dump(genres), 200

    def post(self):
        """Создание жанра, здесь мы получаем данные из запроса и создаем новую сущность в БД."""
        data = request.get_json()
        new_genre = Genre(**data)
        db.session.add(new_genre)
        db.session.commit()
        db.session.close()
        return "", 201


@genres_ns.route('/<int:gid>')
class GenreView(Resource):
    def get(self, gid):
        """Получение конкретного жанра по идентификатору."""
        genre = Genre.query.get(gid)
        return GenreSchema().dump(genre), 200

    def put(self, gid):
        """Обновление жанра по идентификатору."""
        genre = db.session.query(Genre).get(gid)
        req_json = request.json
        genre.name = req_json.get('name')
        db.session.add(genre)
        db.session.commit()
        return "", 204


    def delete(self, gid):
        """Удаление жанра"""
        genre = Genre.query.get(gid)
        db.session.delete(genre)
        db.session.commit()
        return "", 204


if __name__ == '__main__':
    app.run(debug=True)

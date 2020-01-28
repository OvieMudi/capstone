import os
from flask import Flask, request, abort, jsonify, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from models import setup_db, Actor, Movie
from pagination import paginate_results


def create_app(test_config=None):
    '''
    create_app(test_config)
        creates a flask app
    '''
    app = Flask(__name__)

    setup_db(app)
    CORS(app)

    @app.route('/')
    def index():
        return redirect(url_for('get_movies'))

    @app.route('/actors')
    def get_actors():
        try:
            actors = Actor.query.all()
            formated_actors = [actor.format() for actor in actors]
            paginated_actors = paginate_results(formated_actors)

            return jsonify({
                'success': True,
                'actors': paginated_actors,
                'total_results': len(formated_actors)
            })

        except Exception as ex:
            print(ex)
            abort(500)

    @app.route('/movies')
    def get_movies():
        try:
            movies = Movie.query.all()
            formated_movies = [movie.format() for movie in movies]
            paginated_movies = paginate_results(formated_movies)

            return jsonify({
                'success': True,
                'movies': paginated_movies,
                'total_results': len(formated_movies)
            })

        except Exception as ex:
            print(ex)
            abort(500)

    @app.route('/actors', methods=["POST"])
    def post_actors():
        try:
            data = request.get_json()
            name = data.get('name', None)
            age = data.get('age', None)
            gender = data.get('gender', None)

            actor = Actor(name, age, gender)
            actor.insert()

            return jsonify({
                'success': True,
                'actor': actor.format()
            }), 201

        except Exception as ex:
            print(ex)
            abort(422)

    @app.route('/movies', methods=["POST"])
    def post_movies():
        try:
            data = request.get_json()
            title = data.get('title', None)
            release_date = data.get('release_date', None)

            movie = Movie(title, release_date)
            movie.insert()

            return jsonify({
                'success': True,
                'movie': movie.format()
            }), 201

        except Exception as ex:
            print(ex)
            abort(422)

    return app


APP = create_app()

if __name__ == '__main__':
    APP.run(host='0.0.0.0', port=8080, debug=True)

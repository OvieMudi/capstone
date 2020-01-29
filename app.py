from flask import Flask, request, abort, jsonify
from flask_cors import CORS
from werkzeug.exceptions import HTTPException
from models import setup_db, Actor, Movie
from pagination import paginate_results
from auth import Permissions, requires_auth


def get_json_data(attr):
    data = request.get_json()
    return data.get(attr, None)


permissions = Permissions()


def create_app(test_config=None):
    '''
    create_app(test_config)
        creates a flask app
    '''
    app = Flask(__name__)

    setup_db(app)
    CORS(app)

    '''
        Set CORS headers
    '''

    @app.after_request
    def access_control_headers(response):
        response.headers.add('Access-Control-Allow-Headers',
                             'Content-Type,Authorization,true')
        response.headers.add('Access-Control-Allow-Methods',
                             'GET,POST,PATCH,DELETE,OPTIONS')
        return response

    '''
        Index Route
    '''

    @app.route('/')
    def index():
        return jsonify({
            'success': True,
            'message': 'Welcome to Capstone API.'
        })

    '''
        Actors Endpoints
    '''

    @app.route('/actors')
    @requires_auth(permissions.get_actors)
    def get_actors(payload):
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

    @app.route('/actors/<int:actor_id>')
    @requires_auth(permissions.get_actors)
    def get_actor(payload, actor_id):
        try:
            actor = Actor.query.get(actor_id)
            if not actor:
                abort(404)

            return jsonify({
                'success': True,
                'actor': actor.format()
            })

        except HTTPException as err:
            abort(err.code, err.description)

        except Exception as ex:
            print(ex)
            code = getattr(ex, 'code', 422)
            abort(code)

    @app.route('/actors', methods=["POST"])
    @requires_auth(permissions.post_actors)
    def post_actors(payload):
        try:
            data = request.get_json()
            name = data.get('name', None)
            age = data.get('age', None)
            gender = data.get('gender', None)

            if not name or not age or not gender:
                abort(400)

            actor = Actor(name, age, gender)
            actor.insert()

            return jsonify({
                'success': True,
                'message': 'created',
                'actor': actor.format()
            }), 201

        except HTTPException as err:
            abort(err.code, err.description)

        except Exception as ex:
            print(ex)
            abort(422)

    @app.route('/actors/<int:actor_id>', methods=["PATCH"])
    @requires_auth(permissions.patch_actors)
    def patch_actors(payload, actor_id):
        try:
            name = get_json_data('name')
            age = get_json_data('age')
            gender = get_json_data('gender')

            actor = Actor.query.get(actor_id)
            if not actor:
                abort(404)

            if name:
                actor.name = name

            if age:
                actor.age = age

            if gender:
                actor.gender = gender

            if name or age or gender:
                actor.update()

            else:
                abort(400, "a valid input is expected")

            return jsonify({
                'success': True,
                'actor': actor.format()
            })

        except HTTPException as err:
            abort(err.code, err.description)

        except Exception as ex:
            print(ex)
            abort(422)

    @app.route('/actors/<int:actor_id>', methods=["DELETE"])
    @requires_auth(permissions.delete_actors)
    def delete_actors(payload, actor_id):
        try:
            actor = Actor.query.get(actor_id)

            if not actor:
                abort(404)

            id = actor.id
            actor.delete()

            return jsonify({
                'success': True,
                'message': 'deleted',
                'actor_id': id
            })

        except HTTPException as err:
            abort(err.code, err.description)

        except Exception as ex:
            print(ex)
            abort(422)

    '''
        Movies Endpoints
    '''

    @app.route('/movies')
    @requires_auth(permissions.get_movies)
    def get_movies(payload):
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

    @app.route('/movies/<int:movie_id>')
    @requires_auth(permissions.get_movies)
    def get_movie(payload, movie_id):
        try:
            movie = Movie.query.get(movie_id)
            if not movie:
                abort(404)

            return jsonify({
                'success': True,
                'movie': movie.format()
            })

        except HTTPException as err:
            abort(err.code, err.description)

        except Exception as ex:
            print(ex)
            code = getattr(ex, 'code', 422)
            abort(code)

    @app.route('/movies', methods=["POST"])
    @requires_auth(permissions.post_movies)
    def post_movies(payload):
        try:
            data = request.get_json()
            title = data.get('title', None)
            release_date = data.get('release_date', None)

            if not title or not requires_auth:
                abort(400, 'A valid input is required')

            movie = Movie(title, release_date)
            movie.insert()

            return jsonify({
                'success': True,
                'message': 'created',
                'movie': movie.format()
            }), 201

        except HTTPException as err:
            abort(err.code, err.description)

        except Exception as ex:
            print(ex)
            abort(422)

    @app.route('/movies/<int:movie_id>', methods=["PATCH"])
    @requires_auth(permissions.patch_movies)
    def patch_movies(payload, movie_id):
        try:
            title = get_json_data('title')
            release_date = get_json_data('release_date')

            movie = Movie.query.get(movie_id)
            if not movie:
                abort(404)

            if title:
                movie.title = title

            if release_date:
                movie.release_date = release_date

            if title or release_date:
                movie.update()

            else:
                abort(400, "a valid input is expected")

            return jsonify({
                'success': True,
                'movie': movie.format()
            })

        except HTTPException as err:
            abort(err.code, err.description)

        except Exception as ex:
            print(ex)
            abort(422)

    @app.route('/movies/<int:movie_id>', methods=["DELETE"])
    @requires_auth(permissions.delete_movies)
    def delete_movies(payload, movie_id):
        try:
            movie = Movie.query.get(movie_id)

            if not movie:
                abort(404)

            id = movie.id
            movie.delete()

            return jsonify({
                'success': True,
                'message': 'deleted',
                'movie_id': id
            })

        except HTTPException as err:
            abort(err.code, err.description)

        except Exception as ex:
            print(ex)
            abort(422)

    '''
        Error handlers
    '''

    @app.errorhandler(400)
    def invalid_request(error):
        return jsonify({
            "success": False,
            "error": 400,
            "message": 'error.description'
        }), 400

    @app.errorhandler(401)
    def auth_error(error):
        return jsonify({
            "success": False,
            "error": 401,
            "message": str(error.description)
        }), 401

    @app.errorhandler(403)
    def forbidden(error):
        return jsonify({
            "success": False,
            "error": 403,
            "message": str(error.description)
        }), 403

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            "success": False,
            "error": 404,
            "message": str(error.description) or "requested resource not found"
        }), 404

    @app.errorhandler(405)
    def method_not_found(error):
        return jsonify({
            "success": False,
            "error": 405,
            "message": "Method not allowed"
        }), 405

    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
            "success": False,
            "error": 422,
            "message": str("unprocessable")
        }), 422

    @app.errorhandler(500)
    def server_error(error):
        return jsonify({
            "success": False,
            "error": 500,
            "message": "server error"
        }), 500

    return app


APP = create_app()

if __name__ == '__main__':
    APP.run(host='0.0.0.0', port=8080, debug=True)

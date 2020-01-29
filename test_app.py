import os
import json
from unittest import TestCase, main
from environs import Env
from flask_sqlalchemy import SQLAlchemy
from app import create_app
from models import Actor, Movie, setup_db
from configparser import ConfigParser

env = Env()
env.read_env('config.env')

# Read jwt tokens from text file
config = ConfigParser()
config.read('jwt_tokens.txt')

CASTING_ASSISTANT_TOKEN = config.get('jwt_tokens', 'CASTING_ASSISTANT')
CASTING_DIRECTOR_TOKEN = config.get('jwt_tokens', 'CASTING_DIRECTOR')
EXECUTIVE_PRODUCER_TOKEN = config.get('jwt_tokens', 'EXECUTIVE_PRODUCER')

# actor_table_length = None
movie_table_length = None


class CapstoneTest(TestCase):
    """
    Class for the all test cases for Capstone
    """

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "capstone_test"
        self.database_path = env.str('TEST_DATABASE_URI')
        setup_db(self.app, self.database_path)

        self.new_valid_movie = {
            'title': 'valid movie',
            'release_date': '2017-10-02'
        }

        self.new_invalid_movie = {
            'titl': 'valid movie',
        }

        self.new_valid_actor = {
            'name': 'Anakin Skywalker',
            'age': '26',
            'gender': 'male'
        }

        self.new_invalid_actor = {
            'name': 'Ben Solo',
            'gender': 'male'
        }

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()

            movie1 = Movie('title1', '2019-10-10')
            actor1 = Actor('name1', 32, 'female')
            movie1.insert()
            actor1.insert()

    def tearDown(self):
        """Executed after reach test"""
        pass

    '''
      Test Index Route
    '''

    def test_get_200_index_route(self):
        response = self.client().get('/')
        body = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertTrue(body.get('success'))

    '''
      Test for Actors
    '''

    def test_post_actors_201(self):
        response = self.client().post(
            '/actors',
            json=self.new_valid_actor,
            headers={'Authorization': f'Bearer {CASTING_DIRECTOR_TOKEN}'}
        )
        body = json.loads(response.data)

        self.assertEqual(response.status_code, 201)
        self.assertTrue(body.get('success'))
        self.assertIn('actor', body.keys())

    def test_post_actor_400_error(self):
        response = self.client().post(
            '/actors',
            json=self.new_invalid_actor,
            headers={'Authorization': f'Bearer {CASTING_DIRECTOR_TOKEN}'}
        )
        body = json.loads(response.data)
        self.assertEqual(response.status_code, 400)
        self.assertFalse(body.get('success'))
        self.assertIn('error', body.keys())

    def test_get_all_actors_200(self):
        response = self.client().get(
            '/actors',
            headers={'Authorization': f'Bearer {CASTING_ASSISTANT_TOKEN}'}

        )
        body = json.loads(response.data)

        actor_table_length = len(body.get('actors', []))

        self.assertEqual(response.status_code, 200)
        self.assertTrue(body.get('success'))
        self.assertIn('actors', body.keys())
        self.assertIsInstance(body.get('actors'), list)

    def test_get_single_actors_200(self):
        response = self.client().get(
            '/actors/1',
            headers={'Authorization': f'Bearer {CASTING_ASSISTANT_TOKEN}'}

        )
        body = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(body.get('success'))
        self.assertIn('actor', body.keys())
        self.assertIsInstance(body.get('actor'), dict)

    def test_get_single_actors_404_error(self):
        response = self.client().get(
            '/actors/9999999',
            headers={'Authorization': f'Bearer {CASTING_ASSISTANT_TOKEN}'}

        )
        body = json.loads(response.data)
        self.assertEqual(response.status_code, 404)
        self.assertFalse(body.get('success'))
        self.assertIn('error', body.keys())

    def test_patch_actors_200(self):
        response = self.client().patch(
            '/actors/1',
            json=self.new_valid_actor,
            headers={'Authorization': f'Bearer {CASTING_DIRECTOR_TOKEN}'}

        )
        body = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(body.get('success'))
        self.assertIn('actor', body.keys())

    def test_patch_actors_404_error(self):
        response = self.client().patch(
            '/actors/99999',
            json=self.new_valid_actor,
            headers={'Authorization': f'Bearer {CASTING_DIRECTOR_TOKEN}'}

        )
        body = json.loads(response.data)
        self.assertEqual(response.status_code, 404)
        self.assertFalse(body.get('success'))
        self.assertIn('error', body.keys())

    def test_delete_actors_200(self):
        create_response = self.client().post(
            f'/actors',
            json=self.new_valid_actor,
            headers={'Authorization': f'Bearer {EXECUTIVE_PRODUCER_TOKEN}'}
        )

        created_body = json.loads(create_response.data)
        id = created_body.get('actor')['id']

        response = self.client().delete(
            f'/actors/{id}',
            headers={'Authorization': f'Bearer {CASTING_DIRECTOR_TOKEN}'}
        )

        body = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(body.get('success'))
        self.assertIn('actor_id', body.keys())

    def test_delete_actors_404_error(self):
        response = self.client().delete(
            f'/actors/9999999',
            headers={'Authorization': f'Bearer {CASTING_DIRECTOR_TOKEN}'}
        )
        body = json.loads(response.data)
        self.assertEqual(response.status_code, 404)
        self.assertFalse(body.get('success'))
        self.assertIn('error', body.keys())

    '''
      Test for Movies
    '''

    def test_post_movies_201(self):
        response = self.client().post(
            '/movies',
            json=self.new_valid_movie,
            headers={'Authorization': f'Bearer {EXECUTIVE_PRODUCER_TOKEN}'}
        )
        body = json.loads(response.data)

        self.assertEqual(response.status_code, 201)
        self.assertTrue(body.get('success'))
        self.assertIn('movie', body.keys())

    def test_post_movie_400_error(self):
        response = self.client().post(
            '/movies',
            json=self.new_invalid_movie,
            headers={'Authorization': f'Bearer {EXECUTIVE_PRODUCER_TOKEN}'}
        )
        body = json.loads(response.data)
        self.assertEqual(response.status_code, 400)
        self.assertFalse(body.get('success'))
        self.assertIn('error', body.keys())

    def test_get_all_movies_200(self):
        response = self.client().get(
            '/movies',
            headers={'Authorization': f'Bearer {CASTING_ASSISTANT_TOKEN}'}

        )
        body = json.loads(response.data)

        movie_table_length = len(body.get('movies', []))

        self.assertEqual(response.status_code, 200)
        self.assertTrue(body.get('success'))
        self.assertIn('movies', body.keys())
        self.assertIsInstance(body.get('movies'), list)

    def test_get_single_movies_200(self):
        response = self.client().get(
            '/movies/1',
            headers={'Authorization': f'Bearer {CASTING_ASSISTANT_TOKEN}'}

        )
        body = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(body.get('success'))
        self.assertIn('movie', body.keys())
        self.assertIsInstance(body.get('movie'), dict)

    def test_get_single_movies_404_error(self):
        response = self.client().get(
            '/movies/9999999',
            headers={'Authorization': f'Bearer {CASTING_ASSISTANT_TOKEN}'}

        )
        body = json.loads(response.data)
        self.assertEqual(response.status_code, 404)
        self.assertFalse(body.get('success'))
        self.assertIn('error', body.keys())

    def test_patch_movies_200(self):
        response = self.client().patch(
            '/movies/1',
            json=self.new_valid_movie,
            headers={'Authorization': f'Bearer {CASTING_DIRECTOR_TOKEN}'}

        )
        body = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(body.get('success'))
        self.assertIn('movie', body.keys())

    def test_patch_movies_404_error(self):
        response = self.client().patch(
            '/movies/99999',
            json=self.new_valid_movie,
            headers={'Authorization': f'Bearer {CASTING_DIRECTOR_TOKEN}'}

        )
        body = json.loads(response.data)
        self.assertEqual(response.status_code, 404)
        self.assertFalse(body.get('success'))
        self.assertIn('error', body.keys())

    def test_delete_movies_200(self):
        create_response = self.client().post(
            f'/movies',
            json=self.new_valid_movie,
            headers={'Authorization': f'Bearer {EXECUTIVE_PRODUCER_TOKEN}'}
        )

        created_body = json.loads(create_response.data)
        id = created_body.get('movie')['id']

        response = self.client().delete(
            f'/movies/{id}',
            headers={'Authorization': f'Bearer {EXECUTIVE_PRODUCER_TOKEN}'}
        )
        body = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(body.get('success'))

    def test_delete_movies_404_error(self):
        response = self.client().delete(
            f'/movies/99999999',
            headers={'Authorization': f'Bearer {EXECUTIVE_PRODUCER_TOKEN}'}
        )
        body = json.loads(response.data)
        self.assertEqual(response.status_code, 404)
        self.assertFalse(body.get('success'))
        self.assertIn('error', body.keys())

    def test_error_401_anauthorized(self):
        response = self.client().delete(
            f'/movies/9999999',
            headers={'Authorization': 'Bearer some_token'}
        )
        body = json.loads(response.data)
        self.assertEqual(response.status_code, 401)
        self.assertFalse(body.get('success'))
        self.assertIn('error', body.keys())


# Make the tests conveniently executable
if __name__ == "__main__":
    main()

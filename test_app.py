import os
import json
from unittest import TestCase, main
from environs import Env
from flask_sqlalchemy import SQLAlchemy
from app import create_app
from models import Actor, Movie, setup_db

env = Env()
env.read_env('config.env')


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

        self.new_invalid_move = {
            'title': 'valid movie',
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


# Make the tests conveniently executable
if __name__ == "__main__":
    main()

import os
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from datetime import datetime

db = SQLAlchemy()

DATABASE_PATH = os.environ['DATABASE_URI']


def setup_db(app, database_path=DATABASE_PATH):
    '''
    setup_db(app)
        binds a flask application and a SQLAlchemy service
    '''
    app.config['SQLALCHEMY_DATABASE_URI'] = database_path
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.app = app
    db.init_app(app)
    db.create_all()


class Actor(db.Model):
    '''
    Actor class/table
    '''
    __tablename__ = 'Actor'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    age = Column(Integer, nullable=False)
    gender = Column(String(8))

    movies = db.relationship('Movie', secondary='Career')

    def __init__(self, name, age, gender):
        self.name = name
        self.age = age
        self.gender = gender

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def format(self):
        return {
            'id': self.id,
            'name': self.name,
            'age': self.age,
            'gender': self.gender or 'non-binary'
        }

    def __repr__(self):
        return f'<Actor {self.name}, {self.gender or "non-binary"}>'


class Movie(db.Model):
    '''
    Movie class/table
    '''
    __tablename__ = 'Movie'

    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    release_date = Column(DateTime, nullable=False, default=datetime.utcnow())

    actors = db.relationship('Actor', secondary='Career')

    def __init__(self, title, release_date):
        self.title = title
        self.release_date = release_date

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def format(self):
        return {
            'id': self.id,
            'title': self.title,
            'release_date': self.release_date
        }

    def __repr__(self):
        return f'<Movie {self.id}, {self.title}>'


class CareerModel(db.Model):
    '''
    Association class/table for Actor and Movie
    '''

    __tablename__ = 'Career'

    id = Column(Integer, primary_key=True)
    actor_id = Column(Integer, ForeignKey('Actor.id'))
    movie_id = Column(Integer, ForeignKey('Movie.id'))

    actor = db.relationship(Actor, backref=db.backref(
        'career', cascade='all, delete-orphan'))
    movie = db.relationship(Movie, backref=db.backref(
        'career', cascade='all, delete-orphan'))

    def __init__(self, actor_id, movie_id):
        self.actor_id = actor_id
        self.movie_id = movie_id

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def __repr__(self):
        return f'<Movie {self.actor_id}, {self.movie_id}>'

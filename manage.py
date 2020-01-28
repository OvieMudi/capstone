from flask_script import Manager
from flask_migrate import Migrate, Manager, MigrateCommand
from sqlalchemy.orm import Session

from app import APP
from models import db, Actor, Movie, CareerModel

migrate = Migrate(APP, db)
manager = Manager(APP)

manager.add_command('db', MigrateCommand)


@manager.command
def seed_base():
    "Add seed data to the database"

    session = Session()

    actor1 = Actor('Actor1', 20, 'female')
    actor2 = Actor('Actor2', 23, 'male')
    actor3 = Actor('Actor3', 43, 'male')

    movie1 = Movie('Movie1', '2017-10-12')
    movie2 = Movie('Movie2', '2017-10-12')
    movie3 = Movie('Movie1', '2017-10-12')

    objects = [actor1, actor2, actor3, movie1, movie2, movie3]

    db.session.bulk_save_objects(objects)
    db.session.commit()


@manager.command
def seed_relationship():

    career_model11 = CareerModel(1, 1)
    career_model12 = CareerModel(1, 2)
    career_model13 = CareerModel(1, 3)
    career_model21 = CareerModel(2, 1)
    career_model31 = CareerModel(3, 1)

    objects = [career_model11, career_model12, career_model13,
               career_model21, career_model31]

    db.session.bulk_save_objects(objects)
    db.session.commit()


if __name__ == '__main__':
    manager.run()

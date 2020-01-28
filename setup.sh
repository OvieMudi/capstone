export FLASK_APP=app.py
export FLASK_ENV=development

# NOTE: first create a config.env file.
# See config.env.example for required content
. config.env

python manage.py db init
python manage.py db migrate
python manage.py db upgrade

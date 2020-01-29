# Capstone Casting Agency

Capstone is a casting agency that finds and grooms talented aspiring actors, providing a platform for them develop the skills needed to become movie stars.
Capstone also houses a large database of actors and movies around the world.

## Getting Started

#### Deployed App URL

A running API is deployed on [Heroku](https://heroku.com). Explore the API with [Postman](https://www.getpostman.com/) via the URL https://capstone66.herokuapp.com/.

Kindly see the `jwt_tokens.txt` for test tokens.

### Installing Dependencies

#### Python 3.7

Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

#### Virtual Enviornment

We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organaized. Instructions for setting up a virual enviornment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/).

```bash
python3.7 -m venv
source venv/bin/activate
```

## Environment and Database Initial Setup

With Postgres running, restore a database using the command below. The command will create tables and insert seed data.

```bash
source ./setup.sh
```

- **IMPORTANT:** create a `.env` file in the `root directory` that contains your database path. Use the `env.example` file for reference.

#### PIP Dependencies

Once you have your virtual environment setup and running, install dependencies running:

```bash
pip install -r requirements.txt
```

This will install all of the required packages we selected within the `requirements.txt` file.

##### Key Dependencies

- [Flask](http://flask.pocoo.org/) is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM we'll use handle the lightweight sqlite database. You'll primarily work in app.py and can reference models.py.

- [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#) is the extension we'll use to handle cross origin requests from our frontend server.

- [Python-Jose](https://pypi.org/project/python-jose/) is used to encrypt/decrypt and/or sign content using a variety of JWT algorithms.

## Running the server

From within the `root directory`, first ensure you are working from a virtual environment and the `setup.sh` file is run.

To run the server, execute:

```bash
export FLASK_APP=app.py
export FLASK_ENV=development

flask run
```

Setting the `FLASK_ENV` variable to `development` will detect file changes and restart the server automatically.

Setting the `FLASK_APP` variable to `app.py` directs flask to use the `app.py` file where our server lives.

## Endpoints

The endpoints of this API are protected with JWT. A valid token is required to interract with endpoints.
Kindly check the `jwt_tokens.txt` file in repo for sample tokens for test.
_Tokens will expire 24 hours after being generated_

```bash
# Actors
POST '/actors'
GET '/actors'
GET '/actors/<actor_id>'
PATCH '/actors/<actor_id>'
DELETE '/actors/<actor_id>'

# Movies
POST '/movies'
GET '/movies'
GET '/movies/<movie_id>'
PATCH '/movies/<movie_id>'
DELETE '/movies/<movie_id>'
```

#### POST '/actors'

Adds an actor to the database.

- Permission: `post:actors`
- Request params: `None`
  Request body:

```json
{
  "name": "Asajj Ventress",
  "age": 27,
  "gender": "female"
}
```

Response:

```json
{
  "actor": {
    "age": 27,
    "gender": "female",
    "id": 4,
    "name": "Asajj Ventress"
  },
  "message": "created",
  "success": true
}
```

#### GET '/actors'

Fetches all actors from the database with pagination.

- Permission: `get:actors`
- Request query params (integer): `page`

Response

```json
{
  "actors": [
    {
      "age": 20,
      "gender": "male",
      "id": 1,
      "name": "Anakin Skywalker"
    },
    {
      "age": 23,
      "gender": "male",
      "id": 2,
      "name": "Luke Shaw"
    },
    {
      "age": 26,
      "gender": "female",
      "id": 3,
      "name": "Padme Amidala"
    }
  ],
  "success": true,
  "total_results": 3
}
```

#### GET '/actors/<actor_id>'

Fetches an actor from the database by unique `id`.

- Permission: `get:actors`
- Request path params (integer): `actor_id`

Response

```json
{
  "actor": {
    "age": 27,
    "gender": "female",
    "id": 4,
    "name": "Asajj Ventress"
  },
  "success": true
}
```

#### PATCH '/actors/<actor_id>'

Updates an actor in the database by unique `id`.

- Permission: `patch:actors`
- Request Path Params (integer): `actor_id`

Request body:

```json
{
  "name": "Asajj Ventress",
  "age": 30,
  "gender": "female"
}
```

Response

```json
{
  "actor": {
    "age": 30,
    "gender": "female",
    "id": 4,
    "name": "Asajj Ventress"
  },
  "success": true
}
```

#### DELETE '/actors/<actor_id>'

Delete an actor entry in the database by unique `id`.

- Permission: `delete:actors`
- Request Path Params (integer): `actor_id`
- Request body: `None`

Response

```json
{
  "actor_id": 4,
  "message": "deleted",
  "success": true
}
```

#### POST '/movies'

Adds an movie to the database.

- Permission: `post:movies`
- Request params: `None`
  Request body:

```json
{
  "title": "Star Wars: The Clone Wars",
  "release_date": "2015-12-4"
}
```

Response:

```json
{
  "message": "created",
  "movie": {
    "id": 4,
    "release_date": "Tue, 04 Dec 2015 00:00:00 GMT",
    "title": "Star Wars: The Clone Wars"
  },
  "success": true
}
```

#### GET '/movies'

Fetches all movies from the database with pagination.

- Permission: `get:movies`
- Request query params (integer): `page`

Response

```json
{
  "movies": [
    {
      "id": 1,
      "release_date": "Thu, 12 Oct 2017 00:00:00 GMT",
      "title": "Star Wars: Episode I"
    },
    {
      "id": 2,
      "release_date": "Thu, 12 Oct 2017 00:00:00 GMT",
      "title": "Star Wars: Episode II"
    },
    {
      "id": 3,
      "release_date": "Thu, 12 Oct 2017 00:00:00 GMT",
      "title": "Star Wars: Episode III"
    }
  ],
  "success": true,
  "total_results": 3
}
```

#### GET '/movies/<movie_id>'

Fetches an movie from the database by unique `id`.

- Permission: `get:movies`
- Request path params (integer): `movie_id`

Response

```json
{
  "movie": {
    "id": 3,
    "release_date": "Thu, 12 Oct 2017 00:00:00 GMT",
    "title": "Movie1"
  },
  "success": true
}
```

#### PATCH '/movies/<movie_id>'

Updates an movie in the database by unique `id`.

- Permission: `patch:movies`
- Request Path Params (integer): `movie_id`

Request body:

```json
{
  "title": "Movie update",
  "release_date": "2019-10-11"
}
```

Response

```json
{
  "movie": {
    "id": 3,
    "release_date": "Fri, 11 Oct 2019 00:00:00 GMT",
    "title": "Movie update"
  },
  "success": true
}
```

#### DELETE '/movies/<movie_id>'

Delete an movie entry in the database by unique `id`.

- Permission: `delete:movies`
- Request Path Params (integer): `movie_id`
- Request body: `None`

Response

```json
{
  "movie_id": 4,
  "message": "deleted",
  "success": true
}
```

### Error Handling

Errors are returned as JSON objects in the following format:

```
{
    "success": False/True,
    "error": status_code,
    "message": "Error message"
}
```

The API will return three error types with the following messages when requests fail:

- 400: Bad Request
- 401: Unauthorized
- 403: Not Permitted
- 404: Resource Not Found
- 422: Not Processable
- 500: Internal server error

## Testing

To run the tests, run

```
python test_app.py
```

## Technology Stack

- [Python Programming Language](https://www.python.org/)
- [Flask Micro Web Framework](https://www.palletsprojects.com/p/flask/)
- [JSON Web TOken](https://jwt.io/)

## Author

Ovie Udih

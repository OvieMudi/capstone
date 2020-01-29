import json
from flask import request, _request_ctx_stack, abort
from functools import wraps
from jose import jwt
from urllib.request import urlopen


AUTH0_DOMAIN = 'capstone66.auth0.com'
ALGORITHMS = ['RS256']
API_AUDIENCE = '/agency'


class Permissions():
    '''Permissions()
        Exposes available role-based permissions
    '''

    def __init__(
        self,
        get_actors='get:actors',
        get_movies='get:movies',
        post_actors='post:actors',
        post_movies='post:movies',
        patch_actors='patch:actors',
        patch_movies='patch:movies',
        delete_actors='delete:actors',
        delete_movies='delete:movies'
    ):
        self.get_actors = get_actors
        self.get_movies = get_movies
        self.post_actors = post_actors
        self.post_movies = post_movies
        self.patch_actors = patch_actors
        self.patch_movies = patch_movies
        self.delete_actors = delete_actors
        self.delete_movies = delete_movies

    def __repr__(self):
        return f'''<Permissions
         {self.get_actors},
         {self.get_movies},
         {self.post_actors},
         {self.post_movies},
         {self.patch_actors},
         {self.patch_movies},
         {self.delete_actors},
         {self.delete_movies}>'''


# AuthError Exception

class AuthError(Exception):
    '''
    AuthError Exception
    A standardized way to communicate auth failure modes
    '''

    def __init__(self, error, status_code):
        self.error = error
        self.status_code = status_code


# Auth Header

def get_token_auth_header():
    auth_header = request.headers.get('Authorization', None)

    if not auth_header:
        raise AuthError({
            'code': 'authorization_header_missing',
            'description': 'an athorization header is expected'
        }, 400)

    parts = (auth_header.split())

    if (len(parts) != 2 or parts[0].lower() != 'bearer'):
        raise AuthError({
            'code': 'invalid_header',
            'description': 'authorization header must contain "Bearer" \
                 and token'
        }, 401)

    elif len(parts) > 2:
        raise AuthError({
            'code': 'invalid_header',
            'description': 'Authorization header must be bearer token.'
        }, 401)

    token = parts[1]
    return token


def check_permissions(permission, payload):
    if ('permissions' not in payload
            or permission not in payload['permissions']):
        raise AuthError({
            'code': 'invalid_header',
            'description': 'Not authorized to access this resource.'
        }, 403)

    return True


def verify_decode_jwt(token):
    jsonurl = urlopen(f'https://{AUTH0_DOMAIN}/.well-known/jwks.json')
    jwks = json.loads(jsonurl.read())

    try:
        unverified_header = jwt.get_unverified_header(token)
    except Exception as ex:
        raise AuthError({
            'code': ex,
            'description': ex
        }, 400)

    rsa_key = {}
    if 'kid' not in unverified_header:
        raise AuthError({
            'code': 'invalid_header',
            'description': 'jwt malformed.'
        }, 401)

    for key in jwks['keys']:
        if key['kid'] == unverified_header['kid']:
            rsa_key = {
                'kty': key['kty'],
                'kid': key['kid'],
                'use': key['use'],
                'n': key['n'],
                'e': key['e']
            }

    if rsa_key:
        try:
            payload = jwt.decode(
                token,
                rsa_key,
                algorithms=ALGORITHMS,
                audience=API_AUDIENCE,
                issuer=f'https://{AUTH0_DOMAIN}/'
            )

            return payload

        except jwt.ExpiredSignatureError:
            raise AuthError({
                'code': 'token_expired',
                'description': 'Token expired.'
            }, 401)

        except jwt.JWTClaimsError:
            raise AuthError({
                'code': 'invalid_claims',
                'description': 'Incorrect claims. Please, check the audience \
                    and issuer.'
            }, 401)
        except Exception:
            raise AuthError({
                'code': 'invalid_header',
                'description': 'Unable to parse authentication token.'
            }, 401)
    raise AuthError({
        'code': 'invalid_header',
        'description': 'Unable to find the appropriate key.'
    }, 401)


def requires_auth(permission=''):
    def requires_auth_decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            try:
                token = get_token_auth_header()
                print('X3XY')
                payload = verify_decode_jwt(token)
                check_permissions(permission, payload)

            except AuthError as error:
                abort(error.status_code, description=error.error)

            return f(payload, *args, **kwargs)

        return wrapper
    return requires_auth_decorator

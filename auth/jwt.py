from flask import current_app as app
from flask import abort
from datetime import datetime
import datetime as dt

import jwt
import auth
import os


algo = 'HS256'
secret = 'polar'


def make_jwt(user_id):
    payload = {
        'iss': 'polar',
        'user': user_id,
        'iat': datetime.utcnow(),
        'exp': datetime.utcnow() + dt.timedelta(hours=2)
    }

    return jwt.encode(payload, secret, algorithm=algo)


def check_jwt(token):
    try:
        payload = jwt.decode(token, secret, algorithm=algo)
    except Exception as e:
        abort(401)

    return int(payload['user'])

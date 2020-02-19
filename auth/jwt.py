from flask import current_app as app
from flask import abort
from datetime import datetime, timedelta

import jwt
import auth
import os


def make_jwt(user_id):
    encode = jwt.encode({
        'userId': user_id,
        'iat': datetime.utcnow(),
        'exp': datetime.utcnow() + timedelta(hours=2)
    }, 'polar', algorithm='HS256').decode("utf-8")
    return encode


def check_jwt(token):
    try:
        decode = jwt.decode(token, 'polar', algorithms=['HS256'])
    except jwt.ExpiredSignatureError:
        abort(401, "Token expired")
    except jwt.InvalidSignatureError:
        abort(401, "Signature verification failed")
    except jwt.InvalidAlgorithmError:
        abort(401, "The specified algorithm is not allowed")
    except jwt.DecodeError:
        abort(401, "Invalid token type")
    except:
        abort(401, "Unknown error")

    return decode['userId']

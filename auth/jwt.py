from flask import current_app as app
from flask import abort
from datetime import datetime, timedelta

import jwt
import auth
import os

def make_jwt(user_id):
    now = str(datetime.now())
    later = str(datetime.now() + timedelta(hours=2))
    encode = jwt.encode({
        'userId': user_id,
        'timestamp': now,
        'expiry': later
    }, app.secret_key, algorithm='HS256').decode("utf-8")
    return encode


def check_jwt(token):
    try:
        decode = jwt.decode(token, app.secret_key, algorithms=['HS256'])
    except jwt.InvalidSignatureError:
        abort(401, "Signature verification failed")
    except jwt.InvalidAlgorithmError:
        abort(401, "The specified algorithm is not allowed")
    except jwt.DecodeError:
        abort(401, "Invalid token type")
    except:
        abort(401, "Unknown error")

    now = datetime.now()
    later = datetime.strptime(decode['expiry'], '%Y-%m-%d %H:%M:%S.%f')

    if later < now:
        abort(401, "Token expired")

    return True

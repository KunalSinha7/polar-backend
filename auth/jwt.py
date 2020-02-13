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
    res = {
        'status': False,
        'message': None
    }
    
    try:
        decode = jwt.decode(token, app.secret_key, algorithms=['HS256'])
    except jwt.InvalidSignatureError:
        res['message'] = 'Signature verification failed'
        return res
    except jwt.InvalidAlgorithmError:
        res['message'] = 'The specified algorithm is not allowed'
        return res
    except jwt.DecodeError:
        res['message'] = 'Invalid token type'
        return res
    except:
        res['message'] = 'Unknown error'
        return res

    now = datetime.strptime(decode['timestamp'], '%Y-%m-%d %H:')
    prtin(now)

    return 1

import hashlib
import auth

from flask import request, abort, request, g
from functools import wraps



def hash_password(password, salt):
    return hashlib.sha512(str.encode(password + salt)).hexdigest()


def login_required(f):
    @wraps(f)
    def wrap(*args, **kwargs): 
        print('Login Required')
        if not request.headers['auth']:
            abort(401, message='No authorization')
        else:
            g.user = auth.jwt.check_jwt(request.headers['auth'])
        return f(*args, **kwargs)
   
    return wrap
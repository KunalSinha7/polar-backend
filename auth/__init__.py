import hashlib
import auth

from flask import request, abort, request, g
from functools import wraps



def hash_password(password, salt):
    return hashlib.sha512(str.encode(password + salt)).hexdigest()


def login_required(perm):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            print(perm)

            #put code here

            return func(*args, **kwargs)
        return wrapper
    return decorator

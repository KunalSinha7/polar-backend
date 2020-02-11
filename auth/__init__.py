import hashlib


def hash_password(password, salt):
    return hashlib.sha512(str.encode(password + salt)).hexdigest()
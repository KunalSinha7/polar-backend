from flask import Blueprint, jsonify, request, abort
import hashlib

import user.db as db
import auth
import auth.jwt
import uuid

user = Blueprint('user', __name__)


@user.route('/login', methods=['POST'])
def login():
    data = request.get_json()

    if 'email' not in data or 'password' not in data:
        abort(400, "Missing credentials")

    data['password'] = auth.hash_password(data['password'], data['email'])
    
    res = db.login(data)

    jwt = auth.jwt.make_jwt(res[0])
    resp = {
        'firstName': res[1],
        'lastName': res[2],
        'auth': jwt,
        'permissions': 'n',
    }
    return resp


@user.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    missing = []

    if 'firstName' not in data:
        missing.append('firstName')

    if 'lastName' not in data:
        missing.append('lastName')

    if 'email' not in data:
        missing.append('email')

    if 'password' not in data:
        missing.append('password')
    else:
        data['password'] = auth.hash_password(data['password'], data['email'])

    if len(missing) > 0:
        message = 'Incorrect request, missing ' + str(missing)
        abort(400, message)

    user_id = db.create_user(data)
    jwt = auth.jwt.make_jwt(user_id)
    resp = {
        'firstName': data['firstName'],
        'lastName': data['lastName'],
        'auth': jwt,
        'permissions': 'n',
    }

    return resp


@user.route('/getInfo', methods=['POST'])
def getInfo():
    data = request.get_json()
    
    if 'auth' not in data:
        abort(401, "Missing authorization")

    userId = auth.jwt.check_jwt(data['auth'])
    res = db.getInfo(userId)
    
    resp = {
        'firstName': res[1],
        'lastName': res[2],
        'email': res[3],
        'phone': res[4]
    }

    return resp


@user.route('/setInfo', methods=['POST'])
def setInfo():
    data = request.get_json()
    data['userId'] = auth.jwt.check_jwt(data['auth'])
    res = db.setInfo(data)
    return {}


@user.route('/delete', methods=['POST'])
def delete():
    data = request.get_json()
    # db.delete(data)
    return 'deleted'
    
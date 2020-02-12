from flask import Blueprint, jsonify, request, abort
import hashlib

import user.db as db
import auth
import auth.jwt

user = Blueprint('user', __name__)


@user.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    data['password'] = auth.hash_password(data['password'], data['email'])
    resp = db.login(data)
    return 'login route'


@user.route('/logout', methods=['POST'])
def logout():
    data = request.get_json()
    # invalidate jwt
    return 'logout'


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
        message = 'Incorrect request, missing' + str(missing)
        abort(400, message)

    user_id = db.create_user(data)
    jwt = auth.jwt.make_jwt(user_id)

    return jsonify({'Authorization': jwt})


@user.route('/delete', methods=['POST'])
def delete():
    data = request.get_json()
    db.delete(data)
    logout()
    return 'deleted'
    


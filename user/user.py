from flask import Blueprint, jsonify, request, abort, app, g
import hashlib

import user.db as db
import auth
import auth.jwt
import message

import uuid

user = Blueprint('user', __name__)


@user.route('/login', methods=['POST'])
def login():
    data = request.get_json()

    if 'email' not in data or 'password' not in data:
        abort(400, "Missing credentials")

    data['password'] = auth.hash_password(data['password'], data['email'])
    
    res, perms = db.login(data)

    jwt = auth.jwt.make_jwt(res[0])
    resp = {
        'firstName': res[1],
        'lastName': res[2],
        'auth': jwt,
        'permissions': perms,
    }
    return jsonify(resp)


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
    elif 'email' in data:
        data['password'] = auth.hash_password(data['password'], data['email'])

    if len(missing) > 0:
        message = 'Incorrect request, missing ' + str(missing)
        abort(400, message)

    user_id, perms = db.create_user(data)
    jwt = auth.jwt.make_jwt(user_id)
    resp = {
        'firstName': data['firstName'],
        'lastName': data['lastName'],
        'auth': jwt,
        'permissions': perms,
    }

    return jsonify(resp)


@user.route('/registerEmail', methods=['POST'])
def registerEmail():
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
    elif 'email' in data:
        data['password'] = auth.hash_password(data['password'], data['email'])

    if 'token' not in data:
        missing.append('token')

    if len(missing) > 0:
        message = 'Incorrect request, missing ' + str(missing)
        abort(400, message)


    user_id, perms = db.create_user_email(data)
    jwt = auth.jwt.make_jwt(user_id)
    resp = {
        'firstName': data['firstName'],
        'lastName': data['lastName'],
        'auth': jwt,
        'permissions': perms,
    }

    return jsonify(resp)

@user.route('/forgotPassword', methods=['POST'])
def forgotPassword():
    data = request.get_json()

    if 'email' not in data:
        abort(400, 'Missing email')
    
    user_id = db.getUserId(data['email'])
    u_link = uuid.uuid4()
    db.addLink(user_id, u_link)
    s_link = 'https://polarapp.xyz/resetPassword?token=' + str(u_link)
    message.sendNewUser(data['email'], s_link)

    return jsonify('Sent email to {}'.format(data['email']))

@user.route('/resetPassword', methods=['POST'])
def resetPassword():
    data = request.get_json()
    missing = []

    if 'email' not in data:
        missing.append('email')
    
    if 'newPassword' not in data:
        missing.append('newPassword')
    
    if 'token' not in data:
        missing.append('token')

    if len(missing) > 0:
        message = 'Incorrect request, missing ' + str(missing)
        abort(400, message)

    
    user_id = db.checkPasswordToken(data['email'], data['token'])
    db.updatePassword(user_id, auth.hash_password(data['newPassword'], data['email']), data['email'])

    return jsonify('Success')


@user.route('/getInfo', methods=['POST'])
@auth.login_required(perms=None)
def getInfo():
    res = db.getInfo(g.userId)
    
    resp = {
        'firstName': res[1],
        'lastName': res[2],
        'email': res[3],
        'phone': res[4]
    }

    return jsonify(resp)


@user.route('/setInfo', methods=['POST'])
@auth.login_required(perms=None)
def setInfo():
    data = request.get_json()
    data['userId'] = g.userId

    if 'firstName' not in data or 'lastName' not in data or 'phone' not in data:
        abort(400, "Missing data")

    res = db.setInfo(data)
    return jsonify()


@user.route('/delete', methods=['POST'])
@auth.login_required(perms=None)
def delete():
    # db.delete(data)
    return 'deleted'
    
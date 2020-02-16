from flask import Blueprint, jsonify, request, abort

import iam.db as db
import auth
import auth.jwt
import auth.perms

iam = Blueprint('iam', __name__)


@iam.route('/createRole', methods=['POST'])
def creatRole():
    data = request.get_json()
    data['userId'] = auth.jwt.check_jwt(data['auth'])
    auth.perms.checkPerms(data['userId'], 11)
    db.createRole(data)
    return {}


@iam.route('/removeRole', methods=['POST'])
def removeRole():
    data = request.get_json()
    data['userId'] = auth.jwt.check_jwt(data['auth'])
    auth.perms.checkPerms(data['userId'], 11)
    db.removeRole(data['roleId'])
    return {}
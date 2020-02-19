from flask import Blueprint, jsonify, request, abort, g

import iam.db as db
import auth
import auth.jwt
import auth.perms

iam = Blueprint('iam', __name__)


@iam.route('/createRole', methods=['POST'])
@auth.login_required(perms=[11])
def creatRole():
    data = request.get_json()
    if 'roleName' not in data or 'permissions' not in data:
        abort(400, "Missing data")
    db.createRole(data)
    return jsonify()


@iam.route('/removeRole', methods=['POST'])
@auth.login_required(perms=[11])
def removeRole():
    data = request.get_json()
    if 'roleId' not in data:
        abort(400, "Missing data")
    db.removeRole(data['roleId'])
    return jsonify()

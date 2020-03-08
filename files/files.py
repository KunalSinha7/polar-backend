from flask import Blueprint, jsonify, request, abort, app, g
import hashlib

import files.db as db
import auth
import auth.jwt
import auth.perms
import user.db as user

files = Blueprint('files', __name__)

@files.route('/upload', methods=['POST'])
@auth.login_required(perms=[2])
def upload():
    data = request.get_json()
    data['userId'] = g.userId

    if 'name' not in data or 'desc' not in data or 'file' not in data or 'roles' not in data:
        abort(400, "Missing data")
    
    # develop s3 module

    data['store'] = data['name'] + '.txt'
    db.upload(data)

    return jsonify()


@files.route('/delete', methods=['POST'])
@auth.login_required(perms=[2])
def delete():
    data = request.get_json()
    if 'fileId' not in data:
        abort(400, "Missing data")
    # delete from s3
    db.delete(data['fileId'])
    return jsonify()


@files.route('/view', methods=['POST'])
@auth.login_required(perms=[1])
def view():
    res = db.view(g.userId)
    return jsonify(res)
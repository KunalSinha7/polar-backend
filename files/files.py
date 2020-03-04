from flask import Blueprint, jsonify, request, abort, app, g
import hashlib

import files.db as db
import auth
import auth.jwt
import auth.perms

files = Blueprint('files', __name__)

@files.route('/upload', methods=['POST'])
@auth.login_required(perms=[2])
def upload():
    data = request.get_json()
    data['userId'] = g.userId

    if 'name' not in data or 'desc' not in data or 'file' not in data or 'roles' not in data:
        abort(400, "Missing data")
    
    # develop s3 module
    
    data['store'] = 'beep'
    db.upload(data)

    return jsonify()
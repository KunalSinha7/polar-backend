from flask import Blueprint, jsonify, request, abort, app, g, send_file
import hashlib

import files.db as db
import auth
import auth.jwt
import auth.perms
import user.db as user
import boto3

files = Blueprint('files', __name__)

@files.route('/upload', methods=['POST'])
@auth.login_required(perms=[2])
def upload():
    data = request.get_json()
    data['userId'] = g.userId

    if 'name' not in data or 'desc' not in data or 'file' not in data or 'roles' not in data:
        abort(400, "Missing data")
    
    bucket = "polar-files"

    file_name = "C:\\Users\\Darwin Vaz\\Downloads\\CFG.png"
    s3_client = boto3.client('s3')
    response = s3_client.upload_file(data['file'], bucket, data['name'])

    data['store'] = data['name']
    db.upload(data)

    return jsonify()


@files.route('/download', methods=['POST'])
@auth.login_required(perms=[1])
def download():
    data = request.get_json()
    if 'name' not in data:
        abort(400, "File name missing")

    s3 = boto3.resource('s3')
    bucket = "polar-files"
    s3.Bucket(bucket).download_file(data['name'], data['name'])

    return send_file(data['name'], as_attachment=True)
    


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
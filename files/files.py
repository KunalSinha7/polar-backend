from flask import Blueprint, json, jsonify, request, abort, app, g, send_file
import hashlib

import files.db as db
import auth
import auth.jwt
import auth.perms
import user.db as user
import boto3
import botocore
import werkzeug
import os

files = Blueprint('files', __name__)
BUCKET = "polar-files"

@files.route('/upload', methods=['POST'])
@auth.login_required(perms=[2])
def upload():
    file = request.files.get('file')
    form = request.form.to_dict()
    data = json.loads(form['data'])
    data['userId'] = g.userId

    if 'name' not in data or 'desc' not in data or 'file' not in data or 'roles' not in data:
        abort(400, "Missing data")

    data['store'] = data['name']
    fileId = db.upload(data)

    s3_client = boto3.client('s3')

    try:
        s3_client.upload_fileobj(file, BUCKET, data['name'])
    except ValueError:
        db.delete(fileId)
        abort(400, "File object of incorrect type. Must be readable as binary.")
    
    return jsonify()


@files.route('/download', methods=['POST'])
@auth.login_required(perms=[1])
def download():
    data = request.get_json()
    if 'name' not in data:
        abort(400, "File name missing")

    s3 = boto3.resource('s3')
    path = os.path.dirname(os.path.realpath(__file__))

    try:
        s3.Bucket(BUCKET).download_file(data['name'], os.path.join(path, data['name']))
    except botocore.exceptions.ClientError:
        abort(400, "File doesn't exist")

    return send_file(os.path.join(path, data['name']), as_attachment=True)


@files.route('/delete', methods=['POST'])
@auth.login_required(perms=[2])
def delete():
    data = request.get_json()
    if 'fileId' not in data or 'name' not in data:
        abort(400, "Missing data")
    
    db.delete(data['fileId'], data['name'])
    
    s3 = boto3.resource("s3")
    file = s3.Object(BUCKET, data['name'])
    file.delete()
    
    return jsonify()


@files.route('/view', methods=['POST'])
@auth.login_required(perms=None)
def view():
    try:
        auth.perms.checkPerms(g.userId, [1])
    except werkzeug.exceptions.Forbidden:
            return jsonify([])

    res = db.view(g.userId)
    return jsonify(res)
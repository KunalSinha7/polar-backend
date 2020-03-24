from flask import Blueprint, jsonify, request, abort, app, g, send_file
import hashlib

import files.db as db
import auth
import auth.jwt
import auth.perms
import user.db as user
import boto3
import botocore

files = Blueprint('files', __name__)
BUCKET = "polar-files"

@files.route('/upload', methods=['POST'])
@auth.login_required(perms=[2])
def upload():
    data = request.get_json()
    data['userId'] = g.userId

    if 'name' not in data or 'desc' not in data or 'file' not in data or 'roles' not in data:
        abort(400, "Missing data")

    data['store'] = data['name']
    fileId = db.upload(data)

    s3_client = boto3.client('s3')

    try:
        s3_client.upload_fileobj(data['file'], BUCKET, data['name'])
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

    try:
        s3.Bucket(BUCKET).download_file(data['name'], data['name'])
    except botocore.exceptions.ClientError:
        abort(400, "File doesn't exist")

    return send_file(data['name'], as_attachment=True)


@files.route('/delete', methods=['POST'])
@auth.login_required(perms=[2])
def delete():
    data = request.get_json()
    if 'fileId' not in data or 'name' not in data:
        abort(400, "Missing data")
    
    s3 = boto3.resource("s3")
    file = s3.Object(BUCKET, data['name'])
    file.delete()
    
    db.delete(data['fileId'])
    return jsonify()


@files.route('/view', methods=['POST'])
@auth.login_required(perms=[1])
def view():
    s3 = boto3.resource('s3')
    s3.Bucket(BUCKET).put_object(Key=data['name'], Body=data['file'])
    res = db.view(g.userId)
    return jsonify(res)
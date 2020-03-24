from flask import Blueprint, jsonify, request, abort, app, g
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
    
    # s3 = boto3.resource('s3')
    bucket = "polar-files"

    # file = ""
    # s3.Bucket(bucket).upload_file(file, "xyz")


    file_name = "C:\\Users\\Darwin Vaz\\Documents\\photo.jpg"
    object_name = file_name
    s3_client = boto3.client('s3')
    response = s3_client.upload_file(file_name, bucket, "xyz")
    print(response)


    data['store'] = data['name'] + '.txt'
    db.upload(data)

    return jsonify()


@files.route('/download', methods=['POST'])
@auth.login_required(perms=[2])
def download():
    # data = request.get_json()

    s3 = boto3.resource('s3')
    file_name = "xyz"
    bucket = "polar-files"
    # output = f"downloads/{file_name}"
    output = file_name
    s3.Bucket(bucket).download_file(file_name, output)
    print(output)

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
from flask import Blueprint, jsonify, request, abort, app, g
import hashlib

import message.db as db
import message.email as mail
import auth
import auth.jwt
import uuid

message = Blueprint('message', __name__)


@auth.login_required(perms=[7])
@message.route('/email', methods=['POST'])
def email():
    data = request.get_json()

    if 'roles' not in data or 'users' not in data:
        abort(400, 'Missing roles or users')

    if 'message' not in data or 'subject' not in data:
        abort(400, 'no message or subject')

    ids = db.get_id_from_role(data['roles'])

    unique_ids = []
    for i in ids:
        if i[0] not in unique_ids:
            unique_ids.append(i[0])

    emails = db.get_user_emails(unique_ids)

    for e in emails:
        mail.sendEmail(e[0], data['subject'], data['message'])



    return jsonify(data)

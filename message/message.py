from flask import Blueprint, jsonify, request, abort, app, g
import hashlib

import message.db as db
import message.email as mail
import message.text as text
import auth
import auth.jwt
import uuid

message = Blueprint('message', __name__)



@message.route('/email', methods=['POST'])
@auth.login_required(perms=[7])
def email():
    data = request.get_json()

    if 'roles' not in data or 'users' not in data:
        abort(400, 'Missing roles or users')

    if 'message' not in data or 'subject' not in data:
        abort(400, 'no message or subject')

    ids = []
    
    if len(data['roles']) > 0:
        ids = db.get_id_from_role(data['roles'])

    unique_ids = []
    for i in ids:
        if i[0] not in unique_ids:
            unique_ids.append(i[0])

    for u in data['users']:
        if u not in unique_ids:
            unique_ids.append(u)

    emails = []

    if len(unique_ids) > 0:
        emails = db.get_user_emails(unique_ids)

    for e in emails:
        mail.sendEmail(e[0], data['subject'], data['message'])


    return 'success'


@message.route('/text', methods=['POST'])
@auth.login_required(perms=[7])
def textMessage():
    data = request.get_json()

    if 'roles' not in data or 'users' not in data:
        abort(400, 'Missing roles or users')

    if 'message' not in data:
        abort(400, 'No message provided')

    ids = []
    if len(data['roles']) > 0:
        ids = db.get_id_from_role(data['roles'])

    unique_ids = []
    for i in ids:
        if i[0] not in unique_ids:
            unique_ids.append(i[0])

    for u in data['users']:
        if u not in unique_ids:
            unique_ids.append(u)

    phones = []
    if len(unique_ids) > 0:
        phones = db.get_user_phone(unique_ids)


    for p in phones:
        if type(p[0]) is str and len(p[0]) == 10:
            text.sendSMS(p[0], data['message'])

    return 'success'

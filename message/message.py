from flask import Blueprint, jsonify, request, abort, app, g, json
from werkzeug.utils import secure_filename
import hashlib
import os
import pathlib

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
    response = ''
    file = request.files.get('file')
    form = request.form.to_dict()
    data = json.loads(form['data'])

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

    print(emails)

    if file is not None:
        filename = secure_filename(file.filename)

        if filename.count('.') > 1:
            abort(400, 'Invalid file')

        path = os.path.dirname(os.path.realpath(__file__))
        file.save(os.path.join(path, filename))

        for e in emails:
            mail.sendEmailAttachment(e[0], data['subject'], data['message'], filename, path)
            response += 'Email function for ' + e[0] + '\n'
    
        os.remove(os.path.join(path, filename))
    else:
        for e in emails:
            mail.sendEmail(e[0], data['subject'], data['message'])
            response += 'Email function for ' + e[0] + '\n'


    return jsonify(response)


@message.route('/text', methods=['POST'])
@auth.login_required(perms=[7])
def textMessage():
    response = ''
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
            response += 'Text function for ' + p[0] + '\n'

    return jsonify(response)

@message.route('/emailTemplate', methods=['POST'])
@auth.login_required(perms=[7])
def emailTemplate():
    data = request.get_json()
    response = ''

    if 'roles' not in data or 'users' not in data:
        abort(400, 'Missing roles or users')

    if 'template' not in data or 'subject' not in data:
        abort(400, 'no template or subject')

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

    print(emails)

    if data['template'] == 'One':
        if 'bodyOne' not in data or 'bodyTwo' not in data or 'bodyThree' not in data:
            abort(400, 'Invalid request type for template one')

        for e in emails:
            mail.sendEmailTemplateOne(e[0], data['subject'], data['bodyOne'], data['bodyTwo'], data['bodyThree'])
            response += 'Email template one function for ' + e[0] + '\n'
    elif data['template'] == 'Two':
        if 'greeting' not in data or 'bodyOne' not in data or 'bodyTwo' not in data or 'closing' not in data or 'link' not in data:
            abort(400, 'Invalid request type for template two')

        for e in emails:
            mail.sendEmailTemplateTwo(e[0], data['subject'], data['greeting'], data['bodyOne'], data['link'], data['bodyTwo'], data['closing'])
            response += 'Email template two function for ' + e[0] + '\n'
    elif data['template'] == 'Three':
        if 'header' not in data or 'message' not in data or 'link' not in data or 'img' not in data or 'footer' not in data:
            abort(400, 'Ivalid request type for template three')

        for e in emails:
            mail.sendEmailTemplateThree(e[0], data['subject'], data['header'], data['message'], data['link'], data['img'], data['footer'])
            response += 'Email template three function for ' + e[0] + '\n'
    else:
        abort(400, 'Invalid template type')


    return jsonify(response)

@message.route('/getUsers', methods=['POST'])
@auth.login_required(perms=[7])
def getUsers():
    return jsonify(db.get_all_users())

@message.route('/getRoles', methods=['POST'])
@auth.login_required(perms=[7])
def getRoles():
    return jsonify(db.get_all_roles())



@message.route('/eventCheckIn', methods=['POST'])
@auth.login_required(perms=[4])
def eventCheckIn():
    data = request.get_json()

    if 'eventId' not in data or 'message' not in data or 'type' not in data:
        abort(400, 'eventId, message or type not in request')

    users = db.get_check_in_users(data['eventId'])
    mtype = data['type']


    for u in users:
        if mtype == 'email' or mtype == 'both':
            subject = 'A message from polar'

            if 'subject' in data:
                subject = data['subject']
            
            mail.sendEmail(u[0], subject, data['message'])
        
        if mtype == 'text' or mtype == 'both':
            if u[1] is not None and len(u[1]) > 0:
                text.sendSMS(u[1], data['message'])


    return 'Success'


@message.route('/eventRSVP', methods=['POST'])
@auth.login_required(perms=[4])
def eventRSVP():
    data = request.get_json()

    if 'eventId' not in data or 'message' not in data or 'type' not in data:
        abort(400, 'eventId, message or type not in request')

    users = db.get_rsvp_users(data['eventId'])
    mtype = data['type']
    print(users)

    for u in users:
        if mtype == 'email' or mtype == 'both':
            subject = 'A message from polar'

            if 'subject' in data:
                subject = data['subject']
            
            mail.sendEmail(u[0], subject, data['message'])
        
        if mtype == 'text' or mtype == 'both':
            if u[1] is not None and len(u[1]) > 0:
                text.sendSMS(u[1], data['message'])


    return 'Success'
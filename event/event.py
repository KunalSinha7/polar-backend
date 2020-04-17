from flask import Blueprint, json, jsonify, request, abort, app, g

import event.db as db
import auth

event = Blueprint('event', __name__)


@event.route('/all', methods=['POST'])
@auth.login_required(perms=None)
def all():
    res = db.all()
    resp = []

    for row in res:
        json = {}
        json['id'] = row[0]
        json['name'] = row[1]
        json['startTime'] = row[2]
        json['endTime'] = row[3]
        resp.append(json)
    
    return jsonify(resp)


@event.route('/details', methods=['POST'])
@auth.login_required(perms=None)
def details():
    data = request.get_json()
    if 'id' not in data:
        abort(400, "Missing ID")
    
    res, rsvp = db.details(data['id'], g.userId)

    resp = {
        "id": res[0],
        "name": res[1],
        "startTime": res[2],
        "endTime": res[3],
        "location": res[4],
        "desc": res[5],
        "rsvp": rsvp
    }

    return jsonify(resp)


@event.route('/create', methods=['POST'])
@auth.login_required(perms=[3])
def create():
    data = request.get_json()
    if 'name' not in data or 'startTime' not in data or 'endTime' not in data or 'location' not in data or 'desc' not in data or 'reminder' not in data or 'reminderTime' not in data:
        abort(400, "Missing data")
    if 'questions' not in data:
        data['questions'] = []

    db.create(data)

    return jsonify()


@event.route('/delete', methods=['POST'])
@auth.login_required(perms=[5])
def delete():
    data = request.get_json()
    if 'id' not in data:
        abort(400, "Missing ID")
    
    db.delete(data['id'])
    
    return jsonify()


@event.route('/modify', methods=['POST'])
@auth.login_required(perms=[3])
def modify():
    data = request.get_json()
    if 'id' not in data or 'name' not in data or 'startTime' not in data or 'endTime' not in data or 'location' not in data or 'desc' not in data or 'reminder' not in data or 'reminderTime' not in data:
        abort(400, "Missing data")
    
    db.modify(data)

    return jsonify()


@event.route('/rsvp', methods=['POST'])
@auth.login_required(perms=None)
def rsvp():
    data = request.get_json()
    if 'id' not in data:
        abort(400, "Missing ID")
    if 'answers' not in data:
        data['answers'] = []

    data['userId'] = g.userId
    db.rsvp(data)
    return jsonify()


@event.route('/unrsvp', methods=['POST'])
@auth.login_required(perms=None)
def unrsvp():
    data = request.get_json()
    if 'id' not in data:
        abort(400, "Missing ID")
    
    db.unrsvp(data['id'], g.userId)
    return jsonify()
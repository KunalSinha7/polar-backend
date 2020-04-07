from flask import Blueprint, json, jsonify, request, abort, app, g

import event.db as db
import auth

event = Blueprint('event', __name__)


@event.route('/all', methods=['POST'])
@auth.login_required(perms=None)
def all():
    return jsonify(db.all())


@event.route('/details', methods=['POST'])
@auth.login_required(perms=None)
def details():
    data = request.get_json()
    if 'id' not in data:
        abort(400, "Missing ID")
    
    res = db.details(data['id'])

    resp = {
        "id": res[0],
        "name": res[1],
        "time": res[2],
        "location": res[3],
        "desc": res[4]
    }

    return jsonify(resp)


@event.route('/create', methods=['POST'])
@auth.login_required(perms=[3])
def create():
    data = request.get_json()
    if 'name' not in data or 'time' not in data or 'location' not in data or 'desc' not in data:
        abort(400, "Missing data")

    db.create(data)

    return jsonify()
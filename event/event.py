from flask import Blueprint, json, jsonify, request, abort, app, g

import event.db as db
import auth
import auth.perms as perms

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
        "rsvp": rsvp,
        "closed": False if res[8] == 0 else True
    }

    if perms.checkPermsNoAbort(g.userId, [3]):
        resp["reminder"] = res[6]
        resp["reminderTime"] = res[7]

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


@event.route('/rsvpList', methods=['POST'])
@auth.login_required(perms=None)
def rsvpList():
    data = request.get_json()

    if perms.checkPermsNoAbort(g.userId, [3]) or perms.checkPerms(g.userId, [4]):
        if 'eventId' not in data:
            abort(400, 'Missing eventId')

        rsvp_list = db.rsvpList(int(data['eventId']))

        return jsonify(rsvp_list)
    else:
        abort(403, "Insufficient permissions")


@event.route('/close', methods=['POST'])
@auth.login_required(perms=[3])
def close():
    data = request.get_json()

    if 'id' not in data:
        abort(400, "Missing ID")

    db.close(data['id'])

    return jsonify()


@event.route('/checkInTable', methods=['POST'])
@auth.login_required(perms=[4])
def checkInTable():
    data = request.get_json()

    if 'eventId' not in data:
        abort(400, 'Missing ID')

    event_cols = db.checkInTable(data['eventId'])

    return jsonify(event_cols)


@event.route('/checkIn', methods=['POST'])
@auth.login_required(perms=[4])
def checkIn():
    data = request.get_json()

    if 'userId' not in data or 'eventId' not in data:
        abort(400, 'Missing userId or eventId')

    db.checkIn(data['userId'], data['eventId'])

    return 'Success'


@event.route('/modifyRow', methods=['POST'])
@auth.login_required(perms=[4])
def modifyRow():
    data = request.get_json()

    if 'eventId' not in data or 'contents' not in data:
        abort(400, 'Missing eventId or contents')

    db.modifyRow(data['eventId'], data['contents'])

    return 'Success'


@event.route('/insertCol', methods=['POST'])
@auth.login_required(perms=[4])
def insertCol():
    data = request.get_json()

    if 'eventId' not in data or 'data' not in data:
        abort(400, 'eventId or data not in request')

    for d in data['data']:
        if 'Question' not in d or 'IsRsvp' not in d:
            abort(400, 'Incorrect request, missing Question or IsRsvp')

        if d['IsRsvp']:
            db.insertRsvpCol(data['eventId'], d['Question'])
        else:
            db.insertCheckInCol(data['eventId'], d['Question'])
    
    return 'Success'

@event.route('/modifyCol', methods=['POST'])
@auth.login_required(perms=[4])
def modifyCol():
    data = request.get_json()

    if 'eventId' not in data or 'data' not in data:
        abort(400, 'eventId or data not in request')

    eventId = data['eventId']
    checkInCols = db.getCheckInCols(eventId)
    eventCols = db.getEventCols(eventId)


    for r in data['data']:
        if r['before'] in eventCols:
            if r['IsRsvp'] is True:
                db.modifyEventCol(eventId, r['before'], r['Question'])
            else:
                db.moveColEventToCheckIn(eventId, r['before'], r['Question'])
        elif r['before'] in checkInCols:
            if r['IsRsvp'] is False:
                db.modifyCheckInCol(eventId, r['before'], r['Question'])
            else:
                db.moveColCheckInToEvent(eventId, r['before'], r['Question'])
        else:
            print(eventCols)
            print(checkInCols)
            abort(400, 'Column ' + r['before'] + ' not found')

    return 'Success'



@event.route('/deleteCol', methods=['POST'])
@auth.login_required(perms=[4])
def deleteCol():
    data = request.get_json()

    if 'eventId' not in data or 'data' not in data:
        abort(400, 'eventId or data not in request')

    eventId = data['eventId']
    checkInCols = db.getCheckInCols(eventId)
    eventCols = db.getEventCols(eventId)


    for r in data['data']:
        if r in eventCols:
            print(r + ' is an event col') 
            db.deleteRsvpCol(eventId, r)
        elif r in checkInCols:
            db.deleteCheckInCol(eventId, r)
            print(r + ' is a check in col')
        else:
            abort(400, 'Column ' + r + ' not found')

    return 'Success'



@event.route('/colTypes', methods=['POST'])
@auth.login_required(perms=[4])
def colType():
    data = request.get_json()

    if 'eventId' not in data:
        abort(400, 'eventId not in data')

    ecol = db.getEventCols(data['eventId'])
    col = db.getCheckInCols(data['eventId'])
    out = {}

    for c in ecol:
        out[c] = True
        print('event col ' + c)

    for c in col:
        out[c] = False
        print('r col '+ c)


    return jsonify(out)
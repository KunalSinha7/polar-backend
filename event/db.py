from flask import abort
import db
import MySQLdb

def all():
    conn = db.conn()
    cursor = conn.cursor()

    list_all_cmd = 'SELECT eventId, eventName, startTime, endTime FROM Event;'

    cursor.execute(list_all_cmd)

    return cursor.fetchall()


def details(id, userId):
    conn = db.conn()
    cursor = conn.cursor()

    select_cmd = 'SELECT * FROM Event WHERE eventId = %s;'
    rsvp_cmd = 'SELECT * FROM event_%s WHERE userId = %s;'

    cursor.execute(select_cmd, [id])
    res = cursor.fetchone()

    if res is None:
        abort(400, "Event does not exist")
    
    cursor.execute(rsvp_cmd, [id, userId])

    rsvp = {}
    rsvp['questions'] = []
    ret = cursor.fetchone()

    if ret == None:
        rsvp['response'] = False
        for i in range(1, len(cursor.description)):
            rsvp['questions'].append(cursor.description[i][0].replace('\'', ''))
    else:
        rsvp['response'] = True
        rsvp['answers'] = []
        for i in range(1, len(cursor.description)):
            rsvp['questions'].append(cursor.description[i][0].replace('\'', ''))
            rsvp['answers'].append(ret[i])
    
    return res, rsvp


def create(data):
    conn = db.conn()
    cursor = conn.cursor()

    create_cmd = '''INSERT INTO Event
        (eventName, startTime, endTime, location, description, reminder, reminderTime) VALUES
        (%s, %s, %s, %s, %s, %s, %s);'''
    
    table_cmd = '''CREATE TABLE event_%s (
        userId int(11) NOT NULL UNIQUE PRIMARY KEY'''

    args = [data['name'], data['startTime'], data['endTime'], data['location'], data['desc'], int(data['reminder']), int(data['reminderTime'])]
    cursor.execute(create_cmd, args)

    args = [cursor.lastrowid]
    for col in data['questions']:
        table_cmd += ', `%s` varchar(256)'
        args.append(col)
    
    table_cmd += ');'

    cursor.execute(table_cmd, args)

    conn.commit()
    return True


def delete(id):
    conn = db.conn()
    cursor = conn.cursor()

    delete_cmd = 'DELETE FROM Event WHERE eventId = %s;'
    drop_cmd = 'DROP TABLE if exists event_%s'

    cursor.execute(delete_cmd, [id])
    cursor.execute(drop_cmd, [id])

    conn.commit()
    return True


def modify(data):
    conn = db.conn()
    cursor = conn.cursor()

    modify_cmd = '''UPDATE Event SET
        eventName = %s, startTime = %s, endTime = %s, location = %s, description = %s, reminder = %s, reminderTime = %s
        WHERE eventId = %s;'''
    
    args = [data['name'], data['startTime'], data['endTime'], data['location'], data['desc'], int(data['reminder']), int(data['reminderTime']), data['id']]
    cursor.execute(modify_cmd, args)

    conn.commit()
    return True


def rsvp(data):
    conn = db.conn()
    cursor = conn.cursor()

    rsvp_cmd = '''INSERT INTO event_%s
        VALUES ('''

    args = [int(data['id']), data['userId']]
    rsvp_cmd += "%s"

    for resp in data['answers']:
        args.append(resp)
        rsvp_cmd += ", %s"
    
    rsvp_cmd += ");"

    try:
        cursor.execute(rsvp_cmd, args)
    except MySQLdb.ProgrammingError:
        abort(400, "Event does not exist")
    except MySQLdb.OperationalError:
        abort(400, "Answers don't match Questions")
    except MySQLdb.IntegrityError:
        abort(400, "User has already RSVP-ed to this event")

    conn.commit()
    return True


def unrsvp(id, userId):
    conn = db.conn()
    cursor = conn.cursor()

    unrsvp_cmd = 'DELETE FROM event_%s WHERE userId = %s;'

    cursor.execute(unrsvp_cmd, [int(id), userId])
    
    conn.commit()
    return True
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
    
    cursor.execute(rsvp_cmd, [int(id), userId])

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

    check_in_table_cmd = '''CREATE TABLE check_in_event_{} (userId int(11) NOT NULL UNIQUE PRIMARY KEY);'''

    args = [data['name'], data['startTime'], data['endTime'], data['location'], data['desc'], int(data['reminder']), int(data['reminderTime'])]
    cursor.execute(create_cmd, args)

    table_id = cursor.lastrowid
    args = [cursor.lastrowid]
    for col in data['questions']:
        table_cmd += ', `%s` varchar(256)'
        args.append(col)
    
    table_cmd += ');'

    cursor.execute(table_cmd, args)
    cursor.execute(check_in_table_cmd.format(table_id))

    conn.commit()
    return True


def delete(id):
    conn = db.conn()
    cursor = conn.cursor()

    delete_cmd = 'DELETE FROM Event WHERE eventId = %s;'
    drop_cmd = 'DROP TABLE if exists event_%s'

    cursor.execute(delete_cmd, [id])
    cursor.execute(drop_cmd, [int(id)])

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
    check_in_rsvp_cmd = '''INSERT INTO check_in_event_%s (userId) values (%s);'''
    check_in_cmd = '''INSERT INTO CheckIn (userId, eventId) values (%s, %s);'''

    args = [int(data['id']), data['userId']]
    rsvp_cmd += "%s"

    for resp in data['answers']:
        args.append(resp)
        rsvp_cmd += ", %s"
    
    rsvp_cmd += ");"

    try:
        cursor.execute(rsvp_cmd, args)
        cursor.execute(check_in_rsvp_cmd, [int(data['id']), int(data['userId'])])
        cursor.execute(check_in_cmd, [int(data['userId']), int(data['id'])])
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
    check_in_unrsvp_cmd = '''DELETE FROM check_in_event_%s WHERE userId = %s;'''
    un_check_in_cmd = '''DELETE FROM CheckIn WHERE userId = %s AND eventId = %s;'''

    cursor.execute(unrsvp_cmd, [int(id), userId])
    cursor.execute(check_in_unrsvp_cmd, [int(id), userId])
    cursor.execute(un_check_in_cmd, [int(userId), int(id)])

    conn.commit()
    return True


def rsvpList(eventId):
    get_rsvp_list_cmd = '''select e.userId, u.FirstName, u.LastName from event_%s as e join Users as u on e.userId = u.userId;'''
    conn = db.conn()
    cursor = conn.cursor()

    try:
        cursor.execute(get_rsvp_list_cmd, [eventId])
    except MySQLdb.ProgrammingError:
        abort(400, "Event does not exist")

    return cursor.fetchall()


def close(id):
    conn = db.conn()
    cursor = conn.cursor()
    
    close_cmd = 'UPDATE Event SET closed = 1 WHERE eventID = %s;'

    cursor.execute(close_cmd, [id])

    conn.commit()    
    return True


def checkInTable(id):
    conn = db.conn()
    cursor = conn.cursor()

    check_in_table_cmd = '''select * from event_%s e inner join check_in_event_%s c using(userId) inner join (select userId, checkedIn from CheckIn) as ci using(userId);'''

    event_cols = []

    try:
        cursor.execute(check_in_table_cmd, [int(id), int(id)])
        cols = [i[0] for i in cursor.description]
        res = list(cursor.fetchall())
        res.insert(0, cols)

        return res

    except MySQLdb.ProgrammingError as e:
        print(e)
        abort(400, "Event does not exist")

def checkIn(userId, eventId):
    conn = db.conn()
    cursor = conn.cursor()

    update_check_in_cmd = '''update CheckIn set checkedIn=1 where userId = %s and eventId = %s;'''

    try:
        cursor.execute(update_check_in_cmd, [int(userId), int(eventId)])
        conn.commit()
    except MySQLdb.ProgrammingError as e:
        print(e)
        abort(400, 'Event or user does not exist')



def removeCol(id, name):
    conn = db.conn()
    cursor = conn.cursor()

    get_event_cols_cmd = '''SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = '%s';'''

    try:
        cursor.execute(get_event_cols_cmd, [id])
        cols = cursor.fetchall()


        return cols
    except MySQLdb.ProgrammingError as e:
        print(e)
        abort(400, 'Event does not exist')
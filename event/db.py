from flask import abort
import db
import MySQLdb

def all():
    conn = db.conn()
    cursor = conn.cursor()

    list_all_cmd = 'SELECT * FROM Event;'

    cursor.execute(list_all_cmd)

    return cursor.fetchall()


def details(id):
    conn = db.conn()
    cursor = conn.cursor()

    select_cmd = 'SELECT * FROM Event WHERE eventId = %s';

    cursor.execute(select_cmd, [id])
    res = cursor.fetchone()
    
    return res



def create(data):
    conn = db.conn()
    cursor = conn.cursor()

    create_cmd = '''INSERT INTO Event
        (eventName, time, location, description) VALUES
        (%s, %s, %s, %s);'''

    args = [data['name'], data['time'], data['location'], data['desc']]
    cursor.execute(create_cmd, args)

    conn.commit()
    return True
    
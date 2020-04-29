from flask import abort
import db
import MySQLdb

create_user_cmd_phone = '''INSERT INTO Users (firstName, lastName, email, phone, password) 
VALUES (%s, %s, %s, %s, %s);
'''

get_user_emails_cmd = '''select distinct email from Users where userId in (%s);'''
def get_user_emails(user_list):
    conn = db.conn()
    cursor = conn.cursor()

    users = ','.join(['%s'] * len(user_list))
    cursor.execute(get_user_emails_cmd % users, tuple(user_list))

    return cursor.fetchall()

get_id_from_role_cmd = '''select distinct userId from UserRoles where roleId in (%s);'''
def get_id_from_role(role_list):
    conn = db.conn()
    cursor = conn.cursor()

    users = ','.join(['%s'] * len(role_list))
    cursor.execute(get_id_from_role_cmd % users, tuple(role_list))

    return cursor.fetchall() 

get_user_phone_cmd = '''select distinct phone from Users where userId in (%s) and userID IS NOT NULL;'''
def get_user_phone(user_list):
    conn = db.conn()
    cursor = conn.cursor()

    users = ','.join(['%s'] * len(user_list))
    cursor.execute(get_user_phone_cmd % users, tuple(user_list))

    return cursor.fetchall()


get_all_users_cmd = '''select userId, concat(firstName, ' ', lastName) from Users;'''
def get_all_users():
    conn = db.conn()
    cursor = conn.cursor()

    cursor.execute(get_all_users_cmd)
    return cursor.fetchall()

get_all_roles_cmd = '''select roleId, roleName from Roles;'''
def get_all_roles():
    conn = db.conn()
    cursor = conn.cursor()

    cursor.execute(get_all_roles_cmd)
    return cursor.fetchall()



def get_check_in_users(eventId):
    get_check_in_cmd = '''select u.email, u.phone from CheckIn as e join Users as u on e.userId = u.userId where e.eventId = %s and e.checkIn = 1;'''
    conn = db.conn()
    cursor = conn.cursor()

    try:
        cursor.execute(get_check_in_cmd, [eventId])
        return cursor.fetchall()
    except MySQLdb.ProgrammingError as e:
        print(e)
        abort(400, 'Event does not exists')

def get_rsvp_users(eventId):
    get_rsvp_cmd = '''select u.email, u.phone from event_{} as e join Users as u on e.userId = u.userId;'''.format(eventId)
    conn = db.conn()
    cursor = conn.cursor()

    try:
        cursor.execute(get_rsvp_cmd)
        return cursor.fetchall()
    except MySQLdb.ProgrammingError as e:
        print(e)
        abort(400, 'Event does not exists')
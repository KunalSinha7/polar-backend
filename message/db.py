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
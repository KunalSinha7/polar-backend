from flask import abort
import db
import MySQLdb

create_user_cmd_phone = '''INSERT INTO Users (firstName, lastName, email, phone, password) 
VALUES (%s, %s, %s, %s, %s);
'''

create_user_cmd_no_phone = '''INSERT INTO Users (firstName, lastName, email, password) 
VALUES (%s, %s, %s, %s);
'''

unique_email_cmd = '''SELECT COUNT(*) FROM Users where email = %s;'''


def create_user(data):
    conn = db.conn()
    cursor = conn.cursor()

    cursor.execute(unique_email_cmd, [data['email']])

    if cursor.fetchone()[0] > 0:
        abort(400, description='Email is already assigned')

    if len(data) == 4:
        cursor.execute(create_user_cmd_no_phone, [
            data['firstName'], data['lastName'], data['email'], data['password']])
    else:
        cursor.execute(create_user_cmd_phone, [
            data['firstName'], data['lastName'], data['email'], data['phone'], data['password']])

    user_id = cursor.lastrowid
    conn.commit()
    return user_id


def login(data):
    conn = db.conn()
    cursor = conn.cursor()

    login_cmd = 'SELECT * FROM Users WHERE email = %s AND password = %s;'

    cursor.execute(login_cmd, [data['email'], data['password']])

    res = cursor.fetchone()

    if res is None:
        abort(400, "Incorrect credentials provided")

    cursor.close()
    conn.close()
    return res


def getInfo(userId):
    conn = db.conn()
    cursor = conn.cursor()

    get_info_cmd = 'SELECT * FROM Users WHERE userId = %s;'

    cursor.execute(get_info_cmd, [userId])

    res = cursor.fetchone()

    if res is None:
        abort(400, "User doesn't exist")

    cursor.close()
    conn.close()
    return res


def setInfo(data):
    conn = db.conn()
    cursor = conn.cursor()

    edit_cmd = 'UPDATE Users SET firstName = %s, lastName = %s, phone = %s WHERE userId = %s;'

    cursor.execute(edit_cmd, [data['firstName'],
        data['lastName'], data['phone'], data['userId']])

    res = cursor.fetchone()

    if res is not None:
        abort(400, res)

    conn.commit()
    cursor.close()
    conn.close()
    return True


def delete(data):
    conn = db.conn()
    cursor = conn.cursor()

    delete_user_cmd = 'DELETE FROM Users WHERE userId = %d;'
    delete_roles_cmd = 'DELETE FROM UserRoles WHERE userId = %d;'

    cursor.execute(delete_user_cmd, [data['userId']])
    cursor.execute(delete_roles_cmd, [data['userId']])

    cursor.close()
    conn.close()


get_user_id_cmd = '''select userId from Users where email = %s;'''
def getUserId(email):
    conn = db.conn()
    cursor = conn.cursor()
    cursor.execute(get_user_id_cmd,[email])

    if cursor.rowcount != 1:
        abort(400, 'Invalid email')
    else:
        return cursor.fetchone()[0]


add_link_cmd = '''insert into Links (used, link, userId) values (0, %s, %s);'''
def addLink(userId, link):
    conn = db.conn()
    cursor = conn.cursor()

    try:
        cursor.execute(add_link_cmd, [link, userId])
        conn.commit()
    except MySQLdb.IntegrityError:
        abort(501)
    finally:
        cursor.close()
        conn.close()


check_token_cmd = '''update Links set used = 1 where link = %s and userId =%s and used = 0;'''
def checkPasswordToken(email, link):
    user_id = getUserId(email)

    conn = db.conn()
    cursor = conn.cursor()

    try:
        cursor.execute(check_token_cmd, [link, user_id])

        if cursor.rowcount != 1:
            abort(400, 'No found user or link')
        else:
            conn.commit()
    except MySQLdb.IntegrityError:
        abort(501)

    return user_id


update_password_cmd = '''update Users set password = %s where userId = %s and email = %s;'''
def updatePassword(user_id, password, email):
    conn = db.conn()
    cursor = conn.cursor()

    try:
        cursor.execute(update_password_cmd, [password, user_id, email])

        if cursor.rowcount != 1:
            abort(501, 'Something went wrong in updatePassword')
        else:
            conn.commit()
    except MySQLdb.IntegrityError:
        abort(501, 'SQL error in updatePassword')

    return True


def test():
    conn = db.conn()
    cursor = conn.cursor()
    return
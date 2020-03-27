from flask import abort
import db
import MySQLdb

def upload(data):
    conn = db.conn()
    cursor = conn.cursor()

    file_select_cmd = 'SELECT * FROM Files WHERE displayName = %s;'

    cursor.execute(file_select_cmd, [data['name']])
    if cursor.rowcount > 0:
        abort(400, "A file with this name already exists.")

    file_upload_cmd = '''INSERT INTO Files 
    (storageName, displayName, description, userId) 
    VALUES (%s, %s, %s, %s);'''

    role_upload_cmd = 'INSERT INTO FileRoles VALUES'

    cursor.execute(file_upload_cmd, 
        [data['store'], data['name'], data['desc'], data['userId']])
    
    fileId = cursor.lastrowid

    if len(data['roles']) == 0:
        conn.commit()
        return fileId
    
    row = []
    for role in data['roles']:
        role_upload_cmd += ' (%s, %s),'
        row.append(fileId)
        row.append(role)
    
    role_upload_cmd = role_upload_cmd[:len(role_upload_cmd) - 1]

    cursor.execute(role_upload_cmd, tuple(row))
        
    conn.commit()
    return fileId


def delete(fileId):
    conn = db.conn()
    cursor = conn.cursor()
    
    delete_cmd = 'DELETE FROM Files WHERE fileId = %s;'

    cursor.execute(delete_cmd, [fileId])

    conn.commit()
    return True


def getRoles(userId):
    conn = db.conn()
    cursor = conn.cursor()

    roles_cmd = 'SELECT roleId FROM UserRoles WHERE userId = %s;'

    cursor.execute(roles_cmd, [userId])

    return cursor.fetchall()


def view(userId):
    conn = db.conn()
    cursor = conn.cursor()

    view_cmd = '''SELECT f.*, firstName, lastName FROM (
        SELECT DISTINCT(f.fileId), storageName, displayName, description, f.userId
        FROM Users u, UserRoles r, FileRoles fr, Files f
        WHERE u.userId = %s AND u.userId = r.userId AND r.roleId = fr.roleId AND fr.fileId = f.fileId
        UNION
        SELECT DISTINCT(f.fileId), storageName, displayName, description, f.userId
        FROM Files f LEFT JOIN FileRoles r ON f.fileId = r.fileId
        WHERE r.fileId IS NULL)
        AS f, Users u
        WHERE f.userId = u.userId;'''

    cursor.execute(view_cmd, [userId])

    res = cursor.fetchall()

    return res




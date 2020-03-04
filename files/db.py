from flask import abort
import db
import MySQLdb

def upload(data):
    conn = db.conn()
    cursor = conn.cursor()

    file_upload_cmd = '''INSERT INTO Files 
    (storageName, displayName, description, userId) 
    VALUES (%s, %s, %s, %s);'''

    role_upload_cmd = 'INSERT INTO FileRoles VALUES'

    cursor.execute(file_upload_cmd, 
        [data['store'], data['name'], data['desc'], data['userId']])
    
    fileId = cursor.lastrowid
    
    row = []
    for role in data['roles']:
        role_upload_cmd += ' (%s, %s),'
        row.append(fileId)
        row.append(role)
    
    role_upload_cmd = role_upload_cmd[:len(role_upload_cmd) - 1]

    cursor.execute(role_upload_cmd, tuple(row))
    print(cursor.fetchall())
    # not checking for invalid, duplicate roles
        
    conn.commit()
    return True


def delete(fileId):
    conn = db.conn()
    cursor = conn.cursor()
    
    delete_cmd = 'DELETE FROM Files WHERE fileId = %s;'

    cursor.execute(delete_cmd, [fileId])

    conn.commit()
    return True
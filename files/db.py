from flask import abort
import db
import MySQLdb

def upload(data):
    conn = db.conn()
    cursor = conn.cursor()

    file_upload_cmd = '''INSERT INTO Files 
    (storageName, displayName, description, userId) 
    VALUES (%s, %s, %s, %s);'''

    role_upload_cmd

    cursor.execute(file_upload_cmd, 
        [data['store'], data['name'], data['desc'], data['userId']])
    


    return True
from flask import abort
import db

def createRole(data):
    conn = db.conn()
    cursor = conn.cursor()

    


    conn.commit()
    cursor.close()
    conn.close()

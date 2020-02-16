from flask import current_app as app
from flask import abort
import db

def checkPerms(userId, perm):
    conn = db.conn()
    cursor = conn.cursor()




    cursor.close()
    conn.close()
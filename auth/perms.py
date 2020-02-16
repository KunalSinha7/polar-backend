from flask import current_app as app
from flask import abort
import db

def checkPerms(userId, perm):
    conn = db.conn()
    cursor = conn.cursor()

    check_perms_cmd = '''SELECT * FROM PermissionRoles p, UserRoles u
    WHERE p.roleId = u.roleId AND userId = %s AND permissionID = %s;
    '''

    cursor.execute(check_perms_cmd, [userId, perm])

    res = cursor.fetchone()

    if res is None:
        abort(401, "Insufficient privileges")

    cursor.close()
    conn.close()
    return True
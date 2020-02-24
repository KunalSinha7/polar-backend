from flask import current_app as app
from flask import abort, request

import db
import auth

def checkPerms(userId, perms):
    conn = db.conn()
    cursor = conn.cursor()

    check_perms_cmd = '''SELECT permissionId FROM PermissionRoles p, UserRoles u
    WHERE p.roleId = u.roleId AND userId = %s;
    '''

    cursor.execute(check_perms_cmd, [userId])

    res = cursor.fetchall()
    a = [item for t in res for item in t]
    b = all(elem in a for elem in perms)

    if not b:
        abort(403, "Insufficient privileges")

    return True
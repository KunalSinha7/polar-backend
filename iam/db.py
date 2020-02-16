from flask import abort
import db

def createRole(data):
    conn = db.conn()
    cursor = conn.cursor()

    unique_role_cmd = 'SELECT * FROM Roles WHERE roleName = %s;'
    create_cmd = 'INSERT INTO Roles (roleName) VALUES (%s);'
    add_perm_cmd = 'INSERT INTO PermissionRoles VALUES (%s, %s);'

    cursor.execute(unique_role_cmd, [data['roleName']])
    res = cursor.fetchone()
    if res is not None:
        abort(400, "Role already exists")
    
    cursor.execute(create_cmd, [data['roleName']])
    roleId = cursor.lastrowid

    for perm in data["permissions"]:
        cursor.execute(add_perm_cmd, [roleId, perm])

    conn.commit()
    cursor.close()
    conn.close()
    return True


def removeRole(data):
    conn = db.conn()
    cursor = conn.cursor()

    # do deletes cascade?

    conn.commit()
    cursor.close()
    conn.close()
    return True
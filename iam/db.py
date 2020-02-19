from flask import abort
import db


def createRole(data):
    conn = db.conn()
    cursor = conn.cursor()

    unique_role_cmd = 'SELECT * FROM Roles WHERE roleName = %s;'
    create_cmd = 'INSERT INTO Roles (roleName) VALUES (%s);'
    add_perm_cmd = 'INSERT INTO PermissionRoles VALUES'

    cursor.execute(unique_role_cmd, [data['roleName']])
    res = cursor.fetchone()
    if res is not None:
        abort(400, "Role already exists")
    
    cursor.execute(create_cmd, [data['roleName']])
    roleId = cursor.lastrowid

    row = []
    for perm in data["permissions"]:
        add_perm_cmd += ' (%s, %s),'
        row.append(roleId)
        row.append(perm)
        
    add_perm_cmd = add_perm_cmd[:len(add_perm_cmd) - 1]
    add_perm_cmd += ';'

    cursor.execute(add_perm_cmd, tuple(row))

    conn.commit()
    cursor.close()
    conn.close()
    return True


def removeRole(roleId):
    conn = db.conn()
    cursor = conn.cursor()

    delete_cmd = 'DELETE FROM Roles WHERE roleId = %s;'

    cursor.execute(delete_cmd, [roleId])

    conn.commit()
    cursor.close()
    conn.close()
    return True
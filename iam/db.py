from flask import abort
import MySQLdb
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
        if perm > 0 and perm < 12:
            add_perm_cmd += ' (%s, %s),'
            row.append(roleId)
            row.append(perm)

    if len(row) == 0:
        abort(400, "Specified permissions don't exists")

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


def assignRole(data):
    conn = db.conn()
    cursor = conn.cursor()

    insert_cmd = 'INSERT INTO UserRoles VALUES (%s, %s);'

    try:
        cursor.execute(insert_cmd, [data['roleId'], data['userId']])
    except MySQLdb.IntegrityError:
        abort(400, "User already has role or does not exist")

    conn.commit()
    return True


def revokeRole(data):
    conn = db.conn()
    cursor = conn.cursor()

    revoke_cmd = 'DELETE FROM UserRoles WHERE roleId = %s AND userId = %s;'

    cursor.execute(revoke_cmd, [data['roleId'], data['userId']])
    
    conn.commit()
    cursor.close()
    conn.close()
    return True


def permissions():
    conn = db.conn()
    cursor = conn.cursor()
    get_cmd = 'SELECT * FROM Permissions;'
    cursor.execute(get_cmd)
    res = cursor.fetchall()
    return res


get_all_roles_cmd = '''select Roles.roleId, Roles.roleName, PermissionRoles.permissionId from Roles join PermissionRoles on Roles.roleId = PermissionRoles.roleId;'''
def getAllRoles():
    conn = db.conn()
    cursor = conn.cursor()
    cursor.execute(get_all_roles_cmd)
    return cursor.fetchall()

get_roles_nums_cmd = '''select distinct roleId from Roles;'''
def getRoleNums():
    conn = db.conn()
    cursor =  conn.cursor()
    cursor.execute(get_roles_nums_cmd)
    return cursor.fetchall()


get_all_user_roles_cmd = '''select Users.userId, Users.firstName, Users.lastName, Users.phone, Users.email, UserRoles.roleId from Users left join UserRoles on Users.userId = UserRoles.userId;'''
def getAllUserRoles():
    conn = db.conn()
    cursor = conn.cursor()
    cursor.execute(get_all_user_roles_cmd)
    return cursor.fetchall()

insert_user_email_cmd = '''insert into Users (email) values (%s);'''
def insertUserEmail(email):
    conn = db.conn()
    cursor = conn.cursor()

    try:
        cursor.execute(insert_user_email_cmd, [email])
        conn.commit()
        return cursor.lastrowid
    except MySQLdb.IntegrityError:
        abort(400, "User already already exists")


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
        

import db

create_user_cmd_phone = '''INSERT INTO Users (firstName, lastName, email, phone, password) 
VALUES (%s, %s, %s, %s, %s);
'''

create_user_cmd_no_phone = '''INSERT INTO Users (firstName, lastName, email, password) 
VALUES (%s, %s, %s, %s);
'''

def create_user(data):
    conn = db.conn()
    cursor = conn.cursor()

    if len(data) is 4:
        cursor.execute(create_user_cmd_no_phone, [data['firstName'], data['lastName'], data['email'], data['password']])
    else:
        cursor.execute(create_user_cmd_phone, [data['firstName'], data['lastName'], data['email'], data['phone'], data['password']])
    

    user_id = cursor.lastrowid
    conn.commit()
    return user_id


def test():
    conn = db.conn()
    cursor = conn.cursor()
    return
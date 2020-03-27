from flask import abort
import MySQLdb
import db


def make_table_name(id):
    return 'table_' + str(id)


get_all_tables_cmd = '''select tableID, tableName from Tables;'''
def getAllTables():
    conn = db.conn()
    cursor = conn.cursor()

    cursor.execute(get_all_tables_cmd)
    return cursor.fetchall()


create_table_cmd = '''CREATE TABLE {} (`id` int(11) unsigned NOT NULL AUTO_INCREMENT,PRIMARY KEY (`id`)) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;'''
insert_table_cmd = '''insert into Tables (tableName) VALUES (%s);'''
check_table_exists_cmd = '''select * from Tables where tableName = %s;'''
def createTable(tableName):
    conn = db.conn()
    cursor = conn.cursor()
    tableName = tableName.strip()

    cursor.execute(check_table_exists_cmd, [tableName])
    if cursor.rowcount > 0:
        abort(400, 'This table already exists')

    try:
        cursor.execute(insert_table_cmd, [tableName])
        tableId = cursor.lastrowid
        cursor.execute(create_table_cmd.format(make_table_name(str(tableId))))
        conn.commit()

        return tableId
    except Exception as e:
        print(e)
        abort(500, 'SQL error at insert table comand')


add_column_cmd = '''ALTER TABLE {} ADD COLUMN {} text;'''
def addColumn_id(tableId, name):
    add = add_column_cmd.format(make_table_name(tableId), name)
    print(add)

    conn = db.conn()
    cursor = conn.cursor()

    try:
        cursor.execute(add)
    except Exception as e:
        print(e)
        abort(500, 'Exception in addCol')


delete_table_cmd = '''DROP TABLE {};'''
delete_entry_cmd = '''delete from Tables where tableId = %s;'''
select_table_cmd = '''select * from {};'''
def delete_table(tableId):
    drop = delete_table_cmd.format(make_table_name(tableId))
    conn = db.conn()
    cursor = conn.cursor()

    try:
        cursor.execute(select_table_cmd.format(make_table_name(tableId)))
    except Exception as e:
        print(e)
        abort(400, 'Table does not exist') 


    try:
        cursor.execute(delete_entry_cmd, [tableId])
        cursor.execute(drop)
        conn.commit()
    except Exception as e:
        print(e)
        abort(500, 'SQL error at drop')




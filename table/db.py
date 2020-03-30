from flask import abort
import MySQLdb
import db


def make_table_name(id):
    return 'table_' + str(id)

check_table_id_cmd = '''select * from Tables where tableId = %s;'''
def checkTableExists(tableId):
    conn = db.conn()
    cursor = conn.cursor()

    try:
        cursor.execute(check_table_id_cmd, [tableId])

        if cursor.rowcount > 0:
            return True
        else:
            return False
    except Exception as e:
        print(e)
        abort(500, 'Error in check tableExists')

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


add_column_cmd = '''ALTER TABLE {} ADD COLUMN `{}` text;'''
def addColumn_id(tableId, name):
    add = add_column_cmd.format(make_table_name(tableId), name)
    print(add)

    conn = db.conn()
    cursor = conn.cursor()

    try:
        cursor.execute(add)
    except MySQLdb.OperationalError as ex:
        abort(400, 'This column already exists')
    except Exception as e:
        print(e)
        print(type(e))
        abort(500, 'Exception in addCol')

remove_column_cmd = '''ALTER TABLE {} DROP COLUMN `{}`;'''
def removeColumn(tableId, name):
    if name == 'id':
        abort(400, 'Cannot remove this column')

    remove = remove_column_cmd.format(make_table_name(tableId), name)

    conn = db.conn()
    cursor = conn.cursor()

    try:
        cursor.execute(remove)
    except MySQLdb.OperationalError as err:
        print(err)
        abort(400, 'This column does not exist')
    except Exception as e:
        print(e)
        abort(500, 'Error in remove column')


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


modify_column_cmd = '''ALTER TABLE {} CHANGE `{}` `{}` text;'''
def modifyColumn(tableId, oldCol, newCol):
    if oldCol == 'id':
        abort(400, 'Cannot remove this column')

    cols = getColumns(tableId)

    if oldCol not in cols:
        abort(400, 'Column not found')

    cmd = modify_column_cmd.format(make_table_name(tableId), oldCol, newCol)
    conn = db.conn()
    cursor = conn.cursor()
    cursor.execute(cmd)


get_table_columns_cmd = '''select COLUMN_NAME from INFORMATION_SCHEMA.COLUMNS where TABLE_NAME = %s;'''
def getColumns(tableId):
    conn = db.conn()
    cursor = conn.cursor()

    cursor.execute(get_table_columns_cmd, [make_table_name(tableId)])

    return [i[0] for i in cursor.fetchall()]


def viewTable(id):
    conn = db.conn()
    cursor = conn.cursor()

    table_cmd = 'SELECT * FROM table_%s;'

    try:
        cursor.execute(table_cmd, [id])
    except MySQLdb.ProgrammingError:
        abort(400, "Table doesn't exist")

    field_names = [i[0] for i in cursor.description]
    res = list(cursor.fetchall())
    res.insert(0, field_names)

    return res



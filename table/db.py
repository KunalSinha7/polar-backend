from flask import abort
import MySQLdb
import db
from datetime import datetime


def make_table_name(id):
    return 'table_' + str(id)

time = lambda: datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")

tracking_enabled = ((1,),)
tracking_disabled = ((0,),)

check_table_id_cmd = '''select * from Tables where tableId = %s;'''

check_tracking_cmd = 'SELECT trackHistory FROM Tables WHERE tableId = %s;'

insert_history_cmd = '''
INSERT INTO TableHistory 
(tableId, rowId, beforeVal, afterVal, userChangeId, time, type) 
VALUES (%s, %s, %s, %s, %s, %s, %s);
'''

get_row_cmd = 'SELECT * FROM table_%s WHERE id = %s;'


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


get_all_tables_cmd = '''select * from Tables;'''


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


def addColumn_id(tableId, name, userId):
    add = add_column_cmd.format(make_table_name(tableId), name)

    conn = db.conn()
    cursor = conn.cursor()

    try:
        cursor.execute(add)
        
        cursor.execute(check_tracking_cmd, [tableId])
        if cursor.fetchall() == tracking_disabled:
            return
        
        args = [tableId, 0, "", "Column '" + name + "'", userId, time(), 4]

        cursor.execute(insert_history_cmd, args)
        conn.commit()
    except MySQLdb.OperationalError as ex:
        abort(400, 'This column already exists')
    except Exception as e:
        print(e)
        print(type(e))
        abort(500, 'Exception in addCol')


remove_column_cmd = '''ALTER TABLE {} DROP COLUMN `{}`;'''


def removeColumn(tableId, name, userId):
    if name == 'id':
        abort(400, 'Cannot remove this column')

    remove = remove_column_cmd.format(make_table_name(tableId), name)

    conn = db.conn()
    cursor = conn.cursor()

    try:
        cursor.execute(remove)

        cursor.execute(check_tracking_cmd, [tableId])
        if cursor.fetchall() == tracking_disabled:
            return
        
        args = [tableId, 0, "Column '" + name + "'", "", userId, time(), 5]

        cursor.execute(insert_history_cmd, args)
        conn.commit()
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
    delete_cmd = 'DELETE FROM TableHistory WHERE tableId =  %s;'
    conn = db.conn()
    cursor = conn.cursor()

    try:
        cursor.execute(select_table_cmd.format(make_table_name(tableId)))
    except Exception as e:
        print(e)
        abort(400, 'Table does not exist')

    try:
        res = cursor.fetchone()
        if res[2] == 1:
            cursor.execute(delete_cmd, [tableId])

        cursor.execute(delete_entry_cmd, [tableId])
        cursor.execute(drop)
        conn.commit()
    except Exception as e:
        print(e)
        abort(500, 'SQL error at drop')


modify_column_cmd = '''ALTER TABLE {} CHANGE `{}` `{}` text;'''


def modifyColumn(tableId, oldCol, newCol, userId):
    if oldCol == 'id':
        abort(400, 'Cannot remove this column')

    cols = getColumns(tableId)

    if oldCol not in cols:
        abort(400, 'Column not found')

    cmd = modify_column_cmd.format(make_table_name(tableId), oldCol, newCol)
    conn = db.conn()
    cursor = conn.cursor()
    cursor.execute(cmd)
    
    cursor.execute(check_tracking_cmd, [tableId])
    if cursor.fetchall() == tracking_disabled:
        return

    args = [tableId, 0, "Column '" + oldCol + "'", "Column '" + newCol + "'", userId, time(), 6]

    cursor.execute(insert_history_cmd, args)
    conn.commit()


get_table_columns_cmd = '''select COLUMN_NAME from INFORMATION_SCHEMA.COLUMNS where TABLE_NAME = %s;'''


def getColumns(tableId):
    conn = db.conn()
    cursor = conn.cursor()

    cursor.execute(get_table_columns_cmd, [make_table_name(tableId)])

    return [i[0] for i in cursor.fetchall()]


modify_table_name_cmd = '''UPDATE Tables SET tableName = %s where tableId = %s;'''

check_tracking_special = 'SELECT * FROM Tables WHERE tableId = %s;'

def modifyTableName(tableId, name, userId):
    conn = db.conn()
    cursor = conn.cursor()

    if not checkTableExists(tableId):
        abort(400, 'This table does not exist')

    try:
        cursor.execute(check_tracking_special, [tableId])
        res = cursor.fetchone()
        if res[2] == 1:
            args = [tableId, 0, "Table '" + res[1] + "'", "Table '" + name + "'", userId, time(), 0]
            cursor.execute(insert_history_cmd, args)

        cursor.execute(modify_table_name_cmd, [name, tableId])
        conn.commit()
    except Exception as e:
        print(e)
        abort(500, 'Exception in modify table name')


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


describe_cmd = 'DESC table_%s;'

def addEntry(data):
    conn = db.conn()
    cursor = conn.cursor()

    try:
        cursor.execute(describe_cmd, [data['tableId']])
    except MySQLdb.ProgrammingError:
        abort(400, "Table doesn't exist")
    
    res = cursor.fetchall()

    insert_cmd = 'INSERT INTO table_%s ('

    row = [data['tableId']]
    for i in range(1, cursor.rowcount):
        insert_cmd += res[i][0] + ', '

    insert_cmd = insert_cmd[0 : len(insert_cmd) - 2]
    insert_cmd += ') VALUES ('

    num = len(data['contents'])
    if num != cursor.rowcount - 1:
        abort(400, 'Given input does not match table schema')

    for i in range(0, num - 1):
        row.append(data['contents'][i])
        insert_cmd += '%s, '

    row.append(data['contents'][num - 1])
    insert_cmd += '%s);'

    cursor.execute(insert_cmd, tuple(row))
    id = cursor.lastrowid

    cursor.execute(check_tracking_cmd, [data['tableId']])
    if cursor.fetchall() == tracking_disabled:
        conn.commit()
        return True
    
    args = [data['tableId'], id, "", str(data['contents']), data['userId'], time(), 1]

    cursor.execute(insert_history_cmd, args)
    
    conn.commit()
    return True


def removeEntry(table, row, user):
    conn = db.conn()
    cursor = conn.cursor()

    delete_cmd = 'DELETE FROM table_%s WHERE id = %s;'

    cursor.execute(check_tracking_cmd, [table])
    if cursor.fetchall() == tracking_enabled:
        cursor.execute(get_row_cmd, [int(table), int(row)])
        res = cursor.fetchone()
        res = res[1:]

        args = [table, row, str(res), "", user, time(), 2]

        cursor.execute(insert_history_cmd, args)

    try:
        cursor.execute(delete_cmd, [table, row])
    except MySQLdb.ProgrammingError:
        abort(400, "Table doesn't exist")

    conn.commit()
    return True


def modifyEntry(data):
    conn = db.conn()
    cursor = conn.cursor()

    update_cmd = 'UPDATE table_%s SET '

    row = [data['tableId']]

    try:
        cursor.execute(describe_cmd, [row[0]])
    except MySQLdb.ProgrammingError:
        abort(400, "Table doesn't exist")
    
    res = cursor.fetchall()

    num = len(data['contents'])
    if cursor.rowcount != num:
        abort(400, 'Given input does not match table schema')

    for i in range(1, cursor.rowcount):
        update_cmd += res[i][0] + ' = %s, '
        row.append(data['contents'][i])

    cursor.execute(check_tracking_cmd, [data['tableId']])
    if cursor.fetchall() == tracking_enabled:
        cursor.execute(get_row_cmd, [data['tableId'], data['contents'][0]])
        resp = cursor.fetchone()
        resp = resp[1:]

        args = [data['tableId'], data['contents'][0], str(resp), str(data['contents'][1:]), data['userId'], time(), 3]

        cursor.execute(insert_history_cmd, args)

    update_cmd = update_cmd[0 : len(update_cmd) - 2]
    update_cmd += ' WHERE id = %s'
    row.append(data['contents'][0])

    cursor.execute(update_cmd, tuple(row))

    conn.commit()
    return True

def track(id):
    conn = db.conn()
    cursor = conn.cursor()

    track_cmd = 'UPDATE Tables SET trackHistory = 1 WHERE tableId = %s;'
    
    cursor.execute(track_cmd, [id])

    conn.commit()
    return True


def untrack(id):
    conn = db.conn()
    cursor = conn.cursor()

    track_cmd = 'UPDATE Tables SET trackHistory = 0 WHERE tableId = %s;'
    delete_cmd = 'DELETE FROM TableHistory WHERE tableId =  %s;'
    
    cursor.execute(track_cmd, [id])
    cursor.execute(untrack_cmd, [id])

    conn.commit()
    return True


def itemHistory(table, id):
    conn = db.conn()
    cursor = conn.cursor()

    item_history_cmd = 'SELECT * FROM TableHistory WHERE tableId = %s AND rowId = %s ORDER BY changeId DESC;'

    cursor.execute(item_history_cmd, [table, id])
    res = cursor.fetchall()

    return res


def history(table):
    conn = db.conn()
    cursor = conn.cursor()

    history_cmd = 'SELECT * FROM TableHistory WHERE tableId = %s;'
    
    cursor.execute(history_cmd, [table])
    res = cursor.fetchall()

    return res

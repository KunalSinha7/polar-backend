from flask import Blueprint, jsonify, request, abort, g

import table.db as db
import auth
import auth.jwt
import auth.perms
import uuid
import message

table = Blueprint('table', __name__)


@table.route('/all', methods=['POST'])
@auth.login_required(perms=[8])
def allTables():
    tables = db.getAllTables()
    return jsonify(tables)

@table.route('/create', methods=['POST'])
@auth.login_required(perms=[9])
def createTable():
    data = request.get_json()

    if 'tableName' not in data or 'columns' not in data:
        abort(400, 'missing tableName or columns')

    table_id = db.createTable(data['tableName'])

    for c in data['columns']:
        db.addColumn_id(table_id, c)

    return 'success'

@table.route('/delete', methods=['POST'])
@auth.login_required(perms=[9])
def deleteTable():
    data = request.get_json()

    if 'tableId' not in data:
        abort(400, 'Missing tableId')

    db.delete_table(data['tableId'])


    return 'success'
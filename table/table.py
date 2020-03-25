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

    db.createTable(data['tableName'])
    return 'hello world'
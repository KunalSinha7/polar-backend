from flask import g
from flask import current_app as app
import MySQLdb as sql
from MySQLdb.cursors import DictCursor

import db.util
import config_reader as conf
import os

config = conf.read("database")

def make_conn():
    db_table = config["database"]
    return sql.connect(
            host = db_table["host"],
            user = db_table["user"],
            passwd = db_table["pass"],
            db = db_table["name"], 
            use_unicode=True, charset="utf8mb4")

def make_test_conn():
    db_table = config["test_database"]
    return sql.connect(
            host = db_table["host"],
            user = db_table["user"],
            passwd = db_table["pass"],
            db = db_table["name"], 
            use_unicode=True, charset="utf8mb4")

def conn():
    if app.config['TESTING'] is True:
        print('Using testing db')
        g.db_conn = make_test_conn()
    elif not hasattr(g, 'db_conn'):
        g.db_conn = make_conn()

    return g.db_conn

def test_conn():
    return make_test_conn()




    
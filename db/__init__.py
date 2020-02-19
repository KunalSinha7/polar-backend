from flask import g
from flask import current_app as app
import MySQLdb as sql
from MySQLdb.cursors import DictCursor
from configparser import SafeConfigParser

import db.util
import os

parser = SafeConfigParser()
parser.read('../database.ini')

def make_conn():

	return sql.connect(
    	host=parser.get('database','host'), 
    	db=parser.get('database','name'),
    	passwd=parser.get('database','pass'),
    	user=parser.get('database','user'),)

def make_test_conn():
	return sql.connect(
    	host=parser.get('test_database','host'), 
    	db=parser.get('test_database','name'),
    	passwd=parser.get('test_database','pass'),
    	user=parser.get('test_database','user'),)


def conn():
    if app.config['TESTING'] is True:
        g.db_conn = make_test_conn()
    elif not hasattr(g, 'db_conn'):
        g.db_conn = make_conn()

    return g.db_conn

def test_conn():
    return make_test_conn()




    
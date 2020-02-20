from flask import g
from flask import current_app as app
import MySQLdb as sql
from MySQLdb.cursors import DictCursor
import configparser

import db.util
import os





def make_conn():

	path = ''
	if os.path.isfile('/home/ubuntu/database.ini'):
		path = '/home/ubuntu/database.ini'
	else:
		path = '../database.ini'

	parser = configparser.ConfigParser()
	parser.read(path)

	return sql.connect(
    	host=parser.get('database','host'), 
    	db=parser.get('database','name'),
    	passwd=parser.get('database','pass'),
    	user=parser.get('database','user'),)

def make_test_conn():

	path = ''
	if os.path.isfile('/home/ubuntu/database.ini'):
		path = '/home/ubuntu/database.ini'
	else:
		path = '../database.ini'

	parser = configparser.ConfigParser()
	parser.read(path)
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




    
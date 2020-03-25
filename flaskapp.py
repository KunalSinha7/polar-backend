import os

from flask import Flask, jsonify, make_response
from user import user
from iam import iam
from table import table
from message import message
from flask_cors import CORS


import db
import db.util

app = Flask(__name__)
app.register_blueprint(user.user, url_prefix='/user')
app.register_blueprint(iam.iam, url_prefix='/iam')
app.register_blueprint(table.table, url_prefix='/table')
app.register_blueprint(message.message, url_prefix='/message')
CORS(app, support_credentials=True)

if os.environ.get('config') is None:
    PATH = ''
    if os.path.isfile('/home/ubuntu/config.cfg'):
        PATH = '/home/ubuntu/config.cfg'
    else:
        PATH = '../config.cfg'

    app.config.from_pyfile(PATH)

@app.route('/')
def index():
    return ''

@app.cli.command("resetdb")
def makedb():
    db.util.resetDB()

@app.errorhandler(400)
def bad_request(error):
    return make_response(jsonify({'code': 400, 'message': error.description}), 400)

@app.errorhandler(401)
def bad_auth(error):
    return make_response(jsonify({'code': 401, 'message': error.description}), 401)

@app.errorhandler(403)
def unauthorized(error):
    return make_response(jsonify({'code': 403, 'message': error.description}), 403)

if __name__ == '__main__':
    app.run(threaded=True)

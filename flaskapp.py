from flask import Flask, Blueprint, jsonify, make_response
from user import user
from iam import iam
from flask_cors import CORS, cross_origin

import os
import db
import db.util
import auth.jwt

app = Flask(__name__)
app.register_blueprint(user.user, url_prefix='/user')
app.register_blueprint(iam.iam, url_prefix='/iam')
CORS(app, support_credentials=True)

if os.environ.get('config') is None:
    if os.path.isfile('/home/ubuntu/config.cfg'):
        path = '/home/ubuntu/config.cfg'
    else:
        path = '../config.cfg'


@app.cli.command("resetdb")
def makedb():
    db.util.resetDB()


@app.route('/')
def index():
    return 'Hello World'


@app.errorhandler(400)
def bad_request(error):
    return make_response(jsonify({'code': 400, 'message': error.description}), 400)


@app.errorhandler(401)
def unauthorized(error):
    return make_response(jsonify({'code': 401, 'message': error.description}), 401)

@app.errorhandler(403)
def unauthorized(error):
    return make_response(jsonify({'code': 403, 'message': error.description}), 403)

if __name__ == '__main__':
    app.run(threaded=True)

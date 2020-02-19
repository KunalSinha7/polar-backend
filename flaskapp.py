from flask import Flask, Blueprint, jsonify, make_response
from user import user
from iam import iam
from flask_cors import CORS

import os
import db
import db.util
import auth.jwt

app = Flask(__name__)
app.register_blueprint(user.user, url_prefix='/user')
app.register_blueprint(iam.iam, url_prefix='/iam')
CORS(app)

if os.environ.get('config') is None:
    app.config.from_pyfile('../config.cfg')


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


if __name__ == '__main__':
    app.run(threaded=True)


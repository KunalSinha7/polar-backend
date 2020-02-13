from flask import Flask, Blueprint, jsonify, make_response
from user import user

import os
import db
import db.util
import auth.jwt

app = Flask(__name__)
app.register_blueprint(user.user, url_prefix='/user')


if os.environ.get('config') is None:
    app.config.from_pyfile('../config.cfg')


@app.route('/')
def index():
    return "Hello from flask"


@app.route('/test')
def test():
    out = {}
    out['key'] = app.secret_key
    jwt = auth.jwt.make_jwt(2)
    out['jwt'] = jwt.decode('utf-8')
    print(auth.jwt.check_jwt(jwt))

    return jsonify(out)


@app.errorhandler(400)
def bad_request(error):
	return make_response(jsonify({'code': 400, 'message': error.description}), 400)


@app.errorhandler(401)
def unauthorized(error):
    return make_response(jsonify({'code': 401, 'message': error.description}), 401)


if __name__ == '__main__':
    app.run(threaded=True)


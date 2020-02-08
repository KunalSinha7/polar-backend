from flask import Flask, Blueprint, jsonify
from users import user

import db
import db.util

app = Flask(__name__)
app.register_blueprint(user.user, url_prefix='/user')



@app.route('/')
def index():
  return "Hello from flask"

@app.route('/test')
def test():
  out = {}
  out['users'] = db.util.check()
  return jsonify(out)


@app.route('/error', methods=['POST'])
def error():
  out = jsonify("Hello world")
  
  return out, 401


if __name__ == '__main__':
  app.run(threaded=True)
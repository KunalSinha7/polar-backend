from flask import Flask, Blueprint, jsonify
from users import user

app = Flask(__name__)
app.register_blueprint(user.user, url_prefix='/user')



@app.route('/')
def index():
  return "Hello from flask"

@app.route('/test')
def test():
  return 'hello test'


@app.route('/error', methods=['POST'])
def error():
  out = jsonify("Hello world")
  return out, 401


if __name__ == '__main__':
  app.run(threaded=True)
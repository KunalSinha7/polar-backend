from flask import Flask

app = Flask(__name__)




@app.route('/')
def index():
  return "Hello from flask"

@app.route('/test')
def test():
  return 'hello test'

@app.route('/fout')
def four():
  return "Bad request", 401

if __name__ == '__main__':
  app.run(threaded=True)
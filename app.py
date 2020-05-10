
from flask import Flask, jsonify
from resources.routes import routes


import models

DEBUG=True 
PORT=8000 

app = Flask(__name__)


app.register_blueprint(routes, url_prefix='/api/v1/routes')





@app.route('/')
def test():
  return 'test'

@app.route('/test_json')
def get_json():
  return jsonify(['jsonify', 'working'])



if __name__ == '__main__':
  models.initialize()
  app.run(debug=DEBUG, port=PORT) 
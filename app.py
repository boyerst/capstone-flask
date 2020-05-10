
from flask import Flask, jsonify

from resources.routes import routes
from resources.users import users

import models

from flask_cors import CORS

from flask_login import LoginManager

DEBUG=True 
PORT=8000 

app = Flask(__name__)

app.secret_key = "Secret Time."

login_manager = LoginManager()

login_manager.init_app(app)



CORS(routes, origins=['http://localhost:3000'], supports_credentials=True)
CORS(users, origins=['http://localhost:3000'], supports_credentials=True)

app.register_blueprint(routes, url_prefix='/api/v1/routes')
app.register_blueprint(users, url_prefix='/api/v1/users')





@app.route('/')
def test():
  return 'test'

@app.route('/test_json')
def get_json():
  return jsonify(['jsonify', 'working'])



if __name__ == '__main__':
  models.initialize()
  app.run(debug=DEBUG, port=PORT) 

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



@login_manager.user_loader
def load_user(user_id):
  try:
    print("loading the following user")
    user = models.User.get_by_id(user_id) #changed this
    return user 
  except models.DoesNotExist: 
    return None


@login_manager.unauthorized_handler
def unauthorized():
  return jsonify(
    data={
      'error': "User not logged in"
    },
    message='You must be logged in to access that resource',
    status=401
  ), 401



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

import os
from flask import Flask, jsonify, g

from resources.routes import routes
from resources.users import users
from resources.markers import markers

# import logging
# import json, commands, requests, sys

import models

from flask_cors import CORS


from flask_login import LoginManager

DEBUG=True 
PORT=8000 

app = Flask(__name__)

# app.logger.addHandler(logging.StreamHandler(sys.stdout))
# app.logger.setLevel(logging.ERROR)

# app = Flask(__name__, static_folder="./static/dist", template_folder="./static")

app.secret_key = "Secret Time."

login_manager = LoginManager()

login_manager.init_app(app)

print("Here is the app secret_key:")
print(app.secret_key)



# SESSION
# @login_manager.user_loader
# def load_user(user_id):
#   try:
#     print("loading the following user")
#     user = models.User.get_by_id(user_id) 
#     return user 
#   except models.DoesNotExist: 
#     return None

# AUTH
# @login_manager.unauthorized_handler
# def unauthorized():
#   return jsonify(
#     data={
#       'error': "User not logged in"
#     },
#     message='You must be logged in to access that resource',
#     status=401
#   ), 401






CORS(routes, origins=['http://localhost:3000', 'https://wmat-tracks.herokuapp.com'], supports_credentials=True)
CORS(markers, origins=['http://localhost:3000','https://wmat-tracks.herokuapp.com'], supports_credentials=True)
CORS(users, origins=['http://localhost:3000','https://wmat-tracks.herokuapp.com'], supports_credentials=True)


app.register_blueprint(routes, url_prefix='/api/v1/routes')
app.register_blueprint(markers, url_prefix='/api/v1/markers')
app.register_blueprint(users, url_prefix='/api/v1/users')



@app.before_request 
def before_request():
  print("you should see this before each request") 
  g.db = models.DATABASE
  g.db.connect()

@app.after_request 
def after_request(response):
  print("you should see this after each request") #
  g.db.close()
  return response 
       



@app.route('/')
def test():
  return 'test'

@app.route('/test_json')
def get_json():
  return jsonify(['jsonify', 'working'])


if 'ON_HEROKU' in os.environ: 
  print('\non heroku!')
  models.initialize()


if __name__ == '__main__':
  models.initialize()
  app.run(debug=DEBUG, port=PORT) 
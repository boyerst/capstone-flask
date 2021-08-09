
import os
from flask import Flask, g, jsonify, make_response, request
from flask_login import LoginManager


from resources.users import users
from resources.routes import routes
from resources.markers import markers
# from flask import make_response, Response

from flask_cors import CORS
import models

# import logging
# import json, commands, requests, sys

DEBUG=True 
PORT=8000 

app = Flask(__name__)

# app = Flask(__name__, static_folder="./static/dist", template_folder="./static")



app.secret_key = "secret time"
login_manager = LoginManager()
login_manager.init_app(app)

# app.logger.addHandler(logging.StreamHandler(sys.stdout))
# app.logger.setLevel(logging.ERROR)


print("Here is the app secret_key:")
print(app.secret_key)


# @app.route('/cookie/')
# def hello_world():
#     print("here is your COOOOOOOOOOOOOOOOOOOOKIE route")
#     resp = make_response('Hello, World!');
#     resp.set_cookie('same-site-cookie', 'foo', samesite='None');
#     resp.set_cookie('cross-site-cookie', 'bar', samesite='None', secure=True);
#     return resp


@app.route('/')
def hello_world():
    resp = make_response('Hello, World!');
    resp.set_cookie('same-site-cookie', 'foo', samesite='None');
    resp.set_cookie('cross-site-cookie', 'bar', samesite='None', secure=True);
    print("here is your COOOOOOOOOOOOOOOOOOOOKIE route")
    return resp


app.config['SESSION_COOKIE_SAMESITE'] = 'None'
app.config['SESSION_COOKIE_SECURE'] = True

# @app.route('/cookie/')
# def cookie():
#     res = make_response("Setting a cookie")
#     res.set_cookie('foo', 'bar', max_age=60*60*24*365*2)
#     return res



# @app.route('/')
# def index():
#     resp = make_response(render_template(...))
#     resp.set_cookie('somecookiename', 'I am cookie')
#     return resp 

# @app.route('/get-cookie/')
# def get_cookie():
#     username = request.cookies.get('somecookiename')



# @app.route('/setcookie')
# def setcookie():
#     resp = make_response(f"The Cookie has been Set")
#     resp.set_cookie('Name','AskPython')
#     return resp
 
# @app.route('/getcookie')
# def getcookie():
#     name = request.cookies.get('Name')
#     return f"The Site : {name}"


# SESSION
@login_manager.user_loader
def load_user(user_id):
  try:
    print("loading the following user:")
    return models.User.get_by_id(user_id) 
  except models.DoesNotExist: 
    return None


# AUTH
@login_manager.unauthorized_handler
def unauthorized():
  return jsonify(
    data={
      'error': "User not logged in"
    },
    message="You must be logged in to access that resource",
    status=401
  ), 401




CORS(users, origins=['http://localhost:3000', 'https://wmattracks.herokuapp.com'], supports_credentials=True)
CORS(routes, origins=['http://localhost:3000', 'https://wmattracks.herokuapp.com'], supports_credentials=True)
CORS(markers, origins=['http://localhost:3000', 'https://wmattracks.herokuapp.com'], supports_credentials=True)



app.register_blueprint(users, url_prefix='/api/v1/users')
app.register_blueprint(routes, url_prefix='/api/v1/routes')
app.register_blueprint(markers, url_prefix='/api/v1/markers')


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





##################################################################




# import os
# from flask import Flask, jsonify, g

# from resources.routes import routes
# from resources.users import users
# from resources.markers import markers

# # import logging
# # import json, commands, requests, sys

# import models

# from flask_cors import CORS


# from flask_login import LoginManager

# DEBUG=True 
# PORT=8000 

# app = Flask(__name__)

# # app.logger.addHandler(logging.StreamHandler(sys.stdout))
# # app.logger.setLevel(logging.ERROR)

# # app = Flask(__name__, static_folder="./static/dist", template_folder="./static")

# app.secret_key = "Secret Time."

# login_manager = LoginManager()

# login_manager.init_app(app)

# print("Here is the app secret_key:")
# print(app.secret_key)



# # SESSION
# @login_manager.user_loader
# def load_user(user_id):
#   try:
#     print("loading the following user")
#     user = models.User.get_by_id(user_id) 
#     return user 
#   except models.DoesNotExist: 
#     return None

# # AUTH
# # @login_manager.unauthorized_handler
# # def unauthorized():
# #   return jsonify(
# #     data={
# #       'error': "User not logged in"
# #     },
# #     message='You must be logged in to access that resource',
# #     status=401
# #   ), 401






# CORS(routes, origins=['http://localhost:3000', 'https://wmat-tracks.herokuapp.com'], supports_credentials=True)
# CORS(markers, origins=['http://localhost:3000','https://wmat-tracks.herokuapp.com'], supports_credentials=True)
# CORS(users, origins=['http://localhost:3000','https://wmat-tracks.herokuapp.com'], supports_credentials=True)


# app.register_blueprint(routes, url_prefix='/api/v1/routes')
# app.register_blueprint(markers, url_prefix='/api/v1/markers')
# app.register_blueprint(users, url_prefix='/api/v1/users')



# @app.before_request 
# def before_request():
#   print("you should see this before each request") 
#   g.db = models.DATABASE
#   g.db.connect()

# @app.after_request 
# def after_request(response):
#   print("you should see this after each request") #
#   g.db.close()
#   return response 
       



# @app.route('/')
# def test():
#   return 'test'

# @app.route('/test_json')
# def get_json():
#   return jsonify(['jsonify', 'working'])


# if 'ON_HEROKU' in os.environ: 
#   print('\non heroku!')
#   models.initialize()


# if __name__ == '__main__':
#   models.initialize()
#   app.run(debug=DEBUG, port=PORT) 
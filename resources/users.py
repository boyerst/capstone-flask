import models 
from flask import Blueprint, request, jsonify
from flask_bcrypt import generate_password_hash, check_password_hash
from flask_login import login_user, current_user, logout_user
from playhouse.shortcuts import model_to_dict

users = Blueprint('users', 'users')




@users.route('/', methods=['GET'])
def test(): 
  return "user resource hittingf" 



#REGISTER /users/register
@users.route('/register', methods=['POST'])
def register():
  payload = request.get_json()
  print(request.get_json())
  print(payload) 
  payload['email'] = payload['email'].lower()
  payload['username'] = payload['username'].lower()
  try:
    models.User.get(models.User.email == payload['email'])
    return jsonify(
      data={},
      message=f"A user with the email {payload['email']} already exists",
      status=401
    ), 401
  except models.DoesNotExist:
    created_user = models.User.create(
      username=payload['username'],
      email=payload['email'],
      password=generate_password_hash(payload['password'])
    )
    print(created_user)
    login_user(created_user) 
    created_user_dict = model_to_dict(created_user)
    print(created_user_dict)
    print(type(created_user_dict['password']))
    created_user_dict.pop('password')
    return jsonify(
      data=created_user_dict,
      message=f"You have successfully registered user {created_user_dict['email']}",
      status=201
    ), 201



#LOGIN /users/login
@users.route('/login', methods=['POST'])
def login():
  payload = request.get_json()
  payload['email'] = payload['email'].lower()
  payload['username'] = payload['username'].lower()
  try: 
    user = models.User.get(models.User.email == payload['email'])
    user_dict = model_to_dict(user)
    password_is_good = check_password_hash(user_dict['password'], payload['password'])
    if(password_is_good):
      login_user(user)
      user_dict.pop('password')
      return jsonify(
        data=user_dict,
        message=f"Successfully logged in {user_dict['email']}",
        status=200
      ), 200
    else: 
      print('pw is no good')
      return jsonify(
        data={},
        message="Email or password is incorrect", 
        status=401
      ), 401
  except models.DoesNotExist: 
    print('The username is not correct')
    return jsonify(
      data={},
      message="The email or password is incorrect", 
      status=401
    ), 401


#LOGOUT /users/logout
@users.route('/logout', methods=['GET'])
def logout():
  logout_user()
  return jsonify(
    data={}, 
    message="Successfully logged out",
    status=200
  ), 200














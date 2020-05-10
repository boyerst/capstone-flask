import models 

from flask import Blueprint, request, jsonify
from flask_bcrypt import generate_password_hash, check_password_hash
from flask_login import login_user, current_user, logout_user

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
  return "login route hitting"















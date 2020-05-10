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
  print(request.get_json())
  payload = request.get_json()
  payload['email'] = payload['email'].lower()
  payload['username'] = payload['username'].lower()
  print(payload) 
  try:
    models.User.get(models.User.email == payload['email'])
    return jsonify(
      data={},
      message=f"user with the email {payload['email']} already exists",
      status=401
    ), 401
  except models.DoesNotExist:
    created_user = models.User.create(
      username=payload['username'],
      email=payload['email'],
      password=generate_password_hash(payload['password'])
    )
    print(created_user)
    return jsonify(
      data=created_user_dict,
      message=f"Successfully registered user {created_user_dict['email']}",
      status=201
    ), 201

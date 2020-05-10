import models 

from flask import Blueprint


users = Blueprint('users', 'users')




@users.route('/', methods=['GET'])
def test(): 
  return "user resource hittingf" 
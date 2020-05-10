import models


from flask import Blueprint



routes = Blueprint('routes', 'routes')

@routes.route('/')
def routes_index():
  return "routes resource working" 
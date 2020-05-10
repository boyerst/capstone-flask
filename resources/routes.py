import models


from flask import Blueprint, request



routes = Blueprint('routes', 'routes')







@routes.route('/')
def routes_index():
  return "routes resource working" 


@routes.route('/', methods=['POST'])
def create_route():
  payload = request.get_json()
  print(payload)
  new_route = models.Route.create(
    rider_id=payload['rider_id'],
    route_id=payload['route_id'],
    location=payload['location'], 
    length=payload['length'], 
    skill_level=payload['skill_level'],
    obstacles=payload['obstacles'], 
    comments=payload['comments'])
  print(new_route)
  return "route create route hitting - check terminal"
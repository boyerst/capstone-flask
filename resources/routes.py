import models

from flask import Blueprint, request, jsonify, json

from playhouse.shortcuts import model_to_dict 
from decimal import Decimal

from flask_login import current_user, login_required

routes = Blueprint('routes', 'routes')


class CustomJsonEncoder(json.JSONEncoder):
  def default(self, obj):
    if isinstance(obj, Decimal):
      return float(obj)
    return super(CustomJsonEncoder, self).default(obj)



#INDEX /routes
@routes.route('/', methods=['GET'])
@login_required
def routes_index():
  current_user_route_dicts = [model_to_dict(route) for route in current_user.routes] 
  for route_dict in current_user_route_dicts:
    route_dict['user_id'].pop('password')
  print(current_user_route_dicts)
  return jsonify({
    'data': current_user_route_dicts,
    'message': f"Successfully found {len(current_user_route_dicts)} routes",
    'status': 200
  }), 200


#ALL ROUTES /routes/all
@routes.route('/all', methods=['GET'])
@login_required
def all_routes_index():
  routes = models.Route.select()
  route_dicts = [ model_to_dict(route) for route in routes ]
  print(route_dicts)
  return jsonify({
    'data': route_dicts,
    'message': f"Successfully found {len(route_dicts)} routes",
    'status': 200
  }), 200




#SHOW /routes/id
@routes.route('/<id>', methods=['GET'])
def show_route(id):
  route = models.Route.get_by_id(id)
  if not current_user.is_authenticated:
    return jsonify(
      data={
        'markers': route.markers,
        'user_id': route.user_id,
        'location': route.location,
        'length': route.length,
        'images': route.images,
        'skill_level': route.skill_level,
        'comments': route.comments
      },
      message="Registered users can see more info about this route",
      status=200
    ), 200
  else:
    route_dict = model_to_dict(route)
    markers_arr=[]
    for marker in route.markers:
       #can pop things our before adding to route dict
      markers_arr.append(model_to_dict(marker))
    print(route_dict)
    route_dict['marker'] = markers_arr
    route_dict['user_id'].pop('password')
    return (
      json.dumps(route_dict, cls=CustomJsonEncoder)
    ), 200








#CREATE /routes/
@routes.route('/', methods=['POST'])
@login_required
def create_route():
  payload = request.get_json()
  print(payload)
  new_route = models.Route.create(
    user_id=current_user.id,
    location=payload['location'], 
    length=payload['length'], 
    images=payload['images'],
    skill_level=payload['skill_level'],
    comments=payload['comments'])
  route_dict=model_to_dict(new_route)
  print(new_route)
  return jsonify(
    data=route_dict, 
    message = 'successfully created route',
    status=201
    ), 201



#UPDATE /routes/id
@routes.route('/<id>', methods=['PUT'])
@login_required
def update_route(id):
  payload = request.get_json()
  route_to_update = models.Route.get_by_id(id)
  if route_to_update.user_id.id == current_user.id:
    if 'location' in payload:
      route_to_update.location = payload['location'] 
    if 'length' in payload:
      route_to_update.length = payload['length'] 
    if 'images' in payload:
      route_to_update.images = payload['images']
    if 'skill_level' in payload:
      route_to_update.skill_level = payload['skill_level'] 
    if 'comments' in payload:
      route_to_update.comments = payload['comments'] 
    route_to_update.save()
    updated_route_dict = model_to_dict(route_to_update)
    updated_route_dict['user_id'].pop('password')
    return jsonify(
      data=updated_route_dict,
      message=f"Successfully updated route with id {id}",
      status=200
    ), 200
  else: 
    return jsonify(
    data={
      'error': '403 Forbidden'
    },
    message="Route poster's id does not match current user's id. Routes can only be updated by their posters.",
    status=403
    ), 403




#DELETE /route/id
@routes.route('/<id>', methods=['DELETE'])
@login_required
def delete_route(id):
  route_to_delete = models.Route.get_by_id(id)
  if route_to_delete.user_id.id == current_user.id:
    route_to_delete.delete_instance()
    return jsonify(
      data={}, 
      message = f"Successfully deleted Route with id {id}",
      status=200
    ), 200
  else: 
    return jsonify(
    data={
      'error': '403 Forbidden'
    },
    message="Route poster's id does not match current user's id. Routes can only be deleted by their posters.",
    status=403
    ), 403
  return jsonify(
    data={},
    message="Successfully deleted {} route with id {}".format(num_of_rows_deleted, id),
    status=200
  ), 200






#ALL ROUTES /routes/all
# @routes.route('/all', methods=['GET'])
# def route_index():
#   routes = models.Route.select()
#   route_dicts = [ model_to_dict(route) for route in routes ]

#   print(route_dicts)
#   return jsonify(route_dicts), 200

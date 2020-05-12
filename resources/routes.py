import models

from flask import Blueprint, request, jsonify

from playhouse.shortcuts import model_to_dict 


from flask_login import current_user, login_required

routes = Blueprint('routes', 'routes')






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

#SHOW /routes/id
@routes.route('/<id>', methods=['GET'])
def show_route(id):
  route = models.Route.get_by_id(id)
  if not current_user.is_authenticated:
    return jsonify(
      data={
        'user_id': route.user_id,
        'length': route.length,
        'skill_level': route.skill_level,
        'comments': route.comments,
      },
      message="Registered users can see more info about this route",
      status=200
    ), 200
  else:
    route_dict = model_to_dict(route)
    route_dict['user_id'].pop('password')
    return jsonify(
      data=route_dict, 
      message=f"Found route with id {id}",
      status=200
      ), 200



#CREATE /routes/
@routes.route('/', methods=['POST'])
@login_required
def create_route():
  payload = request.get_json()
  print(payload)
  new_route = models.Route.create(
    user_id=payload['user_id'],
    location=payload['location'], 
    length=payload['length'], 
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
def update_route(id):
  payload = request.get_json()
  update_query = models.Route.update(
    user_id=payload['user_id'],
    location=payload['location'], 
    length=payload['length'], 
    skill_level=payload['skill_level'],
    comments=payload['comments']
  ).where(models.Route.id == id)
  num_of_rows_modified = update_query.execute()
  updated_route = models.Route.get_by_id(id) 
  updated_route_dict = model_to_dict(updated_route)
  return jsonify(
    data=updated_route_dict,
    message=f"Successfully updated route with id {id}",
    status=200
  ), 200



#DELETE /route/id
@routes.route('/<id>', methods=['DELETE'])
@login_required
def delete_route(id):
  route_to_delete = models.Route.get_by_id(id)
  if route_to_delete.user_id.id == current_user.id:
    route_to_delete.delete_instance()
    return jsonify(
      data={}, 
      message = f"Successfully deleted route with id {id}",
      status=200
    ), 200
  else: 
    return jsonify(
    data={
      'error': '403 Forbidden'
    },
    message="Route poster's id does not match current user's id. User can only delete their own routes.",
    status=403
    ), 403
  return jsonify(
    data={},
    message="Successfully deleted {} route with id {}".format(num_of_rows_deleted, id),
    status=200
  ), 200















# @routes.route('/<id>', methods=['DELETE']) 
# def delete_route(id):
#   delete_query = models.Route.delete().where(models.Route.id == id)
#   num_of_rows_deleted = delete_query.execute()
#   print(num_of_rows_deleted)
#   return jsonify(
#     data={},
#     message="Successfully deleted route with id {}".format(num_of_rows_deleted, id),
#     status=200
#   ), 200





#ALL ROUTES /routes/all
@routes.route('/all', methods=['GET'])
def route_index():
  routes = models.Route.select()
  route_dicts = [ model_to_dict(route) for route in routes ]

  print(route_dicts)
  return jsonify(route_dicts), 200

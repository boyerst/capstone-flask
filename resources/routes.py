import models

from flask import Blueprint, request, jsonify

from playhouse.shortcuts import model_to_dict 


routes = Blueprint('routes', 'routes')






#INDEX /routes
@routes.route('/')
def routes_index():
  result = models.Route.select()
  route_dicts = [model_to_dict(route) for route in result]

  print(route_dicts)

  return jsonify({
    'data': route_dicts,
    'message': f"Successfully found {len(route_dicts)} routes",
    'status': 200
  }), 200



#CREATE /routes/
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
    rider_id=payload['rider_id'],
    route_id=payload['route_id'],
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
def delete_route(id):
  delete_query = models.Route.delete().where(models.Route.id == id)
  num_of_rows_deleted = delete_query.execute()
  print(num_of_rows_deleted)
  return jsonify(
    data={},
    message="Successfully deleted route with id {}".format(num_of_rows_deleted, id),
    status=200
  ), 200
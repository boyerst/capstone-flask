
import models

from flask import Blueprint, request, jsonify, json

from decimal import Decimal

from playhouse.shortcuts import model_to_dict 

from flask_login import current_user, login_required




markers = Blueprint('markers', 'markers')




class CustomJsonEncoder(json.JSONEncoder):
  def default(self, obj):
    if isinstance(obj, Decimal):
      return float(obj)
    return super(CustomJsonEncoder, self).default(obj)


#INDEX /markers
# @markers.route('/', methods=['GET'])
# def markers_index():
#   current_user_marker_dicts = [model_to_dict(marker) for marker in current_user.markers] 
#   for marker_dict in current_user_marker_dicts:
#     marker_dict['user_id'].pop('password')
#   print(current_user_marker_dicts)
#   return jsonify({
#     'data': current_user_marker_dicts,
#     'message': f"Successfully found {len(current_user_marker_dicts)} markers",
#     'status': 200
#   }), 200


#SHOW /markers/id 
@markers.route('/<id>', methods=['GET'])
def show_marker(id):
  marker = models.Marker.get_by_id(id)
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
    marker_dict = model_to_dict(marker)
    # marker_dict['user_id'].pop('password')
    return jsonify(
      data=marker_dict, 
      message=f"Found route with id {id}",
      status=200
      ), 200



#CREATE /markers/
@markers.route('/', methods=['POST'])
def create_marker():
  payload = request.get_json()
  print(payload)
  new_marker = models.Marker.create(
    route_id=payload['route_id'],
    latitude=payload['latitude'],
    longitude=payload['longitude'],
    image=payload['image'],
    description=payload['description']
    )
  marker_dict=model_to_dict(new_marker)
  print(new_marker)
  return jsonify(
    data=marker_dict, 
    message = 'successfully created marker',
    status=201
    ), 201


#UPDATE /markers/id
@markers.route('/<id>', methods=['PUT'])
def update_marker(id):
  payload = request.get_json()
  update_query = models.Marker.update(
    route_id=payload['route_id'],
    latitude=payload['latitude'],
    longitude=payload['longitude'],
    image=payload['image'],
    description=payload['description']
  ).where(models.Marker.id == id)
  num_of_rows_modified = update_query.execute()
  updated_marker = models.Marker.get_by_id(id) 
  updated_marker_dict = model_to_dict(updated_marker)
  return jsonify(
    data=updated_route_dict,
    message=f"Successfully updated route with id {id}",
    status=200
  ), 200


#DELETE /markers/id
@markers.route('/<id>', methods=['DELETE']) 
def delete_route(id):
  delete_query = models.Marker.delete().where(models.Marker.id == id)
  num_of_rows_deleted = delete_query.execute()
  print(num_of_rows_deleted)
  return jsonify(
    data={},
    message="Successfully deleted marker with id {}".format(num_of_rows_deleted, id),
    status=200
  ), 200



#ALL MARKERS /markers/all
@markers.route('/all', methods=['GET'])
def marker_index():
  markers = models.Marker.select()
  marker_dicts = [ model_to_dict(marker) for marker in markers ]
  print(marker_dicts)
  return json.dumps(marker_dicts, cls=CustomJsonEncoder), 200
 






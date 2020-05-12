
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
@login_required
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
@login_required
def update_marker(id):
  payload = request.get_json()
  marker_to_update = models.Marker.get_by_id(id)
  if marker_to_update.route_id.user_id.id == current_user.id:
    if 'latitude' in payload:
      marker_to_update.latitude = payload['latitude'] 
    if 'longitude' in payload:
      marker_to_update.longitude = payload['longitude'] 
    if 'image' in payload:
      marker_to_update.image = payload['image'] 
    if 'description' in payload:
      marker_to_update.description = payload['description'] 
    marker_to_update.save()
    updated_marker_dict = model_to_dict(marker_to_update)
    # updated_marker_dict['route_id'.'user_id'].pop('password') #how to target password?
    return jsonify(
      data=updated_marker_dict,
      message=f"Successfully updated marker with id {id}",
      status=200
    ), 200
  else: 
    return jsonify(
    data={
      'error': '403 Forbidden'
    },
    message="Marker poster's id does not match current user's id. Markers can only be updated by their posters.",
    status=403
    ), 403




#DELETE /markers/id
@markers.route('/<id>', methods=['DELETE'])
@login_required
def delete_marker(id):
  marker_to_delete = models.Marker.get_by_id(id)
  if marker_to_delete.route_id.user_id.id == current_user.id:
    marker_to_delete.delete_instance()
    return jsonify(
      data={}, 
      message = f"Successfully deleted Marker with id {id}",
      status=200
    ), 200
  else: 
    return jsonify(
    data={
      'error': '403 Forbidden'
    },
    message="Marker poster's id does not match current user's id. Markers can only be deleted by their posters.",
    status=403
    ), 403
  return jsonify(
    data={},
    message="Successfully deleted {} marker with id {}".format(num_of_rows_deleted, id),
    status=200
  ), 200




#ALL MARKERS /markers/all
@markers.route('/all', methods=['GET'])
def marker_index():
  markers = models.Marker.select()
  marker_dicts = [ model_to_dict(marker) for marker in markers ]
  print(marker_dicts)
  return json.dumps(marker_dicts, cls=CustomJsonEncoder), 200
 






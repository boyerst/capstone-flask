
import models

from flask import Blueprint, request, jsonify

from playhouse.shortcuts import model_to_dict 

from flask_login import current_user, login_required

markers = Blueprint('markers', 'markers')




#INDEX /markers
@markers.route('/', methods=['GET'])
def markers_index():
  result = models.Marker.select()
  marker_dicts = [model_to_dict(marker) for marker in result]

  print(marker_dicts)

  return jsonify({
    'data': marker_dicts,
    'message': f"Successfully found {len(marker_dicts)} markers",
    'status': 200
  }), 200


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
from flask import Blueprint, request, jsonify
from .schemas import DeviceSchema
from .services import DeviceService
from app.database.access import DatabaseAccess
from flask_jwt_extended import jwt_required

devices_bp = Blueprint("devices", __name__)
db_access = DatabaseAccess()

@devices_bp.route('/add-device', methods=['POST'])
@jwt_required()
def add_device():
    data = request.get_json()
    device_schema = DeviceSchema()
    errors = device_schema.validate(data)
    if errors:
        return jsonify(errors), 400

    name = data['name']
    interface_type = data['interface_type']
    status = data['status']
    
    # Check if the device already exists
    existing_device, status_code = DeviceService.get_device_by_name(name)
 
    if status_code == 200:
        return jsonify({"message": "Device already exists."}), 409

    results, status_code = DeviceService.add_device(name, interface_type, status)
    if status_code == 201:    
        return results, status_code


@devices_bp.route('/device/<int:device_id>', methods=['GET'])
@jwt_required()
def get_device_by_id(device_id):
    """Retrieve device details by ID"""
    result, status_code = DeviceService.get_device_by_id(device_id)
    device = result.get('device')
    if status_code == 200:
        return jsonify({
            "id": device[0],
            "name": device[1],
            "interface_type": device[2],
            "status": device[3]
        }), status_code
    return jsonify({"message": "Device not found."}), 404
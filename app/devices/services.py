from .models import Device

class DeviceService:
    @staticmethod
    def add_device(name, type, status):
        # Check if the device already exists
        existing_device = Device.find_by_name(name)
        if existing_device:
            return {"message": "Device already exists."}, 409  # Conflict status code
        device_id = Device.insert(name, type, status)
        if device_id:
            return {"message": "Device added successfully", "id": device_id}, 201
        return {"message": "could not add device"}, 400

    @staticmethod
    def get_device_by_id(device_id):
        device = Device.find_by_id(device_id)
        if device:
            return {"device": device}, 200
        return None, 404
    
    @staticmethod
    def get_device_by_name(name):
        device = Device.find_by_name(name)
        if device:
            return {"device": device}, 200
        return None, 404

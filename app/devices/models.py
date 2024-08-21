from app.database.access import DatabaseAccess

class Device:
    db = DatabaseAccess()

    @staticmethod
    def insert(name, type, status):
        device_id = Device.db.insert_device(name, type, status)
        return device_id

    @staticmethod
    def find_by_id(device_id):
        return Device.db.get_device_by_id(device_id)
    
    @staticmethod
    def find_by_name(name):
        return Device.db.get_device_by_name(name)
    
    @staticmethod
    def get_devices():
        return 


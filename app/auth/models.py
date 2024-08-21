from app.database.access import DatabaseAccess
import hashlib

class User:
    def __init__(self, id, username, password_hash):
        self.id = id
        self.username = username
        self.password_hash = password_hash

    @staticmethod
    def create_table():
        db = DatabaseAccess()
        db.create_tables()

    @staticmethod
    def insert(username, password_hash):
        db = DatabaseAccess()
        db.insert_user(username, password_hash)

    @staticmethod
    def find_by_username(username):
        db = DatabaseAccess()
        user_data = db.get_user_by_username(username)
        if user_data:
            print('userdata' ,user_data)
            return User(user_data['id'], user_data['username'], user_data['password_hash'])
        return None

    def check_password(self, password):
        """Compare the provided password with the stored password hash."""
        return self.password_hash == hashlib.sha256(password.encode()).hexdigest()

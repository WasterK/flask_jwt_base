import sqlite3
from sqlite3 import Error

class DatabaseAccess:
    def __init__(self, db_file='kws_pmd.db'):
        """Initialize with the database file name"""
        self.db_file = db_file
        self.connection = self.create_connection()

    def create_connection(self):
        """Create a database connection to the SQLite database"""
        conn = None
        try:
            conn = sqlite3.connect(self.db_file, check_same_thread=False)
            print(f"Connected to the database '{self.db_file}' successfully.")
        except Error as e:
            print(f"Error while connecting to database: {e}")
        return conn

    def create_tables(self):
        """Create all tables if they don't exist"""
        create_users_table_sql = """
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL
        );
        """
        create_devices_table_sql = """
        CREATE TABLE IF NOT EXISTS devices (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT UNIQUE NOT NULL,
            interface_type TEXT CHECK(interface_type IN ('modbus', 'Pulse')) NOT NULL,
            status TEXT NOT NULL
        );
        """
        try:
            cursor = self.connection.cursor()
            cursor.execute(create_users_table_sql)
            cursor.execute(create_devices_table_sql)
            self.connection.commit()
            print("Tables created successfully.")
        except Error as e:
            print(f"Error while creating tables: {e}")

    def insert_user(self, username, password_hash):
        """Insert a new user into the users table"""
        insert_user_sql = """
        INSERT INTO users (username, password_hash) 
        VALUES (?, ?);
        """
        try:
            cursor = self.connection.cursor()
            cursor.execute(insert_user_sql, (username, password_hash))
            self.connection.commit()
            print("User inserted successfully.")
        except Error as e:
            print(f"Error while inserting user: {e}")

    def get_user_by_username(self, username):
        """Retrieve a user by username"""
        get_user_sql = """
        SELECT * FROM users WHERE username = ?;
        """
        try:
            cursor = self.connection.cursor()
            cursor.execute(get_user_sql, (username,))
            user = cursor.fetchone()
            user = {'id': user[0], 'username': user[1], 'password_hash': user[2]}
            return user
        except Error as e:
            print(f"Error while retrieving user: {e}")
            return None

    def insert_device(self, name, interface_type, status):
        """Insert a new device into the devices table and return the device ID"""
        insert_device_sql = """
        INSERT INTO devices (name, interface_type, status) 
        VALUES (?, ?, ?);
        """
        try:
            cursor = self.connection.cursor()
            cursor.execute(insert_device_sql, (name, interface_type, status))
            self.connection.commit()
            device_id = cursor.lastrowid
            print("Device inserted successfully with ID:", device_id)
            return device_id
        except Error as e:
            print(f"Error while inserting device: {e}")
            return None

    def get_device_by_id(self, device_id):
        """Retrieve a device by ID"""
        get_device_sql = """
        SELECT * FROM devices WHERE id = ?;
        """
        try:
            cursor = self.connection.cursor()
            cursor.execute(get_device_sql, (device_id,))
            device = cursor.fetchone()
            return device
        except Error as e:
            print(f"Error while retrieving device: {e}")
            return None

    def get_device_by_name(self, name):
        """Retrieve a device by name"""
        get_device_sql = """
        SELECT * FROM devices WHERE name = ?;
        """
        try:
            cursor = self.connection.cursor()
            cursor.execute(get_device_sql, (name,))
            device = cursor.fetchone()
            return device
        except Error as e:
            print(f"Error while retrieving device: {e}")
            return None

    def close_connection(self):
        """Close the database connection"""
        if self.connection:
            self.connection.close()
            print("Database connection closed.")

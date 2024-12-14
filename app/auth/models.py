import psycopg2
from psycopg2 import sql, Error
from ..config import Config

class UserModule:
    def __init__(self, db_url=None):
        """Initialize with PostgreSQL connection parameters"""
        self.db_url = db_url or Config.DATABASE_URL
        self.connection = self.create_connection()

    def create_connection(self):
        """Establish a connection to the PostgreSQL database"""
        try:
            # Use psycopg2.connect to directly connect with the Render-hosted database
            conn = psycopg2.connect(self.db_url)
            print("Database connection established successfully.")
            return conn
        except Error as e:
            print(f"Error while connecting to the database: {e}")
            return None

    def create_user(self, employee_id, user_name, email, password_hash, first_name, last_name, mobile_number, created_by):
        """Insert a new user into the m_user table"""
        insert_sql = """
        INSERT INTO public.m_user (employee_id, user_name, email, password_hash, first_name, last_name, mobile_number, created_by)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s) RETURNING id;
        """
        try:
            cursor = self.connection.cursor()
            cursor.execute(insert_sql, (employee_id, user_name, email, password_hash, first_name, last_name, mobile_number, created_by))
            user_id = cursor.fetchone()[0]
            self.connection.commit()
            print(f"User created successfully with ID: {user_id}")
            return user_id
        except Error as e:
            print(f"Error while inserting user: {e}")
            return None
        finally:
            cursor.close()

    def get_user_by_username(self, user_name):
        """Retrieve user details by ID"""
        select_sql = """
        SELECT * FROM public.m_user WHERE user_name = %s AND is_delete = false;
        """
        try:
            cursor = self.connection.cursor()
            cursor.execute(select_sql, (user_name,))
            user = cursor.fetchone()
            return user
        except Error as e:
            print(f"Error while fetching user: {e}")
            return None
        finally:
            cursor.close()

    def update_user(self, user_id, email=None, first_name=None, last_name=None, mobile_number=None, modified_by=None):
        """Update user details"""
        update_fields = []
        values = []

        if email:
            update_fields.append("email = %s")
            values.append(email)
        if first_name:
            update_fields.append("first_name = %s")
            values.append(first_name)
        if last_name:
            update_fields.append("last_name = %s")
            values.append(last_name)
        if mobile_number:
            update_fields.append("mobile_number = %s")
            values.append(mobile_number)
        if modified_by:
            update_fields.append("modified_by = %s")
            values.append(modified_by)
            update_fields.append("modified_date = CURRENT_TIMESTAMP")

        if not update_fields:
            print("No fields to update.")
            return False

        values.append(user_id)

        update_sql = sql.SQL("""
        UPDATE public.m_user
        SET {fields}
        WHERE id = %s AND is_delete = false;
        """).format(fields=sql.SQL(", ").join(map(sql.SQL, update_fields)))

        try:
            cursor = self.connection.cursor()
            cursor.execute(update_sql, values)
            self.connection.commit()
            print("User updated successfully.")
            return True
        except Error as e:
            print(f"Error while updating user: {e}")
            return False
        finally:
            cursor.close()

    def delete_user(self, user_id, modified_by):
        """Soft delete a user by setting is_delete to true"""
        delete_sql = """
        UPDATE public.m_user
        SET is_delete = true, modified_by = %s, modified_date = CURRENT_TIMESTAMP
        WHERE id = %s;
        """
        try:
            cursor = self.connection.cursor()
            cursor.execute(delete_sql, (modified_by, user_id))
            self.connection.commit()
            print("User deleted successfully.")
            return True
        except Error as e:
            print(f"Error while deleting user: {e}")
            return False
        finally:
            cursor.close()

    def close_connection(self):
        """Close the database connection"""
        if self.connection:
            self.connection.close()
            print("Database connection closed.")
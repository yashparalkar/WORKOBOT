# database_manager.py
import mysql.connector

# Global variables to hold the connection status and objects
db = None
cursor = None
DB_CONNECTED = False

def connect_to_database():
    """Attempts to connect to the database and sets the global status flag."""
    global db, cursor, DB_CONNECTED
    try:
        # --- IMPORTANT: Use your actual database credentials ---
        db = mysql.connector.connect(
            host="localhost",
            user="root",
            password="password", # Your password
            database="fitness_trainer",
            connection_timeout=5 # Add a timeout
        )
        cursor = db.cursor(buffered=True)
        DB_CONNECTED = True
        print("✅ Database connection successful.")
    except mysql.connector.Error as err:
        print(f"⚠️ DATABASE CONNECTION FAILED: {err}. Running in offline mode.")
        DB_CONNECTED = False

def execute_query(query, values=None):
    """Executes a query only if the database is connected."""
    if not DB_CONNECTED:
        print("Offline mode: Cannot execute query.")
        return
    try:
        cursor.execute(query, values)
        db.commit()
    except mysql.connector.Error as error:
        print(f"Error executing query: {error}")

def fetch_one(query, values=None):
    """Fetches a single result only if the database is connected."""
    if not DB_CONNECTED:
        print("Offline mode: Cannot fetch data.")
        return None
    try:
        cursor.execute(query, values)
        return cursor.fetchone()
    except mysql.connector.Error as error:
        print(f"Error fetching data: {error}")
        return None

# --- Connect when the module is first imported ---
connect_to_database()
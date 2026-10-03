import sqlite3

DATABASE_NAME = "whitepriorix.db"


def get_connection():
    connection = sqlite3.connect(DATABASE_NAME)
    connection.row_factory = sqlite3.Row
    return connection


def create_tables():
    connection = get_connection()
    cursor = connection.cursor()

    # Create the requests table if it does not exist
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS requests (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_name TEXT NOT NULL,
            student_id TEXT,
            problem TEXT NOT NULL,
            request_type TEXT NOT NULL,
            priority INTEGER NOT NULL,
            status TEXT NOT NULL DEFAULT 'waiting'
        )
    """)

    # Check whether student_id already exists
    cursor.execute("PRAGMA table_info(requests)")
    columns = [column["name"] for column in cursor.fetchall()]

    # Add student_id to an existing database if it is missing
    if "student_id" not in columns:
        cursor.execute("""
            ALTER TABLE requests
            ADD COLUMN student_id TEXT
        """)

    connection.commit()
    connection.close()
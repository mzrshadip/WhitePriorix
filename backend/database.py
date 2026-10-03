import sqlite3

DATABASE_NAME = "whitepriorix.db"


def get_connection():
    connection = sqlite3.connect(DATABASE_NAME)
    connection.row_factory = sqlite3.Row
    return connection


def create_tables():
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS requests (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_name TEXT NOT NULL,
            problem TEXT NOT NULL,
            request_type TEXT NOT NULL,
            priority INTEGER NOT NULL,
            status TEXT NOT NULL DEFAULT 'waiting'
        )
    """)

    connection.commit()
    connection.close()
import sqlite3

DB_NAME = "database.sqlite"


def get_db_connection():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row  # Это позволяет получать данные в виде словаря
    return conn
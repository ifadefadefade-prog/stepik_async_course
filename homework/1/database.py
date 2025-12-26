import sqlite3


DB_NAME = 'database.sqlite'


def get_db():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn

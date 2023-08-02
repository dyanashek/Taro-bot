import sqlite3
import logging

database = sqlite3.connect("taro.db", detect_types=sqlite3.PARSE_DECLTYPES|sqlite3.PARSE_COLNAMES)
cursor = database.cursor()

try:
    # creates table users who have filled up the form
    cursor.execute('''CREATE TABLE users (
        id INTEGER PRIMARY KEY,
        user_id TEXT,
        user_username TEXT,
        name TEXT,
        family TEXT,
        instagram TEXT,
        birth DATE,
        service TEXT,
        check_id TEXT,
        check_type TEXT,
        photo TEXT,
        request TEXT,
        request_type TEXT
    )''')
except Exception as ex:
    logging.error(f'Users table already exists. {ex}')

# cursor.execute("DELETE FROM users WHERE id<>10000")
# database.commit()
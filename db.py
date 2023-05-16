import sqlite3
import logging

database = sqlite3.connect("taro.db", detect_types=sqlite3.PARSE_DECLTYPES|sqlite3.PARSE_COLNAMES)
cursor = database.cursor()

try:
    # creates table users who have filled up the form
    cursor.execute('''CREATE TABLE users (
        id INTEGER PRIMARY KEY,
        user_id VARCHAR (30),
        user_username VARCHAR (30),
        name VARCHAR (30),
        family VARCHAR (30),
        instagram VARCHAR (50),
        birth DATE
    )''')
except:
    logging.error('Users table already exists.')

cursor.execute("DELETE FROM users WHERE id<>10000")
database.commit()
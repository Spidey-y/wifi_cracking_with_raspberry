import sqlite3
from sqlite3 import Error

# Function to create a connection to the database
def create_connection():
    conn = None
    try:
        conn = sqlite3.connect('wifi_database.db')
        print("Connection to database successful")
    except Error as e:
        print(f"The error '{e}' occurred")
    return conn

# Check if database exists, if not create tables
def check_database():
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute(''' SELECT count(name) FROM sqlite_master WHERE type='table' AND name='saved_passwords' ''')
    if cursor.fetchone()[0]==1:
        print('Table saved_passwords exists.')
    else:
        cursor.execute('''CREATE TABLE saved_passwords 
                          (id INTEGER PRIMARY KEY,
                           ssid TEXT,
                           password TEXT);''')
        print('Table saved_passwords created.')

    cursor.execute(''' SELECT count(name) FROM sqlite_master WHERE type='table' AND name='saved_handshakes' ''')
    if cursor.fetchone()[0]==1:
        print('Table saved_handshakes exists.')
    else:
        cursor.execute('''CREATE TABLE saved_handshakes 
                          (id INTEGER PRIMARY KEY,
                           ssid TEXT,
                           handshake TEXT);''')
        print('Table saved_handshakes created.')
    conn.commit()
    return conn
    # conn.close()

check_database()

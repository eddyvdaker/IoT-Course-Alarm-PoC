import sqlite3
import os
import time
import urllib.request

db = 'database.sqlite3'


# Deletes old database and creates a new one with an entries table
def create_db():
    try:
        os.remove(db)
    except FileNotFoundError:
        pass

    con = sqlite3.connect(db)
    cur = con.cursor()

    cur.execute("""
    CREATE TABLE entries (
      id integer PRIMARY KEY AUTOINCREMENT,
      t text NOT NULL,
      device_id text NOT NULL,
      device_type text NOT NULL) 
    """)

    con.commit()
    con.close()


# Writes a new entry to the entries table in the database
def write_sql(data):
    con = sqlite3.connect(db)
    cur = con.cursor()
    command = f'INSERT INTO entries (t, device_id, device_type) ' \
              f'VALUES (\'{data["t"]}\', \'{data["device_id"]}\', ' \
              f'\'{data["device_type"]}\')'
    cur.execute(command)
    con.commit()
    con.close()


# Grabs rows from entries table with the specified condition
def read_sql(where):
    con = sqlite3.connect(db)
    cur = con.cursor()
    cur.execute(f'SELECT * FROM entries WHERE {where}')
    data = cur.fetchall()
    con.close()
    return data


# Converts a truple to a list
def truple_to_list(data):
    new_data = []
    for row in data:
        new_data.append(list(row))
    return new_data


# Reads value from status file
def read_status_file(file):
    file = os.path.join('./device_status/' + str(file))
    with open(file, 'r') as f:
        return f.readline()


# Updates status from main app to specified status file
def write_status_file(file, to_write):
    file = os.path.join('./device_status/' + str(file))
    with open(file, 'w') as f:
        f.write(str(to_write))
    return to_write


# Converts a boolean to an 'on' or 'off' string
def bool_to_on_off(to_convert):
    if to_convert:
        return 'On'
    else:
        return 'Off'


# Reads log with specified device type and returns a list
def get_logs(device_type):
    log = truple_to_list(read_sql(f'device_type =\'{device_type}\''))
    log.sort(key=lambda x: x[1], reverse=True)
    new_log = []
    for row in log:
        new_log.append([row[2], time.ctime(float(row[1]))])
    return new_log


# Gets the data from the database and the status and returns an dictionary
# to fill the homepage template
def generate_vars(alarm_status, lights_status):
    doors_log = get_logs('door')
    page_vars = {'alarm_status': bool_to_on_off(alarm_status),
                 'lights_status': bool_to_on_off(lights_status),
                 'door_log': doors_log}
    return page_vars

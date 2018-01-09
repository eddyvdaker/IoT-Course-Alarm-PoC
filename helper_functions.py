import sqlite3
import os
import time

db = 'database.sqlite3'


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


def create_test_data():
    write_sql({'t': time.time(), 'device_id': 'd1', 'device_type': 'door'})
    write_sql({'t': time.time(), 'device_id': 'm3', 'device_type': 'movement'})
    write_sql({'t': time.time(), 'device_id': 'c5', 'device_type': 'camera'})
    write_sql({'t': time.time(), 'device_id': 'd1', 'device_type': 'door'})
    write_sql({'t': time.time(), 'device_id': 'm3', 'device_type': 'movement'})
    write_sql({'t': time.time(), 'device_id': 'c4', 'device_type': 'camera'})
    write_sql({'t': time.time(), 'device_id': 'd7', 'device_type': 'door'})
    write_sql({'t': time.time(), 'device_id': 'm2', 'device_type': 'movement'})
    write_sql({'t': time.time(), 'device_id': 'c1', 'device_type': 'camera'})


def write_sql(data):
    con = sqlite3.connect(db)
    cur = con.cursor()
    command = f'INSERT INTO entries (t, device_id, device_type) ' \
              f'VALUES (\'{data["t"]}\', \'{data["device_id"]}\', ' \
              f'\'{data["device_type"]}\')'
    cur.execute(command)
    con.commit()
    con.close()


def read_sql(where):
    con = sqlite3.connect(db)
    cur = con.cursor()
    cur.execute(f'SELECT * FROM entries WHERE {where}')
    data = cur.fetchall()
    con.close()
    return data


def truple_to_list(data):
    new_data = []
    for row in data:
        new_data.append(list(row))
    return new_data


def read_status_file(file):
    file = os.path.join('./device_status/' + str(file))
    with open(file, 'r') as f:
        return f.readline()


def write_status_file(file, to_write):
    file = os.path.join('./device_status/' + str(file))
    with open(file, 'w') as f:
        f.write(str(to_write))
    return to_write


def bool_to_on_off(to_convert):
    if to_convert:
        return 'On'
    else:
        return 'Off'

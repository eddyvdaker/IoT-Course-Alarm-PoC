from flask import Flask, request, jsonify
import sqlite3
import os

app = Flask(__name__)

db = 'database.sqlite3'

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


def read_alarm_status_file():
    file = 'alarm_status.txt'
    with open(file, 'r') as f:
        return f.readline()


def write_alarm_status_file():
    global ALARM_STATUS
    file = 'alarm_status.txt'
    current_value = read_alarm_status_file()
    if current_value == '1':
        new_value = '0'
    else:
        new_value = '1'

    with open(file, 'w') as f:
        f.write(str(new_value))
    ALARM_STATUS = new_value


@app.route('/', methods=['GET'])
def homepage():
    pass


@app.route('/door', methods=['GET'])
def get_door_data():
    data = truple_to_list(read_sql('device_type = \'door\''))
    return jsonify({'data': data})


@app.route('/movement', methods=['GET'])
def get_movement_data():
    data = truple_to_list(read_sql('device_type = \'movement\''))
    return jsonify({'data': data})


@app.route('/camera', methods=['GET'])
def get_camera_data():
    data = truple_to_list(read_sql('device_type = \'camera\''))
    return jsonify({'data': data})


@app.route('/lights', methods=['GET'])
def get_lights_data():
    pass


@app.route('/alarm_status', methods=['GET'])
def get_alarm_status():
    return jsonify({'alarm status': ALARM_STATUS})


@app.route('/alarm_toggle', methods=['GET'])
def set_alarm_status():
    write_alarm_status_file()
    return jsonify({'alarm status': ALARM_STATUS})


write_sql({'t': 'ab', 'device_id': 'cd', 'device_type': 'door'})
write_sql({'t': 'c', 'device_id': 'd', 'device_type': 'movement'})
write_sql({'t': 'x', 'device_id': 'y', 'device_type': 'camera'})

ALARM_STATUS = read_alarm_status_file()

app.run()
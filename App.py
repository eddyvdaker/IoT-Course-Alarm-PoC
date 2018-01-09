from flask import Flask, jsonify, render_template, redirect
import sqlite3
import os
import time

app = Flask(__name__)
db = 'database.sqlite3'


"""
HELPER FUNCTIONS
"""


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


def generate_vars():
    page_vars = {'alarm_status': bool_to_on_off(ALARM_STATUS),
                 'lights_status': bool_to_on_off(LIGHTS_STATUS)}
    return page_vars


"""
FLASK FUNCTIONS
"""


@app.route('/', methods=['GET'])
def homepage():
    page_vars = generate_vars()
    return render_template('homepage.html', page_vars=page_vars)


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


@app.route('/lights_toggle', methods=['GET'])
def set_lights_status():
    global LIGHTS_STATUS
    LIGHTS_STATUS = not LIGHTS_STATUS
    write_status_file('lights_status.txt', LIGHTS_STATUS)
    return redirect('/')


@app.route('/alarm_toggle', methods=['GET'])
def set_alarm_status():
    global ALARM_STATUS
    ALARM_STATUS = not ALARM_STATUS
    write_status_file('alarm_status.txt', ALARM_STATUS)
    return redirect('/')


if __name__ == '__main__':
    create_db()

    # Create some test data
    write_sql({'t': time.time(), 'device_id': 'd1', 'device_type': 'door'})
    write_sql({'t': time.time(), 'device_id': 'm3', 'device_type': 'movement'})
    write_sql({'t': time.time(), 'device_id': 'c5', 'device_type': 'camera'})
    write_sql({'t': time.time(), 'device_id': 'd1', 'device_type': 'door'})
    write_sql({'t': time.time(), 'device_id': 'm3', 'device_type': 'movement'})
    write_sql({'t': time.time(), 'device_id': 'c4', 'device_type': 'camera'})
    write_sql({'t': time.time(), 'device_id': 'd7', 'device_type': 'door'})
    write_sql({'t': time.time(), 'device_id': 'm2', 'device_type': 'movement'})
    write_sql({'t': time.time(), 'device_id': 'c1', 'device_type': 'camera'})

    ALARM_STATUS = read_status_file('alarm_status.txt')
    LIGHTS_STATUS = read_status_file('lights_status.txt')

    app.run()

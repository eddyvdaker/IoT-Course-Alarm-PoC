from flask import Flask, jsonify, render_template, redirect
from helper_functions import *
from sensors import *

app = Flask(__name__)


@app.route('/', methods=['GET'])
def homepage():
    page_vars = generate_vars(ALARM_STATUS, LIGHTS_STATUS)
    return render_template('homepage.html', page_vars=page_vars)


@app.route('/door', methods=['GET'])
def get_door_data():
    data = truple_to_list(read_sql('device_type = \'door\''))
    return jsonify({'data': data})


@app.route('/movement', methods=['GET'])
def get_movement_data():
    data = truple_to_list(read_sql('device_type = \'movement\''))
    return jsonify({'data': data})

192.168.55.51 - - [10/Jan/2018 01:20:39] "GET /alarm_toggle HTTP/1.1" 302 -
192.168.55.51 - - [10/Jan/2018 01:20:39] "GET / HTTP/1.1" 200 -

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

    start_button_checking()

    ALARM_STATUS = read_status_file('alarm_status.txt')
    LIGHTS_STATUS = read_status_file('lights_status.txt')

    app.run(host='0.0.0.0')

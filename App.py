from flask import Flask, jsonify, render_template, redirect
from helper_functions import *
from sensors import *

app = Flask(__name__)


# Helper function to load all vars into a dictionary
# created to keep homepage() clean.
def generate_vars():
    page_vars = {'alarm_status': bool_to_on_off(ALARM_STATUS),
                 'lights_status': bool_to_on_off(LIGHTS_STATUS)}
    return page_vars


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
    create_test_data()

    try:
        start_button_checking()
    except RuntimeError:
        # Skip if not ran on Pi
        pass

    ALARM_STATUS = read_status_file('alarm_status.txt')
    LIGHTS_STATUS = read_status_file('lights_status.txt')

    app.run(host='0.0.0.0')

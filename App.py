from flask import Flask, jsonify, render_template, redirect, request
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


@app.route('/post_camera', methods=['GET'])
def set_camera_entry():
    """
    task = {
        't': time.time(),
        'device_id': request.json['id'],
        'device_type': 'camera'
    }
    if ALARM_STATUS == 'True':
        write_sql(task)
    return jsonify({'task': task}), 201
    """
    return request.args.get('id'), 201


if __name__ == '__main__':
    create_db()

    start_button_checking()

    ALARM_STATUS = read_status_file('alarm_status.txt')
    LIGHTS_STATUS = read_status_file('lights_status.txt')

    app.run(host='0.0.0.0')

from helper_functions import *
import time
import RPi.GPIO as GPIO
import urllib.request
import threading

GPIO.setmode(GPIO.BCM)

# Lights button
GPIO.setup(3, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# Lights led
GPIO.setup(17, GPIO.OUT)

# Setup alarm led
GPIO.setup(18, GPIO.OUT)

# Door buttons
GPIO.setup(22, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(23, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(24, GPIO.IN, pull_up_down=GPIO.PUD_UP)


# Check if and which door button is pressed (door opened)
def check_doors():
    previous_state = [True, True, True]
    while True:
        input_states = [GPIO.input(22), GPIO.input(23), GPIO.input(24)]
        for i, state in enumerate(input_states):
            if state == False:
                if previous_state[i] == True:
                    if read_status_file('alarm_status.txt') == 'True':
                        write_sql({'t': time.time(),
                                   'device_id': f'd{i}',
                                   'device_type': 'door'})
                        time.sleep(0.2)
                previous_state[i] = False
            else:
                previous_state[i] = True


# Check if the lights button is being pressed
def check_lights():
    while True:
        if GPIO.input(3) == False:
            ip = read_status_file('ip_addr.txt')
            urllib.request.urlopen(f'http://{ip}:5000/lights_toggle')
            time.sleep(0.2)


# If lights status is True turn on lights
def turn_on_off_lights():
    while True:
        if read_status_file('lights_status.txt') == 'True':
            GPIO.output(18, True)
            time.sleep(0.5)
        else:
            GPIO.output(18, False)
            time.sleep(0.5)


def start_button_checking():
    threading.Thread(target=check_doors, args=[]).start()
    threading.Thread(target=check_lights, args=[]).start()
    threading.Thread(target=turn_on_off_lights, args=[]).start()

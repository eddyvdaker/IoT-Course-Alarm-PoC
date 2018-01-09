from helper_functions import *
import time
import RPi.GPIO as GPIO
import urllib.request
import threading

GPIO.setmode(GPIO.BCM)

# Lights button
GPIO.setup(17, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# Door buttons
GPIO.setup(24, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(23, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(22, GPIO.IN, pull_up_down=GPIO.PUD_UP)


def check_doors():
    input_states = [GPIO.input(24), GPIO.input(23), GPIO.input(22)]

    while True:
        for i, state in enumerate(input_states):
            if state == False:
                write_sql({{'t': time.time(),
                            'device_id': f'd{i}',
                            'device_type': 'door'}})
                time.sleep(0.2)


def check_lights():
    while True:
        if GPIO.input(17) == False:
            urllib.request.urlopen('http://10.0.0.58:5000/lights_toggle')
            time.sleep(0.2)


def start_button_checking():
    threading.Thread(target=check_doors, args=[]).start()
    threading.Thread(target=check_lights, args=[]).start()

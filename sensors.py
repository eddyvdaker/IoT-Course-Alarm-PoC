from helper_functions import *
import time
import RPi.GPIO as GPIO
import urllib.request
import threading

GPIO.setmode(GPIO.BCM)

# Lights buttons
lb1 = 4
lb2 = 14
lights_buttons = [lb1, lb2]
GPIO.setup(lb1, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(lb2, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# Lights led
ll1 = 17
ll2 = 18
lights_leds = [ll1, ll2]
GPIO.setup(ll1, GPIO.OUT)
GPIO.setup(ll2, GPIO.OUT)

# Setup alarm led
al1 = 3
alarm_leds = [al1]
GPIO.setup(al1, GPIO.OUT)

# Door buttons
db1 = 22
db2 = 23
db3 = 24
door_buttons = [db1, db2, db3]
GPIO.setup(db1, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(db2, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(db3, GPIO.IN, pull_up_down=GPIO.PUD_UP)


# Check if and which door button is pressed (door opened)
def check_doors():
    previous_state = [True, True, True]
    while True:
        for i, state in enumerate(door_buttons):
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
        for i, state in enumerate(lights_buttons):
            if state == False:
                ip = read_status_file('ip_addr.txt')
                urllib.request.urlopen(f'http://{ip}:5000/lights_toggle?nr={i}')
                time.sleep(0.2)


# If lights status is True turn on lights
def turn_on_off_lights():
    while True:
        status = read_status_file(f'lights_{i}_status.txt')
        for i, state in enumerate(lights_leds):
            if status == 'True':
                GPIO.output(state, True)
                time.sleep(0.5)
            else:
                GPIO.output(state, False)
                time.sleep(0.5)


def start_button_checking():
    threading.Thread(target=check_doors, args=[]).start()
    threading.Thread(target=check_lights, args=[]).start()
    threading.Thread(target=turn_on_off_lights, args=[]).start()


def get_lights_number():
    return len(lights_buttons)


read_status_file('ip_addr.txt')

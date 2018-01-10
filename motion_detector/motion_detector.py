"""
This part of the program is supposed to be ran on the pc with the camera
installed
"""

import cv2
import imutils
import datetime
import time
import urllib.request
import subprocess


if __name__ == '__main__':
    server_ip = '10.0.0.58:5000'
    camera = 1
    camera_id = f'c{camera}'
    send_to_server = True

    camera = cv2.VideoCapture(camera)
    first_frame = None
    min_contour_area = 20

    previous_movement_detected = False
    previous_send_time = time.time()
    screenshot_timeout = 2
    time_format = "%d-%B-%Y-%H:%M:%S"
    path = '/home/eddy/Projects/IoT-Course-Alarm-PoC' \
           '/motion_detector/screenshots/'

    cv2.namedWindow('Security Feed', cv2.WINDOW_NORMAL)
    cv2.namedWindow('Threshold', cv2.WINDOW_NORMAL)
    cv2.namedWindow('Frame Delta', cv2.WINDOW_NORMAL)

    # Loop over frames of video
    while True:
        movement_detected = False
        (grabbed, frame) = camera.read()

        # Resize, grayscale and blur frame
        frame = imutils.resize(frame, width=500)
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        gray = cv2.GaussianBlur(gray, (21, 21), 0)

        # If first frame is None, set current frame to first frame
        if first_frame is None:
            first_frame = gray

        # Calculate absolute difference between current frame nad first frame
        frame_delta = cv2.absdiff(first_frame, gray)
        thresh = cv2.threshold(frame_delta, 25, 255, cv2.THRESH_BINARY)[1]
        thresh = cv2.dilate(thresh, None, iterations=2)

        image, contours, hierarchy = cv2.findContours(thresh.copy(),
                                                      cv2.RETR_EXTERNAL,
                                                      cv2.CHAIN_APPROX_SIMPLE)

        # Loop over contours
        for c in contours:
            # If area is to small, ignore it
            if cv2.contourArea(c) > min_contour_area:
                (x, y, w, h) = cv2.boundingRect(c)
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
                movement_detected = True

        # Draw timestamp
        cv2.putText(frame, datetime.datetime.now().strftime(time_format),
                    (10, frame.shape[0] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5,
                    (0, 0, 255), 1)
        cv2.putText(frame, f'Motion Detected: {movement_detected}', (10, 20),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 1)

        cv2.imshow('Security Feed', frame)
        cv2.imshow('Threshold', thresh)
        cv2.imshow('Frame Delta', frame_delta)

        if movement_detected:
            file = f'{int(time.time())}.png'
            if time.time() - previous_send_time > screenshot_timeout:
                cv2.imwrite(f'{path}{file}', frame)
                previous_send_time = time.time()

            if not previous_movement_detected and send_to_server:
                url = f'http://{server_ip}/post_camera?id={camera_id}'
                urllib.request.urlopen(url)
                copy_cmd = f'scp {path}{file} pi@{server_ip}:/home/pi/' \
                           f'IoT-Course-Alarm-PoC/static/{file}'
                process = subprocess.Popen(copy_cmd.split(),
                                           stdout=subprocess.PIPE,
                                           stderr=subprocess.PIPE)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

        first_frame = gray
        previous_movement_detected = movement_detected

camera.release()
cv2.destroyAllWindows()

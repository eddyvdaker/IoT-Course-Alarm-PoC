"""
This part of the program is supposed to be ran on the pc with the camera
installed
"""

import cv2
import imutils
import datetime
import time


if __name__ == '__main__':
    camera = cv2.VideoCapture(1)
    first_frame = None
    min_contour_area = 20
    previous_send_time = time.time()
    screenshot_timeout = 2
    time_format = "%d-%B-%Y-%H:%M:%S"
    path = './screenshots/'

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

        if movement_detected == True:
            if time.time() - previous_send_time > screenshot_timeout:
                cv2.imwrite(f'{path}'
                            f'{datetime.datetime.now().strftime(time_format)}'
                            f'.png',
                            frame)
                previous_send_time = time.time()

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

        first_frame = gray

camera.release()
cv2.destroyAllWindows()

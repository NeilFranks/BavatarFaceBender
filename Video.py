import numpy as np
import cv2
import math
import socket
import time

from Audio import Audio


class Video(object):
    def __init__(self):

        self.previous_frame = None
        self.took_prev = False

        # SETTINGS
        self.blend_on = False  # whether or not to blend frame to frame
        self.BLEND = 0.6  # how much to blend frame to frame
        self.BLUR_HOR = 1  # how much to blur the pixels together
        self.BLUR_VERT = 1  # how much to blur the pixels together

    def run(self):
        audio = Audio(2)
        audio.start()

        # Open Camera
        try:
            default = 0  # Try Changing it to 1 if webcam not found
            capture = cv2.VideoCapture(default)
        except:
            print("No Camera Source Found!")

        while capture.isOpened():

            # Capture frames from the camera
            _, frame = capture.read()
            ty = np.zeros(frame.shape, np.uint8)

            # blend frame-to-frame (motion blur?)
            blended_frame = self.blend_frames(frame)

            # Apply Gaussian blur
            blur = cv2.GaussianBlur(blended_frame, (1, 1), 0)

            # Change color-space from BGR -> HSV
            rgb = cv2.cvtColor(blur, cv2.COLOR_BGR2RGB)

            vol = audio.get_volume()

            self.drawPolygons(
                rgb,
                ty,
                np.array([0, 0, 0]),
                np.array([80, 80, 80]),
                (0, vol*127, vol*255),
                5
            )

            cv2.imshow("JUICE", ty)
            # cv2.imshow("shsrh", blended_frame)

            # Close the camera if 'q' is pressed
            if cv2.waitKey(1) == ord("q"):
                audio.stop = True
                audio.join()
                break

        capture.release()
        cv2.destroyAllWindows()

    def drawPolygons(self, image, canvas, low_thresh, hi_thresh, color, epsilon):
        # mask = cv2.inRange(rgb, np.array([0,0,0]), np.array([130, 90, 90]))
        # mask = cv2.inRange(rgb, np.array([0,0,0]), np.array([45, 30, 30]))
        mask = cv2.inRange(image, low_thresh, hi_thresh)

        # Kernel for morphological transformation
        kernel = np.ones((5, 5))

        # Apply morphological transformations to filter out the background noise
        dilation = cv2.dilate(mask, kernel, iterations=1)
        erosion = cv2.erode(dilation, kernel, iterations=1)

        # Apply Gaussian Blur and Threshold
        filtered = cv2.GaussianBlur(
            erosion, (self.BLUR_HOR, self.BLUR_VERT), 0)
        _, thresh = cv2.threshold(filtered, 255, 255, 255)

        # Draw masks
        _, contours, _ = cv2.findContours(
            thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE
        )

        for contour in contours:
            poly = cv2.approxPolyDP(contour, epsilon, True)
            cv2.drawContours(canvas, [poly], 0, color, cv2.FILLED)

    def blend_frames(self, frame):
        blended_frame = frame
        if self.blend_on:
            if self.took_prev:
                blended_frame = cv2.addWeighted(
                    self.previous_frame, self.BLEND, frame, 1 - self.BLEND, 0
                )
            else:
                self.took_prev = True

            self.previous_frame = blended_frame
        return blended_frame


Video().run()

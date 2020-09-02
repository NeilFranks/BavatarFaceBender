import cv2
import numpy as np
import threading


class PolygonEffect(object):
    def __init__(self, low_thresh, high_thresh, color, epsilon):
        self.enabled = True
        self.low_thresh = low_thresh  # low end of what colors will make up the contour
        self.high_thresh = high_thresh  # high end of what colors will make up the contour
        self.color = color  # the color the contour will be filled with
        self.epsilon = epsilon  # epsilon is like length of the lines

    def disable(self):
        self.enabled = False

    def draw(self, image, canvas, blur_hor, blur_vert):
        mask = cv2.inRange(
            image,
            np.array(self.get_low_thresh()),
            np.array(self.get_high_thresh())
        )

        # Kernel for morphological transformation
        kernel = np.ones((5, 5))

        # Apply morphological transformations to filter out the background noise
        dilation = cv2.dilate(mask, kernel, iterations=1)
        erosion = cv2.erode(dilation, kernel, iterations=1)

        # Apply Gaussian Blur and Threshold
        filtered = cv2.GaussianBlur(
            erosion, (blur_hor, blur_vert), 0)
        _, thresh = cv2.threshold(filtered, 255, 255, 255)

        # Draw masks
        _, contours, _ = cv2.findContours(
            thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE
        )

        for contour in contours:
            poly = cv2.approxPolyDP(contour, self.get_epsilon(), True)
            cv2.drawContours(canvas, [poly], 0, self.get_color(), cv2.FILLED)

    def fluctate(self):
        t1 = threading.Thread(target=self.fluc_low_thresh)
        t2 = threading.Thread(target=self.fluc_high_thresh)
        t3 = threading.Thread(target=self.fluc_color)
        t4 = threading.Thread(target=self.fluc_epsilon)

        t1.start()
        t2.start()
        t3.start()
        t4.start()
        t1.join()
        t2.join()
        t3.join()
        t4.join()

    def fluc_low_thresh(self):
        self.low_thresh[0].fluctuate()
        self.low_thresh[1].fluctuate()
        self.low_thresh[2].fluctuate()

    def fluc_high_thresh(self):
        self.high_thresh[0].fluctuate()
        self.high_thresh[1].fluctuate()
        self.high_thresh[2].fluctuate()

    def fluc_color(self):
        self.color[0].fluctuate()
        self.color[1].fluctuate()
        self.color[2].fluctuate()

    def fluc_epsilon(self):
        self.epsilon.fluctuate()

    def get_low_thresh(self):
        return [
            self.low_thresh[0].get(),
            self.low_thresh[1].get(),
            self.low_thresh[2].get()
        ]

    def get_high_thresh(self):
        return [
            self.high_thresh[0].get(),
            self.high_thresh[1].get(),
            self.high_thresh[2].get()
        ]

    def get_color(self):
        return (
            self.color[0].get(),
            self.color[1].get(),
            self.color[2].get(),
        )

    def get_epsilon(self):
        return self.epsilon.get()

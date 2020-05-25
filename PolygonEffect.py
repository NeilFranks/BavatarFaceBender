import cv2
import numpy as np
import threading

from FluctuatingValue import FluctuatingValue


class PolygonEffect(object):
    def __init__(self, low_thresh, hi_thresh, color, epsilon):
        self.enabled = True
        self.low_thresh = low_thresh
        self.hi_thresh = hi_thresh
        self.color = color
        self.epsilon = epsilon

    def disable(self):
        self.enabled = False

    def draw(self, image, canvas, blur_hor, blur_vert):
        mask = cv2.inRange(
            image,
            np.array(self.get_low_thresh()),
            np.array(self.get_hi_thresh())
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

    def fluctate(self, fraction):
        t1 = threading.Thread(target=self.fluc_low_thresh, args=(fraction,))
        t2 = threading.Thread(target=self.fluc_hi_thresh, args=(fraction,))
        t3 = threading.Thread(target=self.fluc_color, args=(fraction,))
        t4 = threading.Thread(target=self.fluc_epsilon, args=(fraction,))

        t1.start()
        t2.start()
        t3.start()
        t4.start()
        t1.join()
        t2.join()
        t3.join()
        t4.join()

    def fluc_low_thresh(self, fraction):
        self.low_thresh[0].fluctuate(fraction)
        self.low_thresh[1].fluctuate(fraction)
        self.low_thresh[2].fluctuate(fraction)

    def fluc_hi_thresh(self, fraction):
        self.hi_thresh[0].fluctuate(fraction)
        self.hi_thresh[1].fluctuate(fraction)
        self.hi_thresh[2].fluctuate(fraction)

    def fluc_color(self, fraction):
        self.color[0].fluctuate(fraction)
        self.color[1].fluctuate(fraction)
        self.color[2].fluctuate(fraction)

    def fluc_epsilon(self, fraction):
        self.epsilon.fluctuate(fraction)

    def get_low_thresh(self):
        return [
            self.low_thresh[0].get(),
            self.low_thresh[1].get(),
            self.low_thresh[2].get()
        ]

    def get_hi_thresh(self):
        return [
            self.hi_thresh[0].get(),
            self.hi_thresh[1].get(),
            self.hi_thresh[2].get()
        ]

    def get_color(self):
        return (
            self.color[0].get(),
            self.color[1].get(),
            self.color[2].get(),
        )

    def get_epsilon(self):
        return self.epsilon.get()

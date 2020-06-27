import numpy as np
import cv2
import threading

from Audio import Audio
from FluctuatingValue import FluctuatingValue
from PolygonEffect import PolygonEffect


class Video(threading.Thread):
    def __init__(self, selected_audio_device):
        threading.Thread.__init__(self)

        self.previous_frame = None
        self.took_prev = False

        # SETTINGS
        self.blend_on = False  # whether or not to blend frame to frame
        self.BLEND = 0.6  # how much to blend frame to frame
        self.BLUR_HOR = 1  # how much to blur the pixels together
        self.BLUR_VERT = 1  # how much to blur the pixels together

        # STUFF TO USE
        self.selected_audio_device = selected_audio_device
        self.audio = Audio(self.selected_audio_device)
        self.audio.start()
        self.stop = False  # set this to true to end the Video stream

        self.effects = []

    def run(self):
        self.effects.append(
            PolygonEffect(
                low_thresh=[
                    FluctuatingValue(0, 0, 220, True, lambda frac,
                                     whole: frac*whole),
                    FluctuatingValue(0, 0, 220, True, lambda frac,
                                     whole: frac*whole),
                    FluctuatingValue(0, 0, 220, True, lambda frac,
                                     whole: frac*whole),
                ],
                hi_thresh=[
                    FluctuatingValue(80, 80, 255, True, lambda frac,
                                     whole: frac*whole),
                    FluctuatingValue(80, 80, 255, True, lambda frac,
                                     whole: frac*whole),
                    FluctuatingValue(80, 80, 255, True, lambda frac,
                                     whole: frac*whole),
                ],
                color=(
                    FluctuatingValue(50, 0, 255, True,
                                     lambda frac, whole: frac*whole),
                    FluctuatingValue(50, 0, 255, True,
                                     lambda frac, whole: frac*whole),
                    FluctuatingValue(50, 0, 255, True,
                                     lambda frac, whole: frac*whole),
                ),
                epsilon=FluctuatingValue(5, 1, 11, True,
                                         lambda frac, whole: frac*whole)
            )
        )

        # Open Camera
        try:
            default = 0  # Try Changing it to 1 if webcam not found
            capture = cv2.VideoCapture(default)
        except Exception as e:
            print("No Camera Source Found!")
            print(e)

        while capture.isOpened():
            # Capture frames from the camera
            _, frame = capture.read()
            canvas = np.zeros(frame.shape, np.uint8)

            # blend frame-to-frame (motion blur?)
            blended_frame = self.blend_frames(frame)

            # draw stuff
            self.draw(blended_frame, canvas)
            cv2.imshow('wow', canvas)

            # Close the camera if 'q' is pressed
            if self.stop or cv2.waitKey(1) == ord("q"):
            # if self.stop:
                break

        self.audio.stop = True
        self.audio.join()
        capture.release()
        cv2.destroyAllWindows()

    def draw(self, image, canvas):
        vol = self.audio.get_volume()

        for effect in self.effects:
            effect.fluctate(vol)
            effect.draw(image, canvas, self.BLUR_HOR, self.BLUR_VERT)

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


# Video(0).run()

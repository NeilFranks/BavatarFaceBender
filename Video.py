import numpy as np
import cv2
import threading

from Audio import Audio
import utils


class Video(threading.Thread):
    def __init__(self, selected_audio_device):
        threading.Thread.__init__(self)

        self.previous_frame = None
        self.took_prev = False

        # SETTINGS
        self.blend_on = False  # whether or not to blend frame to frame
        self.BLEND = 0.8  # how much to blend frame to frame
        self.BLUR_HOR = 1  # how much to blur the pixels together
        self.BLUR_VERT = 1  # how much to blur the pixels together
        self.SHOW_REAL_PICTURE = False  # if true, just show real webcam feed

        # STUFF TO USE
        self.selected_audio_device = selected_audio_device
        self.audio = Audio(self.selected_audio_device)
        self.audio.start()
        self.stop = False  # set this to true to end the Video stream

    def run(self):
        # Open Camera
        try:
            default = 0  # Try Changing it to 1 if webcam not found
            capture = cv2.VideoCapture(default)
            capture.set(cv2.CAP_PROP_EXPOSURE, -1)  # disable auto-exposure. under expose in order to get high shutter speed
        except Exception as e:
            print("No Camera Source Found!")
            print(e)

        while capture.isOpened():
            cv2.waitKey(1)

            # Capture frames from the camera
            _, frame = capture.read()
            canvas = np.zeros(frame.shape, np.uint8)

            # blend frame-to-frame (motion blur?)
            blended_frame = self.blend_frames(frame)

            # draw stuff
            if self.SHOW_REAL_PICTURE:
                cv2.imshow('B A V A T A R', blended_frame)
            else:
                self.draw(blended_frame, canvas)
                cv2.imshow('B A V A T A R', canvas)

            if self.stop:
                break

        self.audio.stop = True
        self.audio.join()
        capture.release()
        cv2.destroyAllWindoFws()

    def draw(self, image, canvas):
        try:
            vals = utils.effects.values()
            for effect in vals:
                effect.fluctate()
                effect.draw(image, canvas, self.BLUR_HOR, self.BLUR_VERT)
        except Exception as e:
            # lol, dict probably needs to be threadsafe. check the exception
            print(e)

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

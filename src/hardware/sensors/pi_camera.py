from hardware.sensors.camera import Camera
from picamera import PiCamera
from picamera.array import PiRGBArray
from picamera.exc import PiCameraMMALError
import cv2

class PiCameraWrapper(Camera):

    def __init__(self, resolution=(128,128), rotation=180):
        self.rotation = rotation
        self.resolution = resolution
        self.setup()

    def setup(self, retries=0):
        try:
            self.dev = PiCamera(resolution=self.resolution)
            self.dev.rotation = self.rotation
            print("PiCamera inizializzata.")
        except PiCameraMMALError:
            if retries < 5:
                self.dev.close()
                self.setup(retries + 1)
            else:
                print("Non riesco ad inizializzare la PiCamera.")


    def get_image(self, gray=False):
        if self.dev is None:
            self.setup()
        raw_capture = PiRGBArray(self.dev)
        self.dev.capture(raw_capture, format="bgr")
        frame = raw_capture.array
        if gray:
            cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        return frame

    def release(self):
        if self.dev is not None:
            self.dev.close()
            self.dev = None
            print("PiCamera rilasciata")

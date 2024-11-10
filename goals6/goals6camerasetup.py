"""goals6camerasetup.py

   Tune the camera parameters.
"""

# Import OpenCV
import cv2
import numpy as np

# Set up video capture device (camera).  Note 0 is the camera number.
# If things don't work, you may need to use 1 or 2?
camera = cv2.VideoCapture(0, cv2.CAP_V4L2)
if not camera.isOpened():
    raise Exception("Could not open video device: Maybe change the cam number?")

# Change the frame size and rate.  Note only combinations of
# widthxheight and rate are allowed.  In particular, 1920x1080 only
# reads at 5 FPS.  To get 30FPS we downsize to 640x480.
camera.set(cv2.CAP_PROP_FRAME_WIDTH,  640)
camera.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
camera.set(cv2.CAP_PROP_FPS,           30)

# Change the camera settings.
exposure = 250
wb = 4000
focus = 0

#camera.set(cv2.CAP_PROP_AUTO_EXPOSURE, 3)       # Auto mode
camera.set(cv2.CAP_PROP_AUTO_EXPOSURE, 1)       # Manual mode
#camera.set(cv2.CAP_PROP_EXPOSURE, exposure)     # 3 - 2047, default 250

#camera.set(cv2.CAP_PROP_AUTO_WB, 1.0)           # Enable auto white balance
camera.set(cv2.CAP_PROP_AUTO_WB, 0.0)           # Disable auto white balance
#camera.set(cv2.CAP_PROP_WB_TEMPERATURE, wb)     # 2000 - 6500, default 4000

#camera.set(cv2.CAP_PROP_AUTOFOCUS, 1)           # Enable autofocus
camera.set(cv2.CAP_PROP_AUTOFOCUS, 0)           # Disable autofocus
#camera.set(cv2.CAP_PROP_FOCUS, focus)           # 0 - 250, step 5, default 0

#camera.set(cv2.CAP_PROP_BRIGHTNESS, 128)        # 0 - 255, default 128
#camera.set(cv2.CAP_PROP_CONTRAST,   128)        # 0 - 255, default 128
#camera.set(cv2.CAP_PROP_SATURATION, 128)        # 0 - 255, default 128


# Trackbar object
class OnOffBar():
    def __init__(self, winname, barname):
        # Create the on/off bar:
        cv2.createTrackbar(barname, winname, 0, 1, self.CB)

    def CB(self, track):
        if track:
            print("Turning ON automatic controls - " +
                  "and resetting brightness/contrast/saturation")

            # Turn on Auto
            camera.set(cv2.CAP_PROP_AUTO_EXPOSURE, 3)
            camera.set(cv2.CAP_PROP_AUTO_WB, 1)
            camera.set(cv2.CAP_PROP_AUTOFOCUS, 1)

            # Also reset brightness/contrast/saturation.
            camera.set(cv2.CAP_PROP_BRIGHTNESS, 128)
            camera.set(cv2.CAP_PROP_CONTRAST,   128)
            camera.set(cv2.CAP_PROP_SATURATION, 128)

        else:
            print("Turning OFF automatic controls - " +
                  "resetting the sliders!")

            # Turn off Auto
            camera.set(cv2.CAP_PROP_AUTO_EXPOSURE, 1)
            camera.set(cv2.CAP_PROP_AUTO_WB, 0)
            camera.set(cv2.CAP_PROP_AUTOFOCUS, 0)

            # Reset the trackbars!
            for track in tracks:
                track.reset()


class TrackBar():
    def __init__(self, winname, barname, capprop, minval, maxval, step, value):
        # Store the parameters.
        self.winname = winname
        self.barname = barname
        self.capprop = capprop
        self.minval  = minval
        self.maxval  = maxval
        self.step    = step

        # Create the trackbar.
        limit = int((maxval - minval) / step)
        track = int((value  - minval) / step)
        cv2.createTrackbar(barname, winname, track, limit, self.CB)

        # And immediate reset to the current value.
        self.reset()

    def set(self, value):
        # Update the property
        print("Setting %s to %d" % (self.barname, value))
        camera.set(self.capprop, value)

        # Update the trackbar.
        track = int((value  - self.minval) / self.step)
        cv2.setTrackbarPos(self.barname, self.winname, track)

    def reset(self):
        # Set to the current value.
        self.set(camera.get(self.capprop))
        
    def CB(self, track):
        # Set to the new value.
        self.set(self.minval + track * self.step)

# Create a controls window with the trackbars.
cv2.namedWindow('Controls')
cv2.imshow('Controls', np.zeros((1, 380, 3), np.uint8))

OnOffBar('Controls', 'Automatic')
tracks = [
    TrackBar('Controls', 'Exposure',   cv2.CAP_PROP_EXPOSURE,          3, 2047, 1,  250),
    TrackBar('Controls', 'WBalance',   cv2.CAP_PROP_WB_TEMPERATURE, 2000, 6500, 1, 4000),
    TrackBar('Controls', 'Focus',      cv2.CAP_PROP_FOCUS,             0,  250, 5,    0),
    TrackBar('Controls', 'Brightness', cv2.CAP_PROP_BRIGHTNESS,        0,  255, 1,  128),
    TrackBar('Controls', 'Contrast',   cv2.CAP_PROP_CONTRAST,          0,  255, 1,  128),
    TrackBar('Controls', 'Saturation', cv2.CAP_PROP_SATURATION,        0,  255, 1,  128),
    ]


# Keep scanning, until 'q' hit IN IMAGE WINDOW.
while True:
    # Grab an image from the camera.  Often called a frame (part of sequence).
    ret, frame = camera.read()

    # Show the image with the given title.  Note this won't actually
    # appear (draw on screen) until the waitKey(1) below.
    cv2.imshow('Camera Image', frame)

    # Check for a key press IN THE IMAGE WINDOW: waitKey(0) blocks
    # indefinitely, waitkey(1) blocks for at most 1ms.  If 'q' break.
    # This also flushes the windows and causes it to actually appear.
    if (cv2.waitKey(1) & 0xFF) == ord('q'):
        break

# Close everything up.
camera.release()
cv2.destroyAllWindows()

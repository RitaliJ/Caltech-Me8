"""goals6hsvtune_red.py

   Tune the HSV lower/upper bounds.

   This uses the "Red-Blue Swap" RGB2HSV conversion.
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
camera.set(cv2.CAP_PROP_EXPOSURE, exposure)     # 3 - 2047, default 250

#camera.set(cv2.CAP_PROP_AUTO_WB, 1.0)           # Enable auto white balance
camera.set(cv2.CAP_PROP_AUTO_WB, 0.0)           # Disable auto white balance
camera.set(cv2.CAP_PROP_WB_TEMPERATURE, wb)     # 2000 - 6500, default 4000

#camera.set(cv2.CAP_PROP_AUTOFOCUS, 1)           # Enable autofocus
camera.set(cv2.CAP_PROP_AUTOFOCUS, 0)           # Disable autofocus
camera.set(cv2.CAP_PROP_FOCUS, focus)           # 0 - 250, step 5, default 0

camera.set(cv2.CAP_PROP_BRIGHTNESS, 128)        # 0 - 255, default 128
camera.set(cv2.CAP_PROP_CONTRAST,   128)        # 0 - 255, default 128
camera.set(cv2.CAP_PROP_SATURATION, 128)        # 0 - 255, default 128

# Pick some colors.  Note OpenCV uses BGR color codes by default.
blue  = (255,  0,  0)
green = (  0,255,  0)
red   = (  0,  0,255)
white = (255,255,255)


# Thresholds in Hmin/max, Smin/max, Vmin/max
hsvThreshold = np.array([[0, 179], [0, 255], [0, 255]])

# Trackbar object
class TrackBar():
    def __init__(self, winname, barname, channel, element, limit):
        # Store the parameters.
        self.winname = winname
        self.barname = barname
        self.channel = channel
        self.element = element
        # Create the trackbar.
        cv2.createTrackbar(barname, winname,
                           hsvThreshold[channel,element], limit, self.CB)

    def CB(self, val):
        # Make sure the threshold doesn't pass the opposite limit.
        if self.element == 0:  val = min(val, hsvThreshold[self.channel,1])
        else:                  val = max(val, hsvThreshold[self.channel,0])
        # Update the threshold and the tracker position.
        hsvThreshold[self.channel,self.element] = val
        cv2.setTrackbarPos(self.barname, self.winname, val)

# Create a controls window with the trackbars.
cv2.namedWindow('Controls')
cv2.imshow('Controls', np.zeros((1, 500, 3), np.uint8))

TrackBar('Controls', 'Lower H', 0, 0, 179)
TrackBar('Controls', 'Upper H', 0, 1, 179)
TrackBar('Controls', 'Lower S', 1, 0, 255)
TrackBar('Controls', 'Upper S', 1, 1, 255)
TrackBar('Controls', 'Lower V', 2, 0, 255)
TrackBar('Controls', 'Upper V', 2, 1, 255)


# Keep scanning, until 'q' hit IN IMAGE WINDOW.
while True:
    # Grab an image from the camera.  Often called a frame (part of sequence).
    ret, frame = camera.read()

    # Convert to HSV color space
    hsv = cv2.cvtColor(frame, cv2.COLOR_RGB2HSV)

    # Grab the image shape, determine the center pixel.
    (H, W, D) = frame.shape
    xc = W//2
    yc = H//2

    # Report the center HSV values.
    print(f"HSV(x={xc},y={yc}): {tuple(hsv[yc, xc])}")

    # Draw the center lines on the regular image.
    cv2.line(frame, (xc,0), (xc,H-1), white, 1)
    cv2.line(frame, (0,yc), (W-1,yc), white, 1)

    # Threshold in Hmin/max, Smin/max, Vmin/max
    binary = cv2.inRange(hsv, hsvThreshold[:,0], hsvThreshold[:,1])

    # Show the image with the given title.  Note this won't actually
    # appear (draw on screen) until the waitKey(1) below.
    cv2.imshow('Processed Image', frame)
    cv2.imshow('Binary Image',    binary)

    # Check for a key press IN THE IMAGE WINDOW: waitKey(0) blocks
    # indefinitely, waitkey(1) blocks for at most 1ms.  If 'q' break.
    # This also flushes the windows and causes it to actually appear.
    if (cv2.waitKey(1) & 0xFF) == ord('q'):
        break

# Close everything up.
camera.release()
cv2.destroyAllWindows()

"""goals6simple.py

   Read the camera image in preparation for some image manipulation
   and object detection.

"""

# Import OpenCV
import cv2

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


# Keep scanning, until 'q' hit IN IMAGE WINDOW.
count = 0
while True:
    # Grab an image from the camera.  Often called a frame (part of sequence).
    ret, frame = camera.read()
    count += 1

    # Grab and report the image shape.
    (H, W, D) = frame.shape
    #print(f"Frame #{count:3} is {W}x{H} pixels x{D} color channels.")

    # Convert the BGR image to RGB or HSV.
    # hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)      # For other objects
    # hsv = cv2.cvtColor(frame, cv2.COLOR_RGB2HSV)      # For red objects

    # Print color of center pixel

    # Cross hair on center pixel


    # Show the processed image with the given title.  Note this won't
    # actually appear (draw on screen) until the waitKey(1) below.
    cv2.imshow('Processed Image', frame)
    # cv2.imshow('Binary Image', binary)

    # Check for a key press IN THE IMAGE WINDOW: waitKey(0) blocks
    # indefinitely, waitkey(1) blocks for at most 1ms.  If 'q' break.
    # This also flushes the windows and causes it to actually appear.
    if (cv2.waitKey(1) & 0xFF) == ord('q'):
        break

# Close everything up.
camera.release()
cv2.destroyAllWindows()

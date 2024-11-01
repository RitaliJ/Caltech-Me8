"""goals5simple.py

   Read the camera image and do some simple image manipulation.
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


# Keep scanning, until 'q' hit IN IMAGE WINDOW.
count = 0
while True:
    # Grab an image from the camera.  Often called a frame (part of sequence).
    ret, frame = camera.read()
    count += 1

    # Grab and report the image shape.
    (H, W, D) = frame.shape
    print(f"Frame #{count:3} is {W}x{H} pixels x{D} color channels.")


    # Manipulate the image.  Two options:
    # (a) Directly change a pixel.  E.g. set color channel c to 255:
    # frame[y, x, c] = 255

    # OR:
    # (b) Use OpenCV functions.  E.g. draw line from (xA,yA) to (xB,yB):
    # cv2.line(frame, (xA,yA), (xB,yB), (255,255,255), 1)


    # Convert the BGR image to RGB or HSV.
    # hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)


    # Show the processed image with the given title.  Note this won't
    # actually appear (draw on screen) until the waitKey(1) below.
    cv2.imshow('Processed Image', frame)
    # cv2.imshow('HSV Funkiness', hsv)

    # Check for a key press IN THE IMAGE WINDOW: waitKey(0) blocks
    # indefinitely, waitkey(1) blocks for at most 1ms.  If 'q' break.
    # This also flushes the windows and causes it to actually appear.
    if (cv2.waitKey(1) & 0xFF) == ord('q'):
        break

# Close everything up.
camera.release()
cv2.destroyAllWindows()

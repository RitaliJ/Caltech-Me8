'''keycheck.py

   This sets up the terminal to report individual key presses and
   provides two functions:

     # Import the keycheck functions
     from keycheck import kbhit, getch

     status = khbit()
     ch = getch()

   kbhit() returns True/False whether a key was pressed and hence a
   character is waiting to be retrieved.  It continues to report True
   until the character is retrieved.

   getch() retrieves a waiting charater (after a key press).  If
   called when no key is available (without a press), it returns None.

'''

# Import the necessary packages
import atexit, select, sys, termios

# Import the testing packages
from time import sleep

#
#  Terminal Setup
#
#  Normally the terminal operates on "lines".  It only reports inputs
#  once the <return> key is pressed.  As such, we can not detect
#  individual presses.
#
#  The following changes the terminal into canonical mode, where it
#  makes individual key presses available.  Note we return the
#  terminal to the original settings on exit.
#

# Set up a handler, so the terminal returns to normal on exit.
stdattr = termios.tcgetattr(sys.stdin.fileno())
def reset_attr():
    termios.tcsetattr(sys.stdin.fileno(), termios.TCSAFLUSH, stdattr)
atexit.register(reset_attr)

# Switch the terminal to canonical mode: do not wait for <return>
# presses.  Also prevent the keys from echoing.
newattr    = termios.tcgetattr(sys.stdin.fileno())
newattr[3] = newattr[3] & ~termios.ICANON & ~termios.ECHO
termios.tcsetattr(sys.stdin.fileno(), termios.TCSAFLUSH, newattr)


#
#  Keypress Monitoring
#
#  Define the two functions:  kbhit() and getch()
#

# Report True/False if a key has been pressed, awaiting retrieval.
def kbhit():
    return sys.stdin in select.select([sys.stdin], [], [], 0)[0]

# Grab the character of the last key pressed.  To avoid blocking,
# check to make sure a character is indeed waiting to be retrieved.
def getch():
    if kbhit():
        return sys.stdin.read(1)
    else:
        return None


#
#  Testing
#
#  If run directly, simly run the following test code
#
if __name__ == "__main__":
    print("Press 'q' to quit...")
    while True:
        # Check for a key.
        if kbhit():
            # Grab and report the key
            c = getch()
            print("Saw key '%c'" % c)

            # Quit on the 'q' or 'Q' key.
            if c == 'q' or c == 'Q':
                print("Quitting...")
                break

        # Sleep 10ms before the next check.           
        sleep(0.01)
 

'''goals3democode.py

   Demo code for Goals 3
'''

# Import useful packages
import hebi
import numpy as np              # For future use
import matplotlib.pyplot as plt

from math import pi, sin, cos, asin, acos, atan2, sqrt, inf
from time import sleep, time
from keycheck import kbhit, getch


#
#  HEBI Initialization
#
#  Create the motor group, and pre-allocate the command and feedback
#  data structures.  Remember to set the names list to match your
#  motor.
#
names = ['5.5']
group = hebi.Lookup().get_group_from_names(['robotlab'], names)
if group is None:
  print("Unable to find both motors " + str(names))
  raise Exception("Unable to connect to motors")

command  = hebi.GroupCommand(group.size)
feedback = hebi.GroupFeedback(group.size)

dt = 0.01                       # HEBI feedback comes in at 100Hz!

# Also read the initial position.
feedback = group.get_next_feedback(reuse_fbk=feedback)
pinit = feedback.position[0]


#
#  Define the parameters
#
T = 15.0                         # 5 seconds total run time


#
#  Pre-allocate the storage.
#
N = int(T / dt)                 # 100 samples/second.

Time = [0.0] * N
PAct = [0.0] * N
PCmd = [0.0] * N
PErr = [0.0] * N
VAct = [0.0] * N
VCmd = [0.0] * N
VErr = [0.0] * N

# Helper functions
# Helper Functions
def movetime(po, pf, vmax):
    return abs(3*(pf - po)/(2*vmax))


def calcparams(t0, tf, p0, pf, v0, vf):
    T_move = tf - t0 
    a = p0
    b = v0
    c = 3*(pf - p0)/(T_move)**2 - vf/T_move - 2*v0/T_move
    d = (-2)*(pf - p0)/(T_move)**3 + vf/(T_move)**2 + v0/(T_move)**2
    return (a, b, c, d)


def splinecmds(t, t_spline, spline_params):
    (a, b, c, d) = spline_params
    pcmd = a + b*(t - t_spline) + c*(t - t_spline)**2 + d*(t - t_spline)**3
    vcmd = b + 2*c*(t - t_spline) + 3*d*(t - t_spline)**2
    return (pcmd, vcmd)


#
#  Execute the movement.
#
# Initialize the index and time.
index = 0
t = 0.0
feedback = group.get_next_feedback(reuse_fbk=feedback)
pinit = feedback.position[0]
vmax = 2.5

v0 = 0.0
vf = 0.0

p0 = pinit
pf = p0
t0 = 0.0
tm = inf
tf = t0 + tm
# tf = t0 + movetime(p0, pf, vmax)

(a,b,c,d) = calcparams(t0, tf, p0, pf, v0, vf)
segment_num = 1

while True:
    (pcmd, vcmd) = splinecmds(t, t0, (a, b, c, d))
    # Compute the commands for this time step.
    # Check for key presses.
    if kbhit():
        # Grab and report the key
        c = getch()
        print("Saw key '%c'" % c)
        # Do something
        if c == 'r':
            segment_num = 2
            tf = t
        elif c == 'q':
            break


    if t + dt > tf:
        t0 = t
        p0 = pcmd
        v0 = vcmd
        print(t)
        print(tf)
        print(v0)
        match segment_num:
            case 2:
                pf = pi/2
                tm = movetime(p0, pf, vmax)
            case 3:
                pf = -pi/2
                tm = movetime(p0, pf, vmax)
            case 4:
                pf = pinit
                tm = movetime(p0, pf, vmax)
            case 5:
                v0 = 0.0
                pf = p0
                tm = inf
                
        vf = 0.0
        tf = t0 + tm
        (a, b, c, d) = calcparams(t0, tf, p0, pf, v0, vf)
        segment_num += 1

    # Send the commands.  This returns immediately.
    command.position = [pcmd]
    command.velocity = [vcmd]
    group.send_command(command)

    # Read the actual data. This blocks (internally waits) 10ms for
    # the data and therefor replaces the "sleep(0.01)".
    feedback = group.get_next_feedback(reuse_fbk=feedback)
    pact = feedback.position[0]
    vact = feedback.velocity[0]

    # Store the data for this time step (at the current index).
    Time[index] = t
    PAct[index] = pact
    PCmd[index] = pcmd
    PErr[index] = pact - pcmd
    VAct[index] = vact
    VCmd[index] = vcmd
    VErr[index] = vact - vcmd

    # Advance the index/time.
    index += 1
    t     += dt

    # Break (end) the loop, if we run out of storage or time.
    # if index >= N or t >= T:
    if index >= N:
        break


#
#  Plot.
#
# Create a plot of position and velocity, actual and command!
fig, (ax1, ax2) = plt.subplots(2, 1, sharex=True)

ax1.plot(Time[0:index], PAct[0:index], color='blue', linestyle='-',  label='Act')
ax1.plot(Time[0:index], PCmd[0:index], color='blue', linestyle='--', label='Cmd')
ax1.plot(Time[0:index], PErr[0:index], color='red', linestyle='-.', label='Err')
ax2.plot(Time[0:index], VAct[0:index], color='blue', linestyle='-',  label='Act')
ax2.plot(Time[0:index], VCmd[0:index], color='blue', linestyle='--', label='Cmd')
ax2.plot(Time[0:index], VErr[0:index], color='red', linestyle='-.', label='Err')

ax1.set_title(f'Robot Data - Step 3')
ax1.set_ylabel('Position (rad)')
ax2.set_ylabel('Velocity (rad/s)')
ax2.set_xlabel('Time (s)')

ax1.grid()
ax2.grid()
ax1.legend()
ax2.legend()

plt.show()

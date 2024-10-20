'''goals3democode.py

   Demo code for Goals 3
'''

# Import useful packages
import hebi
import numpy as np              # For future use
import matplotlib.pyplot as plt

from math import pi, sin, cos, asin, acos, atan2, sqrt
from time import sleep, time


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
T = 5.0                         # 5 seconds total run time


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


#
#  Execute the movement.
#
# Initialize the index and time.
index = 0
t = 0.0
feedback = group.get_next_feedback(reuse_fbk=feedback)
p_init = feedback.position[0]
p_final = 1.0
v_init = 0.0
v_final = 0.0
if p_init >= 0:
    p_final = -1.0
v_max = 2.9
T_move = 3*(p_final - p_init)/(2*v_max)
first_move = 1.0


a = p_init
b = v_init
c = 3*(p_final - p_init)/(T_move)**2 - v_final/T_move - 2*v_init/T_move
d = (-2)*(p_final - p_init)/(T_move)**3 + v_final/(T_move)**2 + v_init/(T_move)**2

while True:
    # Compute the commands for this time step.
    if t >= first_move and t < first_move + T_move:
        vcmd = b + 2*c*(t - first_move) + 3*d*(t - first_move)**2
        pcmd = a + b*(t - first_move) + c*(t - first_move)**2 + d*(t - first_move)**3
    elif t < first_move:
        pcmd = p_init
        vcmd = 0.0
    else:
        pcmd = p_final
        vcmd = 0.0
        


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
    if index >= N or t >= T:
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

ax1.set_title(f'Robot Data - Step 7 - {T_move} secs')
ax1.set_ylabel('Position (rad)')
ax2.set_ylabel('Velocity (rad/s)')
ax2.set_xlabel('Time (s)')

ax1.grid()
ax2.grid()
ax1.legend()
ax2.legend()

plt.show()

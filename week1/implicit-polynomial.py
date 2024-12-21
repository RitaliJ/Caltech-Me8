import matplotlib.pyplot as plt
import math
from math import pi, cos, sin, sqrt
# boundary conditions
m = 0.5
c_d = 0.6
dt = 0.01
g = 9.81

vo = 30
theta = 0.25 * pi

def simulate(vo, theta):
    # initial conditions
    pox = 0
    poy = 0
    vox = vo * cos (theta)
    voy = vo * sin (theta)
    t = 0

    t_vec = [t]
    p_x = [pox]
    p_y = [poy]
    v_x = [vox]
    v_y = [voy]

    while (p_y[-1] >= 0 or t == 0):
        t += dt
        t_vec += [t]
        px = p_x[-1] + dt * v_x[-1]
        py = p_y[-1] + dt * v_y[-1]

        mag = sqrt((v_x[-1])**2 + (v_y[-1])**2)

        ax = -c_d /  m * mag * v_x[-1]
        ay = -g - c_d / m * mag * v_y[-1]

        vx = v_x[-1] + ax * dt
        vy = v_y[-1] + ay * dt

        p_x += [px]
        p_y += [py]
        v_x += [vx]
        v_y += [vy]

    return t_vec, p_x, p_y, v_x, v_y

t, px, py, vx, vy = simulate(vo, theta)
print(f'x position where the ball lands: {px[-1]}')

# Plot py vs px.
plt.plot(px,py)
plt.grid()
plt.axis('equal')
plt.xlabel('x (m)')
plt.ylabel('y (m)')
plt.title('Path in Y-X plane')
plt.show()
# Create a figure to plot px/py/vx/vy vs t.
fig, axs = plt.subplots(2, 2)
fig.suptitle('Motion versus time')
# Plot the data in the four subplots.
axs[0, 0].plot(t, px)
axs[0, 1].plot(t, py)
axs[1, 0].plot(t, vx)
axs[1, 1].plot(t, vy)
# Label/connect the top (position) and bottom (velocity) rows.
axs[0, 0].set(ylabel='Position (m)')
axs[0, 0].sharey(axs[0, 1])
axs[1, 0].set(ylabel='Velocity (m/s)')
axs[1, 0].sharey(axs[1, 1])
# Title/label/connect the left (X) and right (Y) columns.
axs[0, 0].set(title='X Axis')
axs[1, 0].set(xlabel='Time (s)')
axs[1, 0].sharex(axs[0, 0])
axs[0, 1].set(title='Y Axis')
axs[1, 1].set(xlabel='Time (s)')
axs[1, 1].sharex(axs[0, 1])
# Draw grid lines and allow only "outside" ticks/labels in each subplot.
for ax in axs.flat:
    ax.grid()
    ax.label_outer()
# Show
plt.show()
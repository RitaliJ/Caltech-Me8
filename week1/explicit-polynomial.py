import matplotlib.pyplot as plt
import math
from math import atan
# boundary conditions
T = 1
d = 1.0
h = 0.5
dt = 0.01
g = 9.81

def parabola(T, d, h):
    # initial conditions
    pox = 0
    poy = 0
    vox = d / T
    voy = (h + 0.5 * g * T**2) / T
    theta = atan(voy / vox)
    print(f'Launch Angle: {theta}')
    t = 0

    t_vec = [t]
    p_x = [pox]
    p_y = [poy]
    v_x = [vox]
    v_y = [voy]

    while (t < T):
        t += dt
        t_vec += [t]
        px = pox + t * vox
        py = poy + t * voy - 0.5 * g * t**2
        vy = voy - g * t

        p_x += [px]
        p_y += [py]
        v_x += [vox]
        v_y += [vy]

    return t_vec, p_x, p_y, v_x, v_y

t, px, py, vx, vy = parabola(T, d, h)
print(f'Max Height: {max(py)}')

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
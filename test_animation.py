import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

# Parameters
length = 10.0  # length of the rod
dx = 0.1       # spatial step size
dt = 0.01      # time step size
alpha = 0.01   # thermal diffusivity
nx = int(length / dx)  # number of spatial points
nt = 500       # number of time steps

# Initial condition: a Gaussian distribution
x = np.linspace(0, length, nx)
u = np.exp(-((x - length / 2)**2) / (2 * 0.1**2))

# Boundary conditions: u(0, t) = 0, u(L, t) = 0
u[0] = 0
u[-1] = 0

# Set up the figure, the axis, and the plot element
fig, ax = plt.subplots()
line, = ax.plot(x, u, 'r-')
ax.set_xlim(0, length)
ax.set_ylim(0, 1)

def update(frame):
    global u
    u_new = u.copy()
    # Update u using the finite difference method
    for i in range(1, nx - 1):
        u_new[i] = u[i] + alpha * dt / dx**2 * (u[i + 1] - 2 * u[i] + u[i - 1])
    u = u_new
    line.set_ydata(u)
    return line,

# Create the animation
ani = FuncAnimation(fig, update, frames=nt, blit=True)

# Save the animation as a GIF
ani.save('heat_equation.gif', writer='imagemagick')

# Show the plot
plt.show()
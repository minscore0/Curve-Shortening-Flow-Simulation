import numpy as np
from scipy.interpolate import splprep, splev
import math

# Given list of points (x, y)
points = [(725, 459), (721, 459), (714, 459), (706, 457), (700, 452), (694, 446), (690, 436), (689, 420), (689, 402), (689, 385), (689, 366), (692, 347), (701, 331), (718, 313), (740, 297), (762, 285), (809, 277), (833, 278), (849, 282), (862, 294), (876, 310), (885, 326), (889, 340), (892, 356), (894, 372), (894, 386), (892, 398), (888, 408), (880, 416), (870, 425), (857, 434), (842, 442), (829, 449), (725, 459)]

# Separate x and y coordinates
x = np.array([point[0] for point in points])
y = np.array([point[1] for point in points])

distances = np.zeros(len(points))
for i in range(1, len(points)):
    distances[i] = distances[i-1] + math.dist(points[i-1], points[i]) # stores the partial sum of arclength at each point
normalized_distances = distances/distances[-1] 

"""
# Calculate the arc length
distances = np.sqrt(np.diff(x)**2 + np.diff(y)**2)
cumulative_distances = np.concatenate(([0], np.cumsum(distances)))

# Normalize the cumulative distances
normalized_distances = cumulative_distances / cumulative_distances[-1]
"""
# Parametric interpolation using normalized arc length
tck, u = splprep([x, y], u=normalized_distances, s=0)

# Define the parameter values for interpolation
new_u = np.linspace(0, 1, 100)

# Interpolate x and y coordinates separately
new_x, new_y = splev(new_u, tck)

# Plot the results to visualize
import matplotlib.pyplot as plt

plt.plot(x, y, 'o', label='Original points')
plt.plot(new_x, new_y, '-', label='Interpolated curve')
plt.legend()
plt.xlabel('X')
plt.ylabel('Y')
plt.title('Arc Length Parameterized Spline Interpolation')
plt.show()
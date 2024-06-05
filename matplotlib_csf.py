import matplotlib.pyplot as plt
import numpy as np
import math

# Improved approach for curve shortening flow

# Define a function to parameterize a circle
def initialize_circle(num_points, radius):
    theta = np.linspace(0, 2 * np.pi, num_points, endpoint=False)
    x = radius * np.cos(theta)
    y = radius * np.sin(theta)
    return np.stack([x, y], axis=1)

def generate_sine_wave_points(num_points, period, amplitude, x_range, center):
    x = np.linspace(x_range[0], x_range[1], num_points)
    y = center[1] + amplitude * np.sin(2 * np.pi * (x - x_range[0]) / period)
    x += center[0] - (x_range[0] + x_range[1]) / 2
    return np.stack([x, y], axis=1)

# Parameters
period = 200
amplitude = 150
x_range = (300, 1200)  # Define the domain
center = (750, 450)  # Center of the sine wave

# Calculate curvature and normal using central differences
def curvature_and_normal(point_1, point_2, point_3):

    tan_1 = (point_3[0]-point_2[0], point_3[1]-point_2[1])
    tan_2 = (point_2[0]-point_1[0], point_2[1]-point_1[1])
        
    tan_1_norm = math.dist((0, 0), tan_1)
    tan_2_norm = math.dist((0, 0), tan_2)

    tan_1 = (tan_1[0]/tan_1_norm, tan_1[1]/tan_1_norm)
    tan_2 = (tan_2[0]/tan_2_norm, tan_2[1]/tan_2_norm)
        
    normal_vec = [tan_1[1]+tan_2[1], -(tan_1[0]+tan_2[0])]
    normal_vec[0] /= math.dist((0, 0), normal_vec)
    normal_vec[1] /= math.dist((0, 0), normal_vec)
    
    tan = ((tan_1[0] + tan_2[0])/2, (tan_1[1] + tan_2[1])/2)
    dtan = (tan_2[0]-tan_1[0], tan_2[1]-tan_1[1])

    # Curvature
    curvature = 2 * (tan_1[0]*tan_2[1] - tan_1[1]*tan_2[0]) / (tan_1_norm + tan_2_norm)
    #curvature = (tan[0]*dtan[1] - tan[1]*dtan[0])/(1)**(3/2)
    
    return curvature, normal_vec

# Update the curve using curve shortening flow
def update_curve(points, dt):

    curvatures = list()
    normal_vecs = list()

    for i in range(len(points)):
        point_2 = points[i]
        point_1 = points[i-1]
        point_3 = points[(i+1)%len(points)]
        curvature, normal = curvature_and_normal(point_1, point_2, point_3)
        curvatures.append(curvature)
        normal_vecs.append(normal)
    
    for i in range(len(points)):
        K = curvatures[i]
        N = normal_vecs[i]
        points[i][0] += dt * K * N[0]
        points[i][1] += dt * K * N[1]
    
    return points

# Smooth the curve periodically to ensure stability
def smooth_curve(points, smoothing_factor=0.01):
    num_points = len(points)
    smoothed_points = points.copy()
    for i in range(num_points):
        smoothed_points[i] = (1 - smoothing_factor) * points[i] + \
                             (smoothing_factor / 2) * (points[i - 1] + points[(i + 1) % num_points])
    return smoothed_points

# Simulation parameters
num_points = 200
radius = 1.0
dt = 1  # Time step
num_iterations = 1000  # Number of iterations
smoothing_interval = 10  # Interval for smoothing the curve

# Initialize the curve
points = generate_sine_wave_points(num_points, period, amplitude, x_range, center)

# Store the initial and final curves for plotting
initial_curve = points.copy()

# Evolve the curve
for i in range(num_iterations):
    points = update_curve(points, dt)
    """
    if i % smoothing_interval == 0:
        points = smooth_curve(points)"""

final_curve = points.copy()

# Plot the initial and final curves
plt.figure(figsize=(8, 8))
plt.plot(initial_curve[:, 0], initial_curve[:, 1], label='Initial Curve')
plt.plot(final_curve[:, 0], final_curve[:, 1], label='Evolved Curve')
plt.axis('equal')
plt.legend()
plt.title('Curve Shortening Flow')
plt.xlabel('X')
plt.ylabel('Y')
plt.show()

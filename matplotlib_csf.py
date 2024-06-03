import matplotlib.pyplot as plt
import numpy as np

# Improved approach for curve shortening flow

# Define a function to parameterize a circle
def initialize_circle(num_points, radius):
    theta = np.linspace(0, 2 * np.pi, num_points, endpoint=False)
    x = radius * np.cos(theta)
    y = radius * np.sin(theta)
    return np.stack([x, y], axis=1)

# Calculate curvature and normal using central differences
def curvature_and_normal(points):
    num_points = len(points)
    curvature = np.zeros(num_points)
    normal = np.zeros((num_points, 2))
    
    for i in range(num_points):
        p_prev = points[i - 1]
        p_curr = points[i]
        p_next = points[(i + 1) % num_points]
        
        # Tangent vectors
        t1 = p_next - p_curr
        t2 = p_curr - p_prev
        
        # Lengths of tangent vectors
        t1_norm = np.linalg.norm(t1)
        t2_norm = np.linalg.norm(t2)
        
        # Unit tangent vectors
        t1 /= t1_norm
        t2 /= t2_norm
        
        # Normal vector as the perpendicular to the tangent
        normal_vec = np.array([-t1[1], t1[0]]) + np.array([-t2[1], t2[0]])
        normal_vec /= np.linalg.norm(normal_vec)
        
        # Curvature
        curvature[i] = 2 * np.cross(t1, t2) / (t1_norm + t2_norm)
        normal[i] = normal_vec
    
    return curvature, normal

# Update the curve using curve shortening flow
def update_curve(points, dt):
    curvature, normal = curvature_and_normal(points)
    points -= dt * curvature[:, None] * normal
    return points

# Smooth the curve periodically to ensure stability
def smooth_curve(points, smoothing_factor=0.1):
    num_points = len(points)
    smoothed_points = points.copy()
    for i in range(num_points):
        smoothed_points[i] = (1 - smoothing_factor) * points[i] + \
                             (smoothing_factor / 2) * (points[i - 1] + points[(i + 1) % num_points])
    return smoothed_points

# Simulation parameters
num_points = 100
radius = 1.0
dt = 0.001  # Time step
num_iterations = 500  # Number of iterations
smoothing_interval = 10  # Interval for smoothing the curve

# Initialize the curve
points = initialize_circle(num_points, radius)

# Store the initial and final curves for plotting
initial_curve = points.copy()

# Evolve the curve
for i in range(num_iterations):
    points = update_curve(points, dt)
    if i % smoothing_interval == 0:
        points = smooth_curve(points)

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

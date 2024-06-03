import numpy as np

def generate_circle_points(num_points, radius, center):
    theta = np.linspace(0, 2 * np.pi, num_points, endpoint=False)
    x = center[0] + radius * np.cos(theta)
    y = center[1] + radius * np.sin(theta)
    return np.stack([x, y], axis=1)

# Parameters
num_points = 50
radius = 200
center = (750, 450)

# Generate circle points
circle_points = generate_circle_points(num_points, radius, center)
circle_points_list = circle_points.tolist()

# Print the list of points
print(circle_points_list)
print(len(circle_points_list))

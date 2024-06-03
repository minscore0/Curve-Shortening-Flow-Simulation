import numpy as np

def generate_sine_wave_points(num_points, period, amplitude, x_range, center):
    x = np.linspace(x_range[0], x_range[1], num_points)
    y = center[1] + amplitude * np.sin(2 * np.pi * (x - x_range[0]) / period)
    x += center[0] - (x_range[0] + x_range[1]) / 2
    return np.stack([x, y], axis=1)

# Parameters
num_points = 100
period = 200
amplitude = 150
x_range = (300, 1200)  # Define the domain
center = (750, 450)  # Center of the sine wave

# Generate sine wave points
sine_wave_points = generate_sine_wave_points(num_points, period, amplitude, x_range, center)
sine_wave_points_list = sine_wave_points.tolist()

# Print the list of points
print(sine_wave_points_list)
